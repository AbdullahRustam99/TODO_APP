"""Guardrails for the TodoAgent."""

from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    input_guardrail,
    output_guardrail,
    GuardrailFunctionOutput,
    RunContextWrapper, # Needed for guardrail function signature
    Runner, # Needed to run topic_checker_agent
    TResponseInputItem # Correct type for input content in guardrail functions
)
from config.config import settings
from openai import AsyncOpenAI
import logging
from typing import Any # Needed for RunContextWrapper[Any]
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class todo(BaseModel): 
    reasoning: str
    is_not_todo: bool
    user_friendly_response: str

# A simple, low-cost model to act as a topic checker.
guardrail_client = AsyncOpenAI(
    api_key=settings.GEMINI_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)
guardrail_model = OpenAIChatCompletionsModel(
    model="arcee-ai/trinity-large-preview:free", # Using a common model for topic checking
    openai_client=guardrail_client
)

# This is the "topic checker" agent.
guardrail_agent = Agent(
    name="TopicChecker",
    model=guardrail_model,
    output_type=todo,
    instructions="""
Your job is to check whether the user's message is related to managing a to-do list.

If the message IS related to task management:
- Adding a task
- Deleting a task
- Updating a task
- Listing tasks
- Completing tasks
- Asking about existing tasks
- Any clear todo/task management request


If the message is NOT related to task management
(e.g., math questions, weather, casual conversation, general knowledge):
- Respond politely and briefly.
- Explain that you can help only with managing tasks.
- Guide the user to ask a task-related question.

Your response MUST be friendly, clear, and short.

Example response for non-task queries:
"I’m here to help with your to-do list. You can ask me to add, remove, update, or list your tasks."

"""
)

@input_guardrail(name="TodoInputGuardrail")
async def is_task_related(
    ctx: RunContextWrapper[Any], # Context provided by Runner
    agent: Agent, # The agent running this guardrail
    user_input: str | list[TResponseInputItem] # The user's input
) -> GuardrailFunctionOutput:
    """
    Input guardrail to check if the user's query is related to task management.
    """
    try:

        logger.info(f"Checking topic for query: '{user_input}'")

        # Run the topic checker agent. Pass the input directly, and context for traceability.
        result = await Runner.run(guardrail_agent, input=user_input, context=ctx.context)
        logger.info(f"Topic checker result: is_todo={result.final_output.is_not_todo}, reasoning='{result.final_output.reasoning}'")
        return GuardrailFunctionOutput(
            output_info=result.final_output.user_friendly_response, 
            tripwire_triggered=result.final_output.is_not_todo,
        )

    except Exception as e:
        logger.error(f"Error in input guardrail: {e}")
        return GuardrailFunctionOutput(
            tripwire_triggered=False,
            output_info="An error occurred while checking your query.",
        )

@output_guardrail(name="TodoOutputGuardrail")
async def is_response_appropriate(
    ctx: RunContextWrapper[Any], # Context provided by Runner
    agent: Agent, # The agent running this guardrail
    response_content: str | list[TResponseInputItem] # The agent's output
) -> GuardrailFunctionOutput:
    """
    Output guardrail to check if the agent's response is appropriate.
    (Placeholder - currently allows all responses.)
    """
    # In a real implementation, you might check for profanity, sensitive data, etc.
    return GuardrailFunctionOutput(
        tripwire_triggered=False,
        output_info=None,
    )