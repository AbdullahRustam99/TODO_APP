# Data Model: Phase II - Frontend UI

**Date**: 2025-12-29
**Feature**: Phase II - Frontend UI
**Input**: Feature specification from `/specs/002-frountend-create-frontend/spec.md`

## Entities

### User
**Description**: Represents an authenticated user with credentials managed by Better Auth

**Fields**:
- `id`: number (required) - Unique identifier for the user
- `email`: string (required) - User's email address for login
- `name`: string (required) - User's display name
- `createdAt`: string (ISO date format) - Account creation timestamp
- `updatedAt`: string (ISO date format) - Last update timestamp

**Validation Rules**:
- Email must be a valid email format
- Email must be unique
- Name must be 1-50 characters

### Task
**Description**: Represents a user's todo item with ID, title, description, completion status, and creation/update timestamps

**Fields**:
- `id`: number (required) - Unique identifier for the task
- `title`: string (required) - Task title/description (max 200 characters)
- `description`: string (optional) - Detailed task description (max 1000 characters)
- `completed`: boolean (required) - Completion status (true/false)
- `userId`: number (required) - Foreign key linking to the user who owns this task
- `createdAt`: string (ISO date format) - Task creation timestamp
- `updatedAt`: string (ISO date format) - Last update timestamp
- `dueDate`: string (optional, ISO date format) - Task due date if applicable
- `priority`: string (optional, values: 'high', 'medium', 'low') - Task priority level

**Validation Rules**:
- Title must be 1-200 characters
- Description, if provided, must be 1-1000 characters
- UserId must reference an existing user
- Priority, if provided, must be one of 'high', 'medium', 'low'
- Due date, if provided, must be a valid future date

### JWT Token
**Description**: Authentication token stored securely in browser and attached to API requests for authorization

**Fields**:
- `token`: string (required) - The JWT token string
- `expiresAt`: string (ISO date format) - Token expiration timestamp
- `userId`: number (required) - User ID associated with this token

**Validation Rules**:
- Token must be a valid JWT format
- Token must not be expired at time of use
- UserId must reference an existing user

### Task Filter
**Description**: Represents the current filter state (All, Active, Completed, Priority) for task display

**Fields**:
- `status`: string (required, values: 'all', 'active', 'completed') - Filter by completion status
- `priority`: string (optional, values: 'high', 'medium', 'low') - Filter by priority level
- `searchQuery`: string (optional) - Text search query for title/description filtering

**Validation Rules**:
- Status must be one of 'all', 'active', 'completed'
- Priority, if provided, must be one of 'high', 'medium', 'low'
- Search query, if provided, must be 1-100 characters

## State Transitions

### Task State Transitions
- `incomplete` → `completed`: When user marks task as complete
- `completed` → `incomplete`: When user unmarks task as complete

### User Authentication States
- `unauthenticated` → `authenticated`: After successful login/signup
- `authenticated` → `unauthenticated`: After logout or token expiration

## Relationships

### User → Task
- One-to-Many relationship
- A user can own multiple tasks
- Each task belongs to exactly one user
- Tasks are filtered by userId when displayed to user

## Data Flow

### Authentication Flow
1. User provides credentials → Better Auth validates → JWT token generated
2. JWT token stored securely in browser
3. Token attached to all API requests automatically
4. Token validated by backend on each request

### Task Management Flow
1. User creates task → Data validated on frontend → API request with JWT
2. Backend validates user permissions → Task saved to database
3. Response with task data returned → Task displayed in UI
4. User interacts with task → Changes validated → API request with JWT
5. Backend updates task → Response returned → UI updated

## TypeScript Interfaces

### User Interface
```typescript
interface User {
  id: number;
  email: string;
  name: string;
  createdAt: string;
  updatedAt: string;
}
```

### Task Interface
```typescript
interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  userId: number;
  createdAt: string;
  updatedAt: string;
  dueDate?: string;
  priority?: 'high' | 'medium' | 'low';
}
```

### JWT Token Interface
```typescript
interface JWTToken {
  token: string;
  expiresAt: string;
  userId: number;
}
```

### Task Filter Interface
```typescript
interface TaskFilter {
  status: 'all' | 'active' | 'completed';
  priority?: 'high' | 'medium' | 'low';
  searchQuery?: string;
}
```

### Authentication State Interface
```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  loading: boolean;
  isAuthenticated: boolean;
  error: string | null;
}
```

### Task State Interface
```typescript
interface TaskState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  currentTask: Task | null;
  filters: TaskFilter;
}
```

### API Response Interface
```typescript
interface APIResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}
```

### Form Validation Errors Interface
```typescript
interface FormErrors {
  title?: string;
  description?: string;
  email?: string;
  password?: string;
  general?: string;
}
```

### Task Creation Request Interface
```typescript
interface CreateTaskRequest {
  title: string;
  description?: string;
  completed?: boolean;
  dueDate?: string;
  priority?: 'high' | 'medium' | 'low';
}
```

### Task Update Request Interface
```typescript
interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
  dueDate?: string;
  priority?: 'high' | 'medium' | 'low';
}
```

### Login Request Interface
```typescript
interface LoginRequest {
  email: string;
  password: string;
}
```

### Register Request Interface
```typescript
interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}
```

### API Client Configuration
```typescript
interface ApiClientConfig {
  baseURL: string;
  timeout: number;
  headers: Record<string, string>;
}
```

## Storage Mechanisms

### Client-Side Storage
- **JWT Token**: Stored in httpOnly cookie when possible, otherwise in secure localStorage with proper security measures
- **User Preferences**: Stored in localStorage (theme preference, UI settings, filter preferences)
- **Cached Data**: Temporary caching of API responses in memory using React state management
- **Form Data**: Temporary storage of form inputs in component state during user interactions

### API Integration
- **Base URL**: Configurable via environment variables (NEXT_PUBLIC_API_BASE_URL)
- **Authentication Header**: `Authorization: Bearer {token}` for all authenticated requests
- **Content Type**: `application/json` for all requests
- **Error Handling**: Standardized error responses with appropriate HTTP status codes and user-friendly messages
- **Request Timeout**: Configurable timeout for API requests to handle network issues gracefully

## Validation Schema

### Task Validation Schema
```typescript
const taskValidationSchema = {
  title: {
    required: true,
    minLength: 1,
    maxLength: 200,
    trim: true,
  },
  description: {
    required: false,
    maxLength: 1000,
    trim: true,
  },
  priority: {
    required: false,
    enum: ['high', 'medium', 'low'],
  },
  dueDate: {
    required: false,
    type: 'date',
  },
  completed: {
    type: 'boolean',
  },
};
```

### User Validation Schema
```typescript
const userValidationSchema = {
  email: {
    required: true,
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    maxLength: 255,
  },
  name: {
    required: true,
    minLength: 1,
    maxLength: 50,
    trim: true,
  },
  password: {
    required: true,
    minLength: 8,
    maxLength: 128,
  },
};
```

### Form Validation Patterns
- Client-side validation occurs on form submission and on field blur
- Validation errors displayed inline near the relevant form fields
- Validation messages use non-technical language for user-friendliness
- Disabled submit buttons during API calls to prevent duplicate submissions