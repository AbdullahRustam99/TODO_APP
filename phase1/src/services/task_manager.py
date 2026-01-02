"""
TaskManager service for the TODO Console Application
Handles in-memory storage and CRUD operations for tasks
"""

from src.models.task import Task
from typing import List, Optional


class TaskManager:
    def __init__(self):
        """
        Initialize the TaskManager with an empty task collection
        Uses a dictionary for O(1) lookup by task ID
        """
        self.tasks = {}
        self._next_id = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task to the collection

        Args:
            title (str): Title of the task (required)
            description (str): Description of the task (optional)

        Returns:
            Task: The created Task instance
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty or whitespace-only")

        task_id = self._next_id
        self._next_id += 1

        task = Task(task_id, title.strip(), description.strip())
        self.tasks[task_id] = task
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID

        Args:
            task_id (int): ID of the task to retrieve

        Returns:
            Task or None: The task if found, None otherwise
        """
        return self.tasks.get(task_id)

    def update_task(self, task_id: int, title: str = None, description: str = None) -> Optional[Task]:
        """
        Update an existing task

        Args:
            task_id (int): ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task

        Returns:
            Task or None: Updated task if successful, None if task doesn't exist
        """
        task = self.get_task(task_id)
        if not task:
            return None

        if title is not None:
            if not title or not title.strip():
                raise ValueError("Task title cannot be empty or whitespace-only")
            task.title = title.strip()

        if description is not None:
            task.description = description.strip()

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID

        Args:
            task_id (int): ID of the task to delete

        Returns:
            bool: True if task was deleted, False if task didn't exist
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def toggle_task_completion(self, task_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task

        Args:
            task_id (int): ID of the task to toggle

        Returns:
            Task or None: Updated task if successful, None if task doesn't exist
        """
        task = self.get_task(task_id)
        if task:
            task.completed = not task.completed
            return task
        return None

    def list_tasks(self) -> List[Task]:
        """
        Get all tasks in the collection

        Returns:
            List[Task]: List of all tasks
        """
        return list(self.tasks.values())

    def list_completed_tasks(self) -> List[Task]:
        """
        Get all completed tasks

        Returns:
            List[Task]: List of completed tasks
        """
        return [task for task in self.tasks.values() if task.completed]

    def list_pending_tasks(self) -> List[Task]:
        """
        Get all pending tasks

        Returns:
            List[Task]: List of pending tasks
        """
        return [task for task in self.tasks.values() if not task.completed]

    def get_next_id(self) -> int:
        """
        Get the next available ID for a new task

        Returns:
            int: The next available task ID
        """
        return self._next_id