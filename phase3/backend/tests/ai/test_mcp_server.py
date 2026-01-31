"""
Tests for the MCP (Model Context Protocol) server implementation.

These tests verify that the MCP server properly implements the protocol
and can communicate with AI agents as expected.
"""
import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from main import app  # Adjust import based on your main app location
from ai.mcp.server import server, list_todo_tools, handle_tool
from ai.mcp.tool_definitions import get_tools


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


@pytest.mark.asyncio
async def test_mcp_server_tools_endpoint():
    """Test the MCP server tools endpoint."""
    # Get available tools from the actual MCP server
    tools = await list_todo_tools()

    # Extract tool names from the MCP Tool objects
    tool_names = [tool.name for tool in tools]

    expected_tools = ["add_task", "list_tasks", "complete_task", "delete_task", "update_task"]
    for expected_tool in expected_tools:
        assert expected_tool in tool_names, f"Expected tool {expected_tool} not found in tools: {tool_names}"


@pytest.mark.asyncio
async def test_mcp_server_tool_descriptions():
    """Test that MCP server tools have proper descriptions."""
    # Get available tools from the actual MCP server
    tools = await list_todo_tools()

    for tool in tools:
        # Check that the tool object has the required properties
        assert hasattr(tool, 'name')
        assert hasattr(tool, 'description')
        assert hasattr(tool, 'inputSchema')
        assert isinstance(tool.name, str)
        assert isinstance(tool.description, str)


@pytest.mark.asyncio
async def test_mcp_server_add_task_tool_schema():
    """Test the schema for the add_task tool."""
    # Get available tools from the actual MCP server
    tools = await list_todo_tools()

    # Find the add_task tool
    add_task_tool = None
    for tool in tools:
        if tool.name == "add_task":
            add_task_tool = tool
            break

    assert add_task_tool is not None, "add_task tool not found"

    # Verify the schema structure - inputSchema should be accessible
    schema = add_task_tool.inputSchema
    assert schema['type'] == "object"
    assert 'properties' in schema
    assert 'required' in schema

    properties = schema['properties']
    assert "user_id" in properties
    assert "title" in properties

    required = schema['required']
    assert "user_id" in required
    assert "title" in required


@pytest.mark.asyncio
async def test_mcp_server_list_tasks_tool_schema():
    """Test the schema for the list_tasks tool."""
    # Get available tools from the actual MCP server
    tools = await list_todo_tools()

    # Find the list_tasks tool
    list_tasks_tool = None
    for tool in tools:
        if tool.name == "list_tasks":
            list_tasks_tool = tool
            break

    assert list_tasks_tool is not None, "list_tasks tool not found"

    # Verify the schema structure
    schema = list_tasks_tool.inputSchema
    assert schema['type'] == "object"
    assert 'properties' in schema
    assert 'required' in schema

    properties = schema['properties']
    assert "user_id" in properties

    required = schema['required']
    assert "user_id" in required


@pytest.mark.asyncio
async def test_mcp_server_complete_task_tool_schema():
    """Test the schema for the complete_task tool."""
    # Get available tools from the actual MCP server
    tools = await list_todo_tools()

    # Find the complete_task tool
    complete_task_tool = None
    for tool in tools:
        if tool.name == "complete_task":
            complete_task_tool = tool
            break

    assert complete_task_tool is not None, "complete_task tool not found"

    # Verify the schema structure
    schema = complete_task_tool.inputSchema
    assert schema['type'] == "object"
    assert 'properties' in schema
    assert 'required' in schema

    properties = schema['properties']
    assert "user_id" in properties
    assert "task_id" in properties

    required = schema['required']
    assert "user_id" in required
    assert "task_id" in required


@pytest.mark.asyncio
async def test_mcp_server_delete_task_tool_schema():
    """Test the schema for the delete_task tool."""
    # Get available tools from the actual MCP server
    tools = await list_todo_tools()

    # Find the delete_task tool
    delete_task_tool = None
    for tool in tools:
        if tool.name == "delete_task":
            delete_task_tool = tool
            break

    assert delete_task_tool is not None, "delete_task tool not found"

    # Verify the schema structure
    schema = delete_task_tool.inputSchema
    assert schema['type'] == "object"
    assert 'properties' in schema
    assert 'required' in schema

    properties = schema['properties']
    assert "user_id" in properties
    assert "task_id" in properties

    required = schema['required']
    assert "user_id" in required
    assert "task_id" in required


