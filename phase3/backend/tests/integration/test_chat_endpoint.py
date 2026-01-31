"""
Integration tests for the AI Chat endpoint.

These tests verify that the chat endpoint properly integrates with the AI agent
and MCP server for processing natural language commands.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from main import app
from uuid import UUID, uuid4
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


@pytest.mark.asyncio
async def test_chat_endpoint_exists_and_responds(client):
    """Test that the chat endpoint exists and returns a proper response."""
    # Mock the conversation manager and agent to avoid actual processing
    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_instance = MagicMock()
        mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent instance
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

        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "conversation_id" in data
        assert "tool_calls" in data
        assert "requires_action" in data


def test_chat_endpoint_missing_message(client):
    """Test that the chat endpoint handles missing message parameter."""
    response = client.post(
        "/api/test-user-123/chat",
        json={},
        headers={"Content-Type": "application/json"}
    )

    # Should return an error for missing required parameters
    assert response.status_code in [422, 500]  # Either validation error or server error


@pytest.mark.asyncio
async def test_chat_endpoint_with_existing_conversation(client):
    """Test the chat endpoint with an existing conversation ID."""
    conv_id = str(uuid4())

    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_instance = MagicMock()
        mock_conv_instance.get_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent instance
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(return_value={
            "response": "Message processed",
            "conversation_id": conv_id,
            "tool_calls": [],
            "requires_action": False
        })
        mock_agent_class.return_value = mock_agent_instance

        # Make a request with a conversation ID
        response = client.post(
            f"/api/test-user-123/chat",
            params={"conversation_id": conv_id},
            json={
                "message": "Update my task"
            },
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["conversation_id"] == conv_id


@pytest.mark.asyncio
async def test_get_user_conversations_endpoint(client):
    """Test the endpoint for getting user conversations."""
    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager:
        mock_conv_instance = MagicMock()
        mock_conv_instance.get_recent_conversations = AsyncMock(return_value=[])
        mock_conv_manager.return_value = mock_conv_instance

        response = client.get("/api/test-user-123/conversations")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_conversation_history_endpoint(client):
    """Test the endpoint for getting conversation history."""
    conv_id = uuid4()

    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager:
        mock_conv_instance = MagicMock()
        mock_conv_instance.get_conversation = AsyncMock(return_value=MagicMock(id=conv_id, user_id="test-user-123"))
        mock_conv_instance.get_conversation_history = AsyncMock(return_value=[])
        mock_conv_manager.return_value = mock_conv_instance

        response = client.get(f"/api/test-user-123/conversations/{conv_id}")

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "messages" in data


@pytest.mark.asyncio
async def test_chat_endpoint_processes_add_task_command(client):
    """Test that the chat endpoint processes add task commands properly."""
    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_instance = MagicMock()
        mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent instance to return an add_task response
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(return_value={
            "response": "Task 'Buy groceries' added successfully",
            "conversation_id": str(uuid4()),
            "tool_calls": [{"name": "add_task", "arguments": {"user_id": "test-user-123", "title": "Buy groceries"}}],
            "requires_action": True
        })
        mock_agent_class.return_value = mock_agent_instance

        response = client.post(
            "/api/test-user-123/chat",
            json={
                "message": "Add a task: Buy groceries"
            },
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "Task 'Buy groceries'" in data["response"]


@pytest.mark.asyncio
async def test_chat_endpoint_processes_list_tasks_command(client):
    """Test that the chat endpoint processes list tasks commands properly."""
    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_instance = MagicMock()
        mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent instance to return a list_tasks response
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(return_value={
            "response": "Here are your tasks: 1. Buy groceries, 2. Clean house",
            "conversation_id": str(uuid4()),
            "tool_calls": [{"name": "list_tasks", "arguments": {"user_id": "test-user-123", "status": "all"}}],
            "requires_action": True
        })
        mock_agent_class.return_value = mock_agent_instance

        response = client.post(
            "/api/test-user-123/chat",
            json={
                "message": "Show me my tasks"
            },
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data["response"].lower()


@pytest.mark.asyncio
async def test_chat_endpoint_processes_complete_task_command(client):
    """Test that the chat endpoint processes complete task commands properly."""
    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_instance = MagicMock()
        mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent instance to return a complete_task response
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(return_value={
            "response": "Task marked as completed successfully",
            "conversation_id": str(uuid4()),
            "tool_calls": [{"name": "complete_task", "arguments": {"user_id": "test-user-123", "task_id": "123"}}],
            "requires_action": True
        })
        mock_agent_class.return_value = mock_agent_instance

        response = client.post(
            "/api/test-user-123/chat",
            json={
                "message": "Complete task 123"
            },
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "completed" in data["response"].lower()


@pytest.mark.asyncio
async def test_chat_endpoint_processes_delete_task_command(client):
    """Test that the chat endpoint processes delete task commands properly."""
    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_instance = MagicMock()
        mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent instance to return a delete_task response
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(return_value={
            "response": "Task deleted successfully",
            "conversation_id": str(uuid4()),
            "tool_calls": [{"name": "delete_task", "arguments": {"user_id": "test-user-123", "task_id": "456"}}],
            "requires_action": True
        })
        mock_agent_class.return_value = mock_agent_instance

        response = client.post(
            "/api/test-user-123/chat",
            json={
                "message": "Delete task 456"
            },
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "deleted" in data["response"].lower()


@pytest.mark.asyncio
async def test_chat_endpoint_processes_update_task_command(client):
    """Test that the chat endpoint processes update task commands properly."""
    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_instance = MagicMock()
        mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent instance to return an update_task response
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(return_value={
            "response": "Task updated successfully",
            "conversation_id": str(uuid4()),
            "tool_calls": [{"name": "update_task", "arguments": {"user_id": "test-user-123", "task_id": "789", "title": "Updated task title"}}],
            "requires_action": True
        })
        mock_agent_class.return_value = mock_agent_instance

        response = client.post(
            "/api/test-user-123/chat",
            json={
                "message": "Update task 789: Change title to 'Updated task title'"
            },
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "updated" in data["response"].lower()


@pytest.mark.asyncio
async def test_chat_endpoint_handles_agent_errors(client):
    """Test that the chat endpoint handles agent errors gracefully."""
    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_instance = MagicMock()
        mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent to raise an exception
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(side_effect=Exception("Agent error"))
        mock_agent_class.return_value = mock_agent_instance

        response = client.post(
            "/api/test-user-123/chat",
            json={
                "message": "Add a task: Test task"
            },
            headers={"Content-Type": "application/json"}
        )

        # Should return a server error
        assert response.status_code == 500


@pytest.mark.asyncio
async def test_conversation_persistence_integration(client):
    """Test that conversations are properly persisted through the endpoint."""
    test_conv_id = uuid4()

    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager:
        # Mock conversation manager to simulate real database operations
        mock_conv_instance = MagicMock()
        mock_conv_instance.get_conversation = AsyncMock(return_value=MagicMock(id=test_conv_id, user_id="test-user-123"))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_instance.update_conversation_timestamp = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        response = client.post(
            f"/api/test-user-123/chat",
            json={
                "message": "Add a task: Test persistence",
                "conversation_id": str(test_conv_id)
            },
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200
        # Verify that conversation methods were called
        mock_conv_instance.get_conversation.assert_called_once()
        mock_conv_instance.add_message.assert_called()
        mock_conv_instance.update_conversation_timestamp.assert_called_once()


@pytest.mark.asyncio
async def test_multiple_concurrent_chat_requests(client):
    """Test handling of multiple concurrent chat requests."""
    import asyncio

    async def make_request():
        with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
             patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

            # Mock conversation manager
            mock_conv_instance = MagicMock()
            mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
            mock_conv_instance.add_message = AsyncMock()
            mock_conv_manager.return_value = mock_conv_instance

            # Mock agent instance
            mock_agent_instance = MagicMock()
            mock_agent_instance.process_message = AsyncMock(return_value={
                "response": "Processed successfully",
                "conversation_id": str(uuid4()),
                "tool_calls": [],
                "requires_action": False
            })
            mock_agent_class.return_value = mock_agent_instance

            response = client.post(
                "/api/test-user-123/chat",
                json={"message": "Test concurrent request"},
                headers={"Content-Type": "application/json"}
            )

            return response.status_code == 200

    # Make multiple concurrent requests
    tasks = [make_request() for _ in range(5)]
    results = await asyncio.gather(*tasks)

    # Verify all requests succeeded
    assert all(results), f"Not all requests succeeded: {results}"


@pytest.mark.asyncio
async def test_chat_endpoint_user_isolation(client):
    """Test that different users' conversations are properly isolated."""
    test_users = ["user-1", "user-2", "user-3"]

    for user_id in test_users:
        with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
             patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

            # Mock conversation manager
            mock_conv_instance = MagicMock()
            mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
            mock_conv_instance.add_message = AsyncMock()
            mock_conv_manager.return_value = mock_conv_instance

            # Mock agent instance
            mock_agent_instance = MagicMock()
            mock_agent_instance.process_message = AsyncMock(return_value={
                "response": f"Processed for {user_id}",
                "conversation_id": str(uuid4()),
                "tool_calls": [],
                "requires_action": False
            })
            mock_agent_class.return_value = mock_agent_instance

            response = client.post(
                f"/api/{user_id}/chat",
                json={"message": "Test message"},
                headers={"Content-Type": "application/json"}
            )

            assert response.status_code == 200
            data = response.json()
            assert user_id in data["response"]


if __name__ == "__main__":
    pytest.main([__file__])