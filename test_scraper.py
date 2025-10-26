#!/usr/bin/env python3
"""
Unit tests for the Zendesk scraper
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from zendesk_scraper import ZendeskScraper


class TestZendeskScraper(unittest.TestCase):
    """Test cases for ZendeskScraper"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scraper = ZendeskScraper(base_url="https://support.pendo.io")
        
    def test_initialization(self):
        """Test scraper initialization"""
        scraper = ZendeskScraper(base_url="https://support.pendo.io")
        self.assertEqual(scraper.base_url, "https://support.pendo.io")
        
    def test_get_article_url_english(self):
        """Test article URL construction for English"""
        url = self.scraper._get_article_url("27240321140763", locale="en-us")
        self.assertEqual(url, "https://support.pendo.io/hc/en-us/articles/27240321140763")
        
    def test_get_article_url_japanese(self):
        """Test article URL construction for Japanese"""
        url = self.scraper._get_article_url("27240321140763", locale="ja")
        self.assertEqual(url, "https://support.pendo.io/hc/ja/articles/27240321140763")
        
    @patch('zendesk_scraper.requests.get')
    def test_scrape_article_success(self, mock_get):
        """Test successful article scraping"""
        # Mock HTML response
        mock_html = """
        <html>
            <body>
                <h1 class="article-title">Test Article Title</h1>
                <div class="article-body">
                    <p>This is the article content.</p>
                    <h2>Section 1</h2>
                    <p>More content here.</p>
                </div>
            </body>
        </html>
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = mock_html.encode('utf-8')
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        article = self.scraper.get_article("12345", locale="en-us")
        
        self.assertIsNotNone(article)
        self.assertEqual(article['id'], "12345")
        self.assertEqual(article['locale'], "en-us")
        self.assertIn("Test Article Title", article['title'])
        self.assertIn("article content", article['body'])
        
    @patch('zendesk_scraper.requests.get')
    def test_scrape_article_not_found(self, mock_get):
        """Test handling of 404 not found"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        article = self.scraper.get_article("99999", locale="ja")
        
        self.assertIsNone(article)
        
    @patch('zendesk_scraper.requests.get')
    def test_get_article_pair(self, mock_get):
        """Test fetching article pair (English and Japanese)"""
        # Mock English article
        english_html = """
        <html>
            <body>
                <h1>English Article</h1>
                <div class="article-body"><p>English content</p></div>
            </body>
        </html>
        """
        
        # Mock Japanese article
        japanese_html = """
        <html>
            <body>
                <h1>日本語記事</h1>
                <div class="article-body"><p>日本語の内容</p></div>
            </body>
        </html>
        """
        
        def mock_get_response(url, timeout=30):
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.raise_for_status = Mock()
            
            if '/en-us/' in url:
                mock_response.content = english_html.encode('utf-8')
            elif '/ja/' in url:
                mock_response.content = japanese_html.encode('utf-8')
            
            return mock_response
        
        mock_get.side_effect = mock_get_response
        
        result = self.scraper.get_article_pair("12345")
        
        self.assertEqual(result['id'], "12345")
        self.assertIsNotNone(result['english'])
        self.assertIsNotNone(result['japanese'])
        self.assertEqual(result['english']['id'], "12345")
        self.assertEqual(result['japanese']['id'], "12345")
        
    @patch('zendesk_scraper.requests.get')
    def test_get_article_pair_no_japanese(self, mock_get):
        """Test fetching article pair when Japanese version doesn't exist"""
        english_html = """
        <html>
            <body>
                <h1>English Article</h1>
                <div class="article-body"><p>English content</p></div>
            </body>
        </html>
        """
        
        def mock_get_response(url, timeout=30):
            mock_response = Mock()
            
            if '/en-us/' in url:
                mock_response.status_code = 200
                mock_response.content = english_html.encode('utf-8')
                mock_response.raise_for_status = Mock()
            elif '/ja/' in url:
                mock_response.status_code = 404
            
            return mock_response
        
        mock_get.side_effect = mock_get_response
        
        result = self.scraper.get_article_pair("12345")
        
        self.assertEqual(result['id'], "12345")
        self.assertIsNotNone(result['english'])
        self.assertIsNone(result['japanese'])


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
