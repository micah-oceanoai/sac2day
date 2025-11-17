# Sacramento Events Finder 🎉

A Python application that uses OpenAI's Responses API with web search capabilities to find and compile information about the top 10 events happening today in Sacramento, California.

## Features

- 🔍 **Automated Event Search**: Searches 16 curated Sacramento event websites
- 📅 **Dynamic Date Detection**: Automatically determines today's date in Pacific Time
- 🤖 **AI-Powered**: Uses OpenAI's Responses API with web_search_preview tool
- 📋 **Structured Output**: Returns events in clean, formatted JSON
- 🎯 **Comprehensive Data**: Includes venue, time, cost, Instagram handles, and more
- 🔧 **Modular Design**: Separated into easy-to-edit Python files
- 📊 **Smart Prioritization**: Prioritizes events by type and size (largest events first)
- 🎪 **Event Type Focus**: Emphasizes concerts, raves, sporting events, and more

## Project Structure

```
sac2day/
├── src/
│   ├── __init__.py           # Package initialization
│   ├── config.py             # Configuration and API key
│   ├── date_utils.py         # Date handling utilities
│   ├── event_urls.py         # Event website URLs
│   ├── prompt_builder.py     # OpenAI prompt construction
│   ├── openai_client.py      # OpenAI API client
│   └── json_handler.py       # JSON parsing and validation
├── main.py                   # Main entry point
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── .gitignore               # Git ignore rules
└── LICENSE                  # GPL-3.0 License
```

## Requirements

- Python 3.8 or higher
- OpenAI API key with access to Responses API (gpt-4.1 model)
- Internet connection

## Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Configure API Key**:
   - The API key is now stored in the `.env` file (already created for you)
   - To change it, edit the `OPENAI_API_KEY` value in `.env`
   - **IMPORTANT**: Never commit the `.env` file to version control (it's already in `.gitignore`)

## Usage

Run the application:

```bash
python3 main.py
```

**Note**: Use `python3` instead of `python` to ensure you're using Python 3.x.

The script will:
1. Determine today's date in Pacific Time (Sacramento timezone)
2. Search the configured event websites using OpenAI's Responses API
3. Extract and verify event information
4. Prioritize events by type and size (largest events first)
5. Return the top 10 largest events in JSON format
6. Print the results to the console

### Event Prioritization

The system uses a two-step prioritization system:

#### Step 1: Absolute Priority - Must-Include Venues
If ANY event is happening today at these venues, it MUST be included:
- **Golden 1 Center** (Golden One Center)
- **Ace of Spades**
- **Channel 24**
- **Harlow's** (Harlow's Restaurant & Nightclub)
- **Crest Theatre**
- **Hard Rock Live Sacramento**

These venues take absolute priority and are included first.

#### Step 2: Combined Scoring System
After including priority venue events, remaining slots are filled using a **combined scoring system** that weighs multiple factors:

**Scoring Weights:**
1. **Event Size (40%)** - Estimated attendance/capacity
   - Larger events score higher
   
2. **Temporary/Special Status (25%)** - Event uniqueness
   - One-time only events (highest)
   - Annual events (high)
   - Limited-time/brief events (high)
   - Special occasions (high)
   - Pop-up events (high)
   - Regular recurring events (low)

3. **Age Demographic Appeal (20%)** - Target audience 18-35
   - Trendy, social, energetic events
   - Nightlife, concerts, festivals
   - Social gatherings
   - Events with younger crowd appeal

4. **Event Type Priority (15%)** - Based on event category
   - Concerts (highest priority)
   - Raves, Music festivals
   - Sporting events, Comedy shows
   - Club nights, Trivia nights
   - Dating events, Speakers
   - Bar crawls, Live plays
   - Markets, Meetups
   - Drag shows

**Important:** These factors are combined into a single score for each event (not applied sequentially). Events are then ranked by their total combined score.

#### Event Type Categories (for reference)
1. **Concerts** - Live music performances
2. **Raves** - Electronic dance music events
3. **Music festivals** - Multi-artist music events
4. **Sporting Events** - Professional and amateur sports
5. **Comedy shows** - Stand-up and comedy performances
6. **Club nights** - Nightclub events and DJ sets
7. **Trivia nights** - Quiz and trivia competitions
8. **Dating events** - Singles mixers and speed dating
9. **Ted Talk type speakers** - Inspirational talks and lectures
10. **Bar crawls** - Multi-venue drinking tours
11. **Live Plays** - Theater and dramatic performances
12. **Markets** - Farmers markets and night markets
13. **Interest-based meetups** - Tech, film, gaming, wellness groups
14. **Drag shows** - Drag performances and competitions

