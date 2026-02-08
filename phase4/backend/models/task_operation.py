from sqlmodel import SQLModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from sqlalchemy.types import JSON


class TaskOperationTypeEnum(str, Enum):
    add_task = "add_task"
    list_tasks = "list_tasks"
    complete_task = "complete_task"
    delete_task = "delete_task"
    update_task = "update_task"


class TaskOperationBase(SQLModel):
    conversation_id: UUID = Field(nullable=False, foreign_key="conversation.id")
    operation_type: TaskOperationTypeEnum = Field(nullable=False)
    operation_params: Dict[str, Any] = Field(sa_type=JSON)
    result: Optional[Dict[str, Any]] = Field(default=None, sa_type=JSON)


class TaskOperation(TaskOperationBase, table=True):
    """
    Represents an action performed on tasks (add, list, complete, update, delete) triggered by AI interpretation.
    """
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TaskOperationCreate(TaskOperationBase):
    """Schema for creating a new task operation."""
    conversation_id: UUID
    operation_type: TaskOperationTypeEnum


class TaskOperationRead(TaskOperationBase):
    """Schema for reading task operation data."""
    id: UUID
    timestamp: datetime