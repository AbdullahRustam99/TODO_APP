from typing import Dict, Any, List, Optional
from agents import (
    Agent,
    Runner,
    RunConfig,
    OpenAIChatCompletionsModel,
    ModelSettings,
    set_tracing_disabled,
    enable_verbose_stdout_logging,
    InputGuardrailTripwireTriggered # Import the exception
)
from agents.mcp import MCPServerStdio
from guardrails import is_task_related # Import the guardrail function
import logging
from openai import AsyncOpenAI
import json
import sys
import os
from config.config import settings

set_tracing_disabled(disabled=True)
enable_verbose_stdout_logging()
logger = logging.getLogger(__name__)

class TodoAgent:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.GEMINI_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )
        model = OpenAIChatCompletionsModel(
            model="z-ai/glm-4.5-air:free",
            openai_client=self.client
        )
        self.config = RunConfig(model=model, model_provider=self.client)
        self.mcp_server = MCPServerStdio(
            name="Todo Management MCP Server",
            params={"command": sys.executable, "args": ["-m", "ai_mcp_server"]},            
        )
        self.agent = Agent(
            name="TodoAssistant",
            instructions="""

You are a Todo Management Assistant.

YOUR RESPONSIBILITIES:
- Add tasks when the user asks to create a todo.
- List tasks when the user asks to see todos.
- Update tasks when the user asks to modify a todo.
- Delete tasks when the user asks to remove a todo.
- Answer questions about existing tasks clearly.
 
YOUR TOOLS:
1. ADD_TASK - Adds a new task to the todo list.

2. LIST_TASKS - Lists all current tasks in the todo list.

3. UPDATE_TASK - Updates an existing task.

4. DELETE_TASK - Deletes a task from the todo list.

5. GET_TASK - Retrieves details of a specific task.

CRITICAL EXECUTION RULES:

- When a tool call succeeds, STOP immediately.
- Do NOT repeat or retry the same tool call.
- Do NOT perform multiple actions for a single request.
- Your job ends after the correct tool is called and a brief confirmation is returned.


TASK HANDLING RULES:
1. A task consists of a clear title and optional details.
2. Never create duplicate tasks with the same title.
3. If a task already exists, inform the user instead of adding it again.
4. When listing tasks, show them in a clear and readable format.
5. When a task is added, updated, or deleted, confirm the action briefly.
6. If the request is unclear, ask a short clarification question.
7. Perform only the action the user requested — no extra actions.

GENERAL BEHAVIOR:
- Be concise and practical.
- Do not invent tasks.
- Do not repeat actions.
- Always reflect the current state of the todo list.

Your goal is to keep the user's todo list accurate and easy to manage.
""",
            mcp_servers=[self.mcp_server],
            model_settings=ModelSettings(parallel_tool_calls=False),
            input_guardrails=[is_task_related] # Add the input guardrail here
        )

    async def process_message(self, user_id: str, message: str) -> str:
        """
        Processes a user message and returns only the final string response,
        as required by the simple, non-streaming backend template.
        """
        await self.mcp_server.connect()
        
        try:
            result = await Runner.run(
                self.agent,
                input=f"[USER_ID: {user_id}] {message}",
                run_config=self.config,

            )
            final_response = result.final_output if result.final_output else "I was able to process your request."

        except InputGuardrailTripwireTriggered as e:
            logger.warning(f"Input guardrail tripped for user {user_id}. Message: '{message}'")
            final_response = e.guardrail_result.output.output_info
        
        logger.info(f"Agent for user {user_id} produced final response: {final_response}")
        return  final_response