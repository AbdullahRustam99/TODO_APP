from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models.user import User, UserCreate
from schemas.user import UserRead
from utils.logging import get_logger
from fastapi import HTTPException, status
import asyncio

logger = get_logger(__name__)

class UserService:
    """
    Service class for handling user-related business logic.
    """

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[UserRead]:
        """
        Get a user by ID.

        Args:
            session: Database session
            user_id: ID of the user to retrieve

        Returns:
            UserRead object if found, None otherwise
        """
        try:
            statement = select(User).where(User.id == user_id)
            result = await session.exec(statement)
            user = result.first()

            if user:
                logger.info(f"Retrieved user {user_id}")
                return UserRead.model_validate(user)
            else:
                logger.warning(f"User {user_id} not found")
                return None
        except Exception as e:
            logger.error(f"Error retrieving user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving user"
            )

    @staticmethod
    async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
        """
        Get a user by email.

        Args:
            session: Database session
            email: Email of the user to retrieve

        Returns:
            User object if found, None otherwise
        """
        try:
            statement = select(User).where(User.email == email)
            result = await session.exec(statement)
            user = result.first()

            if user:
                logger.info(f"Retrieved user with email {email}")
                return user
            else:
                logger.info(f"User with email {email} not found")
                return None
        except Exception as e:
            logger.error(f"Error retrieving user with email {email}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving user"
            )

    @staticmethod
    async def create_user(session: AsyncSession, user_data: UserCreate) -> UserRead:
        """
        Create a new user.

        Args:
            session: Database session
            user_data: User creation data

        Returns:
            Created UserRead object

        Raises:
            HTTPException: If user creation fails
        """
        try:
            # Check if user already exists
            existing_user = await UserService.get_user_by_email(session, user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists"
                )

            user_data_dict = user_data.model_dump()
            db_user = User.model_validate(user_data_dict)

            # Add to session and commit
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)

            logger.info(f"Created user {db_user.id} with email {db_user.email}")

            return UserRead.model_validate(db_user)
        except HTTPException:
            raise
        except Exception as e:
            await session.rollback()
            logger.error(f"Error creating user with email {user_data.email}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating user"
            )