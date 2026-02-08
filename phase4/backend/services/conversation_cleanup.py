"""
Service for managing conversation cleanup jobs.
This service handles the periodic cleanup of expired conversations.
"""
import asyncio
from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from ..models.conversation import Conversation
from ..database.session import get_async_session
import logging


logger = logging.getLogger(__name__)


class ConversationCleanupService:
    """
    Service class for handling conversation cleanup operations.
    """

    @staticmethod
    async def cleanup_expired_conversations():
        """
        Remove conversations that have expired (older than 7 days).
        """
        try:
            async with get_async_session() as session:
                # Find conversations that have expired
                cutoff_time = datetime.utcnow()
                statement = select(Conversation).where(Conversation.expires_at < cutoff_time)

                result = await session.exec(statement)
                expired_conversations = result.all()

                logger.info(f"Found {len(expired_conversations)} expired conversations to clean up")

                for conversation in expired_conversations:
                    # Delete associated messages first due to foreign key constraint
                    from models.message import Message
                    message_statement = select(Message).where(Message.conversation_id == conversation.id)
                    message_result = await session.exec(message_statement)
                    messages = message_result.all()

                    for message in messages:
                        await session.delete(message)

                    # Delete the conversation
                    await session.delete(conversation)

                # Commit all changes
                await session.commit()

                logger.info(f"Successfully cleaned up {len(expired_conversations)} expired conversations")

        except Exception as e:
            logger.error(f"Error during conversation cleanup: {str(e)}")
            # Don't raise the exception as this is a background task

    @staticmethod
    async def start_cleanup_scheduler(interval_minutes: int = 60):
        """
        Start the background cleanup scheduler.

        Args:
            interval_minutes: How often to run the cleanup in minutes (default: 60)
        """
        while True:
            try:
                await ConversationCleanupService.cleanup_expired_conversations()
                await asyncio.sleep(interval_minutes * 60)  # Convert minutes to seconds
            except Exception as e:
                logger.error(f"Error in cleanup scheduler: {str(e)}")
                # Wait a shorter time before retrying if there's an error
                await asyncio.sleep(5 * 60)  # Wait 5 minutes before retrying