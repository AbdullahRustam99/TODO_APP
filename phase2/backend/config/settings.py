from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://username:password@localhost:5432/todo_app")
    db_echo: bool = os.getenv("DB_ECHO", "False").lower() == "true"

    # JWT settings
    jwt_secret: str = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-jwt-signing-key-here")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # Application settings
    app_name: str = "Todo List API"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "allow"
    }

# Create a settings instance
settings = Settings()