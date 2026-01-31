from sqlmodel import SQLModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from sqlalchemy.types import JSON


class MessageRoleEnum(str, Enum):
    user = "user"
    assistant = "assistant"


class MessageBase(SQLModel):
    conversation_id: UUID = Field(nullable=False, foreign_key="conversation.id")
    role: MessageRoleEnum = Field(nullable=False)
    content: str = Field(nullable=False, max_length=10000)
    metadata_: Optional[Dict[str, Any]] = Field(default=None, sa_type=JSON)


class Message(MessageBase, table=True):
    """
    Represents a single message in a conversation, either from user or assistant.
    """
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MessageCreate(MessageBase):
    """Schema for creating a new message."""
    conversation_id: UUID
    role: MessageRoleEnum
    content: str


class MessageRead(MessageBase):
    """Schema for reading message data."""
    id: UUID
    timestamp: datetime