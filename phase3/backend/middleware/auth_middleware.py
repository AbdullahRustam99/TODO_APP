from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse
from config.settings import settings
from auth.jwt_handler import verify_token
import logging
from typing import Callable, Awaitable

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Authentication middleware that handles both internal service-to-service
    and external user authentication.
    """

    def __init__(self, app):
        super().__init__(app)
        self.jwt_bearer = JWTBearer(auto_error=False)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Dispatch the request, performing authentication.

        - If the Authorization header contains the internal service secret,
          the request is marked as internal and allowed to proceed.
        - Otherwise, it attempts to validate a user JWT.
        """
        request.state.is_internal = False
        request.state.user = None

        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                scheme, token = auth_header.split()
                if scheme.lower() == "bearer":
                    # Check for internal service secret
                    if token == settings.jwt_secret:
                        request.state.is_internal = True
                        logger.debug("Internal service request authenticated.")
                        return await call_next(request)

                    # If not the internal secret, try to validate as a user JWT
                    token_payload = verify_token(token)
                    if token_payload:
                        request.state.user = token_payload
                        logger.debug(f"User request authenticated: {token_payload}")
                    else:
                        # If token is invalid (but not the service secret)
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid or expired token",
                        )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid authentication scheme",
                    )
            except HTTPException as e:
                return JSONResponse(
                    status_code=e.status_code, content={"detail": e.detail}
                )
            except Exception as e:
                logger.error(f"Authentication error: {e}", exc_info=True)
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Could not validate credentials"},
                )

        # Let unprotected routes pass through
        return await call_next(request)


class JWTBearer(HTTPBearer):
    """
    Custom JWT Bearer authentication scheme for user-facing routes.
    """
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        Validate token from request.state if already processed by middleware.
        """
        if request.state.user:
            return request.state.user

        if self.auto_error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        return None

def get_current_user_id(request: Request) -> int:
    """
    Dependency to get the current user ID from the request state.
    """
    if request.state.is_internal:
        # For internal requests, trust the user_id from the URL path
        try:
            return int(request.path_params["user_id"])
        except (KeyError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id not found in URL for internal request"
            )

    if request.state.user and "sub" in request.state.user:
        return int(request.state.user["sub"])
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated"
    )

def validate_user_id_from_token(request: Request, url_user_id: int) -> bool:
    """
    Validates that the user_id from the token matches the one in the URL,
    or bypasses the check for internal requests.
    """
    if request.state.is_internal:
        return True

    token_user_id = get_current_user_id(request)
    if token_user_id != url_user_id:
        logger.warning(
            f"User ID mismatch - Token: {token_user_id}, URL: {url_user_id}, Path: {request.url.path}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match user ID in URL",
        )
    
    return True