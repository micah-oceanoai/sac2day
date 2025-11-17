"""
OpenAI client module for Sacramento Events Finder.
Handles communication with OpenAI Responses API using proper SDK.
"""

import time
from typing import Optional
from openai import OpenAI
from src.config import Config
from src.prompt_builder import PromptBuilder
from src.event_urls import EventURLs


class OpenAIClient:
    """Client for interacting with OpenAI Responses API."""
    
    def __init__(self):
        """Initialize the OpenAI client."""
        self.client = OpenAI(api_key=Config.get_api_key())
        self.model = Config.OPENAI_MODEL
        self.max_retries = Config.MAX_RETRIES
        self.timeout = Config.TIMEOUT_SECONDS
        self.allowed_domains = EventURLs.get_domains()
    
    def search_events(self) -> Optional[str]:
        """
        Search for Sacramento events using OpenAI Responses API with web search.
        
        Returns:
            Optional[str]: JSON string response from OpenAI, or None if failed
        """
        user_prompt = PromptBuilder.build_event_search_prompt()
        
        for attempt in range(self.max_retries):
            try:
                print(f"Searching for events (attempt {attempt + 1}/{self.max_retries})...")
                
                # Make the API request using OpenAI SDK with web search and domain filtering
                response = self.client.responses.create(
                    model=self.model,
                    reasoning={"effort": "medium"},
                    tools=[
                        {
                            "type": "web_search",
                            "filters": {
                                "allowed_domains": self.allowed_domains
                            }
                        }
                    ],
                    tool_choice="auto",
                    include=["web_search_call.action.sources"],
                    input=user_prompt
                )
                
                # Extract the output text from the response
                if hasattr(response, 'output_text') and response.output_text:
                    content = response.output_text
                    print("✓ Successfully received response from OpenAI Responses API")
                    return content
                else:
                    print(f"✗ Empty response from OpenAI (attempt {attempt + 1})")
                    print(f"   Response: {str(response)[:200]}")
                    
            except Exception as e:
                print(f"✗ Error on attempt {attempt + 1}: {str(e)}")
                
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"  Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print("✗ All retry attempts failed")
                    return None
        
        return None
    
    def test_connection(self) -> bool:
        """
        Test the connection to OpenAI Responses API.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            response = self.client.responses.create(
                model=self.model,
                tools=[{"type": "web_search"}],
                input="Hello, test connection"
            )
            return True
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False