"""

HTTP-only MCP Server for the separated AI service.
Communicates with the business logic service via HTTP API calls.
"""
import re
from typing import Literal, Optional, Any, Dict
import httpx
from mcp.server.fastmcp import FastMCP
from config.config import settings
import logging
import os
import sys

# Set up logging
logger = logging.getLogger(__name__)

logger.info("--- MCP SERVER SCRIPT STARTING ---")
# Load secure service secret from environment variable
SERVICE_SECRET = settings.BETTER_AUTH_SECRET
logger.info(f"SERVICE_SECRET loaded: '{bool(SERVICE_SECRET)}'") # Log boolean status, not the secret itself.

if not SERVICE_SECRET:
    logger.error("SERVICE_SECRET is NOT SET. Authentication will fail.")

# Create MCP server instance
mcp = FastMCP("separated-task-management-server")
logger.info("FastMCP instance created.")

# Get business service base URL from environment
BUSINESS_SERVICE_URL = settings.BUSINESS_SERVICE_URL

def _get_auth_headers() -> Dict[str, str]:
    if not SERVICE_SECRET:
        logger.error("Attempted to get auth headers but SERVICE_SECRET is not set.")
        return {}
    return {"Authorization": f"Bearer {SERVICE_SECRET}"}

def detect_priority_from_text(text: str) -> str:
    text_lower = text.lower()
    high_priority_patterns = [r'\bhigh\s*priority\b', r'\burgent\b', r'\bcritical\b', r'\bimportant\b', r'\basap\b', r'\bhigh\b']
    low_priority_patterns = [r'\blow\s*priority\b', r'\bminor\b', r'\boptional\b', r'\bwhen\s*you\s*have\s*time\b', r'low']
    if any(re.search(p, text_lower) for p in high_priority_patterns):
        return "high"
    if any(re.search(p, text_lower) for p in low_priority_patterns):
        return "low"
    if re.search(r'\bmedium\b|\bnormal\b', text_lower):
        return "medium"
    return "medium"

@mcp.tool()
async def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    due_date: Optional[str] = None,
) -> dict:
    """
    Create a new task. This tool is idempotent.
    """
    if not SERVICE_SECRET:
        return {"success": False, "done": True, "error": "Internal authentication error: Service secret missing."}

    try:
        existing_tasks_response = await list_tasks(user_id=user_id)
        if existing_tasks_response.get("success"):
            for task in existing_tasks_response.get("tasks", []):
                if task.get("title", "").lower() == title.lower():
                    return {"success": False, "done": True, "message": "Task already exists."}
    except Exception as e:
        logger.error(f"Failed to check for existing tasks during add_task: {e}")
        return {"success": False, "done": True, "error": "Failed to verify if task exists.", "details": str(e)}

    if priority is None:
        combined_text = f"{title} {description or ''}"
        priority = detect_priority_from_text(combined_text)
    else:
        priority = priority.lower()
        if priority not in ["low", "medium", "high"]:
            priority = "medium"

    payload = {"title": title, "description": description, "priority": priority, "completed": False, "due_date": due_date}
    headers = {"Content-Type": "application/json", **_get_auth_headers()}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{BUSINESS_SERVICE_URL}/api/{user_id}/tasks", json=payload, headers=headers)
            if response.status_code in [200, 201]:
                return {"success": True, "done": True, "message": "Task added successfully."}
            else:
                return {"success": False, "done": True, "error": f"Failed to create task: {response.status_code}", "details": response.text}
        except Exception as e:
            return {"success": False, "done": True, "error": "Failed to create task.", "details": str(e)}

@mcp.tool()
async def list_tasks(user_id: str, status: Literal["all", "pending", "completed"] = "all") -> dict:
    """
    Retrieve tasks.
    """
    if not SERVICE_SECRET:
        return {"success": False, "done": True, "error": "Internal authentication error: Service secret missing."}
    params = {"status": status} if status != "all" else {}
    headers = _get_auth_headers()
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BUSINESS_SERVICE_URL}/api/{user_id}/tasks", params=params, headers=headers)
            if response.status_code == 200:
                result = response.json()
                tasks = result if isinstance(result, list) else result.get("tasks", [])
                task_list = [{"id": t.get("id"), "title": t.get("title"), "description": t.get("description"), "completed": t.get("completed", False), "priority": t.get("priority"), "created_at": t.get("created_at")} for t in tasks]
                return {"success": True, "done": True, "tasks": task_list, "count": len(task_list)}
            else:
                return {"success": False, "done": True, "error": f"Failed to list tasks: {response.status_code}", "details": response.text}
        except Exception as e:
            return {"success": False, "done": True, "error": "Failed to list tasks.", "details": str(e)}

