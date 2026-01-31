from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from enum import Enum
from datetime import datetime
from .user import User

class PriorityEnum(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"

class TaskBase(SQLModel):
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=False)  # Made optional to match frontend
    priority: Optional[PriorityEnum] = Field(default=None)  # Changed default to None to match frontend
    due_date: Optional[str] = Field(default=None, max_length=50)  # Changed from datetime to string to match frontend, added max_length for DB

class Task(TaskBase, table=True):
    """
    Represents a user's todo item with properties for content, status, and ownership.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)  # Updated to match new table name
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to User
    user: Optional[User] = Relationship(back_populates="tasks")

class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    # Explicitly define fields to ensure they're properly inherited
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    priority: Optional[PriorityEnum] = None
    due_date: Optional[str] = Field(default=None, max_length=50)

class TaskRead(TaskBase):
    """Schema for reading task data."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    priority: Optional[PriorityEnum] = None  # Explicitly include new field
    due_date: Optional[str] = Field(default=None, max_length=50)  # Changed from datetime to string to match frontend

class TaskUpdate(SQLModel):
    """Schema for updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[str] = Field(default=None, max_length=50)  # Changed from datetime to string to match frontend

class TaskComplete(SQLModel):
    """Schema for updating task completion status."""
    completed: bool