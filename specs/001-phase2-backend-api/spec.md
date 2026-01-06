# Feature Specification: Phase II - Backend API

**Feature Branch**: `001-phase2-backend-api`
**Created**: 2025-12-27
**Status**: Draft
**Input**: User description: "BACKEND

Create the backend specification for Phase II of the Evolution of Todo project.

Requirements:
- Backend must use Python FastAPI and SQLModel ORM
- Connect to Neon Serverless PostgreSQL for data persistence
- Implement RESTful API endpoints for Task CRUD:
  - GET    /api/{user_id}/tasks
  - POST   /api/{user_id}/tasks
  - GET    /api/{user_id}/tasks/{id}
  - PUT    /api/{user_id}/tasks/{id}
  - DELETE /api/{user_id}/tasks/{id}
  - PATCH  /api/{user_id}/tasks/{id}/complete
- Implement JWT authentication and authorization:
  - Verify JWT token from frontend
  - Ensure user_id in URL matches token user
  - Filter tasks by authenticated user only
- Database models:
  - users table: id, email, name, created_at
  - tasks table: id, user_id, title, description, completed, created_at, updated_at
- Middleware for JWT verification
- Proper error handling:
  - 401 Unauthorized if no/invalid token
  - 404 Not Found if task not exist
  - 400 Bad Request if input invalid
- Include logging for critical actions: create/update/delete tasks
- Ensure DB connections are properly closed and managed
- Include ready-to-use SQLModel queries for all CRUD operations
- Secure handling of environment variables: DATABASE_URL, BETTER_AUTH_SECRET

Non-functional:
- Clean Python project structure
- Deterministic API responses
- Readable and maintainable code
- Align with CLAUDE.md patterns for backend

Output expectation:
- Define API endpoints with request and response models
- Define JWT auth middleware and user verification flow
- Define database model"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Secure Task Management (Priority: P1)

As an authenticated user, I want to securely manage my tasks through a RESTful API so that I can organize my work from the frontend application while ensuring my data is protected and isolated from other users.

**Why this priority**: This provides the core functionality that connects the frontend to the backend, enabling users to create, read, update, and delete their tasks with proper security and authentication.

**Independent Test**: Can be fully tested by authenticating with a valid JWT token and performing CRUD operations on tasks, confirming that only the authenticated user's tasks are accessible.

**Acceptance Scenarios**:

1. **Given** I have a valid JWT token, **When** I send a POST request to /api/{my_user_id}/tasks with valid task data, **Then** a new task is created and associated with my user account
2. **Given** I have created tasks, **When** I send a GET request to /api/{my_user_id}/tasks with my valid token, **Then** I receive a list of only my tasks
3. **Given** I have tasks with different completion states, **When** I send a PATCH request to /api/{my_user_id}/tasks/{id}/complete, **Then** the task's completion status is updated

---

### User Story 2 - User Authentication & Authorization (Priority: P2)

As a user of the todo application, I want the backend to verify my identity through JWT tokens and ensure I can only access my own data so that my tasks remain private and secure.

**Why this priority**: Security is critical for user data protection, ensuring that users can only access and modify their own tasks and that unauthorized users cannot access any data.

**Independent Test**: Can be tested by attempting API calls with valid/invalid/missing tokens and confirming that appropriate access controls are enforced.

**Acceptance Scenarios**:

1. **Given** I have a valid JWT token, **When** I make any API request with the token in headers, **Then** the request is processed and my user_id is verified against the URL
2. **Given** I have an invalid or expired JWT token, **When** I make an API request, **Then** I receive a 401 Unauthorized response
3. **Given** I attempt to access another user's tasks with my token, **When** I make a request with mismatched user_id, **Then** I receive a 401 Unauthorized response

---

### User Story 3 - Error Handling & Logging (Priority: P3)

As a system administrator, I want the backend API to properly handle errors and log critical actions so that I can monitor system health and troubleshoot issues effectively.

**Why this priority**: Proper error handling and logging are essential for maintaining system reliability and providing visibility into system operations for debugging and monitoring purposes.

**Independent Test**: Can be tested by making various invalid requests and confirming appropriate error responses and log entries are created.

**Acceptance Scenarios**:

1. **Given** I make a request with invalid task data, **When** I send the request, **Then** I receive a 400 Bad Request response with clear error details
2. **Given** I request a non-existent task, **When** I make the request, **Then** I receive a 404 Not Found response
3. **Given** I perform CRUD operations on tasks, **When** actions are completed, **Then** appropriate log entries are created for create/update/delete operations

---

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST provide RESTful API endpoints for task CRUD operations at /api/{user_id}/tasks and /api/{user_id}/tasks/{id}
- **FR-002**: System MUST verify JWT tokens from incoming requests and authenticate users before processing requests
- **FR-003**: System MUST ensure the user_id in the URL matches the authenticated user from the JWT token
- **FR-004**: System MUST filter tasks so that users can only access tasks associated with their own user_id
- **FR-005**: System MUST provide PATCH endpoint at /api/{user_id}/tasks/{id}/complete to update task completion status
- **FR-006**: System MUST return 401 Unauthorized for requests with no/invalid JWT tokens
- **FR-007**: System MUST return 404 Not Found for requests to non-existent tasks
- **FR-008**: System MUST return 400 Bad Request for requests with invalid input data
- **FR-009**: System MUST log create, update, and delete operations for tasks
- **FR-010**: System MUST securely handle environment variables including DATABASE_URL and BETTER_AUTH_SECRET
- **FR-011**: System MUST properly manage database connections and ensure they are closed after use
- **FR-012**: System MUST use SQLModel ORM for all database operations with Neon Serverless PostgreSQL

### Key Entities *(include if feature involves data)*

- **User**: Represents a registered user with id (integer), email (string), name (string), created_at (timestamp)
- **Task**: Represents a user's todo item with id (integer), user_id (integer), title (string), description (string), completed (boolean), created_at (timestamp), updated_at (timestamp)
- **JWT Token**: Authentication token containing user identity information for verifying user identity and permissions

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Users can successfully authenticate with JWT tokens and perform CRUD operations on their tasks
- **SC-002**: System processes 95% of valid API requests with response times under 500ms
- **SC-003**: Authentication and authorization failures result in appropriate 401 responses within 100ms
- **SC-004**: All critical actions (create, update, delete) are logged with sufficient detail for debugging
- **SC-005**: Database connections are properly managed with no connection leaks during high-traffic scenarios
- **SC-006**: System successfully handles 1000 concurrent authenticated users without performance degradation