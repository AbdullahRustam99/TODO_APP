# Data Model: Phase I - Console TODO App (Arrow-Key Navigation)

**Date**: 2026-01-02
**Feature**: Phase I - Console TODO App (Arrow-Key Navigation)
**Input**: Feature specification and research findings

## Core Entities

### Task
**Description**: Represents a single todo item with properties for identification, content, and completion status.

**Attributes**:
- `id`: integer - Unique identifier for the task (auto-generated)
- `title`: string - Title of the task (required)
- `description`: string - Detailed description of the task (optional, default: "")
- `completed`: boolean - Completion status of the task (true = completed, false = pending)

**Validation Rules**:
- `id` must be unique within the application session
- `title` must not be empty or whitespace-only
- `completed` is a boolean value (true/false)

**State Transitions**:
- A new task starts with `completed` = false
- Status can be toggled between completed (true) and pending (false)

### TaskCollection
**Description**: In-memory storage for tasks, providing CRUD operations.

**Operations**:
- `add_task(title, description)`: Creates a new task with auto-generated ID
- `get_task(task_id)`: Retrieves a task by ID
- `update_task(task_id, title, description)`: Updates task properties
- `delete_task(task_id)`: Removes a task
- `toggle_task_completion(task_id)`: Toggles task completion status
- `list_tasks()`: Returns all tasks
- `list_completed_tasks()`: Returns tasks with completed status
- `list_pending_tasks()`: Returns tasks with pending status

## Relationships

- Each TaskCollection contains multiple Tasks
- Each Task belongs to exactly one TaskCollection
- Task IDs are unique within a TaskCollection

## Constraints

- Task IDs are auto-incrementing integers starting from 1
- Task titles must be between 1 and 255 characters
- Descriptions can be up to 1000 characters
- Task objects are stored in memory only during the application session
- Task titles cannot be empty when adding or updating tasks