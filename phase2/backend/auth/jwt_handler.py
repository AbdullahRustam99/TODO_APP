import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from config.settings import settings
from models.user import UserRead

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new access token with the provided data.

    Args:
        data: Dictionary containing the data to encode in the token
        expires_delta: Optional timedelta for token expiration (defaults to settings value)

    Returns:
        Encoded JWT token as string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": "access"})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )

    return encoded_jwt


def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new refresh token with the provided data.

    Args:
        data: Dictionary containing the data to encode in the token
        expires_delta: Optional timedelta for token expiration (defaults to settings value)

    Returns:
        Encoded JWT token as string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default refresh token expiration to 7 days
        expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)

    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": "refresh"})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )

    return encoded_jwt

def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string to verify

    Returns:
        Decoded token payload as dictionary

    Raises:
        HTTPException: If token is invalid, expired, or cannot be decoded
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )

        # Check if token is expired
        if "exp" in payload:
            exp_timestamp = payload["exp"]
            if datetime.fromtimestamp(exp_timestamp) < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_user_id_from_token(token: str) -> int:
    """
    Extract user ID from JWT token.

    Args:
        token: JWT token string

    Returns:
        User ID as integer

    Raises:
        HTTPException: If token is invalid or user_id is not in token
    """
    payload = verify_token(token)

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Ensure user_id is an integer
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id