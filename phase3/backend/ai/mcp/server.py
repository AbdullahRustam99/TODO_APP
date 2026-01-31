"""
MCP Server for task management operations (Phase III).

This module implements a proper MCP server using the FastMCP SDK.
The server exposes task operations as MCP tools that can be called by AI agents.
All operations are performed via HTTP calls to the backend API, not direct database access.

MCP Tools provided:
- add_task: Create a new task for a user
- list_tasks: Retrieve tasks with optional filtering
- complete_task: Mark a task as complete
- delete_task: Remove a task from the database
- update_task: Modify task title or description
- set_priority: Update task priority level
- list_tasks_by_priority: Filter tasks by priority

Architecture:
- MCP Server runs as a separate process (not inside agent)
- Agent connects via MCPServerStdio transport
- Tools use @mcp.tool() decorator (not @function_tool)
- All operations use HTTP API calls to backend, not direct database access
"""

import os
import re
from typing import Literal, Optional
import httpx
from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP("task-management-server")

# Get backend base URL from environment, default to local development
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://127.0.0.1:8000")


def detect_priority_from_text(text: str) -> str:
    """
    Detect priority level from user input text using NLP patterns.

    Args:
        text: User input text (task title/description)

    Returns:
        str: Detected priority level ("low", "medium", "high") or "medium" if not detected

    Examples:
        >>> detect_priority_from_text("Create HIGH priority task to buy milk")
        "high"
        >>> detect_priority_from_text("Add a task")
        "medium"
        >>> detect_priority_from_text("This is URGENT")
        "high"
    """
    text_lower = text.lower()

    # High priority patterns
    high_priority_patterns = [
        r'\bhigh\s*priority\b',
        r'\burgent\b',
        r'\bcritical\b',
        r'\bimportant\b',
        r'\basap\b',
        r'\bhigh\b',
    ]

    # Low priority patterns
    low_priority_patterns = [
        r'\blow\s*priority\b',
        r'\bminor\b',
        r'\boptional\b',
        r'\bwhen\s*you\s*have\s*time\b',
        r'low',
    ]

    # Check for high priority first (more specific)
    for pattern in high_priority_patterns:
        if re.search(pattern, text_lower):
            return "high"

    # Check for low priority
    for pattern in low_priority_patterns:
        if re.search(pattern, text_lower):
            return "low"

    # Check for medium/normal priority patterns
    if re.search(r'\bmedium\b|\bnormal\b', text_lower):
        return "medium"

    # Default to medium if no pattern matches
    return "medium"


@mcp.tool()
async def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None,
    priority: Optional[str] = None,
) -> dict:
    """
    Create a new task for a user via HTTP API call.

    MCP Tool Contract:
    - Purpose: Add a task to user's todo list
    - Stateless: All state managed by backend API
    - User Isolation: Enforced via user_id parameter in API
    - Priority Detection: Extracts priority from title/description if not provided

    Args:
        user_id: User's unique identifier (string UUID from Better Auth)
        title: Task title (required, max 200 characters)
        description: Task description (optional, max 1000 characters)
        priority: Task priority level (optional: "low", "medium", "high")
            - If not provided, automatically detects from title + description

    Returns:
        dict: Task creation result from backend API
            - task_id (int): Created task ID
            - status (str): "created"
            - title (str): Task title
            - priority (str): Assigned priority level

    Example:
        >>> add_task(user_id="user-123", title="Create HIGH priority task to buy milk")
        {"task_id": 42, "status": "created", "title": "...", "priority": "high"}
        >>> add_task(user_id="user-123", title="Buy groceries", priority="high")
        {"task_id": 43, "status": "created", "title": "...", "priority": "high"}
    """
    # Detect priority from title and description if not provided
    if priority is None:
        # Combine title and description for priority detection
        combined_text = f"{title} {description or ''}"
        priority = detect_priority_from_text(combined_text)
    else:
        # Validate priority value
        priority = priority.lower()
        if priority not in ["low", "medium", "high"]:
            priority = "medium"

    # Prepare the payload for the backend API
    payload = {
        "title": title,
        "description": description,
        "priority": priority,
        "completed": False,  # New tasks are not completed by default
    }

    # Make HTTP request to backend API
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BACKEND_BASE_URL}/api/{user_id}/tasks",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    "task_id": result.get("id"),
                    "status": "created",
                    "title": result.get("title"),
                    "priority": result.get("priority"),
                }
            else:
                # Return error response
                return {
                    "error": f"Failed to create task: {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {
                "error": "Failed to create task",
                "details": str(e)
            }


