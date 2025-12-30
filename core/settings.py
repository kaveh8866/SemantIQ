from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    """
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    
    # OpenRouter
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    
    # Marber
    MARBER_API_KEY: Optional[str] = None
    MARBER_API_URL: str = "https://api.marber.ai/v1"  # Example default, adjust if needed

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
