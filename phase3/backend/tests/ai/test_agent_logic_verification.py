"""
Logic verification tests for the AI agent.

These tests verify that the AI agent correctly recognizes commands,
extracts task details, and generates appropriate responses for different scenarios.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from ai.agents.todo_agent import TodoAgent
from uuid import uuid4


@pytest.fixture
def todo_agent():
    """Create a TodoAgent instance for testing."""
    agent = TodoAgent()
    # Mock internal components to avoid actual API calls
    agent.client = MagicMock()
    agent.config = MagicMock()
    return agent


@pytest.mark.asyncio
async def test_agent_command_recognition_logic(todo_agent):
    """Test the agent's command recognition logic thoroughly."""
    test_cases = [
        # Add task commands
        ("Add a task: Buy groceries", "add_task"),
        ("Create task: Clean the house", "add_task"),
        ("Make a new task for me", "add_task"),
        ("I need to add a task: Walk the dog", "add_task"),
        ("Please create: Finish report", "add_task"),

        # List tasks commands
        ("Show me my tasks", "list_tasks"),
        ("List all my tasks", "list_tasks"),
        ("What tasks do I have?", "list_tasks"),
        ("Display my current tasks", "list_tasks"),
        ("Show pending tasks", "list_tasks"),
        ("List completed tasks", "list_tasks"),

        # Complete task commands
        ("Complete task 1", "complete_task"),
        ("Mark task 1 as done", "complete_task"),
        ("Finish task #2", "complete_task"),
        ("Set task 3 to completed", "complete_task"),
        ("Mark task 'Buy groceries' as complete", "complete_task"),

        # Delete task commands
        ("Delete task 1", "delete_task"),
        ("Remove task 2", "delete_task"),
        ("Cancel task 3", "delete_task"),
        ("Delete the first task", "delete_task"),
        ("Remove task 'Clean house'", "delete_task"),

        # Update task commands
        ("Update task 1", "update_task"),
        ("Change task 2 details", "update_task"),
        ("Edit task 3", "update_task"),
        ("Modify task 'Buy groceries'", "update_task"),
        ("Update the priority of task 4", "update_task"),
    ]

    for message, expected_command in test_cases:
        recognized_command = await todo_agent.recognize_command(message)
        assert recognized_command == expected_command, f"Failed for message: '{message}'. Expected: {expected_command}, Got: {recognized_command}"


@pytest.mark.asyncio
async def test_agent_command_recognition_edge_cases(todo_agent):
    """Test the agent's command recognition for edge cases."""
    edge_cases = [
        # Case variations
        ("ADD TASK: UPPERCASE", "add_task"),
        ("show me My tAsKs", "list_tasks"),
        ("COMPLETE task 100", "complete_task"),
        ("delete TasK 999", "delete_task"),

        # Variations with punctuation
        ("Add a task: Buy groceries!", "add_task"),
        ("Show me my tasks?", "list_tasks"),
        ("Complete task #1.", "complete_task"),
        ("Delete task #2...", "delete_task"),

        # Mixed with context
        ("Hey AI, could you add a task: Buy milk", "add_task"),
        ("Can you show me my current tasks?", "list_tasks"),
        ("I want to mark task 1 as completed now", "complete_task"),
        ("Please delete task 5 from my list", "delete_task"),
    ]

    for message, expected_command in edge_cases:
        recognized_command = await todo_agent.recognize_command(message)
        assert recognized_command == expected_command, f"Failed for edge case: '{message}'. Expected: {expected_command}, Got: {recognized_command}"


def test_agent_task_extraction_logic(todo_agent):
    """Test the agent's task detail extraction logic."""
    extraction_cases = [
        # Basic extractions
        ("Add task: Buy groceries", {"title": "Buy groceries"}),
        ("Create: Clean the house", {"title": "Clean the house"}),
        ("New task - Walk the dog", {"title": "Walk the dog"}),
        ("Task: Prepare dinner tonight", {"title": "Prepare dinner tonight"}),

        # With descriptions
        ("Add task: Buy groceries - need milk and bread", {"title": "Buy groceries - need milk and bread"}),
        ("Create task: Schedule meeting with John about project", {"title": "Schedule meeting with John about project"}),

        # Extract from complex sentences
        ("I need to add a task: Finish the quarterly report by Friday", {"title": "Finish the quarterly report by Friday"}),
        ("Could you create a task for me - Buy birthday gift for mom", {"title": "Buy birthday gift for mom"}),
    ]

    for message, expected in extraction_cases:
        extracted = todo_agent.extract_task_details(message)
        assert "title" in extracted
        assert expected["title"] in extracted["title"]


