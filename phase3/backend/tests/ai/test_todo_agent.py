"""
Unit tests for the TodoAgent functionality.
"""
import pytest
from unittest.mock import AsyncMock, patch
from ai.agents.todo_agent import TodoAgent


@pytest.mark.asyncio
async def test_process_message_basic():
    """Test basic message processing."""
    agent = TodoAgent()

    # Mock the OpenAI client response
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message = AsyncMock()
    mock_response.choices[0].message.content = "I understand your request."
    mock_response.choices[0].message.tool_calls = None

    with patch.object(agent.client.chat.completions, 'create', return_value=mock_response):
        result = await agent.process_message("1", "Add a task: Buy groceries", None)

        assert "response" in result
        assert result["response"] == "I understand your request."


@pytest.mark.asyncio
async def test_recognize_command_add_task():
    """Test recognizing add task command."""
    agent = TodoAgent()

    result = await agent.recognize_command("Add a new task: Clean the house")
    assert result == "add_task"


@pytest.mark.asyncio
async def test_recognize_command_list_tasks():
    """Test recognizing list tasks command."""
    agent = TodoAgent()

    result = await agent.recognize_command("Show me my tasks")
    assert result == "list_tasks"


@pytest.mark.asyncio
async def test_recognize_command_complete_task():
    """Test recognizing complete task command."""
    agent = TodoAgent()

    result = await agent.recognize_command("Mark task as done")
    assert result == "complete_task"


@pytest.mark.asyncio
async def test_recognize_command_delete_task():
    """Test recognizing delete task command."""
    agent = TodoAgent()

    result = await agent.recognize_command("Remove this task")
    assert result == "delete_task"


@pytest.mark.asyncio
async def test_recognize_command_update_task():
    """Test recognizing update task command."""
    agent = TodoAgent()

    result = await agent.recognize_command("Change the task title")
    assert result == "update_task"


def test_extract_task_details():
    """Test extracting task details from a message."""
    agent = TodoAgent()

    result = agent.extract_task_details("Add task: Buy milk and bread")
    assert result["title"] == "Buy milk and bread"

    result = agent.extract_task_details("Clean the garage")
    assert result["title"] == "Clean the garage"