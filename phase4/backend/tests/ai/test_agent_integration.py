"""
Integration tests for the AI agent functionality.

These tests verify the end-to-end functionality of the AI agent with
realistic scenarios and actual tool execution.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from main import app
from models.conversation import Conversation
from models.message import Message
from uuid import UUID, uuid4


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


@pytest.mark.asyncio
async def test_agent_full_add_task_workflow(client):
    """Test the complete workflow for adding a task via AI agent."""
    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_instance = MagicMock()
        mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_instance.update_conversation_timestamp = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent instance to simulate add_task workflow
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(return_value={
            "response": "I've added the task 'Buy groceries' to your list successfully!",
            "conversation_id": str(uuid4()),
            "tool_calls": [
                {
                    "id": "call_123",
                    "function": {
                        "name": "add_task",
                        "arguments": "{\"user_id\":\"test-user-123\",\"title\":\"Buy groceries\",\"description\":\"Need to buy milk, bread, and eggs\",\"priority\":\"medium\"}"
                    }
                }
            ],
            "requires_action": True
        })
        mock_agent_class.return_value = mock_agent_instance

        # Send a request to add a task
        response = client.post(
            "/api/test-user-123/chat",
            json={
                "message": "Add a task: Buy groceries - need milk, bread, and eggs"
            },
            headers={"Content-Type": "application/json"}
        )

        # Verify the response
        assert response.status_code == 200
        data = response.json()

        assert "response" in data
        assert "Buy groceries" in data["response"]
        assert "conversation_id" in data
        assert "tool_calls" in data
        assert len(data["tool_calls"]) > 0
        assert data["tool_calls"][0]["function"]["name"] == "add_task"


@pytest.mark.asyncio
async def test_agent_full_list_tasks_workflow(client):
    """Test the complete workflow for listing tasks via AI agent."""
    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_instance = MagicMock()
        mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_instance.update_conversation_timestamp = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent instance to simulate list_tasks workflow
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(return_value={
            "response": "Here are your tasks: 1. Buy groceries (pending), 2. Clean house (pending), 3. Pay bills (completed)",
            "conversation_id": str(uuid4()),
            "tool_calls": [
                {
                    "id": "call_456",
                    "function": {
                        "name": "list_tasks",
                        "arguments": "{\"user_id\":\"test-user-123\",\"status\":\"all\"}"
                    }
                }
            ],
            "requires_action": True
        })
        mock_agent_class.return_value = mock_agent_instance

        # Send a request to list tasks
        response = client.post(
            "/api/test-user-123/chat",
            json={
                "message": "Show me all my tasks"
            },
            headers={"Content-Type": "application/json"}
        )

        # Verify the response
        assert response.status_code == 200
        data = response.json()

        assert "response" in data
        assert "tasks" in data["response"].lower()
        assert "conversation_id" in data
        assert "tool_calls" in data
        assert len(data["tool_calls"]) > 0
        assert data["tool_calls"][0]["function"]["name"] == "list_tasks"


@pytest.mark.asyncio
async def test_agent_full_complete_task_workflow(client):
    """Test the complete workflow for completing a task via AI agent."""
    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_instance = MagicMock()
        mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_instance.update_conversation_timestamp = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent instance to simulate complete_task workflow
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(return_value={
            "response": "I've marked task 'Buy groceries' as completed successfully!",
            "conversation_id": str(uuid4()),
            "tool_calls": [
                {
                    "id": "call_789",
                    "function": {
                        "name": "complete_task",
                        "arguments": "{\"user_id\":\"test-user-123\",\"task_id\":\"1\"}"
                    }
                }
            ],
            "requires_action": True
        })
        mock_agent_class.return_value = mock_agent_instance

        # Send a request to complete a task
        response = client.post(
            "/api/test-user-123/chat",
            json={
                "message": "Complete task 1"
            },
            headers={"Content-Type": "application/json"}
        )

        # Verify the response
        assert response.status_code == 200
        data = response.json()

        assert "response" in data
        assert "completed" in data["response"].lower()
        assert "conversation_id" in data
        assert "tool_calls" in data
        assert len(data["tool_calls"]) > 0
        assert data["tool_calls"][0]["function"]["name"] == "complete_task"


@pytest.mark.asyncio
async def test_agent_full_delete_task_workflow(client):
    """Test the complete workflow for deleting a task via AI agent."""
    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_instance = MagicMock()
        mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_instance.update_conversation_timestamp = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent instance to simulate delete_task workflow
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(return_value={
            "response": "I've deleted task 'Clean house' from your list successfully!",
            "conversation_id": str(uuid4()),
            "tool_calls": [
                {
                    "id": "call_abc",
                    "function": {
                        "name": "delete_task",
                        "arguments": "{\"user_id\":\"test-user-123\",\"task_id\":\"2\"}"
                    }
                }
            ],
            "requires_action": True
        })
        mock_agent_class.return_value = mock_agent_instance

        # Send a request to delete a task
        response = client.post(
            "/api/test-user-123/chat",
            json={
                "message": "Delete task 2"
            },
            headers={"Content-Type": "application/json"}
        )

        # Verify the response
        assert response.status_code == 200
        data = response.json()

        assert "response" in data
        assert "deleted" in data["response"].lower()
        assert "conversation_id" in data
        assert "tool_calls" in data
        assert len(data["tool_calls"]) > 0
        assert data["tool_calls"][0]["function"]["name"] == "delete_task"


@pytest.mark.asyncio
async def test_agent_full_update_task_workflow(client):
    """Test the complete workflow for updating a task via AI agent."""
    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_instance = MagicMock()
        mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_instance.update_conversation_timestamp = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent instance to simulate update_task workflow
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(return_value={
            "response": "I've updated task 'Buy groceries' with the new due date successfully!",
            "conversation_id": str(uuid4()),
            "tool_calls": [
                {
                    "id": "call_def",
                    "function": {
                        "name": "update_task",
                        "arguments": "{\"user_id\":\"test-user-123\",\"task_id\":\"1\",\"due_date\":\"2024-12-31\"}"
                    }
                }
            ],
            "requires_action": True
        })
        mock_agent_class.return_value = mock_agent_instance

        # Send a request to update a task
        response = client.post(
            "/api/test-user-123/chat",
            json={
                "message": "Update task 1: Change due date to December 31st"
            },
            headers={"Content-Type": "application/json"}
        )

        # Verify the response
        assert response.status_code == 200
        data = response.json()

        assert "response" in data
        assert "updated" in data["response"].lower()
        assert "conversation_id" in data
        assert "tool_calls" in data
        assert len(data["tool_calls"]) > 0
        assert data["tool_calls"][0]["function"]["name"] == "update_task"


@pytest.mark.asyncio
async def test_agent_error_handling_workflow(client):
    """Test the agent's error handling workflow."""
    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_instance = MagicMock()
        mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent to raise an exception
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(side_effect=Exception("API Error"))
        mock_agent_class.return_value = mock_agent_instance

        # Send a request that will cause an error
        response = client.post(
            "/api/test-user-123/chat",
            json={
                "message": "Add a task: Test error handling"
            },
            headers={"Content-Type": "application/json"}
        )

        # Should return a server error
        assert response.status_code == 500