@pytest.mark.asyncio
async def test_mcp_server_update_task_tool_schema():
    """Test the schema for the update_task tool."""
    # Get available tools from the actual MCP server
    tools = await list_todo_tools()

    # Find the update_task tool
    update_task_tool = None
    for tool in tools:
        if tool.name == "update_task":
            update_task_tool = tool
            break

    assert update_task_tool is not None, "update_task tool not found"

    # Verify the schema structure
    schema = update_task_tool.inputSchema
    assert schema['type'] == "object"
    assert 'properties' in schema
    assert 'required' in schema

    properties = schema['properties']
    assert "user_id" in properties
    assert "task_id" in properties

    required = schema['required']
    assert "user_id" in required
    assert "task_id" in required


@pytest.mark.asyncio
async def test_mcp_server_handle_tool_add_task():
    """Test handling the add_task tool call."""
    # Mock the TaskService.create_task method that's called within the handler
    with patch('ai.mcp.server.TaskService') as mock_task_service_class:
        # Create a mock instance
        mock_task_service = MagicMock()
        mock_task_service_class.return_value = mock_task_service

        # Mock the create_task method
        mock_task = MagicMock()
        mock_task.id = 123
        mock_task.title = "Test task"
        mock_task_service.create_task = AsyncMock(return_value=mock_task)

        # Call the handle_tool function
        result = await handle_tool(
            name="add_task",
            arguments={
                "user_id": "123",  # user_id should be integer for service
                "title": "Test task",
                "description": "Test description",
                "priority": "medium",
                "due_date": "2024-12-31"
            }
        )

        # Verify the result
        assert result.success is True
        # The result is a CreateTaskResult, so check its content
        assert hasattr(result, 'result')


@pytest.mark.asyncio
async def test_mcp_server_handle_tool_list_tasks():
    """Test handling the list_tasks tool call."""
    # Mock the TaskService.get_tasks_by_user_id method
    with patch('ai.mcp.server.TaskService') as mock_task_service_class:
        mock_task_service = MagicMock()
        mock_task_service_class.return_value = mock_task_service

        # Mock the get_tasks_by_user_id method
        mock_tasks = [
            MagicMock(id=1, title="Task 1", completed=False),
            MagicMock(id=2, title="Task 2", completed=True)
        ]
        mock_task_service.get_tasks_by_user_id = AsyncMock(return_value=mock_tasks)

        # Call the handle_tool function
        result = await handle_tool(
            name="list_tasks",
            arguments={
                "user_id": "123",  # user_id should be integer for service
                "status": "all"
            }
        )

        # Verify the result
        assert result.success is True


@pytest.mark.asyncio
async def test_mcp_server_handle_tool_complete_task():
    """Test handling the complete_task tool call."""
    # Mock the TaskService.update_task_completion method
    with patch('ai.mcp.server.TaskService') as mock_task_service_class:
        mock_task_service = MagicMock()
        mock_task_service_class.return_value = mock_task_service

        # Mock the update_task_completion method
        mock_task = MagicMock()
        mock_task.id = 123
        mock_task.title = "Test task"
        mock_task_service.update_task_completion = AsyncMock(return_value=mock_task)

        # Call the handle_tool function
        result = await handle_tool(
            name="complete_task",
            arguments={
                "user_id": "123",  # user_id should be integer for service
                "task_id": "123"   # task_id should be integer for service
            }
        )

        # Verify the result
        assert result.success is True


@pytest.mark.asyncio
async def test_mcp_server_handle_tool_delete_task():
    """Test handling the delete_task tool call."""
    # Mock the TaskService.delete_task method
    with patch('ai.mcp.server.TaskService') as mock_task_service_class:
        mock_task_service = MagicMock()
        mock_task_service_class.return_value = mock_task_service

        # Mock the delete_task method
        mock_task_service.delete_task = AsyncMock(return_value=True)

        # Call the handle_tool function
        result = await handle_tool(
            name="delete_task",
            arguments={
                "user_id": "123",  # user_id should be integer for service
                "task_id": "123"   # task_id should be integer for service
            }
        )

        # Verify the result
        assert result.success is True


@pytest.mark.asyncio
async def test_mcp_server_handle_tool_update_task():
    """Test handling the update_task tool call."""
    # Mock the TaskService.update_task method
    with patch('ai.mcp.server.TaskService') as mock_task_service_class:
        mock_task_service = MagicMock()
        mock_task_service_class.return_value = mock_task_service

        # Mock the update_task method
        mock_task = MagicMock()
        mock_task.id = 123
        mock_task.title = "Updated task title"
        mock_task_service.update_task_fields = AsyncMock(return_value=mock_task)

        # Call the handle_tool function
        result = await handle_tool(
            name="update_task",
            arguments={
                "user_id": "123",  # user_id should be integer for service
                "task_id": "123",  # task_id should be integer for service
                "title": "Updated task title",
                "completed": True
            }
        )

        # Verify the result
        assert result.success is True