@mcp.tool()
async def list_tasks(
    user_id: str,
    status: Literal["all", "pending", "completed"] = "all",
) -> dict:
    """
    Retrieve tasks from user's todo list via HTTP API call.

    MCP Tool Contract:
    - Purpose: List tasks with optional status filtering
    - Stateless: Backend handles database queries
    - User Isolation: Enforced via user_id parameter in API

    Args:
        user_id: User's unique identifier (string UUID from Better Auth)
        status: Filter by completion status (default: "all")
            - "all": All tasks
            - "pending": Incomplete tasks only
            - "completed": Completed tasks only

    Returns:
        dict: Task list result from backend API
            - tasks (list): Array of task objects
                - id (int): Task ID
                - title (str): Task title
                - description (str|None): Task description
                - completed (bool): Completion status
                - priority (str): Priority level
                - created_at (str): ISO 8601 timestamp
            - count (int): Total number of tasks returned

    Example:
        >>> list_tasks(user_id="user-123", status="pending")
        {
            "tasks": [
                {"id": 1, "title": "Buy groceries", "completed": False, ...},
                {"id": 2, "title": "Call dentist", "completed": False, ...}
            ],
            "count": 2
        }
    """
    # Build query parameters
    params = {"status": status} if status != "all" else {}

    # Make HTTP request to backend API
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BACKEND_BASE_URL}/api/{user_id}/tasks",
                params=params
            )

            if response.status_code == 200:
                result = response.json()
                tasks = result.get("tasks", [])

                # Convert tasks to expected format
                task_list = [
                    {
                        "id": task.get("id"),
                        "title": task.get("title"),
                        "description": task.get("description"),
                        "completed": task.get("completed", False),
                        "priority": task.get("priority"),
                        "created_at": task.get("created_at"),
                    }
                    for task in tasks
                ]

                return {
                    "tasks": task_list,
                    "count": len(task_list),
                }
            else:
                # Return error response
                return {
                    "error": f"Failed to list tasks: {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {
                "error": "Failed to list tasks",
                "details": str(e)
            }


@mcp.tool()
async def complete_task(
    user_id: str,
    task_id: int,
) -> dict:
    """
    Mark a task as complete via HTTP API call.

    MCP Tool Contract:
    - Purpose: Toggle task completion status to completed
    - Stateless: Updates managed by backend API
    - User Isolation: Enforced via user_id parameter in API

    Args:
        user_id: User's unique identifier (string UUID from Better Auth)
        task_id: Task ID to mark as complete

    Returns:
        dict: Task completion result from backend API
            - task_id (int): Updated task ID
            - status (str): "completed"
            - title (str): Task title

    Example:
        >>> complete_task(user_id="user-123", task_id=3)
        {"task_id": 3, "status": "completed", "title": "Call dentist"}
    """
    # Prepare the payload for toggling completion
    payload = {
        "completed": True
    }

    # Make HTTP request to backend API
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(
                f"{BACKEND_BASE_URL}/api/{user_id}/tasks/{task_id}",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    "task_id": result.get("id"),
                    "status": "completed",
                    "title": result.get("title"),
                }
            else:
                # Return error response
                return {
                    "error": f"Failed to complete task: {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {
                "error": "Failed to complete task",
                "details": str(e)
            }


@mcp.tool()
async def delete_task(
    user_id: str,
    task_id: int,
) -> dict:
    """
    Remove a task from the todo list via HTTP API call.

    MCP Tool Contract:
    - Purpose: Permanently delete task via backend API
    - Stateless: Deletion handled by backend
    - User Isolation: Enforced via user_id parameter in API

    Args:
        user_id: User's unique identifier (string UUID from Better Auth)
        task_id: Task ID to delete

    Returns:
        dict: Task deletion result from backend API
            - task_id (int): Deleted task ID
            - status (str): "deleted"
            - title (str): Task title (from pre-deletion state)

    Example:
        >>> delete_task(user_id="user-123", task_id=2)
        {"task_id": 2, "status": "deleted", "title": "Old reminder"}
    """
    # Make HTTP request to backend API
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(
                f"{BACKEND_BASE_URL}/api/{user_id}/tasks/{task_id}"
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    "task_id": task_id,
                    "status": "deleted",
                    "title": result.get("title", f"Task {task_id}"),
                }
            else:
                # Return error response
                return {
                    "error": f"Failed to delete task: {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {
                "error": "Failed to delete task",
                "details": str(e)
            }


@mcp.tool()
async def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
) -> dict:
    """
    Modify task details via HTTP API call.

    MCP Tool Contract:
    - Purpose: Update task details
    - Stateless: Updates handled by backend API
    - User Isolation: Enforced via user_id parameter in API
    - Partial Updates: At least one field must be provided

    Args:
        user_id: User's unique identifier (string UUID from Better Auth)
        task_id: Task ID to update
        title: New task title (optional, max 200 characters)
        description: New task description (optional, max 1000 characters)
        priority: New task priority (optional: "low", "medium", "high")

    Returns:
        dict: Task update result from backend API
            - task_id (int): Updated task ID
            - status (str): "updated"
            - title (str): Updated task title
            - priority (str): Updated priority level

    Example:
        >>> update_task(user_id="user-123", task_id=1, title="Buy groceries and fruits", priority="high")
        {"task_id": 1, "status": "updated", "title": "...", "priority": "high"}
    """
    # Validate: at least one field must be provided
    if title is None and description is None and priority is None:
        return {
            "error": "At least one of 'title', 'description', or 'priority' must be provided"
        }

    # Prepare the payload for the update
    payload = {}
    if title is not None:
        payload["title"] = title
    if description is not None:
        payload["description"] = description
    if priority is not None:
        payload["priority"] = priority

    # Make HTTP request to backend API
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(
                f"{BACKEND_BASE_URL}/api/{user_id}/tasks/{task_id}",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    "task_id": result.get("id"),
                    "status": "updated",
                    "title": result.get("title"),
                    "priority": result.get("priority"),
                }
            else:
                # Return error response
                return {
                    "error": f"Failed to update task: {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {
                "error": "Failed to update task",
                "details": str(e)
            }


