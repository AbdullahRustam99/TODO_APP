# Phase 4: AI-Powered Task Management System

This directory contains the source code for the AI-powered task management system.

## Project Structure

*   `ai-service/`: Contains the AI agent and MCP server.
*   `backend/`: Contains the FastAPI backend application.
*   `frontend/`: Contains the Next.js frontend application.

## How to Run

### 1. Start the AI Service

```bash
cd phase3/ai-service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

### 2. Start the Backend

```bash
cd phase3/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Start the Frontend

```bash
cd phase3/frontend
npm install
npm run dev
```
