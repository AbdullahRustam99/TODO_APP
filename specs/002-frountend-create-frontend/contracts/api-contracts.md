# API Contracts: Phase II - Frontend UI

**Feature**: Phase II - Frontend UI
**Date**: 2025-12-27
**Input**: Feature specification from `/specs/002-frountend-create-frontend/spec.md`

## Overview

This document defines the API contracts between the frontend and backend for the Todo List application. These contracts ensure consistent communication and data exchange between the client and server.

## Authentication API

### POST /api/auth/signup
**Description**: Create a new user account

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Response (Success - 201)**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user-uuid",
      "email": "user@example.com",
      "name": "John Doe",
      "createdAt": "2025-12-27T10:00:00Z",
      "updatedAt": "2025-12-27T10:00:00Z"
    },
    "token": "jwt-token-string"
  },
  "message": "User created successfully"
}
```

**Response (Error - 400)**:
```json
{
  "success": false,
  "error": "Email already exists"
}
```

### POST /api/auth/login
**Description**: Authenticate user and return JWT token

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (Success - 200)**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user-uuid",
      "email": "user@example.com",
      "name": "John Doe",
      "createdAt": "2025-12-27T10:00:00Z",
      "updatedAt": "2025-12-27T10:00:00Z"
    },
    "token": "jwt-token-string"
  },
  "message": "Login successful"
}
```

**Response (Error - 401)**:
```json
{
  "success": false,
  "error": "Invalid credentials"
}
```

### POST /api/auth/logout
**Description**: Logout user and invalidate token

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Response (Success - 200)**:
```json
{
  "success": true,
  "message": "Logout successful"
}
```

## Task Management API

### GET /api/tasks
**Description**: Retrieve all tasks for the authenticated user

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Response (Success - 200)**:
```json
{
  "success": true,
  "data": [
    {
      "id": "task-uuid",
      "userId": "user-uuid",
      "title": "Complete project",
      "description": "Finish the frontend implementation",
      "isCompleted": false,
      "createdAt": "2025-12-27T10:00:00Z",
      "updatedAt": "2025-12-27T10:00:00Z"
    }
  ]
}
```

### POST /api/tasks
**Description**: Create a new task

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Request**:
```json
{
  "title": "New task",
  "description": "Task description",
  "isCompleted": false
}
```

**Response (Success - 201)**:
```json
{
  "success": true,
  "data": {
    "id": "task-uuid",
    "userId": "user-uuid",
    "title": "New task",
    "description": "Task description",
    "isCompleted": false,
    "createdAt": "2025-12-27T10:00:00Z",
    "updatedAt": "2025-12-27T10:00:00Z"
  },
  "message": "Task created successfully"
}
```

### GET /api/tasks/{id}
**Description**: Retrieve a specific task

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Response (Success - 200)**:
```json
{
  "success": true,
  "data": {
    "id": "task-uuid",
    "userId": "user-uuid",
    "title": "Existing task",
    "description": "Task description",
    "isCompleted": false,
    "createdAt": "2025-12-27T10:00:00Z",
    "updatedAt": "2025-12-27T10:00:00Z"
  }
}
```

### PUT /api/tasks/{id}
**Description**: Update an existing task

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Request**:
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "isCompleted": true
}
```

**Response (Success - 200)**:
```json
{
  "success": true,
  "data": {
    "id": "task-uuid",
    "userId": "user-uuid",
    "title": "Updated task title",
    "description": "Updated description",
    "isCompleted": true,
    "createdAt": "2025-12-27T10:00:00Z",
    "updatedAt": "2025-12-27T11:00:00Z"
  },
  "message": "Task updated successfully"
}
```

### DELETE /api/tasks/{id}
**Description**: Delete a task

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Response (Success - 200)**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

## Error Response Format

All error responses follow this format:

```json
{
  "success": false,
  "error": "Error message describing what went wrong",
  "message": "Human-readable message"
}
```

## HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource successfully created
- `400 Bad Request`: Invalid request format or validation error
- `401 Unauthorized`: Authentication required or token invalid
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Requested resource not found
- `500 Internal Server Error`: Server error

## Authentication Requirements

- All task management endpoints require a valid JWT token in the `Authorization` header
- Authentication tokens must be prefixed with `Bearer `
- Tokens expire after 24 hours and need to be refreshed

## Rate Limiting

- API requests are limited to 1000 requests per hour per user
- Exceeding the limit results in a 429 (Too Many Requests) response

## Request/Response Headers

### Common Request Headers
- `Authorization: Bearer {token}` - Required for authenticated endpoints
- `Content-Type: application/json` - For JSON request bodies
- `Accept: application/json` - Expected response format

### Common Response Headers
- `Content-Type: application/json` - Response format
- `X-RateLimit-Limit: 1000` - Rate limit for the user
- `X-RateLimit-Remaining: 999` - Remaining requests in the current window