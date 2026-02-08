# 🚀 Neon Database Setup Guide

## What is Neon?

Neon is a serverless PostgreSQL database that provides:
- ✅ Serverless PostgreSQL (no need to run local Postgres)
- ✅ Automatic scaling
- ✅ Generous free tier
- ✅ Built-in connection pooling
- ✅ Branching for dev/staging/production

## Getting Your Neon Connection String

### Step 1: Sign up for Neon
1. Go to [https://console.neon.tech/](https://console.neon.tech/)
2. Sign up with GitHub, Google, or email
3. Create a new project (or use existing one)

### Step 2: Get Connection String
1. In your Neon dashboard, click on your project
2. Go to **"Connection Details"**
3. Select **"Pooled connection"** (recommended for serverless)
4. Copy the connection string

It will look like:
```
postgresql://user:password@ep-cool-name-12345678.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### Step 3: Update Your .env File

**Important:** Change `postgresql://` to `postgresql+asyncpg://` for asyncpg driver:

```bash
# Original Neon connection string:
postgresql://user:password@ep-xxxx-region.neon.tech/dbname?sslmode=require

# Updated for asyncpg (add +asyncpg):
postgresql+asyncpg://user:password@ep-xxxx-region.neon.tech/dbname?sslmode=require
```

Update `phase4/.env`:
```env
DATABASE_URL=postgresql+asyncpg://your_user:your_password@ep-xxxx-region.neon.tech/your_db?sslmode=require
```

## What Changed in Your Setup

### ✅ Removed Local Postgres
- No more `postgres` service in docker-compose.yml
- No more postgres volumes
- Faster startup time

### ✅ Updated Configuration Files
- `phase4/.env` - Points to Neon
- `phase4/.env.example` - Updated with Neon format
- `phase4/docker-compose.yml` - Removed postgres service
- `phase4/backend/Dockerfile` - Updated DATABASE_URL format
- `phase4/ai-service/Dockerfile` - Updated DATABASE_URL format

### ✅ Benefits
- No need to manage local database
- Database persists between docker restarts
- Can access database from anywhere
- Built-in backups and point-in-time recovery
- Better performance with connection pooling

## Running Your Stack with Neon

```bash
# 1. Update your .env with Neon connection string
cd phase4
nano .env  # or use your favorite editor

# 2. Update these values:
#    - DATABASE_URL (your Neon connection string)
#    - BETTER_AUTH_SECRET (generate a strong random string)
#    - GEMINI_API_KEY (your Gemini API key)

# 3. Start the stack (no postgres to wait for!)
docker-compose up --build

# Services will start faster without local postgres:
# ✓ Backend connects directly to Neon
# ✓ AI Service connects directly to Neon  
# ✓ Frontend connects to backend
```

## Neon Features You Can Use

### Database Branching
Create separate databases for dev/staging/production:
```bash
# In Neon Console -> Branches
# Create branch: "development"
# Create branch: "staging"
# Each branch has its own connection string
```

### Connection Pooling
Neon automatically pools connections - perfect for serverless!

### Monitoring
Check your database usage in the Neon dashboard:
- Query performance
- Storage usage
- Active connections

## Troubleshooting

### Connection Issues
If you get connection errors:

1. **Check SSL requirement:**
   ```env
   # Neon requires SSL - make sure this is in your connection string:
   ?sslmode=require
   ```

2. **Verify asyncpg format:**
   ```env
   # Must start with postgresql+asyncpg://
   DATABASE_URL=postgresql+asyncpg://...
   ```

3. **Check IP allowlist:**
   - Neon's free tier allows connections from anywhere by default
   - Check "IP Allow" settings if you have restrictions

### Test Connection
You can test your Neon connection with psql:
```bash
psql "postgresql://user:password@ep-xxxx-region.neon.tech/dbname?sslmode=require"
```

## Environment Variables Checklist

Before running `docker-compose up`, ensure these are set in `phase4/.env`:

- [ ] `DATABASE_URL` - Your Neon connection string (with `+asyncpg`)
- [ ] `BETTER_AUTH_SECRET` - Strong random string for JWT
- [ ] `GEMINI_API_KEY` - Your Gemini API key
- [ ] Other variables have sensible defaults

## Summary

You're now using Neon serverless PostgreSQL! 🎉

**No more local Postgres to manage:**
- ❌ No postgres container
- ❌ No postgres volumes
- ❌ No postgres ports to expose
- ✅ Just your connection string in .env

**Start your stack:**
```bash
cd phase4
docker-compose up
```

Happy coding! 🚀
