from typing import Any, Optional
from pydantic import BaseModel, field_validator, ValidationError
import re

def validate_email(email: str) -> str:
    """
    Validate email format using regex.

    Args:
        email: Email string to validate

    Returns:
        Validated email string

    Raises:
        ValueError: If email format is invalid
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError(f"Invalid email format: {email}")
    return email.lower().strip()

def validate_title(title: str) -> str:
    """
    Validate task title - must be 1-255 characters and not just whitespace.

    Args:
        title: Title string to validate

    Returns:
        Validated title string

    Raises:
        ValueError: If title is invalid
    """
    if not title or not title.strip():
        raise ValueError("Title cannot be empty or just whitespace")

    title = title.strip()
    if len(title) > 255:
        raise ValueError(f"Title must be 255 characters or less, got {len(title)}")

    return title

def validate_description(description: Optional[str]) -> Optional[str]:
    """
    Validate task description - if provided, must be 1-1000 characters.

    Args:
        description: Description string to validate (can be None)

    Returns:
        Validated description string or None

    Raises:
        ValueError: If description is invalid
    """
    if description is None:
        return None

    description = description.strip()
    if len(description) > 1000:
        raise ValueError(f"Description must be 1000 characters or less, got {len(description)}")

    return description

def validate_user_id(user_id: int) -> int:
    """
    Validate user ID - must be a positive integer.

    Args:
        user_id: User ID to validate

    Returns:
        Validated user ID

    Raises:
        ValueError: If user ID is invalid
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError(f"User ID must be a positive integer, got {user_id}")
    return user_id

def validate_task_id(task_id: int) -> int:
    """
    Validate task ID - must be a positive integer.

    Args:
        task_id: Task ID to validate

    Returns:
        Validated task ID

    Raises:
        ValueError: If task ID is invalid
    """
    if not isinstance(task_id, int) or task_id <= 0:
        raise ValueError(f"Task ID must be a positive integer, got {task_id}")
    return task_id

class TaskValidator(BaseModel):
    """
    Pydantic model for validating task data.
    """
    title: str
    description: Optional[str] = None

    @field_validator('title')
    @classmethod
    def validate_title_field(cls, v: str) -> str:
        return validate_title(v)

    @field_validator('description')
    @classmethod
    def validate_description_field(cls, v: Optional[str]) -> Optional[str]:
        return validate_description(v)

class UserValidator(BaseModel):
    """
    Pydantic model for validating user data.
    """
    email: str
    name: str

    @field_validator('email')
    @classmethod
    def validate_email_field(cls, v: str) -> str:
        return validate_email(v)

    @field_validator('name')
    @classmethod
    def validate_name_field(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Name cannot be empty or just whitespace")

        name = v.strip()
        if len(name) > 255:
            raise ValueError(f"Name must be 255 characters or less, got {len(name)}")

        return name