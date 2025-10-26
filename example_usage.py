#!/usr/bin/env python3
"""
Example script demonstrating how to use the new web scraping functionality

This script shows how to:
1. Scrape a single article from Zendesk
2. Check if Japanese translation exists
3. Translate if needed
4. Save as markdown files
"""
import os
from dotenv import load_dotenv
from zendesk_scraper import ZendeskScraper
from translation_service import TranslationService
from article_service import ArticleTranslationService
from main import load_glossary  # Reuse the function from main
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def example_scrape_single_article():
    """Example: Scrape a single article without translation"""
    logger.info("=== Example 1: Scraping a single article ===")
    
    scraper = ZendeskScraper(base_url="https://support.pendo.io")
    
    # Example article ID from the problem statement
    article_id = "27240321140763"
    
    # Get English article
    english = scraper.get_article(article_id, locale="en-us")
    if english:
        logger.info(f"English article title: {english['title']}")
        logger.info(f"English article body length: {len(english['body'])} chars")
    
    # Get Japanese article (may not exist)
    japanese = scraper.get_article(article_id, locale="ja")
    if japanese:
        logger.info(f"Japanese article title: {japanese['title']}")
        logger.info(f"Japanese article body length: {len(japanese['body'])} chars")
    else:
        logger.info("No Japanese translation found")


def example_get_article_pair():
    """Example: Get both English and Japanese versions"""
    logger.info("\n=== Example 2: Getting article pair ===")
    
    scraper = ZendeskScraper(base_url="https://support.pendo.io")
    article_id = "27240321140763"
    
    pair = scraper.get_article_pair(article_id)
    
    logger.info(f"Article ID: {pair['id']}")
    logger.info(f"English exists: {pair['english'] is not None}")
    logger.info(f"Japanese exists: {pair['japanese'] is not None}")


def example_full_workflow():
    """Example: Complete workflow with translation"""
    logger.info("\n=== Example 3: Full workflow with translation ===")
    
    # Load environment
    load_dotenv()
    
    # Check if OpenAI key is set
    if not os.getenv("OPENAI_API_KEY"):
        logger.warning("OPENAI_API_KEY not set in .env file.")
        logger.info("Skipping translation example. Set OPENAI_API_KEY to test translation.")
        logger.info("This is expected if you only want to demonstrate scraping without translation.")
        return
    
    # Load glossary
    glossary = load_glossary()
    
    # Initialize services
    translator = TranslationService(
        target_language="Japanese",
        glossary=glossary,
        use_azure=False,
        model=os.getenv("OPENAI_MODEL", "gpt-4")
    )
    
    article_service = ArticleTranslationService(
        base_url="https://support.pendo.io",
        translator=translator,
        output_dir="output"
    )
    
    # Process article
    article_id = "27240321140763"
    result = article_service.process_article(article_id)
    
    logger.info(f"Status: {result['status']}")
    logger.info(f"English file: {result.get('english_file')}")
    logger.info(f"Japanese file: {result.get('japanese_file')}")
    logger.info(f"Translation source: {result.get('translation_source', 'N/A')}")


def main():
    """Run all examples"""
    print("="*70)
    print("Zendesk Article Scraping Examples")
    print("="*70)
    
    # Example 1: Basic scraping
    try:
        example_scrape_single_article()
    except Exception as e:
        logger.error(f"Example 1 failed: {e}")
    
    # Example 2: Get article pair
    try:
        example_get_article_pair()
    except Exception as e:
        logger.error(f"Example 2 failed: {e}")
    
    # Example 3: Full workflow (requires OpenAI key)
    try:
        example_full_workflow()
    except Exception as e:
        logger.error(f"Example 3 failed: {e}")
    
    print("\n" + "="*70)
    print("Examples completed!")
    print("="*70)


if __name__ == "__main__":
    main()
