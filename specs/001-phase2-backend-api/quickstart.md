# Quickstart Guide: Phase II - Backend API

**Date**: 2025-12-27
**Feature**: Phase II - Backend API

## Getting Started

### Prerequisites
- Python 3.13 or higher
- PostgreSQL (or access to Neon Serverless PostgreSQL)
- UV package manager (optional, for environment management)

### Installation

1. Clone the repository
2. Navigate to the backend directory
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install fastapi sqlmodel pyjwt python-multipart uvicorn pytest
   ```

### Environment Setup

Create a `.env` file in the backend root with the following variables:
```
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_app
BETTER_AUTH_SECRET=your-super-secret-jwt-signing-key-here
```

### Running the Application

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication Required
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

### Task Endpoints

#### GET /api/{user_id}/tasks
Retrieve all tasks for the specified user.

**Parameters**:
- `user_id`: The ID of the user whose tasks to retrieve

**Response**: Array of task objects

#### POST /api/{user_id}/tasks
Create a new task for the specified user.

**Parameters**:
- `user_id`: The ID of the user creating the task

**Request Body**:
```json
{
  "title": "Task title",
  "description": "Optional description"
}
```

**Response**: Created task object

#### GET /api/{user_id}/tasks/{id}
Retrieve a specific task by ID.

**Parameters**:
- `user_id`: The ID of the user
- `id`: The ID of the task

**Response**: Task object

#### PUT /api/{user_id}/tasks/{id}
Update a specific task.

**Parameters**:
- `user_id`: The ID of the user
- `id`: The ID of the task

**Request Body**:
```json
{
  "title": "Updated title",
  "description": "Updated description"
}
```

**Response**: Updated task object

#### DELETE /api/{user_id}/tasks/{id}
Delete a specific task.

**Parameters**:
- `user_id`: The ID of the user
- `id`: The ID of the task

**Response**: Empty with 204 status code

#### PATCH /api/{user_id}/tasks/{id}/complete
Update the completion status of a task.

**Parameters**:
- `user_id`: The ID of the user
- `id`: The ID of the task

**Request Body**:
```json
{
  "completed": true
}
```

**Response**: Updated task object

## Authentication

The API uses JWT tokens for authentication. The token must be included in the Authorization header as a Bearer token. The user_id in the token must match the user_id in the URL for authorization validation.

## Error Handling

- `401 Unauthorized`: No/invalid JWT token
- `404 Not Found`: Requested resource doesn't exist
- `400 Bad Request`: Invalid input data
- `422 Unprocessable Entity`: Validation errors

## Testing

Run the tests using pytest:
```bash
pytest
```

For detailed test reports:
```bash
pytest --verbose --cov=backend
```