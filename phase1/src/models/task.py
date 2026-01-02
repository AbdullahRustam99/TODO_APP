"""
Task model for the TODO Console Application
Represents a single todo item with id, title, description, and completion status
"""

class Task:
    def __init__(self, task_id, title, description="", completed=False):
        """
        Initialize a Task instance

        Args:
            task_id (int): Unique identifier for the task
            title (str): Title of the task (required)
            description (str): Detailed description of the task (optional)
            completed (bool): Completion status of the task (default: False)
        """
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed

    def __str__(self):
        """String representation of the task"""
        status_symbol = "✓" if self.completed else "✗"
        status_text = "Completed" if self.completed else "Pending"
        return f"{self.id}. {self.title} - [{status_text}]"

    def to_dict(self):
        """Convert task to dictionary representation"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task instance from dictionary data"""
        return cls(
            task_id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False)
        )