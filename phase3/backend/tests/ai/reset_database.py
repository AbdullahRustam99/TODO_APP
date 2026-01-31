"""
Simple script to recreate database tables
"""

import asyncio
from sqlmodel import SQLModel
from database.session import async_engine
from models.user import User
from models.task import Task

async def reset_database():
    print("Dropping and recreating database tables...")

    # Drop all tables first
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    print("Tables dropped.")

    # Create all tables
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    print("Tables recreated successfully!")
    print("Database reset complete.")

if __name__ == "__main__":
    asyncio.run(reset_database())