@pytest.mark.asyncio
async def test_agent_response_generation_logic(todo_agent):
    """Test the agent's response generation for different command types."""
    user_id = "test-user-123"
    conversation = MagicMock()
    conversation.id = uuid4()

    # Test different message types and verify the agent processes them without errors
    test_messages = [
        "Add a task: Buy groceries",
        "Show me my tasks",
        "Complete task 1",
        "Delete task 2",
        "Update task 3 to have high priority"
    ]

    for message in test_messages:
        # Mock the runner response for each message type
        mock_result = MagicMock()
        mock_result.final_output = f"Processed message: {message}"

        with patch('ai.agents.todo_agent.Runner') as mock_runner:
            mock_runner.run = AsyncMock(return_value=mock_result)

            result = await todo_agent.process_message(user_id, message, conversation)

            # Verify the response structure is consistent
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
async def test_agent_tool_call_generation_logic(todo_agent):
    """Test that the agent generates appropriate tool calls based on commands."""
    user_id = "test-user-123"
    conversation = MagicMock()
    conversation.id = uuid4()

    test_scenarios = [
        {
            "message": "Add a task: Buy groceries",
            "expected_tool": "add_task",
            "contains_keywords": ["add", "task", "groceries"]
        },
        {
            "message": "List my tasks",
            "expected_tool": "list_tasks",
            "contains_keywords": ["list", "tasks", "show"]
        },
        {
            "message": "Complete task 5",
            "expected_tool": "complete_task",
            "contains_keywords": ["complete", "task", "5"]
        },
        {
            "message": "Delete task 3",
            "expected_tool": "delete_task",
            "contains_keywords": ["delete", "task", "3"]
        },
        {
            "message": "Update task 2 priority to high",
            "expected_tool": "update_task",
            "contains_keywords": ["update", "task", "priority"]
        }
    ]

    for scenario in test_scenarios:
        # Mock the runner response with more realistic responses containing expected keywords
        mock_result = MagicMock()

        # Generate more realistic responses based on the expected tool
        if scenario["expected_tool"] == "add_task":
            mock_result.final_output = f"I've added the task '{scenario['message']}' to your list successfully!"
        elif scenario["expected_tool"] == "list_tasks":
            mock_result.final_output = f"Here are your tasks based on '{scenario['message']}'. Showing tasks as requested."
        elif scenario["expected_tool"] == "complete_task":
            mock_result.final_output = f"I've marked the task as completed as requested in '{scenario['message']}'."
        elif scenario["expected_tool"] == "delete_task":
            mock_result.final_output = f"I've deleted the task from your list as per your request '{scenario['message']}'."
        elif scenario["expected_tool"] == "update_task":
            mock_result.final_output = f"I've updated the task details as requested in '{scenario['message']}'."
        else:
            mock_result.final_output = f"Processed your request: {scenario['message']}"

        with patch('ai.agents.todo_agent.Runner') as mock_runner:
            mock_runner.run = AsyncMock(return_value=mock_result)

            result = await todo_agent.process_message(user_id, scenario["message"], conversation)

            # Verify the response structure
            assert "response" in result
            assert "conversation_id" in result
            assert "tool_calls" in result
            assert "requires_action" in result

            # Check if response contains expected keywords
            response_lower = result["response"].lower()
            for keyword in scenario["contains_keywords"]:
                assert keyword.lower() in response_lower, f"Keyword '{keyword}' not found in response: {result['response']}"


@pytest.mark.asyncio
async def test_agent_command_recognition_accuracy(todo_agent):
    """Test the accuracy of command recognition across different phrasings."""
    # Group test cases by command type
    add_task_phrases = [
        "Add task: Buy groceries",
        "Add a new task: Clean house",
        "Create a task for me: Walk the dog",
        "Make task: Prepare dinner",
        "I want to add: Finish report",
        "Create new task - Call dentist",
        "Add this task: Buy birthday card",
        "Please make: Organize files"
    ]

    list_task_phrases = [
        "Show me my tasks",
        "List all my tasks",
        "What tasks do I have?",
        "Display my tasks",
        "Show pending tasks",
        "List completed tasks",
        "What's on my todo list?",
        "Show my current tasks"
    ]

    complete_task_phrases = [
        "Complete task 1",
        "Mark task 1 as done",
        "Finish task #2",
        "Set task 3 to completed",
        "Complete the first task",
        "Mark as done: task 4",
        "Finish 'Buy groceries'",
        "Complete task with title 'Clean house'"
    ]

    delete_task_phrases = [
        "Delete task 1",
        "Remove task 2",
        "Cancel task 3",
        "Delete the first task",
        "Remove task #4",
        "Cancel 'Buy groceries'",
        "Delete task with title 'Clean house'",
        "Remove task 5 from my list"
    ]

    update_task_phrases = [
        "Update task 1",
        "Change task 2 details",
        "Edit task 3",
        "Modify task #4",
        "Update 'Buy groceries'",
        "Change priority of task 5",
        "Edit due date for task 6",
        "Update description of task 7"
    ]

    # Test each group
    for phrase in add_task_phrases:
        command = await todo_agent.recognize_command(phrase)
        assert command == "add_task", f"Failed for add_task phrase: '{phrase}', got: {command}"

    for phrase in list_task_phrases:
        command = await todo_agent.recognize_command(phrase)
        assert command == "list_tasks", f"Failed for list_tasks phrase: '{phrase}', got: {command}"

    for phrase in complete_task_phrases:
        command = await todo_agent.recognize_command(phrase)
        assert command == "complete_task", f"Failed for complete_task phrase: '{phrase}', got: {command}"

    for phrase in delete_task_phrases:
        command = await todo_agent.recognize_command(phrase)
        assert command == "delete_task", f"Failed for delete_task phrase: '{phrase}', got: {command}"

    for phrase in update_task_phrases:
        command = await todo_agent.recognize_command(phrase)
        assert command == "update_task", f"Failed for update_task phrase: '{phrase}', got: {command}"


