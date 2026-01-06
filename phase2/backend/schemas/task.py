from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass

class TaskRead(TaskBase):
    """Schema for reading task data."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskComplete(BaseModel):
    """Schema for updating task completion status."""
    completed: bool