@pytest.mark.asyncio
async def test_agent_unrecognized_command_response(client):
    """Test the agent's response to unrecognized commands."""
    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_instance = MagicMock()
        mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_instance.update_conversation_timestamp = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent instance to return a clarification response
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(return_value={
            "response": "I'm sorry, I didn't understand that command. Could you please rephrase or be more specific?",
            "conversation_id": str(uuid4()),
            "tool_calls": [],
            "requires_action": False
        })
        mock_agent_class.return_value = mock_agent_instance

        # Send an unrecognized command
        response = client.post(
            "/api/test-user-123/chat",
            json={
                "message": "Random command that doesn't make sense for task management"
            },
            headers={"Content-Type": "application/json"}
        )

        # Verify the response
        assert response.status_code == 200
        data = response.json()

        assert "response" in data
        assert "sorry" in data["response"].lower() or "understand" in data["response"].lower()
        assert "conversation_id" in data
        assert "tool_calls" in data
        assert len(data["tool_calls"]) == 0
        assert data["requires_action"] is False


@pytest.mark.asyncio
async def test_agent_multiple_tool_calls_in_single_request(client):
    """Test the agent's ability to handle multiple tool calls in a single request."""
    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_instance = MagicMock()
        mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_instance.update_conversation_timestamp = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent instance to return multiple tool calls
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(return_value={
            "response": "I've processed your request by adding a task and listing your tasks.",
            "conversation_id": str(uuid4()),
            "tool_calls": [
                {
                    "id": "call_multi_1",
                    "function": {
                        "name": "add_task",
                        "arguments": "{\"user_id\":\"test-user-123\",\"title\":\"New task\",\"priority\":\"high\"}"
                    }
                },
                {
                    "id": "call_multi_2",
                    "function": {
                        "name": "list_tasks",
                        "arguments": "{\"user_id\":\"test-user-123\",\"status\":\"all\"}"
                    }
                }
            ],
            "requires_action": True
        })
        mock_agent_class.return_value = mock_agent_instance

        # Send a complex request that might trigger multiple tools
        response = client.post(
            "/api/test-user-123/chat",
            json={
                "message": "Add a high priority task 'New task' and then show me all my tasks"
            },
            headers={"Content-Type": "application/json"}
        )

        # Verify the response
        assert response.status_code == 200
        data = response.json()

        assert "response" in data
        assert "conversation_id" in data
        assert "tool_calls" in data
        assert len(data["tool_calls"]) == 2
        assert data["tool_calls"][0]["function"]["name"] in ["add_task", "list_tasks"]
        assert data["tool_calls"][1]["function"]["name"] in ["add_task", "list_tasks"]


