#!/usr/bin/env python3
"""
Unit tests for the Zendesk KB translation system
"""
import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock
from translation_service import TranslationService
from zendesk_client import ZendeskClient


class TestTranslationService(unittest.TestCase):
    """Test cases for TranslationService"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.glossary = [
            {"source": "Knowledge Base", "target": "ナレッジベース"},
            {"source": "Support", "target": "サポート"}
        ]
        
    def test_initialization(self):
        """Test service initialization"""
        service = TranslationService(
            target_language="Japanese",
            glossary=self.glossary,
            use_azure=False
        )
        self.assertEqual(service.target_language, "Japanese")
        self.assertEqual(len(service.glossary), 2)
    
    def test_system_prompt_includes_glossary(self):
        """Test that system prompt includes glossary terms"""
        service = TranslationService(
            target_language="Japanese",
            glossary=self.glossary
        )
        prompt = service._build_system_prompt()
        
        # Check that glossary terms are in the prompt
        self.assertIn("Knowledge Base", prompt)
        self.assertIn("ナレッジベース", prompt)
        self.assertIn("Support", prompt)
        self.assertIn("サポート", prompt)
        
    def test_system_prompt_preserves_formatting(self):
        """Test that system prompt mentions preserving HTML"""
        service = TranslationService(target_language="Japanese")
        prompt = service._build_system_prompt()
        
        # Check that formatting preservation is mentioned
        self.assertIn("HTML", prompt.upper())
        self.assertIn("format", prompt.lower())
        
    def test_empty_text_handling(self):
        """Test handling of empty text"""
        service = TranslationService(target_language="Japanese")
        
        # Mock the internal client directly
        service._client = Mock()
        
        # Empty strings should be returned as-is
        result = service.translate_text("")
        self.assertEqual(result, "")
        
        result = service.translate_text("   ")
        self.assertEqual(result, "   ")
        
        # Client should not be called for empty strings
        service._client.chat.completions.create.assert_not_called()


class TestZendeskClient(unittest.TestCase):
    """Test cases for ZendeskClient"""
    
    def test_initialization(self):
        """Test client initialization"""
        client = ZendeskClient(
            subdomain="testsubdomain",
            email="test@example.com",
            api_token="test_token"
        )
        self.assertEqual(client.subdomain, "testsubdomain")
        self.assertEqual(client.base_url, "https://testsubdomain.zendesk.com/api/v2")
        
    @patch('zendesk_client.requests.get')
    def test_get_articles_single_page(self, mock_get):
        """Test fetching articles with single page response"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "articles": [
                {"id": 1, "title": "Article 1", "body": "Body 1"},
                {"id": 2, "title": "Article 2", "body": "Body 2"}
            ],
            "next_page": None
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = ZendeskClient("test", "test@example.com", "token")
        articles = client.get_articles()
        
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0]["id"], 1)
        self.assertEqual(articles[1]["id"], 2)
        
    @patch('zendesk_client.requests.get')
    def test_get_article_by_id(self, mock_get):
        """Test fetching a single article by ID"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "article": {
                "id": 123,
                "title": "Test Article",
                "body": "<p>Test content</p>"
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = ZendeskClient("test", "test@example.com", "token")
        article = client.get_article(123)
        
        self.assertIsNotNone(article)
        self.assertEqual(article["id"], 123)
        self.assertEqual(article["title"], "Test Article")


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_configuration_files_exist(self):
        """Test that required configuration files exist"""
        self.assertTrue(os.path.exists("config.yaml"))
        self.assertTrue(os.path.exists("glossary.yaml"))
        self.assertTrue(os.path.exists(".env.example"))
        self.assertTrue(os.path.exists("requirements.txt"))
        
    def test_main_module_imports(self):
        """Test that main module can be imported"""
        try:
            import main
            self.assertTrue(hasattr(main, 'main'))
            self.assertTrue(hasattr(main, 'load_config'))
            self.assertTrue(hasattr(main, 'load_glossary'))
        except ImportError as e:
            self.fail(f"Failed to import main module: {e}")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
