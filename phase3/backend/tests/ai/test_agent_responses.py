"""
Tests to verify the AI agent's responses and logic processing.

These tests check how the agent responds to different types of commands
and verify the response format and content.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from ai.agents.todo_agent import TodoAgent
from models.conversation import Conversation
from uuid import UUID, uuid4


@pytest.fixture
def todo_agent():
    """Create a TodoAgent instance for testing."""
    agent = TodoAgent()
    # Mock the internal components to avoid actual API calls
    agent.client = MagicMock()
    agent.config = MagicMock()
    return agent


@pytest.mark.asyncio
async def test_agent_add_task_command_response(todo_agent):
    """Test the agent's response to add task commands."""
    user_id = "test-user-123"
    message = "Add a task: Buy groceries"
    conversation = MagicMock()
    conversation.id = uuid4()

    # Mock the runner response for add_task
    mock_result = MagicMock()
    mock_result.final_output = "I've added the task 'Buy groceries' for you."

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify the response contains expected elements
        assert "response" in result
        assert "Buy groceries" in result["response"] or "added" in result["response"].lower()
        assert "conversation_id" in result
        assert "tool_calls" in result
        assert "requires_action" in result


@pytest.mark.asyncio
async def test_agent_list_tasks_command_response(todo_agent):
    """Test the agent's response to list tasks commands."""
    user_id = "test-user-123"
    message = "Show me my tasks"
    conversation = MagicMock()
    conversation.id = uuid4()

    # Mock the runner response for list_tasks
    mock_result = MagicMock()
    mock_result.final_output = "Here are your tasks: 1. Buy groceries, 2. Clean house"

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify the response contains expected elements
        assert "response" in result
        assert "tasks" in result["response"].lower()
        assert "conversation_id" in result
        assert "tool_calls" in result
        assert "requires_action" in result


@pytest.mark.asyncio
async def test_agent_complete_task_command_response(todo_agent):
    """Test the agent's response to complete task commands."""
    user_id = "test-user-123"
    message = "Complete task 1"
    conversation = MagicMock()
    conversation.id = uuid4()

    # Mock the runner response for complete_task
    mock_result = MagicMock()
    mock_result.final_output = "I've marked task 1 as completed."

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify the response contains expected elements
        assert "response" in result
        assert "completed" in result["response"].lower()
        assert "conversation_id" in result
        assert "tool_calls" in result
        assert "requires_action" in result


@pytest.mark.asyncio
async def test_agent_delete_task_command_response(todo_agent):
    """Test the agent's response to delete task commands."""
    user_id = "test-user-123"
    message = "Delete task 2"
    conversation = MagicMock()
    conversation.id = uuid4()

    # Mock the runner response for delete_task
    mock_result = MagicMock()
    mock_result.final_output = "I've deleted task 2 for you."

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify the response contains expected elements
        assert "response" in result
        assert "deleted" in result["response"].lower()
        assert "conversation_id" in result
        assert "tool_calls" in result
        assert "requires_action" in result


@pytest.mark.asyncio
async def test_agent_update_task_command_response(todo_agent):
    """Test the agent's response to update task commands."""
    user_id = "test-user-123"
    message = "Update task 3: Change title to 'Updated task'"
    conversation = MagicMock()
    conversation.id = uuid4()

    # Mock the runner response for update_task
    mock_result = MagicMock()
    mock_result.final_output = "I've updated task 3 with the new title."

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify the response contains expected elements
        assert "response" in result
        assert "updated" in result["response"].lower()
        assert "conversation_id" in result
        assert "tool_calls" in result
        assert "requires_action" in result


@pytest.mark.asyncio
async def test_agent_unrecognized_command_response(todo_agent):
    """Test the agent's response to unrecognized commands."""
    user_id = "test-user-123"
    message = "Random message that doesn't match any command"
    conversation = MagicMock()
    conversation.id = uuid4()

    # Mock the runner response for unrecognized commands
    mock_result = MagicMock()
    mock_result.final_output = "I'm sorry, I didn't understand that command. Could you please rephrase?"

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify the response contains expected elements
        assert "response" in result
        assert "sorry" in result["response"].lower() or "understand" in result["response"].lower()
        assert "conversation_id" in result
        assert "tool_calls" in result
        assert "requires_action" in result


