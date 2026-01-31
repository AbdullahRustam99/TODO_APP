from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel

from database.session import get_session_dep
from models.user import UserCreate, User
from services.user_service import UserService
from auth.jwt_handler import create_access_token, create_refresh_token, verify_token
from utils.logging import get_logger
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

router = APIRouter()
logger = get_logger(__name__)

# Models for auth endpoints
class UserLogin(BaseModel):
    email: str
    password: str  # In a real app, this would be hashed, but for this demo we'll keep it simple

class UserRegister(BaseModel):
    email: str
    password: str  # In a real app, this would be hashed
    name: str

class AuthResponse(BaseModel):
    user: dict
    token: str
    refresh_token: str = None

# Initialize security for token verification (for logout)
security = HTTPBearer()

@router.post("/auth/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister,
    session: AsyncSession = Depends(get_session_dep)
):
    """
    Register a new user and return JWT token.

    Args:
        user_data: User registration data (email, password, name)
        session: Database session

    Returns:
        AuthResponse with user data and JWT token
    """
    try:
        # Create user data object for the service
        user_create_data = UserCreate(
            email=user_data.email,
            name=user_data.name
        )

        # Create user in database
        created_user = await UserService.create_user(session, user_create_data)

        # Create JWT tokens
        token_data = {"sub": str(created_user.id), "email": created_user.email}
        token = create_access_token(data=token_data)
        refresh_token = create_refresh_token(data=token_data)

        logger.info(f"Successfully registered user {created_user.id} with email {created_user.email}")

        return AuthResponse(
            user=created_user.model_dump(),
            token=token,
            refresh_token=refresh_token
        )

    except HTTPException:
        # Re-raise HTTP exceptions (like 400 for duplicate email)
        raise
    except Exception as e:
        logger.error(f"Error registering user with email {user_data.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering user"
        )


@router.post("/auth/login", response_model=AuthResponse)
async def login_user(
    user_data: UserLogin,
    session: AsyncSession = Depends(get_session_dep)
):
    """
    Login a user and return JWT token.

    Args:
        user_data: User login data (email, password)
        session: Database session

    Returns:
        AuthResponse with user data and JWT token
    """
    try:
        # Find user by email
        user = await UserService.get_user_by_email(session, user_data.email)

        if not user:
            logger.warning(f"Login attempt with non-existent email: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # In a real app, we would verify the password here.
        # For this implementation, we'll just proceed with login.

        # Create JWT tokens
        token_data = {"sub": str(user.id), "email": user.email}
        token = create_access_token(data=token_data)
        refresh_token = create_refresh_token(data=token_data)

        logger.info(f"Successfully logged in user {user.id} with email {user.email}")

        # Convert user to dict for response
        user_dict = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "created_at": user.created_at
        }

        return AuthResponse(
            user=user_dict,
            token=token,
            refresh_token=refresh_token
        )

    except HTTPException:
        # Re-raise HTTP exceptions (like 401 for invalid credentials)
        raise
    except Exception as e:
        logger.error(f"Error logging in user with email {user_data.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during login"
        )


@router.post("/auth/logout")
async def logout_user(
    token: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Logout endpoint.
    In a real application, this would add the token to a blacklist/jti store.
    For this implementation, we'll just return a success message.
    """
    try:
        # In a real app, you would add the token to a blacklist or token revocation store
        # For this demo, we'll just return a success message
        logger.info(f"User logged out successfully")
        return {"message": "Successfully logged out"}
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during logout"
        )


class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/auth/refresh", response_model=AuthResponse)
async def refresh_token(
    refresh_request: RefreshTokenRequest
):
    """
    Refresh access token using a valid refresh token.

    Args:
        refresh_request: Contains the refresh token to use for generating a new access token

    Returns:
        AuthResponse with new access token and refresh token
    """
    try:
        # Verify the refresh token
        payload = verify_token(refresh_request.refresh_token)

        # Check if this is a refresh token (not an access token)
        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type for refresh",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Extract user data from the refresh token
        user_id = payload.get("sub")
        user_email = payload.get("email")

        if not user_id or not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create new access and refresh tokens
        token_data = {"sub": user_id, "email": user_email}
        new_access_token = create_access_token(data=token_data)
        new_refresh_token = create_refresh_token(data=token_data)

        logger.info(f"Successfully refreshed token for user {user_id}")

        # Return new tokens with minimal user data (we don't have full user details here)
        user_dict = {
            "id": user_id,
            "email": user_email
        }

        return AuthResponse(
            user=user_dict,
            token=new_access_token,
            refresh_token=new_refresh_token
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error refreshing token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )