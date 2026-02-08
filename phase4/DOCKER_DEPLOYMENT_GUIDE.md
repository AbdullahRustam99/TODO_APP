# Docker Deployment Guide - Todo App with AI

This guide will help you deploy the Todo App with AI services using Docker and Docker Compose.

## 📋 Prerequisites

- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)
- OpenRouter API key (for AI features)
- At least 4GB RAM available for Docker

## 🏗️ Architecture

The application consists of 4 services:

```
┌─────────────────────────────────────────────────────────┐
│                     Docker Network                       │
│                      (todo-network)                      │
│                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│  │Frontend  │───▶│ Backend  │───▶│PostgreSQL│         │
│  │  :3000   │    │  :8000   │    │  :5432   │         │
│  └────┬─────┘    └──────────┘    └──────────┘         │
│       │                                                  │
│       │          ┌──────────┐                          │
│       └─────────▶│AI Service│                          │
│                  │  :8001   │                          │
│                  └──────────┘                          │
└─────────────────────────────────────────────────────────┘
```

### Services:

1. **Frontend** (Next.js) - Port 3000
   - User interface
   - Server-side rendering
   - API communication

2. **Backend** (FastAPI) - Port 8000
   - RESTful API
   - Task management
   - User authentication
   - Database operations

3. **AI Service** (OpenAI Agents + MCP) - Port 8001
   - Natural language processing
   - AI-powered task management
   - ChatKit interface

4. **PostgreSQL** - Port 5432
   - Database storage
   - User data
   - Task data
   - Conversation history

## 🚀 Quick Start

### Step 1: Clone and Navigate

```bash
cd phase4
```

### Step 2: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your credentials:
```bash
# Required
GEMINI_API_KEY=your_openrouter_api_key_here
BETTER_AUTH_SECRET=your_generated_secret_here

# Generate a secure secret:
# openssl rand -hex 32
```

### Step 3: Build and Start Services

```bash
# Build all images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Step 4: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **AI Service**: http://localhost:8001
- **API Docs**: http://localhost:8000/docs

## 🔍 Verify Deployment

### Check Service Health

```bash
# Check all containers are running
docker-compose ps

# Check backend health
curl http://localhost:8000/health

# Check AI service health
curl http://localhost:8001/health

# Check frontend (should return HTML)
curl http://localhost:3000
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f ai-service
docker-compose logs -f frontend
docker-compose logs -f postgres
```

## 🛠️ Common Commands

### Start/Stop Services

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart a specific service
docker-compose restart backend

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

### Rebuild Services

```bash
# Rebuild all services
docker-compose build

# Rebuild specific service
docker-compose build backend

# Rebuild and restart
docker-compose up -d --build
```

### View Service Status

```bash
# List all containers
docker-compose ps

# View resource usage
docker stats

# Inspect network
docker network inspect todo-network
```

## 🐛 Troubleshooting

### Service Won't Start

1. **Check logs**:
```bash
docker-compose logs [service-name]
```

2. **Check if port is already in use**:
```bash
# Windows PowerShell
netstat -ano | findstr :3000
netstat -ano | findstr :8000
netstat -ano | findstr :8001

# Linux/Mac
lsof -i :3000
lsof -i :8000
lsof -i :8001
```

3. **Remove old containers and volumes**:
```bash
docker-compose down -v
docker-compose up -d
```

### Database Connection Issues

1. **Wait for database to be ready**:
```bash
docker-compose logs postgres
```

2. **Check database connection**:
```bash
docker exec -it todo-postgres psql -U todouser -d todo_app
```

3. **Recreate database volume**:
```bash
docker-compose down -v
docker-compose up -d
```

### Frontend Not Loading

1. **Check if backend is accessible**:
```bash
curl http://localhost:8000/health
```

2. **Verify environment variables**:
```bash
docker-compose exec frontend env | grep NEXT_PUBLIC
```

3. **Rebuild frontend**:
```bash
docker-compose build frontend
docker-compose up -d frontend
```

### AI Service Errors

1. **Verify API key**:
```bash
docker-compose exec ai-service env | grep GEMINI_API_KEY
```

2. **Check if backend is reachable**:
```bash
docker-compose exec ai-service curl http://backend:8000/health
```

## 🔐 Security Notes

### For Production Deployment:

1. **Change default credentials**:
   - Update `BETTER_AUTH_SECRET` with a strong random value
   - Change PostgreSQL credentials in docker-compose.yml

2. **Update CORS settings**:
   - Modify `allow_origins` in backend/main.py
   - Set specific frontend domain instead of "*"

3. **Use secrets management**:
   - Don't commit `.env` file
   - Use Docker secrets or external secret managers

4. **Network security**:
   - Remove port mappings for postgres (5432) in production
   - Use reverse proxy (nginx) for frontend/backend

5. **SSL/TLS**:
   - Add HTTPS support
   - Use proper certificates

## 📊 Database Management

### Backup Database

```bash
# Create backup
docker exec todo-postgres pg_dump -U todouser todo_app > backup.sql

# Restore backup
docker exec -i todo-postgres psql -U todouser todo_app < backup.sql
```

### Access Database CLI

```bash
docker exec -it todo-postgres psql -U todouser -d todo_app
```

### Common SQL Commands

```sql
-- List tables
\dt

-- View users
SELECT * FROM "user";

-- View tasks
SELECT * FROM task;

-- Exit
\q
```

## 🧹 Cleanup

### Remove Everything

```bash
# Stop and remove containers, networks
docker-compose down

# Remove volumes (deletes all data)
docker-compose down -v

# Remove images
docker rmi phase4-frontend phase4-backend phase4-ai-service

# Full cleanup
docker system prune -a --volumes
```

## 📈 Scaling Services

### Scale Backend Instances

```bash
# Run 3 backend instances
docker-compose up -d --scale backend=3

# Note: You'll need a load balancer for this to work properly
```

## 🌐 Network Configuration

The application uses a custom bridge network `todo-network`:

- **Internal DNS**: Services can reach each other by service name
  - `http://backend:8000`
  - `http://ai-service:8001`
  - `http://postgres:5432`

- **External Access**: Only exposed ports are accessible from host
  - Frontend: 3000
  - Backend: 8000
  - AI Service: 8001
  - PostgreSQL: 5432 (optional, can be removed)

## 🔄 Update Strategy

### Update Application Code

1. Pull latest code:
```bash
git pull origin main
```

2. Rebuild and restart:
```bash
docker-compose up -d --build
```

### Update Dependencies

1. Update `requirements.txt` or `package.json`
2. Rebuild specific service:
```bash
docker-compose build backend
docker-compose up -d backend
```

## 📝 Environment Variables Reference

### Backend Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DATABASE_URL | postgresql+asyncpg://... | PostgreSQL connection string |
| BETTER_AUTH_SECRET | - | JWT signing secret (required) |
| JWT_ALGORITHM | HS256 | JWT algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | 30 | Access token expiry |
| REFRESH_TOKEN_EXPIRE_DAYS | 7 | Refresh token expiry |
| DEBUG | false | Debug mode |
| DB_ECHO | false | SQL query logging |

### AI Service Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| GEMINI_API_KEY | - | OpenRouter API key (required) |
| BETTER_AUTH_SECRET | - | JWT signing secret |
| BUSINESS_SERVICE_URL | http://backend:8000 | Backend API URL |
| CONVERSATION_RETENTION_DAYS | 7 | Chat history retention |

### Frontend Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| NEXT_PUBLIC_API_BASE_URL | http://localhost:8000 | Backend API URL |
| NEXT_PUBLIC_CHATKIT_API_URL | http://localhost:8001 | AI Service URL |
| NODE_ENV | production | Node environment |

## 🎯 Next Steps

After successful Docker deployment:

1. ✅ Test all features
2. ✅ Configure production environment variables
3. ✅ Set up backup strategy
4. ✅ Configure monitoring (optional)
5. ✅ Prepare for Kubernetes deployment (Phase 4 next step)

## 📞 Support

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Verify environment variables in `.env`
3. Ensure Docker has enough resources
4. Check firewall/antivirus settings
5. Review this troubleshooting guide

## 🚀 Ready for Kubernetes?

Once Docker Compose deployment is working:
- All services are containerized ✅
- Networking is configured ✅
- Health checks are implemented ✅
- Environment variables are managed ✅

You're ready to proceed with Kubernetes deployment!
