"""FastAPI entrypoint for the ChatKit backend with TodoAgent."""

from __future__ import annotations
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, StreamingResponse
from typing import Optional, Dict, Any
import logging
from contextlib import asynccontextmanager
from uuid import uuid4

from chatkit.server import ChatKitServer, StreamingResult
from chatkit.store import Store, Page
from chatkit.types import ThreadMetadata, UserMessageItem, ThreadItem, AssistantMessageItem, ThreadItemAddedEvent, ErrorEvent
import json
from todo_agent import TodoAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MemoryStore(Store):
    """In-memory implementation of ChatKit Store for development."""

    def __init__(self):
        self.threads: Dict[str, ThreadMetadata] = {}
        self.items: Dict[str, Dict[str, Any]] = {}
        self.attachments: Dict[str, Any] = {}

    async def load_threads(self, *, context: Dict[str, Any] | None = None, **kwargs) -> Page:
        """Load all threads for a user, extracting user_id from context."""
        user_id = context.get("user_id") if context else None
        if not user_id:
            # If no user_id is found, return an empty page.
            return Page(data=[], has_more=False)
            
        threads = [t for t in self.threads.values() if t.user and t.user.id == user_id]
        return Page(data=threads, has_more=False)

    async def load_thread(self, thread_id: str, *args, context: Dict[str, Any] | None = None, **kwargs) -> ThreadMetadata | None:
        """Load a single thread, create if doesn't exist."""
        thread = self.threads.get(thread_id)
        if thread is None:
            # Create a new thread if it doesn't exist to prevent NoneType errors downstream.
            user_id = context.get("user_id", "unknown") if context else "unknown"
            thread = ThreadMetadata(
                id=thread_id,
                user_id=user_id,
                created_at=0,  # Using a simple timestamp
                updated_at=0,
            )
            self.threads[thread_id] = thread
        return thread

    async def save_thread(self, thread: ThreadMetadata, *args, context: Dict[str, Any] | None = None, **kwargs) -> None:
        """Save a thread."""
        self.threads[thread.id] = thread

    async def delete_thread(self, thread_id: str, *args, context: Dict[str, Any] | None = None, **kwargs) -> None:
        """Delete a thread."""
        self.threads.pop(thread_id, None)
        self.items.pop(thread_id, None)

    async def load_thread_items(self, thread_id: str, *args, context: Dict[str, Any] | None = None, **kwargs) -> Page:
        """Load all items for a thread."""
        items = list(self.items.get(thread_id, {}).values())
        return Page(data=items, has_more=False)

    async def load_item(self, thread_id: str, item_id: str, *args, context: Dict[str, Any] | None = None, **kwargs) -> ThreadItem | None:
        """Load a single item."""
        return self.items.get(thread_id, {}).get(item_id)

    async def save_item(self, thread_id: str, item: ThreadItem, *args, context: Dict[str, Any] | None = None, **kwargs) -> None:
        """Save an item."""
        if thread_id not in self.items:
            self.items[thread_id] = {}
        self.items[thread_id][item.id] = item

    async def add_thread_item(self, thread_id: str, item: ThreadItem, *args, context: Dict[str, Any] | None = None, **kwargs) -> None:
        """Add an item to a thread."""
        await self.save_item(thread_id, item, context=context)

    async def delete_thread_item(self, thread_id: str, item_id: str, *args, context: Dict[str, Any] | None = None, **kwargs) -> None:
        """Delete an item from a thread."""
        if thread_id in self.items:
            self.items[thread_id].pop(item_id, None)

    async def save_attachment(self, attachment: Any, *args, context: Dict[str, Any] | None = None, **kwargs) -> None:
        """Save an attachment."""
        self.attachments[attachment.id] = attachment

    async def load_attachment(self, attachment_id: str, *args, context: Dict[str, Any] | None = None, **kwargs) -> Any | None:
        """Load an attachment."""
        return self.attachments.get(attachment_id)

    async def delete_attachment(self, attachment_id: str, *args, context: Dict[str, Any] | None = None, **kwargs) -> None:
        """Delete an attachment."""
        self.attachments.pop(attachment_id, None)


# Global instances
todo_agent: Optional[TodoAgent] = None
chatkit_server: Optional[ChatKitServer] = None


