from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt_handler import verify_token, get_user_id_from_token
from typing import Optional, Dict, Any
import logging

# Set up logger
logger = logging.getLogger(__name__)

class JWTBearer(HTTPBearer):
    """
    Custom JWT Bearer authentication scheme.
    This class handles extracting and validating JWT tokens from request headers.
    """
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[Dict[str, Any]]:
        """
        Extract and validate JWT token from request.

        Args:
            request: FastAPI request object

        Returns:
            Token payload if valid, None if auto_error is False and no token

        Raises:
            HTTPException: If token is invalid or missing (when auto_error=True)
        """
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme",
                )

            token = credentials.credentials
            return verify_token(token)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization code",
            )

def validate_user_id_from_token(request: Request, token_user_id: int, url_user_id: int) -> bool:
    """
    Validate that the user_id in the JWT token matches the user_id in the URL.

    Args:
        request: FastAPI request object (for logging)
        token_user_id: User ID extracted from JWT token
        url_user_id: User ID from the URL path parameter

    Returns:
        True if user IDs match, raises HTTPException if they don't match
    """
    if token_user_id != url_user_id:
        logger.warning(
            f"User ID mismatch - Token: {token_user_id}, URL: {url_user_id}, Path: {request.url.path}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match user ID in URL",
        )

    return True