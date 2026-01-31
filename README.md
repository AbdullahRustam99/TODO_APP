# Todo App with AI Chatbot

This project is a Todo application integrated with an AI chatbot, designed to be fully responsive and user-friendly.

## Key Features & Improvements

*   **Responsive Frontend UI:** The application now boasts a fully responsive dashboard with a mobile-friendly bottom navigation bar and adaptable filter tabs, ensuring optimal viewing across all devices.
*   **AI Chatbot Service (Backend):** Integrated an AI assistant, powered by FastAPI, for natural language task management. This service now includes Docker support, verified dependencies, and proper Git ignore configurations.
*   **Core Backend API (Python/FastAPI):** The project includes a robust core backend API, built with Python and FastAPI, handling primary application logic and data management.
*   **Robust Frontend Build:** Achieved a clean compilation by resolving numerous TypeScript errors, build issues, and dependency conflicts across frontend utilities and API clients.
*   **Enhanced Code Quality:** Improved maintainability through addressing various code quality and typing issues throughout the codebase.

## How to Run the Application

To get the application running, follow these steps:

### 1. Core Backend API Setup (`phase3/backend`)

This is the main backend service for the Todo application, built with Python and FastAPI.

1.  **Navigate:** `cd phase3/backend`
2.  **Environment Variables:** Create a `.env` file for any necessary backend configurations (e.g., database credentials, JWT secrets). Specific variables will depend on the backend's implementation.
3.  **Install Dependencies:** `uv pip install --system --no-cache-dir -r requirements.txt` (install `uv` first if needed: `pip install uv`)
4.  **Run Service:** `uvicorn main:app --host 0.0.0.0 --port 8000 --reload` (replace `main:app` with the actual entry point if different, and adjust port if necessary; keep this terminal open)

### 2. AI Service Backend Setup (`phase3/ai-service`)

This service uses Python and FastAPI.

1.  **Navigate:** `cd phase3/ai-service`
2.  **Environment Variables:** Create `.env` with `GEMINI_API_KEY`, `BETTER_AUTH_SECRET`, and optionally `BUSINESS_SERVICE_URL`, `CONVERSATION_RETENTION_DAYS`.
    *   `GEMINI_API_KEY`: Your API key for OpenRouter AI (using `z-ai/glm-4.5-air:free`).
    *   `BETTER_AUTH_SECRET`: A strong secret string.
3.  **Install Dependencies:** `uv pip install --system --no-cache-dir -r requirements.txt` (install `uv` first if needed: `pip install uv`)
4.  **Run Service:** `uvicorn main:app --host 0.0.0.0 --port 8000 --reload` (keep this terminal open)

### 3. Frontend Web Application Setup (`phase3/frontend`)

This is a Next.js application.

1.  **Navigate (new terminal):** `cd phase3/frontend`
2.  **Environment Variables:** Create `.env.local` with `NEXT_PUBLIC_CHATKIT_API_URL=http://localhost:8000`
3.  **Install Dependencies:** `npm install`
4.  **Run Application:** `npm run dev`

### 3. Access the Application

Open your browser to: **[http://localhost:3000/dashboard](http://localhost:3000/dashboard)**
This is the AI TODO APP project with five phases:
1. Console App
2. Web App (COMPLETED)
3. AI Chatbot
4. Bonus Features
5. Deployment


## Features

- User authentication (register, login, logout)
- Create, read, update, and delete tasks
- Set task priorities (High, Medium, Low)
- Set due dates and categories for tasks
- Filter and sort tasks
- Dashboard with analytics
- Responsive design for mobile and desktop
- Accessibility features

## Tech Stack

- Backend: Python, FastAPI, SQLAlchemy, JWT
- Frontend: Next.js, TypeScript, Tailwind CSS
- Database: SQLite (with option to switch to PostgreSQL/MySQL)
- Ai Agent: Chatkit, OpenAI Agent SDK
- Database: SQLite (with option to switch to PostgreSQL/MySQL)
