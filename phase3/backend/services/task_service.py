from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models.task import Task, TaskCreate, TaskUpdate, TaskComplete
from models.user import User
from models.task import TaskRead
from utils.logging import get_logger
from fastapi import HTTPException, status
from datetime import datetime
import asyncio

logger = get_logger(__name__)

class TaskService:
    """
    Service class for handling task-related business logic with authorization.
    """

    @staticmethod
    async def get_tasks_by_user_id(session: AsyncSession, user_id: int) -> List[TaskRead]:
        """
        Get all tasks for a specific user.
        """
        try:
            # Query tasks for the specific user
            statement = select(Task).where(Task.user_id == user_id)
            result = await session.exec(statement)
            tasks = result.all()

            # Convert to response schema
            task_list = [TaskRead.model_validate(task) for task in tasks]

            logger.info(f"Retrieved {len(task_list)} tasks for user {user_id}")

            return task_list
        except Exception as e:
            logger.error(f"Error retrieving tasks for user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving tasks"
            )

    @staticmethod
    async def get_task_by_id(session: AsyncSession, user_id: int, task_id: int) -> TaskRead:
        """
        Get a specific task by ID for a specific user.
        """
        try:
            # Query for the specific task that belongs to the user
            statement = select(Task).where(Task.user_id == user_id, Task.id == task_id)
            result = await session.exec(statement)
            task = result.first()

            if not task:
                logger.warning(f"Task {task_id} not found for user {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )

            logger.info(f"Retrieved task {task_id} for user {user_id}")

            return TaskRead.model_validate(task)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving task {task_id} for user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving task"
            )

    @staticmethod
    async def create_task(session: AsyncSession, user_id: int, task_data: TaskCreate) -> TaskRead:
        """
        Create a new task for a specific user.
        """
        try:
            task_data_dict = task_data.model_dump()
            task_data_dict['user_id'] = user_id
            db_task = Task.model_validate(task_data_dict)

            # Add to session
            session.add(db_task)
            await session.flush()
            await session.refresh(db_task)

            logger.info(f"Created task {db_task.id} for user {user_id}")

            return TaskRead.model_validate(db_task)
        except Exception as e:
            await session.rollback()
            logger.error(f"Error creating task for user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating task"
            )

    @staticmethod
    async def update_task(session: AsyncSession, user_id: int, task_id: int, task_data: TaskUpdate) -> TaskRead:
        """
        Update a specific task for a specific user.
        """
        try:
            # Query for the specific task that belongs to the user
            statement = select(Task).where(Task.user_id == user_id, Task.id == task_id)
            result = await session.exec(statement)
            task = result.first()

            if not task:
                logger.warning(f"Task {task_id} not found for user {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )

            # Update task fields if provided
            update_data = task_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(task, field, value)

            # Update the updated_at timestamp
            task.updated_at = datetime.utcnow()

            # Add changes to the session
            session.add(task)
            await session.flush()
            await session.refresh(task)

            logger.info(f"Updated task {task_id} for user {user_id}")

            return TaskRead.model_validate(task)
        except HTTPException:
            raise
        except Exception as e:
            await session.rollback()
            logger.error(f"Error updating task {task_id} for user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating task"
            )

    @staticmethod
    async def delete_task(session: AsyncSession, user_id: int, task_id: int) -> bool:
        """
        Delete a specific task for a specific user.
        """
        try:
            # Query for the specific task that belongs to the user
            statement = select(Task).where(Task.user_id == user_id, Task.id == task_id)
            result = await session.exec(statement)
            task = result.first()

            if not task:
                logger.warning(f"Task {task_id} not found for user {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )

            # Delete the task
            await session.delete(task)
            await session.flush()

            logger.info(f"Deleted task {task_id} for user {user_id}")

            return True
        except HTTPException:
            raise
        except Exception as e:
            await session.rollback()
            logger.error(f"Error deleting task {task_id} for user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting task"
            )

    @staticmethod
    async def update_task_completion(session: AsyncSession, user_id: int, task_id: int, completion_data: TaskComplete) -> TaskRead:
        """
        Update the completion status of a specific task for a specific user.
        """
        try:
            # Query for the specific task that belongs to the user
            statement = select(Task).where(Task.user_id == user_id, Task.id == task_id)
            result = await session.exec(statement)
            task = result.first()

            if not task:
                logger.warning(f"Task {task_id} not found for user {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )

            # Update completion status
            task.completed = completion_data.completed
            task.updated_at = datetime.utcnow()

            # Add changes to the session
            session.add(task)
            await session.flush()
            await session.refresh(task)

            logger.info(f"Updated completion status for task {task_id} for user {user_id}")

            return TaskRead.model_validate(task)
        except HTTPException:
            raise
        except Exception as e:
            await session.rollback()
            logger.error(f"Error updating completion status for task {task_id} for user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating task completion status"
            )