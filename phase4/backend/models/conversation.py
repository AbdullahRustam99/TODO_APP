from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class ConversationBase(SQLModel):
    user_id: str = Field(nullable=False, max_length=255)
    expires_at: datetime = Field(nullable=False)


class Conversation(ConversationBase, table=True):
    """
    Represents a conversation session between user and AI assistant, including message history.
    """
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation."""
    user_id: str
    expires_at: datetime


class ConversationRead(ConversationBase):
    """Schema for reading conversation data."""
    id: UUID
    created_at: datetime
    updated_at: datetime