class TodoChatKitServer(ChatKitServer):
    """ChatKit server that wraps the TodoAgent."""

    def __init__(self, todo_agent: TodoAgent):
        self.todo_agent = todo_agent
        super().__init__(MemoryStore())

    async def respond(self, thread: ThreadMetadata, input_user_message: UserMessageItem | None, context: Dict[str, Any]):
        """Implement the abstract respond method to handle user messages."""
        try:
            user_id = context.get("user_id", "unknown")
            
            # Get the message content
            message_content = ""
            if input_user_message and hasattr(input_user_message, 'content'):
                message_content = input_user_message.content
            
            logger.info(f"Processing message from user {user_id}: {message_content}")
            
            # Use TodoAgent to generate response
            response = await self.todo_agent.process_message(user_id, message_content)
            
            # Create an AssistantMessageItem for the response, ensuring all fields are correctly formatted.
            assistant_item = AssistantMessageItem(
                id=f"msg_{uuid4()}",
                thread_id=thread.id,  # Pass the thread_id
                created_at=0,  # Pass a timestamp
                content=[{"type": "output_text", "text": response}],  # Format content as a list of blocks
            )
            
            # Yield ThreadItemAddedEvent to add the assistant message to the thread
            yield ThreadItemAddedEvent(
                type="thread.item.added",
                thread_id=thread.id,
                item=assistant_item
            )
            
        except Exception as e:
            logger.error(f"Error in respond(): {e}", exc_info=True)
            yield ErrorEvent(
                type="error",
                error=str(e)
            )

    async def process(self, payload: bytes | str, context: Dict[str, Any]) -> StreamingResult | dict | str:
        """Process ChatKit events using TodoAgent."""
        try:
            # Parse the incoming payload
            if isinstance(payload, bytes):
                body = json.loads(payload.decode('utf-8'))
            else:
                body = json.loads(payload)

            logger.info(f"Processing ChatKit event: {body.get('type')}")

            # Extract user_id from context or payload
            user_id = str(context.get("user_id", body.get("user", {}).get("id", "unknown")))

            # Call the parent process method which handles ChatKit protocol
            result = await super().process(payload, context)

            return result

        except Exception as e:
            logger.error(f"Error in ChatKitServer.process(): {e}", exc_info=True)
            return {"type": "error", "content": str(e)}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize agents on startup, cleanup on shutdown."""
    global todo_agent, chatkit_server

    logger.info("Initializing TodoAgent...")
    todo_agent = TodoAgent()
    logger.info("TodoAgent initialized")

    logger.info("Initializing ChatKit Server...")
    chatkit_server = TodoChatKitServer(todo_agent)
    logger.info("ChatKit Server initialized")

    yield

    logger.info("Shutting down...")
    todo_agent = None
    chatkit_server = None


app = FastAPI(
    title="ChatKit Backend with TodoAgent",
    description="ChatKit backend powered by TodoAgent",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chatkit")
async def chatkit_endpoint(request: Request) -> Response:
    """Proxy the ChatKit web component payload to the server implementation."""
    global chatkit_server

    if chatkit_server is None:
        logger.error("ChatKit server not initialized")
        return JSONResponse({"error": "Server not initialized"}, status_code=500)

    try:
        payload = await request.body()
        
        # Extract user_id from the request if available
        context = {"request": request}
        try:
            import json
            body = json.loads(payload.decode('utf-8'))
            if "user" in body and "id" in body["user"]:
                context["user_id"] = str(body["user"]["id"])
        except Exception as e:
            logger.debug(f"Could not extract user_id from payload: {e}")

        result = await chatkit_server.process(payload, context)

        if isinstance(result, StreamingResult):
            return StreamingResponse(result, media_type="text/event-stream")
        if hasattr(result, "json"):
            return Response(content=result.json, media_type="application/json")
        return JSONResponse(result)

    except Exception as e:
        logger.error(f"Error in chatkit_endpoint: {e}", exc_info=True)
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "chatkit-todo-assistant",
        "initialized": chatkit_server is not None
    }


@app.post("/chatkit/api")
async def chatkit_api_endpoint(request: Request) -> Response:
    """Alias for /chatkit endpoint for compatibility."""
    return await chatkit_endpoint(request)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)