"""
Date utility module for Sacramento Events Finder.
Handles date operations and timezone conversions.
"""

from datetime import datetime
from typing import Dict
import pytz


class DateUtils:
    """Utility class for date operations."""
    
    @staticmethod
    def get_today_info(timezone: str = "America/Los_Angeles") -> Dict[str, str]:
        """
        Get today's date information in the specified timezone.
        
        Args:
            timezone: Timezone string (default: America/Los_Angeles for Sacramento)
            
        Returns:
            Dict containing various date formats
        """
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        
        return {
            "date": now.strftime("%Y-%m-%d"),
            "day_name": now.strftime("%A"),
            "month_name": now.strftime("%B"),
            "day": now.strftime("%d"),
            "year": now.strftime("%Y"),
            "full_date": now.strftime("%A, %B %d, %Y"),
            "iso_format": now.isoformat(),
            "display_format": now.strftime("%B %d, %Y")
        }
    
    @staticmethod
    def get_today_string(timezone: str = "America/Los_Angeles") -> str:
        """
        Get today's date as a formatted string.
        
        Args:
            timezone: Timezone string (default: America/Los_Angeles)
            
        Returns:
            str: Today's date in format "Monday, January 15, 2024"
        """
        info = DateUtils.get_today_info(timezone)
        return info["full_date"]
    
    @staticmethod
    def get_today_date(timezone: str = "America/Los_Angeles") -> str:
        """
        Get today's date in YYYY-MM-DD format.
        
        Args:
            timezone: Timezone string (default: America/Los_Angeles)
            
        Returns:
            str: Today's date in YYYY-MM-DD format
        """
        info = DateUtils.get_today_info(timezone)
        return info["date"]