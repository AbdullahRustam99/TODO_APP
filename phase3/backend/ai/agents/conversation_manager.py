from typing import List, Dict, Any
from sqlmodel.ext.asyncio.session import AsyncSession
from models.conversation import Conversation, ConversationCreate
from models.message import Message, MessageCreate, MessageRoleEnum
from sqlmodel import select
from uuid import UUID, uuid4
from datetime import datetime


class ConversationManager:
    """
    Manager class for handling conversation-related operations.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_conversation(self, user_id: str) -> Conversation:
        """
        Create a new conversation for the user.
        """
        from datetime import timedelta
        expires_at = datetime.utcnow() + timedelta(days=7)  # 7-day retention as specified

        conversation = Conversation(
            user_id=user_id,  # Keep as string as expected by model
            expires_at=expires_at,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.db_session.add(conversation)
        await self.db_session.commit()
        await self.db_session.refresh(conversation)

        return conversation

    async def get_conversation(self, conversation_id: UUID) -> Conversation:
        """
        Get a specific conversation by ID.
        """
        statement = select(Conversation).where(Conversation.id == conversation_id)
        result = await self.db_session.exec(statement)
        conversation = result.first()
        return conversation

    async def add_message(self, conversation_id: UUID, role: MessageRoleEnum, content: str) -> Message:
        """
        Add a message to a conversation.
        """
        # Get the user_id from the conversation to associate with the message
        conversation = await self.get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")

        message = Message(
            conversation_id=conversation_id,
            user_id=conversation.user_id,
            role=role.value if hasattr(role, 'value') else role,
            content=content,
            created_at=datetime.utcnow()
        )

        self.db_session.add(message)
        await self.db_session.commit()
        await self.db_session.refresh(message)

        return message

    async def update_conversation_timestamp(self, conversation_id: UUID):
        """
        Update the updated_at timestamp for a conversation.
        """
        conversation = await self.get_conversation(conversation_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()
            self.db_session.add(conversation)
            await self.db_session.commit()

    async def get_recent_conversations(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get recent conversations for a user.
        """
        statement = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
        result = await self.db_session.exec(statement)
        conversations = result.all()

        return [
            {
                "id": str(conv.id),
                "user_id": conv.user_id,
                "created_at": conv.created_at.isoformat() if conv.created_at else None,
                "updated_at": conv.updated_at.isoformat() if conv.updated_at else None
            }
            for conv in conversations
        ]

    async def get_conversation_history(self, conversation_id: UUID) -> List[Dict[str, Any]]:
        """
        Get the full history of messages in a conversation.
        """
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
        result = await self.db_session.exec(statement)
        messages = result.all()

        return [
            {
                "id": str(msg.id),
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat() if msg.created_at else None
            }
            for msg in messages
        ]