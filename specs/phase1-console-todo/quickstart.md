# Quickstart Guide: Phase I - Console TODO App

**Date**: 2025-12-27
**Feature**: Phase I - Console TODO App

## Getting Started

### Prerequisites
- Python 3.13 or higher
- UV package manager (optional, for environment management)

### Installation

1. Clone the repository
2. Navigate to the project directory
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies (if any are added in the future)

### Running the Application

Execute the main application file:
```bash
python src/main.py
```

The application will start and display a prompt where you can enter commands.

## Available Commands

### `add`
Add a new task with a title and optional description.
```
add Buy groceries
add Complete project proposal - Description for the project
```

### `view`
View all tasks with their ID, title, description, and status.
```
view
```

### `update`
Update an existing task by ID with a new title and/or description.
```
update 1 New task title
update 2 - Description only
update 3 Updated title - New description
```

### `delete`
Delete a task by its ID.
```
delete 1
```

### `mark`
Mark a task as pending, in_progress, or done.
```
mark 1 pending
mark 2 in_progress
mark 3 done
```

### `help`
Display available commands and their usage.
```
help
```

### `exit`
Exit the application gracefully.
```
exit
```

## Example Workflow

```
$ python src/main.py
Welcome to the TODO App! Type 'help' for available commands.
> add Buy groceries
Task 1 added: Buy groceries (pending)
> add Complete project proposal - Important project work
Task 2 added: Complete project proposal (pending) [Important project work]
> view
ID | Title                    | Description           | Status
1  | Buy groceries            |                       | pending
2  | Complete project proposal| Important project work| pending
> mark 2 in_progress
Task 2 marked as in_progress
> exit
Goodbye!
```

## Troubleshooting

- If you get a "command not found" error, ensure you're running Python from the correct directory
- If the application crashes, check that you're providing the correct arguments to each command
- For invalid task IDs, the application will display an appropriate error message