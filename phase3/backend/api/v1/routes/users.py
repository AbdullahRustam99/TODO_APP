from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from ...database.session import get_session_dep
from ...schemas.user import UserRead, UserCreate
from ...services.user_service import UserService
from ...utils.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_session_dep)
):
    """
    Retrieve a specific user by ID.

    Args:
        request: FastAPI request object
        user_id: The ID of the user to retrieve
        session: Database session

    Returns:
        UserRead object

    Raises:
        HTTPException: If user not found
    """
    try:
        user = await UserService.get_user_by_id(session, user_id)

        if not user:
            logger.warning(f"User {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        logger.info(f"Successfully retrieved user {user_id}")
        return user

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user"
        )


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: Request,
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session_dep)
):
    """
    Create a new user.

    Args:
        request: FastAPI request object
        user_data: User creation data
        session: Database session

    Returns:
        Created UserRead object

    Raises:
        HTTPException: If user creation fails
    """
    try:
        created_user = await UserService.create_user(session, user_data)

        logger.info(f"Successfully created user {created_user.id}")
        return created_user

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )