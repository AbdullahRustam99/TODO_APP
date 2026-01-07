# Data Model: Phase I - Console TODO App

**Date**: 2025-12-27
**Feature**: Phase I - Console TODO App
**Input**: Feature specification and research findings

## Core Entities

### Task
**Description**: Represents a single todo item with properties for identification, content, status, and creation time.

**Attributes**:
- `id`: integer - Unique identifier for the task (auto-generated)
- `title`: string - Title/description of the task (required)
- `description`: string - Detailed description of the task (optional, default: "")
- `status`: enum (TaskStatus) - Current state of the task (pending, in_progress, done)
- `created_at`: datetime - Timestamp when the task was created

**Validation Rules**:
- `id` must be unique within the application session
- `title` must not be empty or whitespace-only
- `status` must be one of the allowed values: pending, in_progress, done

**State Transitions**:
- A new task starts with status "pending"
- Status can transition from any state to any other state
- Status changes should be tracked for audit purposes

### TaskStatus (Enum)
**Values**:
- `pending`: Task is created but not yet started
- `in_progress`: Task is currently being worked on
- `done`: Task has been completed

### TaskCollection
**Description**: In-memory storage for tasks, providing CRUD operations.

**Operations**:
- `add_task(title, description)`: Creates a new task with auto-generated ID
- `get_task(task_id)`: Retrieves a task by ID
- `update_task(task_id, title, description)`: Updates task properties
- `delete_task(task_id)`: Removes a task
- `mark_task_status(task_id, status)`: Updates task status
- `list_tasks()`: Returns all tasks
- `list_tasks_by_status(status)`: Returns tasks with specific status

## Relationships

- Each TaskCollection contains multiple Tasks
- Each Task belongs to exactly one TaskCollection
- Task IDs are unique within a TaskCollection

## Constraints

- Task IDs are auto-incrementing integers starting from 1
- Task titles must be between 1 and 255 characters
- Descriptions can be up to 1000 characters
- Task objects are stored in memory only during the application session