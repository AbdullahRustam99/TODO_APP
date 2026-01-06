from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)
    name: str = Field(nullable=False, max_length=255)

class User(UserBase, table=True):
    """
    Represents a registered user in the system with authentication information.
    """
    __tablename__ = "users"  # Use 'users' instead of 'user' to avoid PostgreSQL reserved keyword

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    """Schema for creating a new user."""
    pass

class UserRead(UserBase):
    """Schema for reading user data."""
    id: int
    created_at: datetime