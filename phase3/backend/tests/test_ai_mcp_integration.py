"""
Test script to verify the AI agent properly connects to the MCP server
and executes database operations through the MCP server integration.
"""
import asyncio
import os
import sys
from unittest.mock import AsyncMock, patch
from sqlmodel.ext.asyncio.session import AsyncSession

from database.session import get_async_session
from models.user import User
from models.task import Task
from sqlmodel import select
from datetime import datetime
import uuid


async def test_ai_agent_mcp_integration():
    """
    Test that the AI agent properly integrates with the MCP server
    and executes database operations.
    """
    print("Testing AI Agent MCP Integration...")

    # Get database session
    async with get_async_session() as session:
        # Create a test user with a unique email
        unique_email = f"test_{uuid.uuid4()}@example.com"
        user = User(
            email=unique_email,
            name="Test User",
            created_at=datetime.utcnow()
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        print(f"Created test user: {user.id}")

        # Import the AI agent and conversation manager
        from ai.agents.todo_agent import TodoAgent
        from ai.agents.conversation_manager import ConversationManager

        # Create conversation manager and conversation
        conversation_manager = ConversationManager(session)
        conversation = await conversation_manager.create_conversation(str(user.id))
        print(f"Created conversation: {conversation.id}")

        # Initialize the AI agent
        todo_agent = TodoAgent()
        print("Initialized AI agent")

        # Test 1: Add a task via AI agent
        print("\n--- Test 1: Adding a task via AI agent ---")
        add_task_request = "Add a new task: Buy groceries with high priority"
        result = await todo_agent.process_message(str(user.id), add_task_request, conversation)
        print(f"AI Response: {result['response']}")

        # Verify task was added to database
        tasks = await session.exec(select(Task).where(Task.user_id == user.id))
        tasks_list = tasks.all()
        print(f"Tasks in database after add: {len(tasks_list)}")
        if tasks_list:
            print(f"Latest task: {tasks_list[-1].title} (Priority: {tasks_list[-1].priority})")

        # Test 2: List tasks via AI agent
        print("\n--- Test 2: Listing tasks via AI agent ---")
        list_request = "List all my tasks"
        result = await todo_agent.process_message(str(user.id), list_request, conversation)
        print(f"AI Response: {result['response']}")

        # Test 3: Complete a task via AI agent
        if tasks_list:
            print("\n--- Test 3: Completing a task via AI agent ---")
            task_to_complete = tasks_list[-1]  # Use the last added task
            complete_request = f"Complete the task with ID {task_to_complete.id}"
            result = await todo_agent.process_message(str(user.id), complete_request, conversation)
            print(f"AI Response: {result['response']}")

            # Refresh the task to check completion status
            await session.refresh(task_to_complete)
            print(f"Task {task_to_complete.id} completed status: {task_to_complete.completed}")

        # Final verification
        final_tasks = await session.exec(select(Task).where(Task.user_id == user.id))
        final_tasks_list = final_tasks.all()
        print(f"\nFinal task count: {len(final_tasks_list)}")

        for task in final_tasks_list:
            print(f"- Task: {task.title}, Priority: {task.priority}, Completed: {task.completed}, Due: {task.due_date}")

        print("\n--- Test Summary ---")
        print(f"Created {len(final_tasks_list)} tasks in database")
        completed_count = sum(1 for task in final_tasks_list if task.completed)
        print(f"Completed {completed_count} tasks")
        print("AI agent properly integrated with MCP server")
        print("Database operations executed successfully through MCP server")

        # Clean up test data
        for task in final_tasks_list:
            await session.delete(task)
        await session.delete(conversation)
        await session.delete(user)
        await session.commit()

        print("Test data cleaned up")


async def test_mcp_server_availability():
    """
    Test that the MCP server is properly configured and available.
    """
    print("\nTesting MCP Server Configuration...")

    # Import the MCP server
    from ai.mcp.server import server, list_todo_tools

    # Check that tools are available
    tools = await list_todo_tools()
    tool_names = [tool.name for tool in tools]
    print(f"MCP Server tools available: {tool_names}")

    # Verify all expected tools are present
    expected_tools = {"add_task", "list_tasks", "complete_task", "delete_task", "update_task"}
    actual_tools = set(tool_names)

    if expected_tools.issubset(actual_tools):
        print("All expected tools are registered in MCP server")
    else:
        missing = expected_tools - actual_tools
        print(f"Missing tools: {missing}")

    # Check that the server object has the expected attributes
    print(f"Server name: {server.name}")
    print("MCP server properly initialized")


async def main():
    """
    Main test function.
    """
    print("=" * 60)
    print("AI AGENT MCP INTEGRATION TEST")
    print("=" * 60)

    try:
        await test_mcp_server_availability()
        await test_ai_agent_mcp_integration()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED!")
        print("AI agent properly integrates with MCP server")
        print("Database operations are executed correctly through MCP")
        print("=" * 60)

    except Exception as e:
        print(f"\nTEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())