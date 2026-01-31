"""
Logic tests for the TodoAgent functionality.

These tests verify the core logic of the AI agent including:
- Command recognition
- Task detail extraction
- Proper response formatting
- Error handling
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
async def test_process_message_success(todo_agent):
    """Test successful message processing."""
    # Mock data
    user_id = "test-user-123"
    message = "Add a task: Buy groceries"
    conversation = MagicMock()
    conversation.id = UUID("12345678-1234-5678-1234-567812345678")

    # Mock the runner response
    mock_result = AsyncMock()
    mock_result.final_output = "Task 'Buy groceries' added successfully"

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        result = await todo_agent.process_message(user_id, message, conversation)

        # Assertions
        assert "response" in result
        assert "conversation_id" in result
        assert "tool_calls" in result
        assert "requires_action" in result
        assert result["response"] == "Task 'Buy groceries' added successfully"


@pytest.mark.asyncio
async def test_process_message_with_error(todo_agent):
    """Test message processing with error handling."""
    # Mock data
    user_id = "test-user-123"
    message = "Add a task: Buy groceries"
    conversation = MagicMock()
    conversation.id = UUID("12345678-1234-5678-1234-567812345678")

    # Mock the runner to raise an exception
    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(side_effect=Exception("API Error"))

        result = await todo_agent.process_message(user_id, message, conversation)

        # Assertions for error case
        assert "response" in result
        assert "conversation_id" in result
        assert "tool_calls" in result
        assert "requires_action" in result
        assert "error" in result["response"]


@pytest.mark.asyncio
async def test_recognize_command_add_task(todo_agent):
    """Test recognizing add task commands."""
    test_messages = [
        "Add a task: Buy groceries",
        "Create task: Clean the house",
        "Make a new task: Pay bills",
        "Add task: Schedule meeting"
    ]

    for msg in test_messages:
        command = await todo_agent.recognize_command(msg)
        assert command == "add_task"


@pytest.mark.asyncio
async def test_recognize_command_list_tasks(todo_agent):
    """Test recognizing list tasks commands."""
    test_messages = [
        "Show me my tasks",
        "List my tasks",
        "Display my tasks",
        "What are my tasks?"
    ]

    for msg in test_messages:
        command = await todo_agent.recognize_command(msg)
        assert command == "list_tasks"


@pytest.mark.asyncio
async def test_recognize_command_complete_task(todo_agent):
    """Test recognizing complete task commands."""
    test_messages = [
        "Complete task 1",
        "Mark task as done",
        "Finish this task",
        "Task is done"
    ]

    for msg in test_messages:
        command = await todo_agent.recognize_command(msg)
        assert command == "complete_task"


@pytest.mark.asyncio
async def test_recognize_command_delete_task(todo_agent):
    """Test recognizing delete task commands."""
    test_messages = [
        "Delete task 1",
        "Remove this task",
        "Cancel this task",
        "Get rid of task"
    ]

    for msg in test_messages:
        command = await todo_agent.recognize_command(msg)
        assert command == "delete_task"


@pytest.mark.asyncio
async def test_recognize_command_update_task(todo_agent):
    """Test recognizing update task commands."""
    test_messages = [
        "Update task 1",
        "Change this task",
        "Edit task details",
        "Modify task"
    ]

    for msg in test_messages:
        command = await todo_agent.recognize_command(msg)
        assert command == "update_task"


@pytest.mark.asyncio
async def test_recognize_command_unknown(todo_agent):
    """Test recognizing unknown commands."""
    test_messages = [
        "Hello",
        "How are you?",
        "What's the weather?",
        "Random message"
    ]

    for msg in test_messages:
        command = await todo_agent.recognize_command(msg)
        assert command is None


def test_extract_task_details_basic(todo_agent):
    """Test extracting task details from simple messages."""
    message = "Add task: Buy groceries"
    details = todo_agent.extract_task_details(message)

    assert "title" in details
    assert "description" in details
    assert details["title"] == "Buy groceries"
    assert details["description"] == ""


def test_extract_task_details_with_colon(todo_agent):
    """Test extracting task details from messages with colon separator."""
    message = "Add a new task: Buy groceries: with milk and bread"
    details = todo_agent.extract_task_details(message)

    assert "title" in details
    assert "description" in details
    # Should take everything after the first colon as title
    assert details["title"] == "Buy groceries: with milk and bread"
    assert details["description"] == ""


def test_extract_task_details_no_colon(todo_agent):
    """Test extracting task details from messages without colon."""
    message = "Clean the house"
    details = todo_agent.extract_task_details(message)

    assert "title" in details
    assert "description" in details
    assert details["title"] == "Clean the house"
    assert details["description"] == ""


@pytest.mark.asyncio
async def test_agent_initialization(todo_agent):
    """Test that the agent initializes correctly."""
    assert hasattr(todo_agent, 'client')
    assert hasattr(todo_agent, 'config')
    assert hasattr(todo_agent, 'process_message')
    assert hasattr(todo_agent, 'recognize_command')
    assert hasattr(todo_agent, 'extract_task_details')


if __name__ == "__main__":
    pytest.main([__file__])