@mcp.tool()
async def complete_task(user_id: str, task_id: int) -> dict:
    """
    Mark a task as complete.
    """
    if not SERVICE_SECRET:
        return {"success": False, "done": True, "error": "Internal authentication error: Service secret missing."}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.patch(f"{BUSINESS_SERVICE_URL}/api/{user_id}/tasks/{task_id}/complete", json=payload, headers=headers)
            if response.status_code in [200, 204]:
                return {"success": True, "done": True, "message": f"Task {task_id} marked as complete."}
            else:
                return {"success": False, "done": True, "error": f"Failed to complete task: {response.status_code}", "details": response.text}
        except Exception as e:
            return {"success": False, "done": True, "error": "Failed to complete task.", "details": str(e)}

@mcp.tool()
async def delete_task(user_id: str, task_id: int) -> dict:
    """
    Remove a task.
    """
    if not SERVICE_SECRET:
        return {"success": False, "done": True, "error": "Internal authentication error: Service secret missing."}
    headers = _get_auth_headers()
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f"{BUSINESS_SERVICE_URL}/api/{user_id}/tasks/{task_id}", headers=headers)
            if response.status_code in [200, 204]:
                return {"success": True, "done": True, "message": "Task deleted successfully."}
            else:
                return {"success": False, "done": True, "error": f"Failed to delete task: {response.status_code}", "details": response.text}
        except Exception as e:
            return {"success": False, "done": True, "error": "Failed to delete task.", "details": str(e)}

@mcp.tool()
async def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[str] = None) -> dict:
    """
    Modify task details.
    """
    if not SERVICE_SECRET:
        return {"success": False, "done": True, "error": "Internal authentication error: Service secret missing."}
    if title is None and description is None and priority is None:
        return {"success": False, "done": True, "error": "At least one of 'title', 'description', or 'priority' must be provided."}
    payload = {k: v for k, v in {"title": title, "description": description, "priority": priority}.items() if v is not None}
    headers = {"Content-Type": "application/json", **_get_auth_headers()}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f"{BUSINESS_SERVICE_URL}/api/{user_id}/tasks/{task_id}", json=payload, headers=headers)
            if response.status_code in [200, 204]:
                return {"success": True, "done": True, "message": f"Task {task_id} updated successfully."}
            else:
                return {"success": False, "done": True, "error": f"Failed to update task: {response.status_code}", "details": response.text}
        except Exception as e:
            return {"success": False, "done": True, "error": "Failed to update task.", "details": str(e)}

@mcp.tool()
async def set_priority(user_id: str, task_id: int, priority: str) -> dict:
    """
    Set or update a task's priority.
    """
    if not SERVICE_SECRET:
        return {"success": False, "done": True, "error": "Internal authentication error: Service secret missing."}
    priority = priority.lower()
    if priority not in ["low", "medium", "high"]:
        return {"success": False, "done": True, "error": "Priority must be one of: 'low', 'medium', 'high'."}
    payload = {"priority": priority}
    headers = {"Content-Type": "application/json", **_get_auth_headers()}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f"{BUSINESS_SERVICE_URL}/api/{user_id}/tasks/{task_id}", json=payload, headers=headers)
            if response.status_code in [200, 204]:
                return {"success": True, "done": True, "message": f"Priority for task {task_id} updated successfully."}
            else:
                return {"success": False, "done": True, "error": f"Failed to update priority: {response.status_code}", "details": response.text}
        except Exception as e:
            return {"success": False, "done": True, "error": "Failed to update priority.", "details": str(e)}

@mcp.tool()
async def list_tasks_by_priority(user_id: str, priority: str, status: Literal["all", "pending", "completed"] = "all") -> dict:
    """
    Retrieve tasks filtered by priority.
    """
    if not SERVICE_SECRET:
        return {"success": False, "done": True, "error": "Internal authentication error: Service secret missing."}
    priority = priority.lower()
    if priority not in ["low", "medium", "high"]:
        return {"success": False, "done": True, "error": "Priority must be one of: 'low', 'medium', 'high'."}
    params = {"priority": priority}
    if status != "all":
        params["status"] = status
    headers = _get_auth_headers()
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BUSINESS_SERVICE_URL}/api/{user_id}/tasks", params=params, headers=headers)
            if response.status_code == 200:
                result = response.json()
                tasks = result.get("tasks", [])
                task_list = [{"id": t.get("id"), "title": t.get("title"), "priority": t.get("priority"), "completed": t.get("completed", False), "description": t.get("description"), "created_at": t.get("created_at")} for t in tasks]
                return {"success": True, "done": True, "tasks": task_list, "count": len(task_list), "priority": priority, "status": status}
            else:
                return {"success": False, "done": True, "error": f"Failed to list tasks by priority: {response.status_code}", "details": response.text}
        except Exception as e:
            return {"success": False, "done": True, "error": "Failed to list tasks by priority.", "details": str(e)}

if __name__ == "__main__":
    try:
        logger.info("MCP script running in __main__")
        mcp.run()
    except Exception as e:
        logger.error("An unhandled exception occurred in ai_mcp_server.py", exc_info=True)
        raise