@mcp.tool()
async def set_priority(
    user_id: str,
    task_id: int,
    priority: str,
) -> dict:
    """
    Set or update a task's priority level via HTTP API call.

    MCP Tool Contract:
    - Purpose: Update task priority level
    - Stateless: Updates handled by backend API
    - User Isolation: Enforced via user_id parameter in API

    Args:
        user_id: User's unique identifier (string UUID from Better Auth)
        task_id: Task ID to update
        priority: New priority level ("low", "medium", "high")

    Returns:
        dict: Priority update result from backend API
            - task_id (int): Updated task ID
            - status (str): "updated"
            - priority (str): New priority level
            - title (str): Task title

    Example:
        >>> set_priority(user_id="user-123", task_id=3, priority="high")
        {"task_id": 3, "status": "updated", "priority": "high", "title": "Call dentist"}
    """
    # Validate priority value
    priority = priority.lower()
    if priority not in ["low", "medium", "high"]:
        return {
            "error": "Priority must be one of: 'low', 'medium', 'high'"
        }

    # Prepare the payload for the update
    payload = {
        "priority": priority
    }

    # Make HTTP request to backend API
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(
                f"{BACKEND_BASE_URL}/api/{user_id}/tasks/{task_id}",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    "task_id": result.get("id"),
                    "status": "updated",
                    "priority": result.get("priority"),
                    "title": result.get("title"),
                }
            else:
                # Return error response
                return {
                    "error": f"Failed to update priority: {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {
                "error": "Failed to update priority",
                "details": str(e)
            }


@mcp.tool()
async def list_tasks_by_priority(
    user_id: str,
    priority: str,
    status: Literal["all", "pending", "completed"] = "all",
) -> dict:
    """
    Retrieve tasks filtered by priority level via HTTP API call.

    MCP Tool Contract:
    - Purpose: List tasks filtered by priority and optional completion status
    - Stateless: Backend handles database queries
    - User Isolation: Enforced via user_id parameter in API

    Args:
        user_id: User's unique identifier (string UUID from Better Auth)
        priority: Priority level to filter ("low", "medium", "high")
        status: Additional filter by completion status (default: "all")
            - "all": All tasks at this priority
            - "pending": Incomplete tasks only
            - "completed": Completed tasks only

    Returns:
        dict: Filtered task list result from backend API
            - tasks (list): Array of task objects matching priority
                - id (int): Task ID
                - title (str): Task title
                - priority (str): Priority level
                - completed (bool): Completion status
                - description (str|None): Task description
                - created_at (str): ISO 8601 timestamp
            - count (int): Total number of tasks returned
            - priority (str): Filter priority level
            - status (str): Filter status

    Example:
        >>> list_tasks_by_priority(user_id="user-123", priority="high", status="pending")
        {
            "tasks": [
                {"id": 1, "title": "Call dentist", "priority": "high", "completed": False, ...},
                {"id": 3, "title": "Fix bug", "priority": "high", "completed": False, ...}
            ],
            "count": 2,
            "priority": "high",
            "status": "pending"
        }
    """
    # Validate priority value
    priority = priority.lower()
    if priority not in ["low", "medium", "high"]:
        return {
            "error": "Priority must be one of: 'low', 'medium', 'high'"
        }

    # Build query parameters
    params = {"priority": priority}
    if status != "all":
        params["status"] = status

    # Make HTTP request to backend API
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BACKEND_BASE_URL}/api/{user_id}/tasks",
                params=params
            )

            if response.status_code == 200:
                result = response.json()
                tasks = result.get("tasks", [])

                # Convert tasks to expected format
                task_list = [
                    {
                        "id": task.get("id"),
                        "title": task.get("title"),
                        "priority": task.get("priority"),
                        "completed": task.get("completed", False),
                        "description": task.get("description"),
                        "created_at": task.get("created_at"),
                    }
                    for task in tasks
                ]

                return {
                    "tasks": task_list,
                    "count": len(task_list),
                    "priority": priority,
                    "status": status,
                }
            else:
                # Return error response
                return {
                    "error": f"Failed to list tasks by priority: {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {
                "error": "Failed to list tasks by priority",
                "details": str(e)
            }


async def run_mcp_server():
    """
    Entry point to run the MCP server.
    """
    async with mcp:
        await mcp.run()


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_mcp_server())
