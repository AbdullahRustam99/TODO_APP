from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging
import json
from pydantic import BaseModel

from sqlmodel.ext.asyncio.session import AsyncSession
from models.conversation import Conversation, ConversationCreate
from models.message import Message, MessageCreate, MessageRoleEnum
from database.session import get_session_dep
from sqlmodel import select

router = APIRouter(tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None

logger = logging.getLogger(__name__)


@router.post("/{user_id}/chat")
async def chat_with_ai(
    user_id: str,
    request: ChatRequest,
    db_session: AsyncSession = Depends(get_session_dep)
):
    """
    Send a message to the AI chatbot and receive a response.
    The AI agent will handle tool execution through the MCP server.
    """
    try:
        # Import inside function to avoid Pydantic schema generation issues at startup
        from ai.agents.conversation_manager import ConversationManager
        from ai.agents.todo_agent import TodoAgent

        # Initialize conversation manager
        conversation_manager = ConversationManager(db_session)

        # Get or create conversation
        if request.conversation_id is None:
            conversation = await conversation_manager.create_conversation(user_id)
        else:
            conversation = await conversation_manager.get_conversation(request.conversation_id)
            if not conversation:
                # If conversation doesn't exist, create a new one
                conversation = await conversation_manager.create_conversation(user_id)

        # Add user message to conversation
        await conversation_manager.add_message(
            conversation_id=conversation.id,
            role=MessageRoleEnum.user,
            content=request.message
        )

        # Initialize AI agent
        todo_agent = TodoAgent()

        # Process the message with the AI agent
        # The agent will handle tool execution internally through the MCP server
        result = await todo_agent.process_message(user_id, request.message, conversation)

        # Add AI response to conversation
        await conversation_manager.add_message(
            conversation_id=conversation.id,
            role=MessageRoleEnum.assistant,
            content=result["response"]
        )

        # Update conversation timestamp
        await conversation_manager.update_conversation_timestamp(conversation.id)

        return result

    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@router.get("/{user_id}/conversations")
async def get_user_conversations(
    user_id: str,
    db_session: AsyncSession = Depends(get_session_dep)
):
    """
    Get a list of user's conversations.
    """
    try:
        from ai.agents.conversation_manager import ConversationManager

        conversation_manager = ConversationManager(db_session)
        conversations = await conversation_manager.get_recent_conversations(user_id)
        return conversations
    except Exception as e:
        logger.error(f"Error getting user conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving conversations: {str(e)}")


@router.get("/{user_id}/conversations/{conversation_id}")
async def get_conversation_history(
    user_id: str,
    conversation_id: UUID,
    db_session: AsyncSession = Depends(get_session_dep)
):
    """
    Get the full history of a specific conversation.
    """
    try:
        from ai.agents.conversation_manager import ConversationManager

        conversation_manager = ConversationManager(db_session)
        conversation = await conversation_manager.get_conversation(conversation_id)

        # Verify that the conversation belongs to the user
        if conversation and conversation.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        messages = await conversation_manager.get_conversation_history(conversation_id)
        return {"id": conversation_id, "messages": messages}
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        logger.error(f"Error getting conversation history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation history: {str(e)}")