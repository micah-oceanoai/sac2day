#!/usr/bin/env python3
"""
Sacramento Events Finder - Main Entry Point

This script searches for today's top events in Sacramento, California
using the OpenAI API with web search capabilities.

Usage:
    python main.py
"""

import sys
from src.config import Config
from src.date_utils import DateUtils
from src.openai_client import OpenAIClient
from src.json_handler import JSONHandler


def print_header():
    """Print application header."""
    print("=" * 70)
    print("Sacramento Events Finder".center(70))
    print("=" * 70)
    print()


def print_search_info():
    """Print search information."""
    today_info = DateUtils.get_today_info(Config.TIMEZONE)
    print(f"📅 Search Date: {today_info['full_date']}")
    print(f"📍 Location: {Config.CITY}, {Config.STATE}")
    print(f"🎯 Target: Top {Config.MAX_EVENTS} events")
    print()
    print("-" * 70)
    print()


def main():
    """Main application entry point."""
    try:
        # Print header
        print_header()
        
        # Validate configuration
        print("🔧 Validating configuration...")
        Config.validate()
        print("✓ Configuration valid")
        print()
        
        # Print search information
        print_search_info()
        
        # Initialize OpenAI client
        print("🤖 Initializing OpenAI client...")
        client = OpenAIClient()
        print("✓ OpenAI client initialized")
        print()
        
        # Search for events
        print("🔍 Searching for Sacramento events...")
        print("   (This may take 30-60 seconds as the AI searches multiple websites)")
        print()
        
        response = client.search_events()
        
        if response is None:
            print()
            print("=" * 70)
            print("✗ ERROR: Failed to retrieve events from OpenAI API")
            print("=" * 70)
            print()
            print("Possible reasons:")
            print("  - API rate limit reached")
            print("  - Network connectivity issues")
            print("  - Invalid API key")
            print("  - Service temporarily unavailable")
            print()
            sys.exit(1)
        
        # Process and validate JSON
        print("📋 Processing response...")
        formatted_json = JSONHandler.process_response(response)
        
        if formatted_json is None:
            print()
            print("=" * 70)
            print("✗ ERROR: Failed to process JSON response")
            print("=" * 70)
            print()
            print("Raw response:")
            print(response[:500] + "..." if len(response) > 500 else response)
            print()
            sys.exit(1)
        
        # Print results
        print()
        print("=" * 70)
        print("🎉 RESULTS: Top Sacramento Events Today")
        print("=" * 70)
        print()
        print(formatted_json)
        print()
        print("=" * 70)
        print("✓ Search completed successfully!")
        print("=" * 70)
        print()
        
    except KeyboardInterrupt:
        print()
        print()
        print("=" * 70)
        print("⚠ Search cancelled by user")
        print("=" * 70)
        print()
        sys.exit(0)
        
    except Exception as e:
        print()
        print("=" * 70)
        print(f"✗ UNEXPECTED ERROR: {str(e)}")
        print("=" * 70)
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()