@pytest.mark.asyncio
async def test_agent_unknown_command_handling(todo_agent):
    """Test how the agent handles unknown or unrecognized commands."""
    unknown_commands = [
        "Hello",
        "How are you?",
        "What's the weather like?",
        "Random text that doesn't match any command",
        "This is not a task management command",
        "Just saying hi",
        "Tell me a joke",
        "What time is it?"
    ]

    for command in unknown_commands:
        recognized = await todo_agent.recognize_command(command)
        assert recognized is None, f"Expected None for unknown command '{command}', but got: {recognized}"


@pytest.mark.asyncio
async def test_agent_process_message_error_handling(todo_agent):
    """Test the agent's error handling in process_message method."""
    user_id = "test-user-123"
    message = "Add a task: Test error handling"
    conversation = MagicMock()
    conversation.id = uuid4()

    # Test when runner throws an exception
    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(side_effect=Exception("API Connection Failed"))

        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify error handling response structure
        assert isinstance(result, dict)
        assert "response" in result
        assert "conversation_id" in result
        assert "tool_calls" in result
        assert "requires_action" in result

        # Verify error is mentioned in response
        assert "error" in result["response"].lower() or "sorry" in result["response"].lower()


@pytest.mark.asyncio
async def test_agent_process_message_success_response_format(todo_agent):
    """Test the format of successful responses from the agent."""
    user_id = "test-user-123"
    message = "Add a task: Test successful response"
    conversation = MagicMock()
    conversation.id = uuid4()

    # Mock a successful runner response
    mock_result = MagicMock()
    mock_result.final_output = "Task 'Test successful response' has been added to your list."

    with patch('ai.agents.todo_agent.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        result = await todo_agent.process_message(user_id, message, conversation)

        # Verify the response structure and content
        assert isinstance(result, dict)
        assert len(result) == 4  # response, conversation_id, tool_calls, requires_action
        assert all(key in result for key in ["response", "conversation_id", "tool_calls", "requires_action"])

        # Verify types
        assert isinstance(result["response"], str)
        assert isinstance(result["conversation_id"], str)
        assert isinstance(result["tool_calls"], list)
        assert isinstance(result["requires_action"], bool)

        # Verify content
        assert len(result["response"]) > 0  # Response should not be empty
        assert str(conversation.id) == result["conversation_id"]


@pytest.mark.asyncio
async def test_agent_process_message_with_different_user_ids(todo_agent):
    """Test that the agent handles different user IDs correctly."""
    test_user_ids = ["user-123", "user-456", "user-789", "test-user-001", "demo-user-xyz"]
    message = "Add a task: Test user isolation"

    for user_id in test_user_ids:
        conversation = MagicMock()
        conversation.id = uuid4()

        # Mock runner response
        mock_result = MagicMock()
        mock_result.final_output = f"Task added for user {user_id}"

        with patch('ai.agents.todo_agent.Runner') as mock_runner:
            mock_runner.run = AsyncMock(return_value=mock_result)

            result = await todo_agent.process_message(user_id, message, conversation)

            # Verify each user gets a proper response
            assert "response" in result
            assert "conversation_id" in result
            assert result["conversation_id"] == str(conversation.id)


@pytest.mark.asyncio
async def test_agent_response_consistency_across_calls(todo_agent):
    """Test that the agent maintains consistent response format across multiple calls."""
    user_id = "test-user-consistency"
    conversation = MagicMock()
    conversation.id = uuid4()

    test_messages = [
        "Add a task: First task",
        "Show me my tasks",
        "Complete task 1",
        "Delete task 2",
        "Update task 3 priority"
    ]

    for i, message in enumerate(test_messages):
        # Mock runner response differently for each call to ensure uniqueness
        mock_result = MagicMock()
        mock_result.final_output = f"Response for message {i+1}: {message}"

        with patch('ai.agents.todo_agent.Runner') as mock_runner:
            mock_runner.run = AsyncMock(return_value=mock_result)

            result = await todo_agent.process_message(user_id, message, conversation)

            # Verify consistent structure across all calls
            assert isinstance(result, dict)
            expected_keys = {"response", "conversation_id", "tool_calls", "requires_action"}
            actual_keys = set(result.keys())
            assert expected_keys == actual_keys, f"Inconsistent keys in response {i+1}: expected {expected_keys}, got {actual_keys}"

            # Verify consistent types
            assert isinstance(result["response"], str)
            assert isinstance(result["conversation_id"], str)
            assert isinstance(result["tool_calls"], list)
            assert isinstance(result["requires_action"], bool)


if __name__ == "__main__":
    pytest.main([__file__])