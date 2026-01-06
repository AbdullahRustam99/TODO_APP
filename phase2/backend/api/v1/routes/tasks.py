from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from database.session import get_session_dep
from models.task import TaskRead, TaskCreate, TaskUpdate, TaskComplete
from services.task_service import TaskService
from middleware.auth_middleware import validate_user_id_from_token
from auth.jwt_handler import get_user_id_from_token
from utils.logging import get_logger
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import logging

router = APIRouter()
logger = get_logger(__name__)

# Initialize security for token extraction
security = HTTPBearer()


@router.get("/tasks", response_model=List[TaskRead])
async def get_tasks(
    request: Request,
    user_id: int,
    token: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session_dep)
):
    """
    Retrieve all tasks for the specified user.

    Args:
        request: FastAPI request object
        user_id: The ID of the user whose tasks to retrieve
        token: JWT token for authentication
        session: Database session

    Returns:
        List of TaskRead objects

    Raises:
        HTTPException: If authentication fails or user_id validation fails
    """
    try:
        # Extract and validate token
        token_user_id = get_user_id_from_token(token.credentials)

        # Validate that token user_id matches URL user_id
        validate_user_id_from_token(
            request=request,
            token_user_id=token_user_id,
            url_user_id=user_id
        )

        # Get tasks for the user
        tasks = await TaskService.get_tasks_by_user_id(session, user_id)

        logger.info(f"Successfully retrieved {len(tasks)} tasks for user {user_id}")
        return tasks

    except HTTPException:
        # Re-raise HTTP exceptions (like 401, 403, 404)
        raise
    except Exception as e:
        logger.error(f"Error retrieving tasks for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving tasks"
        )


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: Request,
    user_id: int,
    task_data: TaskCreate,
    token: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session_dep)
):
    """
    Create a new task for the specified user.

    Args:
        request: FastAPI request object
        user_id: The ID of the user creating the task
        task_data: Task creation data
        token: JWT token for authentication
        session: Database session

    Returns:
        Created TaskRead object

    Raises:
        HTTPException: If authentication fails, user_id validation fails, or task creation fails
    """
    try:
        # Extract and validate token
        token_user_id = get_user_id_from_token(token.credentials)

        # Validate that token user_id matches URL user_id
        validate_user_id_from_token(
            request=request,
            token_user_id=token_user_id,
            url_user_id=user_id
        )

        # Create the task
        created_task = await TaskService.create_task(session, user_id, task_data)

        logger.info(f"Successfully created task {created_task.id} for user {user_id}")
        return created_task

    except HTTPException:
        # Re-raise HTTP exceptions (like 401, 403, 400)
        raise
    except Exception as e:
        logger.error(f"Error creating task for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating task"
        )


@router.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task(
    request: Request,
    user_id: int,
    task_id: int,
    token: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session_dep)
):
    """
    Retrieve a specific task by ID for the specified user.

    Args:
        request: FastAPI request object
        user_id: The ID of the user
        task_id: The ID of the task to retrieve
        token: JWT token for authentication
        session: Database session

    Returns:
        TaskRead object

    Raises:
        HTTPException: If authentication fails, user_id validation fails, or task not found
    """
    try:
        # Extract and validate token
        token_user_id = get_user_id_from_token(token.credentials)

        # Validate that token user_id matches URL user_id
        validate_user_id_from_token(
            request=request,
            token_user_id=token_user_id,
            url_user_id=user_id
        )

        # Get the specific task
        task = await TaskService.get_task_by_id(session, user_id, task_id)

        logger.info(f"Successfully retrieved task {task_id} for user {user_id}")
        return task

    except HTTPException:
        # Re-raise HTTP exceptions (like 401, 403, 404)
        raise
    except Exception as e:
        logger.error(f"Error retrieving task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving task"
        )


@router.put("/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    request: Request,
    user_id: int,
    task_id: int,
    task_data: TaskUpdate,
    token: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session_dep)
):
    """
    Update a specific task for the specified user.

    Args:
        request: FastAPI request object
        user_id: The ID of the user
        task_id: The ID of the task to update
        task_data: Task update data
        token: JWT token for authentication
        session: Database session

    Returns:
        Updated TaskRead object

    Raises:
        HTTPException: If authentication fails, user_id validation fails, or task not found
    """
    try:
        # Extract and validate token
        token_user_id = get_user_id_from_token(token.credentials)

        # Validate that token user_id matches URL user_id
        validate_user_id_from_token(
            request=request,
            token_user_id=token_user_id,
            url_user_id=user_id
        )

        # Update the task
        updated_task = await TaskService.update_task(session, user_id, task_id, task_data)

        logger.info(f"Successfully updated task {task_id} for user {user_id}")
        return updated_task

    except HTTPException:
        # Re-raise HTTP exceptions (like 401, 403, 404)
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating task"
        )


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    request: Request,
    user_id: int,
    task_id: int,
    token: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session_dep)
):
    """
    Delete a specific task for the specified user.

    Args:
        request: FastAPI request object
        user_id: The ID of the user
        task_id: The ID of the task to delete
        token: JWT token for authentication
        session: Database session

    Raises:
        HTTPException: If authentication fails, user_id validation fails, or task not found
    """
    try:
        # Extract and validate token
        token_user_id = get_user_id_from_token(token.credentials)

        # Validate that token user_id matches URL user_id
        validate_user_id_from_token(
            request=request,
            token_user_id=token_user_id,
            url_user_id=user_id
        )

        # Delete the task
        await TaskService.delete_task(session, user_id, task_id)

        logger.info(f"Successfully deleted task {task_id} for user {user_id}")
        return

    except HTTPException:
        # Re-raise HTTP exceptions (like 401, 403, 404)
        raise
    except Exception as e:
        logger.error(f"Error deleting task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting task"
        )


@router.patch("/tasks/{task_id}/complete", response_model=TaskRead)
async def update_task_completion(
    request: Request,
    user_id: int,
    task_id: int,
    completion_data: TaskComplete,
    token: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session_dep)
):
    """
    Update the completion status of a specific task for the specified user.

    Args:
        request: FastAPI request object
        user_id: The ID of the user
        task_id: The ID of the task to update
        completion_data: Task completion data
        token: JWT token for authentication
        session: Database session

    Returns:
        Updated TaskRead object

    Raises:
        HTTPException: If authentication fails, user_id validation fails, or task not found
    """
    try:
        # Extract and validate token
        token_user_id = get_user_id_from_token(token.credentials)

        # Validate that token user_id matches URL user_id
        validate_user_id_from_token(
            request=request,
            token_user_id=token_user_id,
            url_user_id=user_id
        )

        # Update task completion status
        updated_task = await TaskService.update_task_completion(session, user_id, task_id, completion_data)

        logger.info(f"Successfully updated completion status for task {task_id} for user {user_id}")
        return updated_task

    except HTTPException:
        # Re-raise HTTP exceptions (like 401, 403, 404)
        raise
    except Exception as e:
        logger.error(f"Error updating completion status for task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating task completion status"
        )