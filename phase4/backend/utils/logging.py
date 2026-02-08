import logging
import sys
from typing import Optional
from config.settings import settings

def setup_logging(
    log_level: Optional[str] = None,
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging configuration for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Custom log format string

    Returns:
        Configured logger instance
    """
    # Determine log level from settings or use provided value
    level = log_level or ("DEBUG" if settings.debug else "INFO")
    level = getattr(logging, level.upper())

    # Default log format
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configure the root logger
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),  # Log to stdout
        ]
    )

    # Create and return a logger for the application
    logger = logging.getLogger("todo_api")
    logger.setLevel(level)

    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Get a named logger instance.

    Args:
        name: Name for the logger

    Returns:
        Logger instance with the specified name
    """
    return logging.getLogger(f"todo_api.{name}")

# Create a default logger for the application
logger = setup_logging()