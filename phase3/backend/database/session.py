from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Session, SQLModel, create_engine
from typing import AsyncGenerator
from contextlib import asynccontextmanager
import os
from config.settings import settings

# Create the async database engine
db_url = settings.database_url

if db_url.startswith("postgresql://"):
    # Convert to asyncpg format
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgresql+asyncpg://"):
    # Already in correct format
    db_url = db_url
elif db_url.startswith("sqlite://") and not db_url.startswith("sqlite+aiosqlite"):
    # Convert to aiosqlite format
    db_url = db_url.replace("sqlite://", "sqlite+aiosqlite://", 1)
elif db_url.startswith("sqlite+aiosqlite"):
    # Already in correct format
    db_url = db_url

# For Neon PostgreSQL with asyncpg, SSL is handled automatically
# The issue is with URL parameters that asyncpg doesn't expect
if "postgresql+asyncpg" in db_url and "?sslmode=" in db_url:
    # Extract the base URL without query parameters
    base_url = db_url.split('?')[0]
    # For Neon, we often just need the base URL as asyncpg handles SSL automatically
    db_url = base_url

# Create sync database URL (convert async URLs to sync format)
sync_db_url = db_url
if "postgresql+asyncpg://" in sync_db_url:
    sync_db_url = sync_db_url.replace("postgresql+asyncpg://", "postgresql://")
elif "sqlite+aiosqlite://" in sync_db_url:
    sync_db_url = sync_db_url.replace("sqlite+aiosqlite://", "sqlite://")

# Set appropriate engine options based on database type
if "postgresql" in db_url:
    # For PostgreSQL, use asyncpg with proper SSL handling
    async_engine = create_async_engine(
        db_url,
        echo=settings.db_echo,  # Set to True for SQL query logging during development
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,  # Recycle connections every 5 minutes
        # SSL is handled automatically by asyncpg for Neon
    )
    # Create sync engine for synchronous operations
    sync_engine = create_engine(
        sync_db_url,
        echo=settings.db_echo,
        pool_pre_ping=True,
        pool_recycle=300,
    )
else:  # SQLite
    async_engine = create_async_engine(
        db_url,
        echo=settings.db_echo,  # Set to True for SQL query logging during development
    )
    # Create sync engine for synchronous operations
    sync_engine = create_engine(
        sync_db_url,
        echo=settings.db_echo,
    )

@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager for database sessions.
    Ensures the session is properly closed after use.
    """
    async with AsyncSession(async_engine) as session:
        try:
            yield session
        finally:
            await session.close()

async def get_session_dep():
    """
    Dependency function for FastAPI to provide async database sessions with proper
    transaction management.
    """
    async with AsyncSession(async_engine) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

def get_session() -> Session:
    """
    Dependency function to get a synchronous database session.

    Yields:
        Session: SQLModel database session

    Example:
        ```python
        @app.get("/items")
        def get_items(session: Session = Depends(get_session)):
            items = session.exec(select(Item)).all()
            return items
        ```
    """
    with Session(sync_engine) as session:
        yield session


def get_sync_session() -> Session:
    """
    Generator function to get a synchronous database session for use in synchronous contexts like MCP servers.

    Yields:
        Session: SQLModel synchronous database session
    """
    session = Session(sync_engine)
    try:
        yield session
    finally:
        session.close()


def create_sync_session() -> Session:
    """
    Create and return a synchronous database session for direct use.

    Returns:
        Session: SQLModel synchronous database session
    """
    return Session(sync_engine)

