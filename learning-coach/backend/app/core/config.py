from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Personalized Learning Coach"
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    LLM_PROVIDER: str = "openai"
    DEMO_MODE: bool = True
    SECRET_KEY: str = "learning-coach-secret-2025"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
