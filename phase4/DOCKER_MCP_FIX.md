# Docker MCP Connection Fix

## Problem Identified

The MCP server subprocess was unable to communicate with the backend API when running in Docker containers because:

1. **Environment Variable Inheritance Issue**: The MCP server is spawned as a subprocess using `python -m ai_mcp_server`. Subprocesses don't automatically inherit Docker container environment variables.

2. **Wrong Service URL**: Without proper environment variables, `BUSINESS_SERVICE_URL` defaulted to `http://localhost:8000` instead of `http://backend:8000` (the Docker service name).

3. **Network Isolation**: Inside the ai-service container, `localhost:8000` doesn't exist - the backend service is accessible via `http://backend:8000` on the Docker network.

## Root Cause

In `ai-service/todo_agent.py`, the MCP server was initialized without explicitly passing environment variables:

```python
# OLD CODE (broken in Docker)
self.mcp_server = MCPServerStdio(
    name="Todo Management MCP Server",
    params={"command": sys.executable, "args": ["-m", "ai_mcp_server"]},
)
```

## Solution Applied

### 1. Pass Environment Variables to MCP Subprocess

**File: `ai-service/todo_agent.py`**

```python
# Create environment for MCP subprocess with all necessary variables
mcp_env = os.environ.copy()
mcp_env["BUSINESS_SERVICE_URL"] = settings.BUSINESS_SERVICE_URL
mcp_env["BETTER_AUTH_SECRET"] = settings.SERVICE_SECRET
mcp_env["GEMINI_API_KEY"] = settings.GEMINI_API_KEY

self.mcp_server = MCPServerStdio(
    name="Todo Management MCP Server",
    params={
        "command": sys.executable, 
        "args": ["-m", "ai_mcp_server"],
        "env": mcp_env  # ✅ Explicitly pass environment
    },
)
```

### 2. Enhanced Logging in MCP Server

**File: `ai-service/ai_mcp_server.py`**

- Added logging for all HTTP requests (URL, method, status code)
- Log authentication header presence (without exposing secrets)
- Log when SERVICE_SECRET or BUSINESS_SERVICE_URL are loaded

### 3. Fixed httpx Client Configuration

Changed all `httpx.AsyncClient()` to `httpx.AsyncClient(trust_env=False)` to prevent proxy issues.

### 4. Fixed complete_task Payload

The `/tasks/{task_id}/complete` endpoint expects a JSON body. Fixed:

```python
payload = {"completed": True}
response = await client.patch(url, json=payload, headers=headers)
```

## Testing the Fix

### 1. Rebuild and Start Containers

```bash
docker-compose down
docker-compose build --no-cache ai-service
docker-compose up -d
```

### 2. Check Logs

**AI Service logs (should show MCP connecting to correct URL):**
```bash
docker logs todo-ai-service -f
```

Look for:
```
TodoAgent initializing with BUSINESS_SERVICE_URL: http://backend:8000
MCP Server will use BUSINESS_SERVICE_URL: http://backend:8000
--- MCP SERVER SCRIPT STARTING ---
BUSINESS_SERVICE_URL from env: http://backend:8000
Final BUSINESS_SERVICE_URL: http://backend:8000
```

**Backend logs (should show requests from ai-service):**
```bash
docker logs todo-backend -f
```

### 3. Test via Frontend

1. Open the app in browser: `http://localhost:3000`
2. Log in
3. Use the chat interface to add a task: "Add task: Test Docker MCP"
4. Check logs to verify:
   - AI service receives the message
   - MCP server makes HTTP request to `http://backend:8000/api/{user_id}/tasks`
   - Backend receives and processes the request
   - Task appears in the UI

### 4. Verify Network Communication

**Test backend is accessible from ai-service container:**
```bash
docker exec todo-ai-service curl http://backend:8000/health
```

Should return: `{"status":"healthy"}`

### 5. Test MCP Tool Calls Directly

Check that tools are being called by looking for these log entries:

```bash
docker logs todo-ai-service 2>&1 | grep "add_task:"
docker logs todo-ai-service 2>&1 | grep "list_tasks:"
```

Should see:
```
add_task: Making POST request to http://backend:8000/api/1/tasks
add_task: Received response status=201
add_task: Task added successfully
```

## Expected Behavior After Fix

### ✅ Working System Flow:

1. User sends message in chat: "Add a task to buy groceries"
2. AI service receives message via `/chatkit` endpoint
3. TodoAgent processes message with AI model
4. AI model decides to call `add_task` tool
5. MCP server subprocess makes HTTP POST to `http://backend:8000/api/{user_id}/tasks`
6. Backend authenticates using SERVICE_SECRET
7. Backend creates task in database
8. Backend returns 201 Created
9. MCP server returns success to agent
10. Agent returns confirmation to user
11. Frontend updates task list via SSE

### ❌ Old Broken Behavior:

1-4. Same as above
5. MCP server tries to call `http://localhost:8000/api/{user_id}/tasks` ❌
6. Connection fails (nothing on localhost:8000)
7. No task created
8. No error visible to user

## Configuration Checklist

Ensure these environment variables are set in `.env`:

```bash
# Critical for MCP communication
BUSINESS_SERVICE_URL=http://backend:8000
BETTER_AUTH_SECRET=your-secret-here

# Required by backend
DATABASE_URL=postgresql+asyncpg://...
GEMINI_API_KEY=your-key-here
```

## Troubleshooting

### Issue: "Failed to create task" errors

**Check:**
1. Backend is healthy: `docker exec todo-ai-service curl http://backend:8000/health`
2. Authentication secret matches between services
3. Logs show correct URL: `http://backend:8000` not `http://localhost:8000`

### Issue: No MCP logs appearing

**Check:**
1. MCP subprocess is starting: Look for "MCP SERVER SCRIPT STARTING" in logs
2. Agent is calling tools: Look for "Making POST/GET/PATCH request" in logs

### Issue: 401 Unauthorized

**Check:**
1. `BETTER_AUTH_SECRET` is the same in both `.env` and hardcoded in `ai_mcp_server.py`
2. Authorization header is being sent: Look for "Has Auth=True" in logs

## Files Changed

- `ai-service/todo_agent.py` - Pass environment to MCP subprocess
- `ai-service/ai_mcp_server.py` - Enhanced logging, fixed httpx client, load env vars
- `ai-service/complete_task` function - Add JSON payload

## Why It Works Locally But Not in Docker

**Local environment:**
- All services run on `localhost` with different ports
- Environment variables are available to all Python processes
- `BUSINESS_SERVICE_URL=http://localhost:8000` works correctly

**Docker environment:**
- Services run in isolated containers with their own networks
- Each container has its own `localhost`
- Must use Docker service names: `http://backend:8000`
- Subprocesses don't inherit container env vars unless explicitly passed

This fix ensures the MCP subprocess has access to the correct service URLs and authentication credentials in the Docker environment.
