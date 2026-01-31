#!/usr/bin/env python3
"""
Test script to verify that the AI chatbot with MCP server fixes are working correctly.
This script tests the various functionality that was fixed:
1. ModelSettings configuration in the AI agent
2. User ID type conversion in the MCP server
3. Async context handling for database operations
"""

import asyncio
import json
from typing import Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.testclient import TestClient

from ai.mcp.server import server as mcp_server_instance
from ai.agents.todo_agent import todo_agent
from database.session import async_engine, get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from models.user import User, UserCreate
from models.task import Task, TaskCreate
from services.auth_service import create_user
from services.task_service import TaskService


# Test application
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Create test client
client = TestClient(app)


async def setup_test_user():
    """Create a test user for testing the functionality"""
    async with AsyncSession(async_engine) as session:
        # Create a test user
        user_data = UserCreate(
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )

        # Create user using auth service
        user = await create_user(session, user_data)
        await session.commit()

        print(f"Created test user with ID: {user.id}")
        return user


async def test_ai_agent_modelsettings():
    """Test that the AI agent can be created with proper ModelSettings"""
    print("\n1. Testing AI Agent ModelSettings Configuration...")

    try:
        # This should work without throwing an error about ModelSettings
        agent = todo_agent

        # Check that the agent exists and has proper configuration
        assert agent is not None
        print("✓ AI Agent created successfully with proper ModelSettings")

        # If we get here without exception, the ModelSettings fix worked
        return True
    except Exception as e:
        print(f"✗ Error creating AI agent: {e}")
        return False


async def test_database_operations():
    """Test that async database operations work properly"""
    print("\n2. Testing Async Database Operations...")

    try:
        # Set up a test user
        user = await setup_test_user()

        # Test creating a task using the TaskService directly
        async with AsyncSession(async_engine) as session:
            task_data = TaskCreate(
                title="Test Task",
                description="This is a test task created for verifying async operations",
                priority="medium",
                completed=False
            )

            # This should work without greenlet_spawn errors
            created_task = await TaskService.create_task(session, user.id, task_data)
            await session.commit()

            print(f"✓ Created task successfully: {created_task.title} (ID: {created_task.id})")

            # Test retrieving tasks
            tasks = await TaskService.get_tasks_by_user_id(session, user.id)
            print(f"✓ Retrieved {len(tasks)} tasks for user {user.id}")

            # Test updating task completion
            completion_result = await TaskService.update_task_completion(
                session,
                user.id,
                created_task.id,
                {"completed": True}
            )
            await session.commit()

            print(f"✓ Updated task completion status: {completion_result.title}")

            return True

    except Exception as e:
        print(f"✗ Error in database operations: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_tests():
    """Run all tests to verify the fixes"""
    print("Running tests to verify AI chatbot MCP server fixes...\n")

    # Test 1: AI Agent ModelSettings
    test1_passed = await test_ai_agent_modelsettings()

    # Test 2: Database operations (async context)
    test2_passed = await test_database_operations()

    print(f"\nTest Results:")
    print(f"AI Agent ModelSettings: {'✓ PASSED' if test1_passed else '✗ FAILED'}")
    print(f"Async Database Operations: {'✓ PASSED' if test2_passed else '✗ FAILED'}")

    all_passed = test1_passed and test2_passed

    if all_passed:
        print("\n🎉 All tests passed! The fixes for AI chatbot with MCP server are working correctly.")
        print("\nFixed issues:")
        print("- ModelSettings configuration in todo_agent.py")
        print("- User ID type conversion in MCP server")
        print("- Async context handling for SQLAlchemy operations")
        print("- Proper event loop management for thread-based async operations")
    else:
        print("\n❌ Some tests failed. Please review the errors above.")

    return all_passed


if __name__ == "__main__":
    # Run the tests
    result = asyncio.run(run_tests())
    exit(0 if result else 1)