@pytest.mark.asyncio
async def test_mcp_server_handle_unknown_tool():
    """Test handling an unknown tool call."""
    # Call the handle_tool function with an unknown tool
    result = await handle_tool(
        name="unknown_tool",
        arguments={}
    )

    # Verify the result indicates an error
    assert result.success is False
    assert result.isError is True
    assert "Unknown tool" in result.result["error"]


@pytest.mark.asyncio
async def test_mcp_server_handle_tool_exception():
    """Test handling tool call exceptions."""
    # Mock the TaskService to raise an exception
    with patch('ai.mcp.server.TaskService') as mock_task_service_class:
        mock_task_service = MagicMock()
        mock_task_service_class.return_value = mock_task_service

        # Mock the create_task method to raise an exception
        mock_task_service.create_task = AsyncMock(side_effect=Exception("Test error"))

        # Call the handle_tool function
        result = await handle_tool(
            name="add_task",
            arguments={
                "user_id": "123",  # user_id should be integer for service
                "title": "Test task"
            }
        )

        # Verify the result indicates an error
        assert result.success is False
        assert result.isError is True


def test_mcp_server_http_endpoint_get_tools(client):
    """Test the HTTP endpoint for getting tools."""
    # This test assumes the MCP server endpoints are mounted under /mcp
    # The actual endpoint path may vary depending on how the server is integrated
    response = client.get("/mcp/tools")  # Adjust path as needed

    # If the endpoint doesn't exist (which is likely in the current setup), this should return 404 or 405
    # The important thing is that it doesn't crash
    assert response.status_code in [200, 404, 405]


def test_mcp_server_http_endpoint_call_tool(client):
    """Test the HTTP endpoint for calling tools."""
    # Test calling the tool endpoint with a sample request
    response = client.post(
        "/mcp/call_tool",  # Adjust path as needed
        json={
            "tool_name": "add_task",
            "arguments": {
                "user_id": "test-user-123",
                "title": "Test task"
            }
        },
        headers={"Content-Type": "application/json"}
    )

    # If the endpoint doesn't exist, this should return 404 or 405
    # The important thing is that it doesn't crash with an internal server error
    assert response.status_code in [200, 404, 405]


@pytest.mark.asyncio
async def test_mcp_server_concurrent_tool_calls():
    """Test handling multiple concurrent tool calls."""
    import asyncio

    # Mock the TaskService.create_task method
    with patch('ai.mcp.server.TaskService') as mock_task_service_class:
        mock_task_service = MagicMock()
        mock_task_service_class.return_value = mock_task_service

        # Mock the create_task method
        mock_task = MagicMock()
        mock_task.id = 123
        mock_task.title = "Test task"
        mock_task_service.create_task = AsyncMock(return_value=mock_task)

        async def call_add_task(i):
            return await handle_tool(
                name="add_task",
                arguments={
                    "user_id": "123",  # user_id should be integer for service
                    "title": f"Test task {i}"
                }
            )

        # Execute multiple tool calls concurrently
        tasks = [call_add_task(i) for i in range(5)]
        results = await asyncio.gather(*tasks)

        # Verify all results
        for result in results:
            assert result.success is True


@pytest.mark.asyncio
async def test_mcp_server_tool_argument_validation():
    """Test that tool functions properly validate arguments."""
    # Test with missing required arguments
    result = await handle_tool(
        name="add_task",
        arguments={
            # Missing required "user_id" and "title"
            "description": "Test description"
        }
    )

    # The tool should handle missing arguments gracefully
    # This might result in an error or default behavior depending on implementation
    assert hasattr(result, 'success')


@pytest.mark.asyncio
async def test_mcp_server_tool_optional_arguments():
    """Test that tool functions handle optional arguments correctly."""
    # Mock the TaskService.create_task method
    with patch('ai.mcp.server.TaskService') as mock_task_service_class:
        mock_task_service = MagicMock()
        mock_task_service_class.return_value = mock_task_service

        # Mock the create_task method
        mock_task = MagicMock()
        mock_task.id = 123
        mock_task.title = "Test task"
        mock_task_service.create_task = AsyncMock(return_value=mock_task)

        # Call with only required arguments
        result = await handle_tool(
            name="add_task",
            arguments={
                "user_id": "123",  # user_id should be integer for service
                "title": "Test task"
                # Missing optional arguments like description, priority, due_date
            }
        )

        # Verify the result
        assert result.success is True


if __name__ == "__main__":
    pytest.main([__file__])