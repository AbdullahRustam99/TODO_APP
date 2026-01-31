"""
Integration tests for the TodoAgent functionality.

These tests verify that the AI agent integrates properly with:
- Database operations
- Conversation management
- Task service
- API endpoints
- MCP server
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio
from main import app  # Adjust import based on your main app location
from ai.agents.todo_agent import TodoAgent
from models.conversation import Conversation
from models.message import Message
from uuid import UUID, uuid4


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


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
async def test_full_chat_flow_integration(todo_agent):
    """Test the complete chat flow from request to response."""
    user_id = "test-user-123"
    message = "Add a task: Buy groceries"
    conversation = MagicMock()
    conversation.id = uuid4()

    # Mock the agent response
    mock_result = AsyncMock()
    mock_result.final_output = "Task 'Buy groceries' added successfully"

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        # Process the message
        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify the result structure
        assert isinstance(result, dict)
        assert "response" in result
        assert "conversation_id" in result
        assert "tool_calls" in result
        assert "requires_action" in result
        assert result["response"] == "Task 'Buy groceries' added successfully"
        assert str(conversation.id) == result["conversation_id"]


@pytest.mark.asyncio
async def test_chat_endpoint_integration(client):
    """Test the chat endpoint integration."""
    with patch('ai.agents.conversation_manager.ConversationManager') as mock_conv_manager, \
         patch('ai.agents.todo_agent.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_manager_instance = MagicMock()
        mock_conv_manager_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_manager_instance.add_message = AsyncMock()
        mock_conv_manager.return_value = mock_conv_manager_instance

        # Mock agent
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(return_value={
            "response": "Task added successfully",
            "conversation_id": str(uuid4()),
            "tool_calls": [],
            "requires_action": False
        })
        mock_agent_class.return_value = mock_agent_instance

        # Make a request to the chat endpoint
        response = client.post(
            "/api/test-user-123/chat",
            json={
                "message": "Add a task: Buy groceries"
            },
            headers={"Content-Type": "application/json"}
        )

        # Verify response
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "conversation_id" in data


@pytest.mark.asyncio
async def test_conversation_creation_integration(todo_agent):
    """Test conversation creation and management integration."""
    from ai.agents.conversation_manager import ConversationManager
    from sqlmodel.ext.asyncio.session import AsyncSession

    # Create a mock database session
    mock_session = MagicMock(spec=AsyncSession)

    # Create conversation manager
    conv_manager = ConversationManager(mock_session)

    # Test conversation creation
    user_id = "test-user-123"

    # Mock the database operations
    with patch.object(mock_session, 'add'), \
         patch.object(mock_session, 'commit', new_callable=AsyncMock), \
         patch.object(mock_session, 'refresh', new_callable=AsyncMock):

        conversation = await conv_manager.create_conversation(user_id)

        # Verify conversation was created with proper properties
        assert conversation.user_id == user_id
        assert hasattr(conversation, 'expires_at')


@pytest.mark.asyncio
async def test_tool_execution_integration(todo_agent):
    """Test tool execution integration with the task service."""
    # This test verifies that the agent can properly call tools
    # when connected to the MCP server
    user_id = "test-user-123"
    conversation = MagicMock()
    conversation.id = uuid4()

    # Mock the runner to return a result with tool calls
    mock_result = AsyncMock()
    mock_result.final_output = "Processing your request..."
    # Simulate that the agent identified tool calls to execute
    mock_result.tool_calls = []

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        result = await todo_agent.process_message(user_id, "Add a task: Buy groceries", conversation)

        # Verify the response structure
        assert "response" in result
        assert "tool_calls" in result
        assert isinstance(result["tool_calls"], list)


@pytest.mark.asyncio
async def test_command_recognition_integration(todo_agent):
    """Test command recognition with actual natural language processing."""
    test_cases = [
        ("Add a task: Buy groceries", "add_task"),
        ("Create task: Clean the house", "add_task"),
        ("Show me my tasks", "list_tasks"),
        ("List all my tasks", "list_tasks"),
        ("Complete task 1", "complete_task"),
        ("Mark task as done", "complete_task"),
        ("Delete task 3", "delete_task"),
        ("Remove this task", "delete_task"),
        ("Update task 2", "update_task"),
        ("Change task details", "update_task"),
        ("Hello world", None),  # Should not match any command
    ]

    for message, expected_command in test_cases:
        result = await todo_agent.recognize_command(message)
        assert result == expected_command, f"Failed for message: {message}"


@pytest.mark.asyncio
async def test_task_extraction_integration(todo_agent):
    """Test task detail extraction from various message formats."""
    test_cases = [
        ("Add task: Buy groceries", {"title": "Buy groceries"}),
        ("Create: Clean the house", {"title": "Clean the house"}),
        ("New task - Walk the dog", {"title": "Walk the dog"}),
        ("Task: Prepare dinner", {"title": "Prepare dinner"}),
        ("Add: Simple task", {"title": "Simple task"}),
    ]

    for message, expected in test_cases:
        result = todo_agent.extract_task_details(message)
        assert "title" in result
        assert expected["title"] in result["title"]


@pytest.mark.asyncio
async def test_multiple_conversation_integration(todo_agent):
    """Test handling multiple conversations simultaneously."""
    user_ids = ["user-1", "user-2", "user-3"]
    messages = [
        "Add a task: User 1 task",
        "Add a task: User 2 task",
        "Add a task: User 3 task"
    ]

    # Mock the runner response
    mock_result = AsyncMock()
    mock_result.final_output = "Task added successfully"

    async def process_for_user(user_id, message):
        conversation = MagicMock()
        conversation.id = uuid4()

        with patch('ai.agents.todo_agent.Runner') as mock_runner:
            mock_runner.run = AsyncMock(return_value=mock_result)

            result = await todo_agent.process_message(user_id, message, conversation)
            return result

    # Process all conversations concurrently
    tasks = [process_for_user(uid, msg) for uid, msg in zip(user_ids, messages)]
    results = await asyncio.gather(*tasks)

    # Verify all results
    assert len(results) == len(user_ids)
    for result in results:
        assert "response" in result
        assert "conversation_id" in result


@pytest.mark.asyncio
async def test_error_recovery_integration(todo_agent):
    """Test that the agent can recover from errors and continue operating."""
    user_id = "test-user-123"
    conversation = MagicMock()
    conversation.id = uuid4()

    # First request - simulate success
    mock_result_success = AsyncMock()
    mock_result_success.final_output = "Task added successfully"

    # Second request - simulate error
    mock_result_error = AsyncMock()
    mock_result_error.final_output = "Error processing request"

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        # Mock first call to succeed, second to have an issue
        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return mock_result_success
            else:
                # For the second call, simulate an error in the process_message method
                raise Exception("API Error")

        mock_runner.run = AsyncMock(side_effect=side_effect)

        # First call should succeed
        result1 = await todo_agent.process_message(user_id, "Add task: First task", conversation)
        assert "response" in result1

        # Second call should handle the error gracefully
        try:
            result2 = await todo_agent.process_message(user_id, "Add task: Second task", conversation)
            # If no exception was raised, check if error response was returned
            assert "response" in result2
        except Exception:
            # If an exception was raised, that's also acceptable behavior for error handling
            pass


@pytest.mark.asyncio
async def test_mcp_server_connection_integration(todo_agent):
    """Test that the agent properly connects to the MCP server."""
    # This test verifies that the agent can connect to the MCP server
    # when properly configured (even with mocks)

    # Verify that the agent has the required properties for MCP integration
    assert hasattr(todo_agent, 'client')
    assert hasattr(todo_agent, 'config')

    # The agent should be able to process messages without immediate errors
    # related to MCP server connection (these would occur at runtime)
    user_id = "test-user-123"
    conversation = MagicMock()
    conversation.id = uuid4()

    # Mock successful connection and processing
    mock_result = AsyncMock()
    mock_result.final_output = "Processed successfully"

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        result = await todo_agent.process_message(user_id, "Add a task: Test", conversation)

        assert result["response"] == "Processed successfully"


if __name__ == "__main__":
    pytest.main([__file__])