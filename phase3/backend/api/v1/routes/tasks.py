from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from database.session import get_session_dep
from models.task import TaskRead, TaskCreate, TaskUpdate, TaskComplete
from services.task_service import TaskService
from middleware.auth_middleware import get_current_user_id, validate_user_id_from_token
from utils.logging import get_logger
from services.sse_service import notify_clients # Import notify_clients

router = APIRouter()
logger = get_logger(__name__)

@router.get("/tasks", response_model=List[TaskRead])
async def get_tasks(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_session_dep),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Retrieve all tasks for the specified user.
    """
    validate_user_id_from_token(request, url_user_id=user_id)
    
    try:
        tasks = await TaskService.get_tasks_by_user_id(session, user_id)
        logger.info(f"Successfully retrieved {len(tasks)} tasks for user {user_id}")
        return tasks
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
    session: AsyncSession = Depends(get_session_dep),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Create a new task for the specified user.
    """
    validate_user_id_from_token(request, url_user_id=user_id)
    
    try:
        created_task = await TaskService.create_task(session, user_id, task_data)
        logger.info(f"Successfully created task {created_task.id} for user {user_id}")
        await notify_clients(user_id, "tasks_updated") # Notify clients
        return created_task
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
    session: AsyncSession = Depends(get_session_dep),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Retrieve a specific task by ID for the specified user.
    """
    validate_user_id_from_token(request, url_user_id=user_id)

    try:
        task = await TaskService.get_task_by_id(session, user_id, task_id)
        logger.info(f"Successfully retrieved task {task_id} for user {user_id}")
        return task
    except HTTPException:
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
    session: AsyncSession = Depends(get_session_dep),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Update a specific task for the specified user.
    """
    validate_user_id_from_token(request, url_user_id=user_id)

    try:
        updated_task = await TaskService.update_task(session, user_id, task_id, task_data)
        logger.info(f"Successfully updated task {task_id} for user {user_id}")
        await notify_clients(user_id, "tasks_updated") # Notify clients
        return updated_task
    except HTTPException:
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
    session: AsyncSession = Depends(get_session_dep),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Delete a specific task for the specified user.
    """
    validate_user_id_from_token(request, url_user_id=user_id)

    try:
        await TaskService.delete_task(session, user_id, task_id)
        logger.info(f"Successfully deleted task {task_id} for user {user_id}")
        await notify_clients(user_id, "tasks_updated") # Notify clients
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
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
    session: AsyncSession = Depends(get_session_dep),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Update the completion status of a specific task for the specified user.
    """
    validate_user_id_from_token(request, url_user_id=user_id)

    try:
        updated_task = await TaskService.update_task_completion(session, user_id, task_id, completion_data)
        logger.info(f"Successfully updated completion status for task {task_id} for user {user_id}")
        await notify_clients(user_id, "tasks_updated") # Notify clients
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating completion status for task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating task completion status"
        )