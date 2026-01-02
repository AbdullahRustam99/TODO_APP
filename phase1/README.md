# TODO Console Application

Interactive console-based TODO application with number-based menu selection. The application provides task management (Add, View, Update, Delete, Mark Complete) with in-memory storage using Python data structures.

## Features

- Number-based menu selection (1-6) and Enter key selection
- Menu-driven interface with visual selection
- Add, view, update, delete, and mark tasks as complete/incomplete
- In-memory storage (tasks persist only during session)
- Error handling and validation

## Requirements

- Python 3.13 or higher

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies: `uv sync` (or `pip install -r requirements.txt`)

## Usage

Run the application:
```bash
uv run python main.py
```

Or if installed as a package:
```bash
todo-app
```

## Navigation

- Use **number keys (1-6)** to select menu options
- Use **Enter** to confirm your selection

## Menu Options

- **Add Task**: Add a new task with title and optional description
- **View Tasks**: See all tasks with ID, title, and completion status (✓ Completed / ✗ Pending)
- **Update Task**: Update an existing task by ID
- **Delete Task**: Remove a task by ID with confirmation
- **Mark Task Complete / Incomplete**: Toggle task completion status by ID
- **Exit**: Close the application

## License

MIT