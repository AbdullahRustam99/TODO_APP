# API Contract: Task Management API

**Date**: 2025-12-27
**Feature**: Phase II - Backend API
**Version**: 1.0.0

## Overview

This document specifies the RESTful API contract for task management operations. All endpoints require JWT authentication and enforce user isolation through user_id validation.

## Authentication

All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

The user_id in the token must match the user_id in the URL path for authorization validation.

## Base Path

`/api/{user_id}`

## Endpoints

### GET /api/{user_id}/tasks

**Purpose**: Retrieve all tasks for the specified user

**Parameters**:
- `user_id` (path): The ID of the authenticated user

**Headers**:
- `Authorization`: Bearer token with valid JWT

**Success Response**:
- `200 OK`
- `Content-Type: application/json`
```json
[
  {
    "id": 1,
    "user_id": 123,
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
]
```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User_id in token doesn't match user_id in URL

### POST /api/{user_id}/tasks

**Purpose**: Create a new task for the specified user

**Parameters**:
- `user_id` (path): The ID of the authenticated user

**Headers**:
- `Authorization`: Bearer token with valid JWT
- `Content-Type`: application/json

**Request Body**:
```json
{
  "title": "Task title",
  "description": "Optional task description"
}
```

**Success Response**:
- `201 Created`
- `Content-Type: application/json`
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Task title",
  "description": "Optional task description",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid request body or missing required fields
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User_id in token doesn't match user_id in URL

### GET /api/{user_id}/tasks/{id}

**Purpose**: Retrieve a specific task by ID

**Parameters**:
- `user_id` (path): The ID of the authenticated user
- `id` (path): The ID of the task to retrieve

**Headers**:
- `Authorization`: Bearer token with valid JWT

**Success Response**:
- `200 OK`
- `Content-Type: application/json`
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User_id in token doesn't match user_id in URL
- `404 Not Found`: Task with specified ID doesn't exist

### PUT /api/{user_id}/tasks/{id}

**Purpose**: Update a specific task

**Parameters**:
- `user_id` (path): The ID of the authenticated user
- `id` (path): The ID of the task to update

**Headers**:
- `Authorization`: Bearer token with valid JWT
- `Content-Type`: application/json

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description"
}
```

**Success Response**:
- `200 OK`
- `Content-Type: application/json`
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid request body
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User_id in token doesn't match user_id in URL
- `404 Not Found`: Task with specified ID doesn't exist

### DELETE /api/{user_id}/tasks/{id}

**Purpose**: Delete a specific task

**Parameters**:
- `user_id` (path): The ID of the authenticated user
- `id` (path): The ID of the task to delete

**Headers**:
- `Authorization`: Bearer token with valid JWT

**Success Response**:
- `204 No Content`

**Error Responses**:
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User_id in token doesn't match user_id in URL
- `404 Not Found`: Task with specified ID doesn't exist

### PATCH /api/{user_id}/tasks/{id}/complete

**Purpose**: Update the completion status of a task

**Parameters**:
- `user_id` (path): The ID of the authenticated user
- `id` (path): The ID of the task to update

**Headers**:
- `Authorization`: Bearer token with valid JWT
- `Content-Type`: application/json

**Request Body**:
```json
{
  "completed": true
}
```

**Success Response**:
- `200 OK`
- `Content-Type: application/json`
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Task title",
  "description": "Task description",
  "completed": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid request body (completed field missing or invalid)
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User_id in token doesn't match user_id in URL
- `404 Not Found`: Task with specified ID doesn't exist

## Data Models

### Task
```json
{
  "id": 1,
  "user_id": 123,
  "title": "string",
  "description": "string (optional)",
  "completed": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### Request/Response Validation

All requests and responses must conform to these validation rules:
- `id` and `user_id` must be positive integers
- `title` must be 1-255 characters
- `description` can be up to 1000 characters (optional)
- `completed` must be a boolean value
- `created_at` and `updated_at` must be valid ISO 8601 timestamps