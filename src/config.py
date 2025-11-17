"""
Configuration module for Sacramento Events Finder.
Handles API keys, constants, and application settings.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for application settings."""
    
    # OpenAI API Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-5"  # Model for Responses API with web search
    
    # Application Constants
    MAX_EVENTS: int = 10
    TIMEOUT_SECONDS: int = 120
    MAX_RETRIES: int = 3
    
    # Location Settings
    CITY: str = "Sacramento"
    STATE: str = "California"
    TIMEZONE: str = "America/Los_Angeles"
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that required configuration is present.
        
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")
        
        if not cls.OPENAI_API_KEY.startswith("sk-"):
            raise ValueError("OPENAI_API_KEY appears to be invalid")
        
        return True
    
    @classmethod
    def get_api_key(cls) -> str:
        """
        Get the OpenAI API key.
        
        Returns:
            str: The API key
        """
        return cls.OPENAI_API_KEY


# Validate configuration on import
Config.validate()