@pytest.mark.asyncio
async def test_agent_command_recognition_various_formats(todo_agent):
    """Test the agent's ability to recognize commands in various formats."""
    test_cases = [
        # Add task variations
        ("Add task: Buy groceries", "add_task"),
        ("Create a task: Clean house", "add_task"),
        ("Add new task - Walk the dog", "add_task"),
        ("Make task: Prepare dinner", "add_task"),

        # List tasks variations
        ("Show me my tasks", "list_tasks"),
        ("List my tasks", "list_tasks"),
        ("What tasks do I have?", "list_tasks"),
        ("Display my tasks", "list_tasks"),

        # Complete task variations
        ("Complete task 1", "complete_task"),
        ("Mark task 1 as done", "complete_task"),
        ("Finish task 2", "complete_task"),
        ("Set task 3 to completed", "complete_task"),

        # Delete task variations
        ("Delete task 1", "delete_task"),
        ("Remove task 2", "delete_task"),
        ("Cancel task 3", "delete_task"),
        ("Delete the first task", "delete_task"),

        # Update task variations
        ("Update task 1", "update_task"),
        ("Change task 2 details", "update_task"),
        ("Edit task 3", "update_task"),
        ("Modify task 4 title", "update_task"),
    ]

    for message, expected_command_type in test_cases:
        command = await todo_agent.recognize_command(message)
        assert command == expected_command_type, f"Failed for message: '{message}', expected: {expected_command_type}, got: {command}"


@pytest.mark.asyncio
async def test_agent_command_recognition_case_insensitive(todo_agent):
    """Test the agent's ability to recognize commands regardless of case."""
    test_cases = [
        ("ADD A TASK: BUY GROCERIES", "add_task"),
        ("show me my TASKS", "list_tasks"),
        ("Complete TASK 1", "complete_task"),
        ("DELETE task 2", "delete_task"),
        ("update TaSk 3", "update_task"),
    ]

    for message, expected_command_type in test_cases:
        command = await todo_agent.recognize_command(message)
        assert command == expected_command_type, f"Failed for case-insensitive test: '{message}', expected: {expected_command_type}, got: {command}"


def test_agent_task_extraction_various_formats(todo_agent):
    """Test the agent's ability to extract task details from various message formats."""
    test_cases = [
        ("Add task: Buy groceries", {"title": "Buy groceries"}),
        ("Create: Clean the house", {"title": "Clean the house"}),
        ("Task - Walk the dog", {"title": "Walk the dog"}),
        ("New task: Prepare dinner with ingredients", {"title": "Prepare dinner with ingredients"}),
        ("Add: Simple task", {"title": "Simple task"}),
    ]

    for message, expected in test_cases:
        details = todo_agent.extract_task_details(message)
        assert "title" in details
        assert expected["title"] in details["title"]


@pytest.mark.asyncio
async def test_agent_process_message_with_different_users(todo_agent):
    """Test that the agent handles different users correctly."""
    test_users = ["user-1", "user-2", "user-3", "user-4", "user-5"]
    message = "Add a task: Test task for user isolation"

    for user_id in test_users:
        conversation = MagicMock()
        conversation.id = uuid4()

        # Mock the runner response
        mock_result = MagicMock()
        mock_result.final_output = f"Task added successfully for {user_id}"

        with patch('ai.agents.todo_agent.Runner') as mock_runner:
            mock_runner.run = AsyncMock(return_value=mock_result)

            result = await todo_agent.process_message(user_id, message, conversation)

            # Verify each user gets a proper response
            assert "response" in result
            assert user_id in result["response"]


