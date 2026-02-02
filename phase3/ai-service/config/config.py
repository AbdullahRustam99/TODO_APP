import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl
from typing import ClassVar
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SERVICE_SECRET = "abfe95adc6a3d85f1d8533a0fbf151b18240d817b471dda39a925555d886549c32c667dbeb184b9e9c73da3227c0dae5f83a"
    BUSINESS_SERVICE_URL: HttpUrl = "https://abdullahcoder54-todo-app.hf.space"
    CONVERSATION_RETENTION_DAYS: int = 7

    def model_post_init(self, __context):
        if not self.GEMINI_API_KEY:
            self.GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
        if not self.BETTER_AUTH_SECRET:
            self.BETTER_AUTH_SECRET = os.environ.get("BETTER_AUTH_SECRET")

        if not self.GEMINI_API_KEY or not self.BETTER_AUTH_SECRET:
            raise RuntimeError(
                "Critical env vars missing in MCP subprocess"
            )


settings = Settings()
