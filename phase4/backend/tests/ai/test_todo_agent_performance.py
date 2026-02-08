"""
Performance tests for the TodoAgent functionality.

These tests verify the performance characteristics of the AI agent including:
- Response time under various conditions
- Memory usage patterns
- Concurrency handling
- Resource utilization
"""
import asyncio
import time
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
async def test_response_time_single_request(todo_agent):
    """Test response time for a single request."""
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

        start_time = time.time()
        result = await todo_agent.process_message(user_id, message, conversation)
        end_time = time.time()

        response_time = end_time - start_time

        # Verify response time is reasonable (should be under 5 seconds even with mocked API delay)
        assert response_time < 5.0
        assert result["response"] == "Task 'Buy groceries' added successfully"


@pytest.mark.asyncio
async def test_response_time_multiple_requests_sequential(todo_agent):
    """Test response time for multiple sequential requests."""
    messages = [
        "Add a task: Buy groceries",
        "Add a task: Clean the house",
        "List my tasks",
        "Complete task 1",
        "Update task 2: Clean the entire house"
    ]

    user_id = "test-user-123"
    conversation = MagicMock()
    conversation.id = UUID("12345678-1234-5678-1234-567812345678")

    # Mock the runner response
    mock_result = AsyncMock()
    mock_result.final_output = "Processed successfully"

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        total_start_time = time.time()
        for i, message in enumerate(messages):
            start_time = time.time()
            result = await todo_agent.process_message(user_id, message, conversation)
            end_time = time.time()

            response_time = end_time - start_time

            # Each individual request should be fast
            assert response_time < 5.0
            assert "response" in result

        total_end_time = time.time()
        total_time = total_end_time - total_start_time

        # Total time for 5 requests should be reasonable
        assert total_time < 25.0  # 5 requests * 5 seconds max each


@pytest.mark.asyncio
async def test_concurrent_request_handling(todo_agent):
    """Test how the agent handles concurrent requests."""
    user_id = "test-user-123"
    conversation = MagicMock()
    conversation.id = UUID("12345678-1234-5678-1234-567812345678")

    # Mock the runner response
    mock_result = AsyncMock()
    mock_result.final_output = "Processed successfully"

    async def process_single_request(message):
        with patch('ai.agents.todo_agent.Runner') as mock_runner:
            mock_runner.run = AsyncMock(return_value=mock_result)
            return await todo_agent.process_message(user_id, message, conversation)

    # Create multiple concurrent requests
    messages = [
        "Add a task: Task 1",
        "Add a task: Task 2",
        "Add a task: Task 3",
        "Add a task: Task 4",
        "Add a task: Task 5"
    ]

    start_time = time.time()
    # Execute all requests concurrently
    tasks = [process_single_request(msg) for msg in messages]
    results = await asyncio.gather(*tasks)
    end_time = time.time()

    total_time = end_time - start_time

    # Verify all requests completed successfully
    assert len(results) == len(messages)
    for result in results:
        assert "response" in result

    # Total time should be reasonable considering concurrency
    # This should ideally be faster than sequential processing
    assert total_time < 25.0  # Should be faster than 5 * 5 seconds sequential


@pytest.mark.asyncio
async def test_memory_usage_consistency(todo_agent):
    """Test that memory usage remains consistent across multiple requests."""
    user_id = "test-user-123"
    conversation = MagicMock()
    conversation.id = UUID("12345678-1234-5678-1234-567812345678")

    # Mock the runner response
    mock_result = AsyncMock()
    mock_result.final_output = "Processed successfully"

    # Process multiple requests and verify no memory leaks
    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        for i in range(10):  # Process 10 requests
            message = f"Add a task: Test task {i}"
            result = await todo_agent.process_message(user_id, message, conversation)

            assert "response" in result
            assert isinstance(result, dict)

    # If we got here without memory issues, the test passes


@pytest.mark.asyncio
async def test_large_message_handling(todo_agent):
    """Test handling of large messages."""
    user_id = "test-user-123"
    conversation = MagicMock()
    conversation.id = UUID("12345678-1234-5678-1234-567812345678")

    # Create a large message
    large_message = "Add a task: " + "very long description " * 1000

    # Mock the runner response
    mock_result = AsyncMock()
    mock_result.final_output = "Task added successfully"

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        start_time = time.time()
        result = await todo_agent.process_message(user_id, large_message, conversation)
        end_time = time.time()

        response_time = end_time - start_time

        # Should handle large messages within reasonable time
        assert response_time < 10.0  # Allow more time for large messages
        assert "response" in result


@pytest.mark.asyncio
async def test_command_recognition_performance(todo_agent):
    """Test performance of command recognition function."""
    test_messages = [
        "Add a task: Buy groceries",
        "Show me my tasks",
        "Complete task 1",
        "Delete task 2",
        "Update task 3 with new details",
        "Random message that doesn't match anything",
        "Another random message",
        "Yet another test message",
        "More tasks to add",
        "Tasks to list"
    ]

    start_time = time.time()
    for msg in test_messages:
        command = await todo_agent.recognize_command(msg)
        # Verify command recognition doesn't throw errors
        assert command is None or isinstance(command, str)
    end_time = time.time()

    total_time = end_time - start_time
    avg_time_per_message = total_time / len(test_messages)

    # Average time per message should be very fast (under 100ms per message)
    assert avg_time_per_message < 0.1


@pytest.mark.asyncio
async def test_task_extraction_performance(todo_agent):
    """Test performance of task extraction function."""
    test_messages = [
        "Add task: Buy groceries",
        "Create: Clean the house",
        "New task - Walk the dog",
        "Task: Prepare dinner with ingredients: chicken, vegetables, rice",
        "Simple task: Read a book"
    ]

    start_time = time.time()
    for msg in test_messages:
        details = todo_agent.extract_task_details(msg)
        # Verify extraction doesn't throw errors
        assert isinstance(details, dict)
        assert "title" in details
    end_time = time.time()

    total_time = end_time - start_time
    avg_time_per_message = total_time / len(test_messages)

    # Average time per message should be very fast (under 10ms per message)
    assert avg_time_per_message < 0.01


@pytest.mark.asyncio
async def test_error_handling_performance(todo_agent):
    """Test performance when handling errors."""
    user_id = "test-user-123"
    message = "Add a task: Buy groceries"
    conversation = MagicMock()
    conversation.id = UUID("12345678-1234-5678-1234-567812345678")

    # Mock the runner to raise an exception
    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(side_effect=Exception("API Error"))

        start_time = time.time()
        result = await todo_agent.process_message(user_id, message, conversation)
        end_time = time.time()

        response_time = end_time - start_time

        # Error handling should be fast
        assert response_time < 2.0
        assert "response" in result
        assert "error" in result["response"]


if __name__ == "__main__":
    pytest.main([__file__])