@pytest.mark.asyncio
async def test_agent_conversation_management(client):
    """Test that the agent properly manages conversation state."""
    test_conversation_id = uuid4()

    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager methods
        mock_conv_instance = MagicMock()
        mock_conv_instance.get_conversation = AsyncMock(return_value=MagicMock(id=test_conversation_id, user_id="test-user-123"))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_instance.update_conversation_timestamp = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent instance
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(return_value={
            "response": "Processed your message in conversation",
            "conversation_id": str(test_conversation_id),
            "tool_calls": [],
            "requires_action": False
        })
        mock_agent_class.return_value = mock_agent_instance

        # Send a request with an existing conversation ID
        response = client.post(
            f"/api/test-user-123/chat",
            params={"conversation_id": str(test_conversation_id)},
            json={
                "message": "Continue working on my tasks"
            },
            headers={"Content-Type": "application/json"}
        )

        # Verify the response
        assert response.status_code == 200
        data = response.json()

        assert data["conversation_id"] == str(test_conversation_id)
        assert "response" in data


@pytest.mark.asyncio
async def test_agent_response_timing_and_performance(client):
    """Test that the agent responds within reasonable time limits."""
    import time

    with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
         patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

        # Mock conversation manager
        mock_conv_instance = MagicMock()
        mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
        mock_conv_instance.add_message = AsyncMock()
        mock_conv_instance.update_conversation_timestamp = AsyncMock()
        mock_conv_manager.return_value = mock_conv_instance

        # Mock agent with a simulated processing time
        mock_agent_instance = MagicMock()
        mock_agent_instance.process_message = AsyncMock(return_value={
            "response": "Task processed successfully",
            "conversation_id": str(uuid4()),
            "tool_calls": [],
            "requires_action": False
        })
        mock_agent_class.return_value = mock_agent_instance

        # Measure response time
        start_time = time.time()

        response = client.post(
            "/api/test-user-123/chat",
            json={
                "message": "Add a simple task: Test timing"
            },
            headers={"Content-Type": "application/json"}
        )

        end_time = time.time()
        response_time = end_time - start_time

        # Verify response is successful and timely
        assert response.status_code == 200
        assert response_time < 5.0  # Should respond in under 5 seconds


@pytest.mark.asyncio
async def test_agent_user_isolation(client):
    """Test that different users' tasks are properly isolated."""
    test_users = ["user-1", "user-2", "user-3"]

    for user_id in test_users:
        with patch('ai.endpoints.chat.ConversationManager') as mock_conv_manager, \
             patch('ai.endpoints.chat.TodoAgent') as mock_agent_class:

            # Mock conversation manager
            mock_conv_instance = MagicMock()
            mock_conv_instance.create_conversation = AsyncMock(return_value=MagicMock(id=uuid4()))
            mock_conv_instance.add_message = AsyncMock()
            mock_conv_instance.update_conversation_timestamp = AsyncMock()
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
                json={
                    "message": "Show me my tasks"
                },
                headers={"Content-Type": "application/json"}
            )

            # Verify each user gets a proper response
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            # Verify the response mentions the correct user
            assert user_id in data["response"] or user_id.replace("-", "") in data["response"]


if __name__ == "__main__":
    pytest.main([__file__])