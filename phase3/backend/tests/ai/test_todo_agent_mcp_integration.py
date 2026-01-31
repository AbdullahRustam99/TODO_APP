"""
MCP Integration tests for the TodoAgent functionality.

These tests verify that the TodoAgent properly connects to and uses the MCP server
for tool discovery and execution.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from ai.agents.todo_agent import TodoAgent
from models.conversation import Conversation
from uuid import UUID


@pytest.fixture
def todo_agent():
    """Create a TodoAgent instance for testing."""
    agent = TodoAgent()
    # Mock the internal components to avoid actual API calls
    agent.client = MagicMock()
    agent.config = MagicMock()
    agent._agent = MagicMock()
    return agent


@pytest.mark.asyncio
async def test_agent_initialization_with_mcp_server():
    """Test that the agent initializes with proper MCP server connection."""
    agent = TodoAgent()

    # Verify that the agent has the necessary components
    assert hasattr(agent, 'client')
    assert hasattr(agent, 'config')
    assert hasattr(agent, 'server_params')


@pytest.mark.asyncio
async def test_agent_connects_to_mcp_server():
    """Test that the agent can connect to the MCP server."""
    agent = TodoAgent()

    # Mock the runner and MCP server
    with patch('ai.agents.todo_agent.Runner') as mock_runner, \
         patch('ai.agents.todo_agent.MCPServerStdio') as mock_mcp_server:

        # Mock the runner response
        mock_result = AsyncMock()
        mock_result.final_output = "Task added successfully"

        mock_runner.run = AsyncMock(return_value=mock_result)

        # Mock the MCP server instance
        mock_server_instance = MagicMock()
        mock_mcp_server.return_value = mock_server_instance

        # Process a message to trigger the server connection
        user_id = "test-user-123"
        message = "Add a task: Buy groceries"
        conversation = MagicMock()
        conversation.id = UUID("12345678-1234-5678-1234-567812345678")

        result = await agent.process_message(user_id, message, conversation)

        # Verify that the agent processed the message successfully
        assert "response" in result
        assert result["response"] == "Task added successfully"


@pytest.mark.asyncio
async def test_agent_handles_tool_calls_through_mcp(todo_agent):
    """Test that the agent properly handles tool calls through the MCP server."""
    # Mock the runner to return a result that includes tool calls
    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_result = AsyncMock()
        mock_result.final_output = "Processing your request..."
        # Mock the result to include some tool calls
        mock_result.tool_calls = [
            {
                "id": "call_123",
                "function": {
                    "name": "add_task",
                    "arguments": '{"user_id": "test-user-123", "title": "Buy groceries"}'
                }
            }
        ]

        mock_runner.run = AsyncMock(return_value=mock_result)

        user_id = "test-user-123"
        message = "Add a task: Buy groceries"
        conversation = MagicMock()
        conversation.id = UUID("12345678-1234-5678-1234-567812345678")

        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify the result contains the expected response
        assert "response" in result
        assert "conversation_id" in result
        assert "tool_calls" in result
        assert result["response"] == "Processing your request..."


@pytest.mark.asyncio
async def test_agent_processes_add_task_command(todo_agent):
    """Test that the agent processes add task commands properly."""
    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_result = AsyncMock()
        mock_result.final_output = "Adding task: Buy groceries"

        mock_runner.run = AsyncMock(return_value=mock_result)

        user_id = "test-user-123"
        message = "Add a task: Buy groceries"
        conversation = MagicMock()
        conversation.id = UUID("12345678-1234-5678-1234-567812345678")

        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify the response
        assert result["response"] == "Adding task: Buy groceries"
        assert str(conversation.id) == result["conversation_id"]


@pytest.mark.asyncio
async def test_agent_processes_list_tasks_command(todo_agent):
    """Test that the agent processes list tasks commands properly."""
    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_result = AsyncMock()
        mock_result.final_output = "Here are your tasks: 1. Buy groceries, 2. Clean house"

        mock_runner.run = AsyncMock(return_value=mock_result)

        user_id = "test-user-123"
        message = "Show me my tasks"
        conversation = MagicMock()
        conversation.id = UUID("12345678-1234-5678-1234-567812345678")

        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify the response
        assert "here are your tasks" in result["response"].lower()


@pytest.mark.asyncio
async def test_agent_processes_complete_task_command(todo_agent):
    """Test that the agent processes complete task commands properly."""
    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_result = AsyncMock()
        mock_result.final_output = "Task marked as completed"

        mock_runner.run = AsyncMock(return_value=mock_result)

        user_id = "test-user-123"
        message = "Complete task 1"
        conversation = MagicMock()
        conversation.id = UUID("12345678-1234-5678-1234-567812345678")

        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify the response
        assert "completed" in result["response"].lower()


@pytest.mark.asyncio
async def test_agent_processes_delete_task_command(todo_agent):
    """Test that the agent processes delete task commands properly."""
    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_result = AsyncMock()
        mock_result.final_output = "Task deleted successfully"

        mock_runner.run = AsyncMock(return_value=mock_result)

        user_id = "test-user-123"
        message = "Delete task 1"
        conversation = MagicMock()
        conversation.id = UUID("12345678-1234-5678-1234-567812345678")

        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify the response
        assert "deleted" in result["response"].lower()


@pytest.mark.asyncio
async def test_agent_processes_update_task_command(todo_agent):
    """Test that the agent processes update task commands properly."""
    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_result = AsyncMock()
        mock_result.final_output = "Task updated successfully"

        mock_runner.run = AsyncMock(return_value=mock_result)

        user_id = "test-user-123"
        message = "Update task 1: Change title to 'Updated task'"
        conversation = MagicMock()
        conversation.id = UUID("12345678-1234-5678-1234-567812345678")

        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify the response
        assert "updated" in result["response"].lower()


@pytest.mark.asyncio
async def test_agent_error_handling(todo_agent):
    """Test that the agent handles errors properly."""
    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(side_effect=Exception("API Error"))

        user_id = "test-user-123"
        message = "Add a task: Test task"
        conversation = MagicMock()
        conversation.id = UUID("12345678-1234-5678-1234-567812345678")

        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify error handling response
        assert "error" in result["response"].lower()
        assert "API Error" in result["response"]


@pytest.mark.asyncio
async def test_agent_command_recognition_add_task(todo_agent):
    """Test command recognition for add task commands."""
    test_messages = [
        "Add a task: Buy groceries",
        "Create task: Clean house",
        "Add task - Walk the dog",
        "Make a new task: Prepare dinner"
    ]

    for message in test_messages:
        command = await todo_agent.recognize_command(message)
        assert command == "add_task", f"Failed to recognize add_task command for: {message}"


@pytest.mark.asyncio
async def test_agent_command_recognition_list_tasks(todo_agent):
    """Test command recognition for list tasks commands."""
    test_messages = [
        "Show me my tasks",
        "List my tasks",
        "What tasks do I have?",
        "Display my tasks",
        "Show all tasks"
    ]

    for message in test_messages:
        command = await todo_agent.recognize_command(message)
        assert command == "list_tasks", f"Failed to recognize list_tasks command for: {message}"


@pytest.mark.asyncio
async def test_agent_command_recognition_complete_task(todo_agent):
    """Test command recognition for complete task commands."""
    test_messages = [
        "Complete task 1",
        "Mark task 2 as done",
        "Finish this task",
        "Set task as completed"
    ]

    for message in test_messages:
        command = await todo_agent.recognize_command(message)
        assert command == "complete_task", f"Failed to recognize complete_task command for: {message}"


@pytest.mark.asyncio
async def test_agent_command_recognition_delete_task(todo_agent):
    """Test command recognition for delete task commands."""
    test_messages = [
        "Delete task 1",
        "Remove task 2",
        "Cancel this task",
        "Delete the first task"
    ]

    for message in test_messages:
        command = await todo_agent.recognize_command(message)
        assert command == "delete_task", f"Failed to recognize delete_task command for: {message}"


@pytest.mark.asyncio
async def test_agent_command_recognition_update_task(todo_agent):
    """Test command recognition for update task commands."""
    test_messages = [
        "Update task 1",
        "Change task 2 details",
        "Edit this task",
        "Modify the first task"
    ]

    for message in test_messages:
        command = await todo_agent.recognize_command(message)
        assert command == "update_task", f"Failed to recognize update_task command for: {message}"


@pytest.mark.asyncio
async def test_agent_command_recognition_unknown(todo_agent):
    """Test command recognition for unknown commands."""
    test_messages = [
        "Hello there",
        "How are you?",
        "What's the weather?",
        "Random message"
    ]

    for message in test_messages:
        command = await todo_agent.recognize_command(message)
        assert command is None, f"Unexpected command recognition for: {message}"


def test_agent_task_extraction(todo_agent):
    """Test task detail extraction from messages."""
    test_cases = [
        ("Add task: Buy groceries", {"title": "Buy groceries"}),
        ("Create: Clean the house", {"title": "Clean the house"}),
        ("New task - Walk the dog", {"title": "Walk the dog"}),
        ("Task: Prepare dinner with ingredients", {"title": "Prepare dinner with ingredients"})
    ]

    for message, expected in test_cases:
        details = todo_agent.extract_task_details(message)
        assert "title" in details
        assert expected["title"] in details["title"]


@pytest.mark.asyncio
async def test_agent_with_different_users(todo_agent):
    """Test that the agent works correctly with different users."""
    test_users = ["user-1", "user-2", "user-3", "user-4", "user-5"]
    message = "Add a task: Test task"

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_result = AsyncMock()
        mock_result.final_output = "Task added successfully"
        mock_runner.run = AsyncMock(return_value=mock_result)

        for user_id in test_users:
            conversation = MagicMock()
            conversation.id = UUID("12345678-1234-5678-1234-567812345678")

            result = await todo_agent.process_message(user_id, message, conversation)

            # Verify each user gets a proper response
            assert "response" in result
            assert "Task added" in result["response"]


@pytest.mark.asyncio
async def test_agent_conversation_isolation(todo_agent):
    """Test that conversations are properly isolated."""
    user_id = "test-user-123"
    message = "Add a task: Test task"

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_result = AsyncMock()
        mock_result.final_output = "Task added successfully"
        mock_runner.run = AsyncMock(return_value=mock_result)

        # Create multiple conversation instances
        conversations = []
        for i in range(3):
            conv = MagicMock()
            conv.id = UUID(f"12345678-1234-5678-1234-56781234567{i}")
            conversations.append(conv)

        # Process messages for each conversation
        for conv in conversations:
            result = await todo_agent.process_message(user_id, message, conv)
            assert "response" in result
            assert result["conversation_id"] == str(conv.id)


@pytest.mark.asyncio
async def test_agent_multiple_operations_sequence(todo_agent):
    """Test sequence of operations to ensure agent handles them properly."""
    operations = [
        ("Add a task: First task", "add_task"),
        ("Add a task: Second task", "add_task"),
        ("Show me my tasks", "list_tasks"),
        ("Complete task 1", "complete_task"),
        ("Update task 2: Change title", "update_task"),
        ("Delete task 2", "delete_task")
    ]

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock()

        for message, expected_command in operations:
            # Mock different responses based on the expected command
            mock_result = AsyncMock()
            if "add" in expected_command:
                mock_result.final_output = "Task added successfully"
            elif "list" in expected_command:
                mock_result.final_output = "Here are your tasks"
            elif "complete" in expected_command:
                mock_result.final_output = "Task completed"
            elif "update" in expected_command:
                mock_result.final_output = "Task updated"
            elif "delete" in expected_command:
                mock_result.final_output = "Task deleted"

            mock_runner.run.return_value = mock_result

            command = await todo_agent.recognize_command(message)
            assert command == expected_command

            conversation = MagicMock()
            conversation.id = UUID("12345678-1234-5678-1234-567812345678")

            result = await todo_agent.process_message("test-user-123", message, conversation)
            assert "response" in result


if __name__ == "__main__":
    pytest.main([__file__])