# Quickstart Guide: Phase I - Console TODO App (Arrow-Key Navigation)

**Date**: 2026-01-02
**Feature**: Phase I - Console TODO App (Arrow-Key Navigation)

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

The application will start and display an interactive menu with visual selection using arrow keys.

## Navigation Guide

### Menu Navigation
- Use **Up Arrow (↑)** to move selection up in the menu
- Use **Down Arrow (↓)** to move selection down in the menu
- Use **Enter** to select the highlighted menu option
- Menu selections loop (bottom to top, top to bottom)

### Available Menu Options

#### Add Task
- Navigate to "Add Task" and press Enter
- Enter task title when prompted
- Optionally enter task description
- Task will be added with auto-generated ID

#### View Tasks
- Navigate to "View Tasks" and press Enter
- See all tasks with ID, title, and completion status (✓ Completed / ✗ Pending)

#### Update Task
- Navigate to "Update Task" and press Enter
- Enter the task ID when prompted
- Enter new title and/or description when prompted
- Task will be updated in memory

#### Delete Task
- Navigate to "Delete Task" and press Enter
- Enter the task ID when prompted
- Confirm deletion when prompted
- Task will be removed from memory

#### Mark Task Complete / Incomplete
- Navigate to "Mark Task Complete / Incomplete" and press Enter
- Enter the task ID when prompted
- Task completion status will be toggled

#### Exit
- Navigate to "Exit" and press Enter
- Application will terminate gracefully

## Example Workflow

```
$ python src/main.py
┌─────────────────────────┐
│     TODO APPLICATION    │
├─────────────────────────┤
│ > Add Task              │
│   View Tasks            │
│   Update Task           │
│   Delete Task           │
│   Mark Task Complete    │
│   Exit                  │
└─────────────────────────┘

[Use arrow keys to navigate, Enter to select]

[User presses Down Arrow twice, then Enter]
> Selected: View Tasks
> No tasks available

[User presses Up Arrow 5 times to loop to "Add Task", then Enter]
> Selected: Add Task
> Enter task title: Buy groceries
> Enter task description (optional): Weekly shopping
> Task added with ID: 1

[User presses Down Arrow once and Enter to view tasks]
> Selected: View Tasks
> 1. Buy groceries [Weekly shopping] - ✗ Pending
```

## Troubleshooting

- If arrow keys don't respond, ensure you're running in a terminal that supports curses (most modern terminals do)
- If the application crashes, check that you're providing valid inputs when prompted
- For invalid task IDs, the application will display an appropriate error message and return to the menu
- If you see display issues, resize your terminal window or try a different terminal application