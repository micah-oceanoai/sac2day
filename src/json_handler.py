"""
JSON handler module for Sacramento Events Finder.
Handles parsing, validation, and formatting of JSON responses.
"""

import json
import re
from typing import Dict, Any, Optional


class JSONHandler:
    """Class for handling JSON operations."""
    
    @staticmethod
    def extract_json(text: str) -> Optional[str]:
        """
        Extract JSON from text that might contain markdown or other formatting.
        
        Args:
            text: Raw text that may contain JSON
            
        Returns:
            Optional[str]: Extracted JSON string, or None if not found
        """
        # Remove markdown code blocks if present
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        
        # Try to find JSON object
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json_match.group(0)
        
        return text.strip()
    
    @staticmethod
    def parse_json(json_string: str) -> Optional[Dict[str, Any]]:
        """
        Parse JSON string into a dictionary.
        
        Args:
            json_string: JSON string to parse
            
        Returns:
            Optional[Dict]: Parsed JSON as dictionary, or None if parsing fails
        """
        try:
            # First, try to extract clean JSON
            clean_json = JSONHandler.extract_json(json_string)
            
            # Parse the JSON
            data = json.loads(clean_json)
            return data
            
        except json.JSONDecodeError as e:
            print(f"✗ JSON parsing error: {str(e)}")
            print(f"  Error at line {e.lineno}, column {e.colno}")
            return None
        except Exception as e:
            print(f"✗ Unexpected error parsing JSON: {str(e)}")
            return None
    
    @staticmethod
    def validate_event_structure(data: Dict[str, Any]) -> bool:
        """
        Validate that the JSON has the expected structure.
        
        Args:
            data: Parsed JSON data
            
        Returns:
            bool: True if structure is valid, False otherwise
        """
        try:
            # Check top-level structure
            if "events" not in data:
                print("✗ Missing 'events' key in JSON")
                return False
            
            if not isinstance(data["events"], list):
                print("✗ 'events' is not a list")
                return False
            
            # Check each event has required fields
            required_fields = [
                "title", "description", "start_time", "end_time",
                "venue", "address", "estimated_size", "cost",
                "is_free", "is_sold_out",
                "ticket_link", "organizers", "instagram_handles",
                "vibe_description"
            ]
            
            for i, event in enumerate(data["events"]):
                for field in required_fields:
                    if field not in event:
                        print(f"✗ Event {i+1} missing required field: {field}")
                        return False
                
                # Check instagram_handles is a list
                if not isinstance(event.get("instagram_handles"), list):
                    print(f"✗ Event {i+1} has invalid instagram_handles structure (should be array)")
                    return False
                
                # Check is_free and is_sold_out are booleans
                if not isinstance(event.get("is_free"), bool):
                    print(f"✗ Event {i+1} has invalid is_free value (should be boolean)")
                    return False
                
                if not isinstance(event.get("is_sold_out"), bool):
                    print(f"✗ Event {i+1} has invalid is_sold_out value (should be boolean)")
                    return False
            
            event_count = len(data['events'])
            print(f"✓ JSON structure validated ({event_count} events)")
            
            # Info message about event count
            if event_count < 10:
                print(f"ℹ INFO: Found {event_count} events happening today (fewer than max of 10)")
                print(f"  This is expected if there aren't many events scheduled for today")
            elif event_count == 10:
                print(f"✓ Maximum of 10 events found for today")
            
            return True
            
        except Exception as e:
            print(f"✗ Validation error: {str(e)}")
            return False
    
    @staticmethod
    def format_json(data: Dict[str, Any], indent: int = 2) -> str:
        """
        Format JSON data for pretty printing.
        
        Args:
            data: Dictionary to format
            indent: Number of spaces for indentation
            
        Returns:
            str: Formatted JSON string
        """
        return json.dumps(data, indent=indent, ensure_ascii=False)
    
    @staticmethod
    def process_response(response_text: str) -> Optional[str]:
        """
        Process the OpenAI response and return formatted JSON.
        
        Args:
            response_text: Raw response from OpenAI
            
        Returns:
            Optional[str]: Formatted JSON string, or None if processing fails
        """
        # Parse the JSON
        data = JSONHandler.parse_json(response_text)
        
        if data is None:
            print("✗ Failed to parse JSON from response")
            return None
        
        # Validate structure
        if not JSONHandler.validate_event_structure(data):
            print("⚠ JSON structure validation failed, but will attempt to display")
        
        # Format and return
        return JSONHandler.format_json(data)