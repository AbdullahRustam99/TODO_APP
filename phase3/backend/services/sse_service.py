# phase3/backend/services/sse_service.py

from asyncio import Queue
from typing import Dict

# In-memory store for SSE queues.
# The key will be a user identifier (e.g., user_id as a string)
# The value will be the asyncio.Queue for that user.
# In a multi-worker setup, this would need to be replaced with
# a more robust solution like Redis Pub/Sub.
sse_connections: Dict[str, Queue] = {}

async def notify_clients(user_id: str, message: str):
    """
    Sends a message to a specific user's SSE queue if they are connected.
    """
    user_id_str = str(user_id) # Ensure user_id is a string
    if user_id_str in sse_connections:
        await sse_connections[user_id_str].put(message)

def get_sse_queue(user_id: str) -> Queue:
    """
    Retrieves the SSE queue for a user, creating it if it doesn't exist.
    """
    user_id_str = str(user_id)
    if user_id_str not in sse_connections:
        sse_connections[user_id_str] = Queue()
    return sse_connections[user_id_str]

def remove_sse_queue(user_id: str):
    """
    Removes the SSE queue for a user when they disconnect.
    """
    user_id_str = str(user_id)
    if user_id_str in sse_connections:
        del sse_connections[user_id_str]