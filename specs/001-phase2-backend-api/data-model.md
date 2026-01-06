# Data Model: Phase II - Backend API

**Date**: 2025-12-27
**Feature**: Phase II - Backend API
**Input**: Feature specification and research findings

## Core Entities

### User
**Description**: Represents a registered user in the system with authentication information.

**Attributes**:
- `id`: integer - Unique identifier for the user (primary key, auto-generated)
- `email`: string - User's email address (unique, required, indexed)
- `name`: string - User's display name (required, max 255 characters)
- `created_at`: datetime - Timestamp when the user was created (auto-generated)

**Validation Rules**:
- `id` must be unique within the database
- `email` must be a valid email format and unique
- `name` must not be empty and must be less than 255 characters
- `created_at` is set automatically when record is created

**Relationships**:
- One User has many Tasks (via user_id foreign key)

### Task
**Description**: Represents a user's todo item with properties for content, status, and ownership.

**Attributes**:
- `id`: integer - Unique identifier for the task (primary key, auto-generated)
- `user_id`: integer - Foreign key linking to the User who owns this task (required)
- `title`: string - Title of the task (required, max 255 characters)
- `description`: string - Detailed description of the task (optional, max 1000 characters)
- `completed`: boolean - Whether the task is completed (default: false)
- `created_at`: datetime - Timestamp when the task was created (auto-generated)
- `updated_at`: datetime - Timestamp when the task was last updated (auto-generated, updates on change)

**Validation Rules**:
- `id` must be unique within the database
- `user_id` must reference an existing User
- `title` must not be empty or whitespace-only
- `completed` defaults to false when creating new tasks
- `created_at` is set automatically when record is created
- `updated_at` is automatically updated when the record changes

**State Transitions**:
- A new task starts with `completed` as false
- The `completed` state can transition from false to true or true to false

### JWT Token (Conceptual)
**Description**: Represents authentication token containing user identity information.

**Attributes**:
- `sub`: string - Subject identifier (user ID)
- `exp`: integer - Expiration timestamp (Unix timestamp)
- `iat`: integer - Issued at timestamp (Unix timestamp)
- `user_id`: integer - User identifier for authorization validation

**Validation Rules**:
- Token must be properly signed and verified
- Token must not be expired at the time of validation
- `user_id` in token must match the user_id in the request URL for authorization

## Relationships

- One User → Many Tasks (via user_id foreign key)
- Each Task belongs to exactly one User
- Task `user_id` references User `id` (foreign key relationship)

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## Constraints

- Database uses referential integrity to ensure data consistency
- Cascade delete on User deletion removes associated Tasks
- Email uniqueness constraint prevents duplicate user accounts
- Non-null constraints on required fields ensure data completeness
- Indexes on user_id in tasks table for efficient querying
- Default values ensure consistent behavior for optional fields