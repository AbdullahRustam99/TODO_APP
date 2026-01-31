# phase3/backend/api/v1/routes/events.py

from fastapi import APIRouter, Request, status, Depends, HTTPException # Added HTTPException and status
from fastapi.responses import StreamingResponse # Keep StreamingResponse for type hinting if needed, though EventSourceResponse is used
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
import logging

from services.sse_service import get_sse_queue, remove_sse_queue
from middleware.auth_middleware import get_current_user_id # Corrected import path for get_current_user_id

logger = logging.getLogger(__name__)
router = APIRouter()

async def event_generator(request: Request, user_id: str):
    """
    Asynchronous generator that yields SSE events for a specific user.
    """
    queue = get_sse_queue(user_id)
    try:
        logger.info(f"SSE client connected: {user_id}")
        # Send an initial ping or welcome message
        yield {"event": "connected", "data": "Successfully connected to task events."}

        while True:
            if await request.is_disconnected():
                logger.info(f"SSE client disconnected: {user_id}")
                break
            
            # Wait for a message in the queue
            # Set a timeout to periodically check for disconnect or send keepalives
            try:
                message = await asyncio.wait_for(queue.get(), timeout=15.0) # Timeout to send keepalives
                yield {"event": "task_refresh", "data": message} # Use 'task_refresh' event name
                queue.task_done() # Signal that the task was processed
            except asyncio.TimeoutError:
                yield {"event": "keepalive", "data": "ping"} # Send a keepalive event
            except Exception as e:
                logger.error(f"Error getting message from queue for user {user_id}: {e}", exc_info=True)
                break # Break if there's an issue with the queue

    except asyncio.CancelledError:
        logger.info(f"SSE client connection cancelled for user: {user_id}")
    except Exception as e:
        logger.error(f"Error in SSE event generator for user {user_id}: {e}", exc_info=True)
    finally:
        remove_sse_queue(user_id) # Clean up the queue

@router.get("/events", response_class=StreamingResponse) # Use StreamingResponse for FastAPI to correctly handle the SSE
async def sse_endpoint(request: Request, user_id: str = Depends(get_current_user_id)):
    """
    Endpoint for Server-Sent Events (SSE) to notify clients of task updates.
    Clients can connect to this endpoint to receive real-time notifications.
    """
    # get_current_user_id will ensure the user is authenticated and provide their ID
    # The dependency already handles HTTPException for unauthorized access.
    logger.info(f"User {user_id} requesting SSE connection.")
    return EventSourceResponse(event_generator(request, user_id))