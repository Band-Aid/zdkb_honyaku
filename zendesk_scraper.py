"""
Zendesk Web Scraper
Handles fetching articles by scraping Zendesk Help Center web pages
"""
import requests
from bs4 import BeautifulSoup
import html2text
from typing import Optional, Dict
import logging
import re

logger = logging.getLogger(__name__)


class ZendeskScraper:
    """Scraper for fetching articles from Zendesk Help Center web pages"""
    
    def __init__(self, base_url: str = "https://support.pendo.io"):
        """
        Initialize Zendesk scraper
        
        Args:
            base_url: Base URL of the Zendesk Help Center (default: https://support.pendo.io)
        """
        self.base_url = base_url.rstrip('/')
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        self.html_converter.body_width = 0  # Don't wrap text
        
    def _get_article_url(self, article_id: str, locale: str = "en-us") -> str:
        """
        Construct the article URL
        
        Args:
            article_id: The article ID
            locale: The locale (e.g., 'en-us' or 'ja')
            
        Returns:
            Full article URL
        """
        return f"{self.base_url}/hc/{locale}/articles/{article_id}"
    
    def _scrape_article_content(self, url: str) -> Optional[Dict]:
        """
        Scrape article content from a URL
        
        Args:
            url: The article URL
            
        Returns:
            Dictionary with title and body in markdown, or None if not found
        """
        try:
            response = requests.get(url, timeout=30)
            
            # Check if article exists
            if response.status_code == 404:
                logger.info(f"Article not found at {url}")
                return None
                
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract article title
            title_element = soup.find('h1', class_=re.compile(r'article.*title|title'))
            if not title_element:
                # Try alternative selectors
                title_element = soup.find('h1')
            
            title = title_element.get_text(strip=True) if title_element else "Untitled"
            
            # Extract article body
            # Try common Zendesk article body class names
            body_element = soup.find('div', class_=re.compile(r'article.*body|article-body'))
            if not body_element:
                # Try alternative selectors
                body_element = soup.find('article')
                if not body_element:
                    body_element = soup.find('div', class_='article-content')
            
            if not body_element:
                logger.warning(f"Could not find article body at {url}")
                return None
            
            # Convert HTML to Markdown
            body_html = str(body_element)
            body_markdown = self.html_converter.handle(body_html)
            
            logger.info(f"Successfully scraped article: {title[:50]}...")
            
            return {
                "title": title,
                "body": body_markdown.strip()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching article from {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error parsing article from {url}: {e}")
            return None
    
    def get_article(self, article_id: str, locale: str = "en-us") -> Optional[Dict]:
        """
        Fetch a single article by ID and locale
        
        Args:
            article_id: The article ID (just the number, not the full URL)
            locale: The locale to fetch the article for (default: en-us)
            
        Returns:
            Article dictionary with title and body in markdown, or None if not found
        """
        url = self._get_article_url(article_id, locale)
        logger.info(f"Fetching article {article_id} in locale {locale} from {url}")
        
        article = self._scrape_article_content(url)
        if article:
            article['id'] = article_id
            article['locale'] = locale
            article['url'] = url
        
        return article
    
    def get_article_pair(self, article_id: str) -> Dict:
        """
        Fetch both English and Japanese versions of an article
        
        Args:
            article_id: The article ID
            
        Returns:
            Dictionary with 'english' and 'japanese' keys, where japanese may be None
        """
        english_article = self.get_article(article_id, locale="en-us")
        japanese_article = self.get_article(article_id, locale="ja")
        
        return {
            "id": article_id,
            "english": english_article,
            "japanese": japanese_article
        }