@pytest.mark.asyncio
async def test_agent_process_message_returns_correct_structure(todo_agent):
    """Test that the agent always returns the correct response structure."""
    user_id = "test-user-123"
    message = "Add a task: Test structure"
    conversation = MagicMock()
    conversation.id = uuid4()

    # Mock the runner response
    mock_result = MagicMock()
    mock_result.final_output = "Task processed successfully"

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify the response structure
        assert isinstance(result, dict)
        assert "response" in result
        assert "conversation_id" in result
        assert "tool_calls" in result
        assert "requires_action" in result

        # Verify types
        assert isinstance(result["response"], str)
        assert isinstance(result["conversation_id"], str)
        assert isinstance(result["tool_calls"], list)
        assert isinstance(result["requires_action"], bool)


@pytest.mark.asyncio
async def test_agent_error_handling_in_process_message(todo_agent):
    """Test that the agent handles errors gracefully in process_message."""
    user_id = "test-user-123"
    message = "Add a task: Test error handling"
    conversation = MagicMock()
    conversation.id = uuid4()

    # Mock the runner to raise an exception
    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(side_effect=Exception("API Error"))

        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify error handling response structure
        assert isinstance(result, dict)
        assert "response" in result
        assert "conversation_id" in result
        assert "tool_calls" in result
        assert "requires_action" in result

        # Verify error message is in the response
        assert "error" in result["response"].lower()


@pytest.mark.asyncio
async def test_agent_process_message_with_complex_commands(todo_agent):
    """Test the agent's response to complex commands with multiple parts."""
    user_id = "test-user-123"
    test_cases = [
        "Add a new task with high priority: Buy groceries by Friday",
        "Create a task to clean the house - it's urgent",
        "I need to add a task: Finish the project report by tomorrow",
        "Can you create a task for me: Schedule dentist appointment next week"
    ]

    for message in test_cases:
        conversation = MagicMock()
        conversation.id = uuid4()

        # Mock the runner response
        mock_result = MagicMock()
        mock_result.final_output = "Task processed successfully"

        with patch('ai.agents.todo_agent.Runner') as mock_runner:
            mock_runner.run = AsyncMock(return_value=mock_result)

            result = await todo_agent.process_message(user_id, message, conversation)

            # Verify the response structure
            assert "response" in result
            assert "conversation_id" in result
            assert "tool_calls" in result
            assert "requires_action" in result


@pytest.mark.asyncio
async def test_agent_command_recognition_with_context(todo_agent):
    """Test the agent's command recognition with context clues."""
    test_cases = [
        # Commands with context
        ("Could you please add a task: Buy milk", "add_task"),
        ("Can you show me what tasks I have?", "list_tasks"),
        ("I've finished task 1, please mark it as done", "complete_task"),
        ("I no longer need task 2, please remove it", "delete_task"),
        ("I need to change the due date for task 3", "update_task"),
    ]

    for message, expected_command_type in test_cases:
        command = await todo_agent.recognize_command(message)
        assert command == expected_command_type, f"Failed for contextual message: '{message}', expected: {expected_command_type}, got: {command}"


@pytest.mark.asyncio
async def test_agent_response_quality_for_different_scenarios(todo_agent):
    """Test the quality of agent responses for different scenarios."""
    scenarios = [
        {
            "message": "Add a task: Buy groceries",
            "expected_elements": ["task", "groceries", "add"]
        },
        {
            "message": "List all my tasks",
            "expected_elements": ["tasks", "list", "show"]
        },
        {
            "message": "Complete task 123",
            "expected_elements": ["complete", "task", "123"]
        },
        {
            "message": "Update task 456 to have high priority",
            "expected_elements": ["update", "task", "456", "priority"]
        }
    ]

    for scenario in scenarios:
        user_id = "test-user-123"
        conversation = MagicMock()
        conversation.id = uuid4()

        # Mock the runner response
        mock_result = MagicMock()
        mock_result.final_output = f"Processed: {scenario['message']}"

        with patch('ai.agents.todo_agent.Runner') as mock_runner:
            mock_runner.run = AsyncMock(return_value=mock_result)

            result = await todo_agent.process_message(user_id, scenario["message"], conversation)

            # Check that response contains expected elements
            response_lower = result["response"].lower()
            for element in scenario["expected_elements"]:
                assert element.lower() in response_lower


if __name__ == "__main__":
    pytest.main([__file__])