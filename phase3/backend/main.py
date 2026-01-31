from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from api.v1.routes import tasks, auth, events
from ai.endpoints import chat
from database.session import async_engine
from middleware.auth_middleware import AuthMiddleware
from models import task, user, conversation, message  # Import models to register them with SQLModel
from utils.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
import sqlmodel

app = FastAPI(title="Todo List API", version="1.0.0")

# Add Authentication middleware
app.add_middleware(AuthMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

@app.on_event("startup")
async def startup():
    """Create database tables on startup"""
    async with async_engine.begin() as conn:
        await conn.run_sync(sqlmodel.SQLModel.metadata.create_all)

# Include API routes
app.include_router(tasks.router, prefix="/api/{user_id}", tags=["tasks"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(events.router, prefix="/api", tags=["events"])

@app.get("/")
def read_root():
    return {"message": "Todo List API - Phase II Backend"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
