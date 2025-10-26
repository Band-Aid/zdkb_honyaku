"""
Zendesk API Client
Handles fetching articles from Zendesk Help Center
"""
import requests
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ZendeskClient:
    """Client for interacting with Zendesk Help Center API"""
    
    def __init__(self, subdomain: str, email: str, api_token: str):
        """
        Initialize Zendesk client
        
        Args:
            subdomain: Zendesk subdomain
            email: Zendesk account email
            api_token: Zendesk API token
        """
        self.subdomain = subdomain
        self.base_url = f"https://{subdomain}.zendesk.com/api/v2"
        self.auth = (f"{email}/token", api_token)
        
    def get_articles(self, locale: str = "en-us") -> List[Dict]:
        """
        Fetch all articles from Zendesk Help Center
        
        Args:
            locale: The locale to fetch articles for (default: en-us)
            
        Returns:
            List of article dictionaries
        """
        articles = []
        url = f"{self.base_url}/help_center/{locale}/articles.json"
        
        while url:
            try:
                response = requests.get(url, auth=self.auth)
                response.raise_for_status()
                data = response.json()
                
                articles.extend(data.get("articles", []))
                url = data.get("next_page")
                
                logger.info(f"Fetched {len(data.get('articles', []))} articles. Total: {len(articles)}")
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching articles: {e}")
                raise
                
        return articles
    
    def get_article(self, article_id: int, locale: str = "en-us") -> Optional[Dict]:
        """
        Fetch a single article by ID
        
        Args:
            article_id: The article ID
            locale: The locale to fetch the article for
            
        Returns:
            Article dictionary or None if not found
        """
        url = f"{self.base_url}/help_center/{locale}/articles/{article_id}.json"
        
        try:
            response = requests.get(url, auth=self.auth)
            response.raise_for_status()
            data = response.json()
            return data.get("article")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching article {article_id}: {e}")
            return None
