# Quickstart: AI Chatbot for Todo Management

## Prerequisites

- Python 3.11+
- Node.js 18+ / npm
- uv (for Python dependency management)
- Access to Gemini API
- Existing backend services running (from Phase II)

## Backend Setup

1. **Install backend dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   # Or if using poetry:
   poetry install
   ```

2. **Backend environment variables**:
   ```bash
   # In backend/.env
   GEMINI_API_KEY=your-gemini-api-key
   DATABASE_URL=sqlite:///./todo_app.db  # or your PostgreSQL URL
   BETTER_AUTH_SECRET=your-better-auth-secret
   ```

3. **Run database migrations** (if needed for conversation tables):
   ```bash
   python -m alembic upgrade head
   ```

## Frontend Setup

1. **Install frontend dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Frontend environment variables**:
   ```bash
   # In frontend/.env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_CHATKIT_API_KEY=your-chatkit-key  # if using ChatKit services
   ```

## Running the Services

1. **Start the backend**:
   ```bash
   cd backend
   python main.py
   ```

2. **Start the frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the AI chat interface**:
   - Navigate to http://localhost:3000/dashboard/ai
   - The ChatKit UI will be available for natural language task management

## Testing the Chatbot

1. **Backend API test**:
   ```bash
   curl -X POST http://localhost:8000/api/{user_id}/chat \
     -H "Authorization: Bearer {better_auth_token}" \
     -H "Content-Type: application/json" \
     -d '{"message": "Add a task: buy groceries"}'
   ```

2. **Expected response**:
   ```json
   {
     "response": "I've added the task 'buy groceries' for you.",
     "conversation_id": "uuid-string",
     "tool_calls": [
       {
         "function": {
           "name": "add_task",
           "arguments": "{\"user_id\":\"{user_id}\",\"title\":\"buy groceries\",\"description\":\"\"}"
         },
         "id": "call_123"
       }
     ],
     "requires_action": true
   }
   ```

## Development

1. **Running backend tests**:
   ```bash
   cd backend
   pytest tests/ai/
   ```

2. **Running frontend tests**:
   ```bash
   cd frontend
   npm test
   ```

3. **Code structure**:
   - `backend/ai/agents/` - AI agent logic and conversation management
   - `backend/ai/mcp/` - MCP server and tool definitions
   - `backend/ai/endpoints/` - Chat API endpoints
   - `frontend/src/components/AI/` - ChatKit UI and AI interface components
   - `frontend/src/pages/dashboard/ai.tsx` - AI chat page
   - `tests/ai/` - AI-specific tests

4. **Adding new tools**:
   - Add the function to `backend/ai/mcp/tool_definitions.py`
   - Register it with the AI agent
   - Update the API contract if needed