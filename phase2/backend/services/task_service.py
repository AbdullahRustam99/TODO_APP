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

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve

        Returns:
            List of TaskRead objects

        Raises:
            HTTPException: If database query fails
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

        Args:
            session: Database session
            user_id: ID of the user
            task_id: ID of the task to retrieve

        Returns:
            TaskRead object

        Raises:
            HTTPException: If task doesn't exist or doesn't belong to user
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

        Args:
            session: Database session
            user_id: ID of the user creating the task
            task_data: Task creation data

        Returns:
            Created TaskRead object

        Raises:
            HTTPException: If task creation fails
        """
        try:
            # Create new task instance
            db_task = Task(
                user_id=user_id,
                title=task_data.title,
                description=task_data.description,
                completed=task_data.completed,
                priority=task_data.priority,
                due_date=task_data.due_date
            )

            # Add to session and commit
            session.add(db_task)
            await session.commit()
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

        Args:
            session: Database session
            user_id: ID of the user
            task_id: ID of the task to update
            task_data: Task update data

        Returns:
            Updated TaskRead object

        Raises:
            HTTPException: If task doesn't exist or doesn't belong to user
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

            # Commit changes
            session.add(task)
            await session.commit()
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

        Args:
            session: Database session
            user_id: ID of the user
            task_id: ID of the task to delete

        Returns:
            True if task was deleted successfully

        Raises:
            HTTPException: If task doesn't exist or doesn't belong to user
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
            await session.commit()

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

        Args:
            session: Database session
            user_id: ID of the user
            task_id: ID of the task to update
            completion_data: Task completion data

        Returns:
            Updated TaskRead object

        Raises:
            HTTPException: If task doesn't exist or doesn't belong to user
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

            # Commit changes
            session.add(task)
            await session.commit()
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