The system selects exactly **10 events total**:
- First: All events from priority venues (if any exist today)
- Then: Highest-scoring events based on combined weighted factors
- Result: A balanced mix optimized for size, uniqueness, demographic appeal, and event type

### Expected Output

The application outputs JSON with the following structure:

```json
{
  "search_date": "2024-01-15",
  "location": "Sacramento, California",
  "events": [
    {
      "title": "Event Title (max 7 words, includes headliners for multi-day events)",
      "description": "Brief description (max 15 words)",
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
      "instagram_handles": [
        "@eventhandle",
        "@venuehandle",
        "@performerhandle"
      ],
      "vibe_description": "20-word description of the event atmosphere"
    }
  ]
}
```

### Field Descriptions

- **title**: Event name (max 7 words). For multi-day events, includes today's headliners
- **description**: Brief event description (max 15 words)
- **start_time**: Event start time with timezone
- **end_time**: Event end time with timezone
- **venue**: Venue name
- **address**: Full street address
- **estimated_size**: Attendance estimate (Small/Medium/Large with ranges)
- **cost**: Ticket price or "Free"
- **is_free**: Boolean - true if event is free, false if it costs money
- **is_sold_out**: Boolean - true if sold out, false if tickets available
- **ticket_link**: URL to purchase tickets (cheapest option)
- **organizers**: Event organizer names
- **instagram_handles**: Array of Instagram handles including event, venue, organizers, and performers (no duplicates)
- **vibe_description**: 20-word atmospheric description for promotional purposes

## Event Sources

The application searches the following websites for events:

1. Eventbrite Sacramento
2. Sactoday Events
3. Sacramento365
4. Downtown Sacramento Events
5. Visit Sacramento
6. Sacramento Bee Events
7. Yelp Sacramento Events
8. Downtown Grid Sacramento
9. KCRA Entertainment
10. Golden 1 Center
11. Ace of Spades
12. **Channel 24** (NEW)
13. Sacramento Observer
14. ABC10 Events
15. Ticketmaster
16. Sacramento365 (duplicate for redundancy)
17. Cal Expo Events

## Configuration

### Modifying Settings

Edit `src/config.py` to change:
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: The OpenAI model to use (default: gpt-4.1)
- `OPENAI_API_BASE_URL`: Base API URL (default: https://api.openai.com/v1)
- `RESPONSES_ENDPOINT`: Responses API endpoint (default: /responses)
- `MAX_EVENTS`: Number of events to return (default: 10)
- `TIMEOUT_SECONDS`: API timeout (default: 120)
- `MAX_RETRIES`: Number of retry attempts (default: 3)

### Adding/Removing Event URLs

Edit `src/event_urls.py` to modify the `URLS` list.

### Customizing the Prompt

Edit `src/prompt_builder.py` to modify how the AI searches for and structures event data.

## Error Handling

The application includes comprehensive error handling:
- **API Failures**: Automatic retry with exponential backoff
- **Invalid JSON**: Graceful parsing with error messages
- **Missing Data**: Fields marked as "N/A" when unavailable
- **Network Issues**: Clear error messages and troubleshooting hints

## Troubleshooting

### "Failed to retrieve events from OpenAI API"
- Check your internet connection
- Verify your API key is valid and has access to Responses API
- Ensure you haven't exceeded API rate limits
- Confirm your OpenAI account has access to gpt-4.1 model
- Verify the Responses API endpoint is accessible

### "Failed to process JSON response"
- The AI may have returned malformed JSON
- Check the raw response printed in the error message
- Try running the script again

### "Configuration validation failed"
- Ensure your API key is set in `src/config.py`
- Verify the API key starts with "sk-"

## Development

### Running Tests

Currently, the best way to test is to run the main script:

```bash
python main.py
```

### Modifying Modules

Each module is self-contained and can be edited independently:
- **config.py**: Change settings and constants
- **date_utils.py**: Modify date handling logic
- **event_urls.py**: Update event website list
- **prompt_builder.py**: Customize AI prompts
- **openai_client.py**: Modify API interaction
- **json_handler.py**: Change JSON processing
- **main.py**: Update application flow

## Cost Considerations

Each run of this application makes one API call to OpenAI Responses API, which incurs costs based on:
- The model used (gpt-4.1)
- The web search operations performed
- The length of the prompt (includes all URLs and instructions)
- The length of the response (JSON for 10 events)

Estimated cost per run: $0.10 - $0.50 (varies based on web searches and response length)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the error messages carefully
- Ensure all dependencies are installed
- Verify your OpenAI API configuration

## Acknowledgments

- Built with OpenAI's API
- Event data sourced from various Sacramento event websites
- Timezone handling via pytz

---

**Note**: This application requires an OpenAI API key with access to the Responses API and the gpt-4.1 model with web_search_preview tool.