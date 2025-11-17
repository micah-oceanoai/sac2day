"""
Event URLs module for Sacramento Events Finder.
Contains the list of websites to search for events.
"""

from typing import List


class EventURLs:
    """Class containing Sacramento event website URLs."""
    
    URLS: List[str] = [
        "https://www.eventbrite.com/d/ca--sacramento/events--today/",
        "https://sactoday.6amcity.com/events",
        "https://sacramento365.com/",
        "https://www.downtownsac.org/events/",
        "https://www.visitsacramento.com/events/",
        "https://www.sacbee.com/events/",
        "https://www.yelp.com/search?find_desc=Things+To+Do+Tonight&find_loc=Sacramento%2C+CA",
        "https://sacramento.downtowngrid.com/events/",
        "https://www.kcra.com/article/entertainment-sacramento-things-to-do-nov-14-16/69382896",
        "https://www.golden1center.com/events/",
        "https://www.aceofspadessac.com/",
        "https://channel24sac.com/",
        "https://cresttheater.com/events/",
        "https://www.harlows.com/events/",
        "https://safecreditunionconventioncenter.com/",
        "https://thundervalleyresort.com/",
        "https://www.mondaviarts.org/",
        "https://www.broadwaysacramento.com/",
        "https://bstreettheatre.org/",
        "https://sacobserver.com/calendar-of-events/",
        "https://www.abc10.com/article/news/local/events-happening-this-weekend-in-sacramento/103-23b29cdd-98a1-4b89-9916-c63a9b646206",
        "https://www.ticketmaster.com/discover/concerts?tm_link=tm_homeA_brands",
        "https://sacramento365.com/",
        "https://calexpo.com/events/"
    ]
    
    # Domain list for web search (extracted from URLs)
    DOMAINS: List[str] = [
        "eventbrite.com",
        "sactoday.6amcity.com",
        "sacramento365.com",
        "downtownsac.org",
        "visitsacramento.com",
        "sacbee.com",
        "yelp.com",
        "sacramento.downtowngrid.com",
        "kcra.com",
        "golden1center.com",
        "aceofspadessac.com",
        "channel24sac.com",
        "cresttheater.com",
        "harlows.com",
        "safecreditunionconventioncenter.com",
        "thundervalleyresort.com",
        "mondaviarts.org",
        "broadwaysacramento.com",
        "bstreettheatre.org",
        "sacobserver.com",
        "abc10.com",
        "ticketmaster.com",
        "calexpo.com"
    ]
    
    @classmethod
    def get_urls(cls) -> List[str]:
        """
        Get the list of event URLs.
        
        Returns:
            List[str]: List of event website URLs
        """
        return cls.URLS
    
    @classmethod
    def get_url_count(cls) -> int:
        """
        Get the count of URLs.
        
        Returns:
            int: Number of URLs
        """
        return len(cls.URLS)
    
    @classmethod
    def get_urls_formatted(cls) -> str:
        """
        Get URLs formatted as a numbered list for display.
        
        Returns:
            str: Formatted URL list
        """
        return "\n".join([f"{i+1}. {url}" for i, url in enumerate(cls.URLS)])
    
    @classmethod
    def get_domains(cls) -> List[str]:
        """
        Get the list of domains for web search.
        
        Returns:
            List[str]: List of domains
        """
        return cls.DOMAINS
    
    @classmethod
    def get_domains_formatted(cls) -> str:
        """
        Get domains formatted for web search queries.
        
        Returns:
            str: Formatted domain list
        """
        return " OR ".join([f"site:{domain}" for domain in cls.DOMAINS])