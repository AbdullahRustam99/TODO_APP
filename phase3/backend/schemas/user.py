from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    """Schema for creating a new user."""
    pass

class UserRead(UserBase):
    """Schema for reading user data."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    """Schema for updating user data."""
    email: Optional[str] = None
    name: Optional[str] = None