# AI TODO APP

This is the AI TODO APP project with five phases:
1. Console App
2. Web App (COMPLETED)
3. AI Chatbot
4. Bonus Features
5. Deployment

## Current Status

Phase 2: Web App is now complete! The application includes a full-stack web application with:
- Backend API built with FastAPI
  - User authentication and authorization (JWT)
  - Task management with CRUD operations
  - Priority levels, due dates, and categories
  - Filtering and sorting capabilities
  - Database integration with SQLAlchemy
- Frontend built with Next.js
  - Dashboard with task management
  - Authentication pages (login/signup)
  - Task modal for creating and editing
  - Analytics and productivity charts
  - Responsive UI with modern design
  - Accessibility features

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory: `cd phase2/backend`
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables in a `.env` file:
   ```
   DATABASE_URL=sqlite:///./todo_app.db
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
6. Run the application: `python main.py`

### Frontend Setup

1. Navigate to the frontend directory: `cd phase2/frontend`
2. Install dependencies: `npm install` or `yarn install`
3. Set up environment variables in a `.env` file:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
4. Run the development server: `npm run dev` or `yarn dev`
5. Open http://localhost:3000 in your browser

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