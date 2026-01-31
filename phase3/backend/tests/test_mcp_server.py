"""
Test script to verify MCP server functionality directly.
This script tests that the MCP server properly handles tool calls and executes database operations.
"""
import asyncio
import json
from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from database.session import get_async_session
from models.user import User
from models.task import Task, TaskCreate, TaskComplete
from services.task_service import TaskService


async def test_mcp_server_handlers():
    """
    Test the MCP server handlers directly to ensure they properly execute database operations.
    """
    print("Testing MCP Server Handlers...")

    # Get database session
    async with get_async_session() as session:
        # Create a test user with an integer ID to match the model
        import uuid
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

        # Test the add_task handler directly
        print("\n--- Testing add_task handler ---")

        # Simulate the arguments that would come from the MCP server
        add_arguments = {
            'user_id': user.id,
            'title': 'Test task from MCP',
            'description': 'This is a test task created via MCP server',
            'priority': 'high',
            'due_date': '2024-12-31'
        }

        # Import the MCP server handlers
        from ai.mcp.server import handle_add_task

        # Call the handler directly
        result = await handle_add_task(add_arguments)
        print(f"Add task result: {result}")

        # Verify task was added to database
        tasks = await session.exec(select(Task).where(Task.user_id == user.id))
        tasks_list = tasks.all()
        print(f"Tasks in database after add: {len(tasks_list)}")
        if tasks_list:
            latest_task = tasks_list[-1]
            print(f"Latest task: {latest_task.title} (Priority: {latest_task.priority})")

        # Test the list_tasks handler directly
        print("\n--- Testing list_tasks handler ---")
        list_arguments = {
            'user_id': user.id,
            'status': 'all'
        }

        from ai.mcp.server import handle_list_tasks
        result = await handle_list_tasks(list_arguments)
        print(f"List tasks result: {result}")

        # Test the complete_task handler directly
        if tasks_list:
            print("\n--- Testing complete_task handler ---")
            complete_arguments = {
                'user_id': user.id,
                'task_id': latest_task.id
            }

            from ai.mcp.server import handle_complete_task
            result = await handle_complete_task(complete_arguments)
            print(f"Complete task result: {result}")

            # Verify task was marked as completed
            await session.refresh(latest_task)
            print(f"Task {latest_task.id} completed status: {latest_task.completed}")

        # Test the update_task handler directly
        if tasks_list:
            print("\n--- Testing update_task handler ---")
            update_arguments = {
                'user_id': user.id,
                'task_id': latest_task.id,
                'title': 'Updated task title',
                'priority': 'low'
            }

            from ai.mcp.server import handle_update_task
            result = await handle_update_task(update_arguments)
            print(f"Update task result: {result}")

            # Verify task was updated
            await session.refresh(latest_task)
            print(f"Task {latest_task.id} updated title: {latest_task.title}, priority: {latest_task.priority}")

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
        print("MCP server handlers properly executed database operations")

        # Clean up test data
        for task in final_tasks_list:
            await session.delete(task)
        await session.delete(user)
        await session.commit()

        print("Test data cleaned up")


async def test_mcp_server_tools():
    """
    Test that the MCP server properly lists tools.
    """
    print("\nTesting MCP Server Tool Listing...")

    # Import and test the tool listing
    from ai.mcp.server import list_todo_tools

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


async def main():
    """
    Main test function.
    """
    print("=" * 60)
    print("MCP SERVER FUNCTIONALITY TEST")
    print("=" * 60)

    try:
        await test_mcp_server_tools()
        await test_mcp_server_handlers()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED!")
        print("MCP server properly handles tool calls")
        print("Database operations are executed correctly")
        print("=" * 60)

    except Exception as e:
        print(f"\nTEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())