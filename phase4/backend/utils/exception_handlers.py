from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from .logging import get_logger
from typing import Union

logger = get_logger(__name__)

async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions globally.

    Args:
        request: FastAPI request object
        exc: HTTP exception

    Returns:
        JSONResponse with error details
    """
    logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail} - Path: {request.url.path}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": "http_exception",
                "status_code": exc.status_code,
                "message": str(exc.detail)
            }
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle request validation exceptions globally.

    Args:
        request: FastAPI request object
        exc: Request validation exception

    Returns:
        JSONResponse with validation error details
    """
    logger.warning(f"Validation Exception: Path: {request.url.path}, Errors: {exc.errors()}")

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "type": "validation_error",
                "status_code": 422,
                "message": "Validation failed",
                "details": exc.errors()
            }
        }
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle general exceptions globally.

    Args:
        request: FastAPI request object
        exc: General exception

    Returns:
        JSONResponse with error details
    """
    logger.error(f"General Exception: {str(exc)} - Path: {request.url.path}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "internal_error",
                "status_code": 500,
                "message": "Internal server error"
            }
        }
    )