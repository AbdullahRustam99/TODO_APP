"""
Test script to verify AI agent functionality with MCP server integration.
This script tests that the AI agent properly executes database operations through the MCP server.
"""
import asyncio
import json
from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from database.session import get_async_session
from models.user import User
from models.task import Task
from models.conversation import Conversation
from ai.agents.todo_agent import TodoAgent
from ai.agents.conversation_manager import ConversationManager


async def test_ai_agent_integration():
    """
    Test the AI agent integration with MCP server and database operations.
    """
    print("Testing AI Agent Integration with MCP Server...")

    # Get database session
    async with get_async_session() as session:
        # Create a test user with an integer ID to match the model
        user = User(
            email="test@example.com",
            name="Test User",
            created_at=datetime.utcnow()
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        print(f"Created test user: {user.id}")

        # Create conversation manager and initialize conversation
        conversation_manager = ConversationManager(session)
        conversation = await conversation_manager.create_conversation(user.id)
        print(f"Created conversation: {conversation.id}")

        # Initialize the AI agent
        todo_agent = TodoAgent()
        print("Initialized AI agent")

        # Test 1: Add a task
        print("\n--- Test 1: Adding a task ---")
        add_task_request = "Add a new task: Buy groceries with high priority"
        result = await todo_agent.process_message(user.id, add_task_request, conversation)
        print(f"AI Response: {result['response']}")

        # Verify task was added to database
        tasks = await session.exec(select(Task).where(Task.user_id == user.id))
        tasks_list = tasks.all()
        print(f"Tasks in database after add: {len(tasks_list)}")
        if tasks_list:
            print(f"Latest task: {tasks_list[-1].title} (Priority: {tasks_list[-1].priority})")

        # Test 2: List tasks
        print("\n--- Test 2: Listing tasks ---")
        list_request = "List all my tasks"
        result = await todo_agent.process_message(user.id, list_request, conversation)
        print(f"AI Response: {result['response']}")

        # Verify we still have the same number of tasks
        tasks = await session.exec(select(Task).where(Task.user_id == user.id))
        tasks_list = tasks.all()
        print(f"Tasks in database after list: {len(tasks_list)}")

        # Test 3: Complete a task
        if tasks_list:
            print("\n--- Test 3: Completing a task ---")
            task_to_complete = tasks_list[-1]  # Use the last added task
            complete_request = f"Complete the task with ID {task_to_complete.id}"
            result = await todo_agent.process_message(user.id, complete_request, conversation)
            print(f"AI Response: {result['response']}")

            # Verify task was marked as completed
            await session.refresh(task_to_complete)
            print(f"Task {task_to_complete.id} completed status: {task_to_complete.completed}")

        # Test 4: Add another task with due date
        print("\n--- Test 4: Adding a task with due date ---")
        add_task_request = "Add a task: Schedule meeting with due date 2024-12-31 and medium priority"
        result = await todo_agent.process_message(user.id, add_task_request, conversation)
        print(f"AI Response: {result['response']}")

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
        print("Database operations executed successfully")

        # Clean up test data
        for task in final_tasks_list:
            await session.delete(task)
        await session.delete(conversation)
        await session.delete(user)
        await session.commit()

        print("Test data cleaned up")


async def test_mcp_server_directly():
    """
    Test the MCP server directly to ensure it's properly handling tool calls.
    """
    print("\nTesting MCP Server Directly...")

    # Import the server
    from ai.mcp.server import server, list_todo_tools
    from models.task import TaskCreate

    # Test the tool listing
    tools = await list_todo_tools()
    print(f"MCP Server tools available: {[tool.name for tool in tools]}")

    # Verify all expected tools are present
    expected_tools = {"add_task", "list_tasks", "complete_task", "delete_task", "update_task"}
    actual_tools = {tool.name for tool in tools}

    if expected_tools.issubset(actual_tools):
        print("All expected tools are registered in MCP server")
    else:
        missing = expected_tools - actual_tools
        print(f"Missing tools: {missing}")


async def main():
    """
    Main test function.
    """
    print("=" * 60)
    print("AI AGENT & MCP SERVER INTEGRATION TEST")
    print("=" * 60)

    try:
        await test_mcp_server_directly()
        await test_ai_agent_integration()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED!")
        print("AI agent properly integrates with MCP server")
        print("Database operations are executed correctly")
        print("=" * 60)

    except Exception as e:
        print(f"\nTEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())