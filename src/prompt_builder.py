"""
Prompt builder module for Sacramento Events Finder.
Constructs detailed prompts for OpenAI API requests.
"""

from typing import List
from src.date_utils import DateUtils
from src.event_urls import EventURLs
from src.config import Config


class PromptBuilder:
    """Class for building OpenAI API prompts."""
    
    @staticmethod
    def build_event_search_prompt() -> str:
        """
        Build a comprehensive prompt for searching Sacramento events.
        
        Returns:
            str: Formatted prompt for OpenAI API
        """
        today_info = DateUtils.get_today_info(Config.TIMEZONE)
        today_date = today_info["date"]
        today_full = today_info["full_date"]
        urls = EventURLs.get_urls()
        
        prompt = f"""You are an expert event researcher for Sacramento, California.

TODAY'S DATE: {today_full} ({today_date})
CURRENT DAY: {today_info['day_name']}
SEARCH FOR: Events happening on {today_date} ONLY

Your task is to search for and compile information about events happening TODAY - {today_date} ({today_info['day_name']}) in Sacramento, California.

CRITICAL REQUIREMENTS:
1. You MUST return EXACTLY {Config.MAX_EVENTS} events - no more, no less
2. ALL events MUST be happening TODAY ({today_date}) - verify the date carefully
3. The "events" array in your JSON response MUST contain exactly {Config.MAX_EVENTS} items
4. DOUBLE-CHECK: Every event's date must match TODAY ({today_date}) before including it

PRIORITY VENUES - ALWAYS INCLUDE IF EVENT EXISTS TODAY:
If ANY event is happening TODAY at these venues, you MUST include it in your results:
- Golden 1 Center (Golden One Center)
- Ace of Spades
- Channel 24
- Harlow's (Harlow's Restaurant & Nightclub)
- Crest Theatre
- Hard Rock Live Sacramento

These venues take ABSOLUTE PRIORITY - if an event exists at any of these venues today, include it even if it means excluding other larger events.

IMPORTANT INSTRUCTIONS:
1. Use DOMAIN-SPECIFIC web searches with these exact search queries for each domain:
   - "events {today_info['day_name']} {today_info['month_name']} {today_info['day']} {today_info['year']} Sacramento site:[domain]"
   - "events today {today_date} Sacramento site:[domain]"
   - "{today_info['day_name']} events Sacramento site:[domain]"
   
   Search ONLY these domains:
{EventURLs.get_domains_formatted()}

2. Perform DEEP web searches on each domain:
   - Use multiple search queries per domain to find events
   - Look specifically for event calendars, "events today", "this {today_info['day_name']}", "{today_info['month_name']} {today_info['day']}" pages
   - Check event detail pages to verify the exact date
   - Look for date indicators like "{today_info['day_name']}, {today_info['month_name']} {today_info['day']}" or "{today_date}"

3. Find events that are happening TODAY ({today_date} - {today_info['day_name']}).
   - **ABSOLUTE PRIORITY: Only include events from TODAY ({today_date})**
   - CRITICAL: Verify each event is actually happening on {today_date} ({today_info['day_name']}, {today_info['month_name']} {today_info['day']}, {today_info['year']})
   - Check the event date multiple times before including it
   - Look for explicit date mentions on the event page
   - FIRST, check for events at the priority venues listed above happening TODAY
   - DO NOT include events from other dates - even if it means returning fewer than {Config.MAX_EVENTS} events
   - It's better to return 2-3 accurate events from TODAY than 10 events with wrong dates

3. EVENT TYPE REQUIREMENTS:
   
   **INCLUDE ONLY FUN, ENTERTAINMENT, AND SOCIAL EVENTS:**
   - Concerts, live music, DJ sets
   - Raves and dance parties
   - Music festivals
   - Sporting events (professional and college sports)
   - Comedy shows and stand-up
   - Live performances, plays, theater
   - Club nights and nightlife
   - Dating events, singles nights, speed dating
   - Movie screenings and film events
   - Cultural conventions (comic book, anime, gaming, pop culture)
   - Art exhibitions and gallery openings
   - Food and drink festivals
   - Markets (farmers markets, night markets, craft fairs)
   - Trivia nights at bars/venues
   - Bar crawls and pub events
   - Drag shows and LGBTQ+ events
   - Interest-based social meetups (gaming, film, tech, wellness)
   - Seasonal activities (ice skating, holiday events)
   
   **EXCLUDE WORK-RELATED AND PROFESSIONAL EVENTS:**
   - Business conferences and trade shows
   - Professional networking events
   - Industry conventions (unless entertainment-focused like comic cons)
   - Corporate seminars and workshops
   - Heavy industry events
   - Professional development sessions
   
   **IF NO EVENTS FOUND FOR TODAY:**
   Include recurring seasonal/weekly events that happen on {today_info['day_name']}s:
   - Ice skating rinks open today
   - Weekly trivia nights at bars
   - Regular DJ nights at clubs
   - Recurring comedy open mics
   - Weekly farmers markets
   - Regular live music nights

4. PRIORITIZE events in this exact order (most important first):
   1. Concerts and live music
   2. Raves and electronic music events
   3. Music festivals
   4. Cultural conventions (comic, anime, gaming)
   5. Sporting events
   6. Comedy shows
   7. Live performances and plays
   8. Club nights and DJ events
   9. Dating events and singles nights
   10. Movie screenings
   11. Ted Talk type speakers
   12. Bar crawls
   13. Drag shows
   14. Trivia nights
   15. Markets (farmers markets, night markets)
   16. Interest-based meetups
   17. Seasonal activities (ice skating, etc.)

5. SCORING SYSTEM - Return the TOP {Config.MAX_EVENTS} events using this combined scoring approach:
   
   **After including all priority venue events, score remaining events by combining these factors:**
   
   - **Event Size** (Weight: 40%)
     * Estimated attendance/capacity
     * Larger events score higher
   
   - **Temporary/Special Event Status** (Weight: 25%)
     * One-time events (not recurring) - highest score
     * Annual events (once per year) - high score
     * Brief/limited-time events - high score
     * Special occasions and celebrations - high score
     * Pop-up events and temporary installations - high score
     * Regular recurring events (weekly/monthly) - low score
   
   - **Age Demographic Appeal** (Weight: 20%)
     * Events appealing to ages 18-35 - high score
     * Trendy, social, and energetic events - high score
     * Nightlife, concerts, festivals, social gatherings - high score
     * Events for children or seniors - low score
   
   - **Event Type Priority** (Weight: 15%)
     * Score based on the event type list (concerts highest)
   
   Calculate a combined score for each event and select the top-scoring events to fill remaining slots after priority venues.

6. For each event, extract the following information:
   - title: Event title (maximum 7 words). If this is a multi-day event, include the headliners/performers for TODAY in the title
   - description: Brief description (maximum 15 words)
   - start_time: When the event starts (include time and timezone)
   - end_time: When the event ends (include time and timezone)
   - venue: Name of the venue hosting the event
   - address: Full street address of the venue
   - estimated_size: Estimated attendance/capacity (e.g., "Small (50-100)", "Medium (100-500)", "Large (500+)")
   - cost: Ticket price or "Free" (e.g., "$25", "$10-$50", "Free")
   - is_free: Boolean true/false - true if the event is free, false if it costs money
   - is_sold_out: Boolean true/false - true if tickets are sold out, false if tickets are available (use false if unknown)
   - ticket_link: URL to purchase tickets. **PREFER the venue's official website link over third-party ticket sellers** (e.g., prefer venue.com over ticketmaster.com)
   - organizers: Name(s) of event organizers
   - instagram_handles: Array of Instagram handles (as strings) including:
     * Event Instagram handle
     * Venue Instagram handle
     * Organizer Instagram handles
     * Performer/Artist Instagram handles (for concerts, shows, etc.)
     * Remove duplicates and exclude "N/A" entries
     * Format: ["@handle1", "@handle2", "@handle3"]
   - vibe_description: A 20-word description of the event's atmosphere/vibe as you would describe it for a promotional poster

7. If any information is not available, use "N/A" as the value.

8. CRITICAL SELECTION CRITERIA:
   
   **STEP 1 - ABSOLUTE PRIORITY (Must Include):**
   Include ALL events happening today at these venues:
     * Golden 1 Center (Golden One Center)
     * Ace of Spades
     * Channel 24
     * Harlow's (Harlow's Restaurant & Nightclub)
     * Crest Theatre
     * Hard Rock Live Sacramento
   
   **STEP 2 - COMBINED SCORING (Fill Remaining Slots):**
   For remaining slots, calculate a combined score using:
     * Event Size (40% weight)
     * Temporary/Special Status (25% weight)
     * Age Demographic Appeal 18-35 (20% weight)
     * Event Type Priority (15% weight)
   
   Select the highest-scoring events to reach UP TO {Config.MAX_EVENTS} total events (only if they're from TODAY).
   
   **IMPORTANT:** Do not apply factors sequentially - combine them into a single score for each event, then rank by total score.

9. Return ONLY valid JSON in this exact format:
{{
  "search_date": "{today_date}",
  "location": "{Config.CITY}, {Config.STATE}",
  "events": [
    {{
      "title": "Event Title Here (with headliners if multi-day)",
      "description": "Brief description here",
      "start_time": "6:00 PM PST",
      "end_time": "10:00 PM PST",
      "venue": "Venue Name",
      "address": "123 Main St, Sacramento, CA 95814",
      "estimated_size": "Medium (200-400)",
      "cost": "$25",
      "is_free": false,
      "is_sold_out": false,
      "ticket_link": "https://example.com/tickets",
      "organizers": "Organizer Name",
      "instagram_handles": ["@eventhandle", "@venuehandle", "@performerhandle"],
      "vibe_description": "Energetic and vibrant atmosphere with live music and dancing under the stars perfect for all ages"
    }}
  ]
}}

CRITICAL FINAL REQUIREMENTS:
- **ABSOLUTE PRIORITY: Only include events happening TODAY ({today_date})**
- Return UP TO {Config.MAX_EVENTS} events, but ONLY events from TODAY
- If fewer than {Config.MAX_EVENTS} events exist TODAY, return only what exists (e.g., 5 events is fine if that's all that's happening)
- **MANDATORY: ALL events must be happening TODAY ({today_date}) - verify dates carefully**
- **ORDERING: List events in this order:**
  1. FIRST: All priority venue events (Golden 1 Center, Ace of Spades, Channel 24, Harlow's, Crest Theatre, Hard Rock Live)
  2. THEN: Remaining events ordered by combined score (highest to lowest)
- **STEP 1: Include ALL events from priority venues happening TODAY**
- **STEP 2: Fill remaining slots (up to {Config.MAX_EVENTS} total) with highest-scoring events happening TODAY using combined scoring:**
  * Event Size (40%) + Temporary/Special (25%) + Age Appeal 18-35 (20%) + Event Type (15%)
  * Do NOT apply factors sequentially - calculate one combined score per event
- **TICKET LINKS: Prefer venue's official website over third-party sellers (e.g., prefer aceofspadessac.com over ticketmaster.com)**
- **DATE VERIFICATION: Quadruple-check that each event is on {today_date} before including it**
- **DO NOT include events from other dates under any circumstances**
- Return valid JSON only (no markdown, no explanations)
- Ensure all required fields are present for each event
- Better to return fewer accurate events than include events from wrong dates"""

        return prompt
    