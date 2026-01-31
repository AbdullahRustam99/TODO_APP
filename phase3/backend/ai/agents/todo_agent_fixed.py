from typing import Dict, Any, List, Optional
from agents import (
    Agent,
    Runner,
    RunConfig,
    OpenAIChatCompletionsModel,
    ModelSettings,
    set_tracing_disabled
)
from agents.mcp import MCPServerStdio
from config.settings import settings
from models.conversation import Conversation
from models.message import MessageRoleEnum
import logging
from openai import AsyncOpenAI
import json
import sys
import subprocess
import os

# Disable tracing as shown in the example
set_tracing_disabled(disabled=True)

logger = logging.getLogger(__name__)


class TodoAgentFixed:
    """
    AI agent that interprets natural language commands for task management.
    Uses OpenAI Agents SDK with Google Gemini API and stdio MCP server for tool integration.
    """

    def __init__(self):
        # Configure the OpenAI client with Google Gemini API
        self.client = AsyncOpenAI(
            api_key=settings.gemini_api_key,
           base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  # Gemini-compatible endpoint
        )

        # Create the model using the OpenAIChatCompletionsModel as shown in the example
        model = OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            openai_client=self.client
        )

        # Create run configuration as shown in the example
        self.config = RunConfig(
            model=model,
            model_provider=self.client,
        )

        # Set up the MCP server connection for tools using stdio subprocess approach
        # This spawns a local subprocess that communicates via stdio with the agent
        self.mcp_server = MCPServerStdio(
            name="Todo Management MCP Server",
            params={
                "command": sys.executable,  # Use the same Python executable
                "args": ["-m", "ai.mcp.server"],  # Use the existing server module
            },
            # Increase timeout for database operations
            client_session_timeout_seconds=30.0
        )

        # Create the agent using the OpenAI Agents SDK and connect it to the MCP server
        self.agent = Agent(
            name="TodoAssistant",
            instructions="""
            You are an AI assistant for a todo management system. Your role is to help users manage their tasks using natural language.
            You can perform the following operations:
            1. Add tasks
            2. List tasks
            3. Complete tasks
            4. Delete tasks
            5. Update tasks

            Always respond in a friendly and helpful manner. When a user asks to perform an action,
            use the appropriate tool to carry out the request. If you don't understand a request,
            ask for clarification.

            Remember to respect user privacy - users can only operate on their own tasks.
            """,
            mcp_servers=[self.mcp_server],
            # Disable parallel tool calls to prevent database lock issues
            model_settings=ModelSettings(parallel_tool_calls=False)
        )

    async def process_message(self, user_id: str, message: str, conversation: Conversation) -> Dict[str, Any]:
        """
        Process a user message and return appropriate response and tool calls.
        """
        try:
            # Run the agent with the user message using the configuration as shown in the example
            # Use the MCP server in a context manager to ensure proper lifecycle
            async with self.mcp_server:
                result = await Runner.run(
                    self.agent,
                    input=f"[USER_ID: {user_id}] {message}",
                    run_config=self.config
                )

            # Process the response
            message_content = result.final_output if result.final_output else "I processed your request."

            # Extract tool calls if any (these would be handled by the agent framework through MCP)
            tool_calls = []
            requires_action = False

            # Format the response
            conversation_id = str(conversation.id) if conversation else "unknown"
            formatted_result = {
                "response": message_content,
                "conversation_id": conversation_id,
                "tool_calls": tool_calls,
                "requires_action": requires_action
            }

            logger.info(f"Processed message for user {user_id}: {formatted_result}")
            return formatted_result

        except Exception as e:
            logger.error(f"Error processing message for user {user_id}: {str(e)}")
            conversation_id = str(conversation.id) if conversation else "unknown"
            return {
                "response": f"I'm sorry, I encountered an error processing your request: {str(e)}",
                "conversation_id": conversation_id,
                "tool_calls": [],
                "requires_action": False
            }