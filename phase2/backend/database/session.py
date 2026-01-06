from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
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
else:  # SQLite
    async_engine = create_async_engine(
        db_url,
        echo=settings.db_echo,  # Set to True for SQL query logging during development
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
    Dependency function for FastAPI to provide async database sessions.
    """
    async with AsyncSession(async_engine) as session:
        yield session