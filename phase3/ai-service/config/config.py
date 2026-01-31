import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the directory of the current file
config_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the .env file
env_file_path = os.path.join(config_dir, '..', '.env')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file_path, extra='ignore')

    GEMINI_API_KEY: str
    BUSINESS_SERVICE_URL: str = "https://abdullahcoder54-todo-app.hf.space"
    CONVERSATION_RETENTION_DAYS: int = 7
    BETTER_AUTH_SECRET: str

settings = Settings()
