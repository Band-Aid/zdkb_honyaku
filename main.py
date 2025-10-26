#!/usr/bin/env python3
"""
Zendesk Knowledge Base Translation Batch Program

This program fetches articles from Zendesk and translates them using OpenAI or Azure OpenAI,
maintaining consistent terminology through a glossary/translation memory.
"""
import os
import sys
import json
import yaml
import logging
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

from zendesk_client import ZendeskClient
from translation_service import TranslationService


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('translation.log')
    ]
)
logger = logging.getLogger(__name__)


def load_config(config_file: str = "config.yaml") -> Dict:
    """
    Load configuration from YAML file
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Loaded configuration from {config_file}")
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return {}


def load_glossary(glossary_file: str) -> List[Dict[str, str]]:
    """
    Load glossary/translation memory from YAML file
    
    Args:
        glossary_file: Path to glossary file
        
    Returns:
        List of term dictionaries
    """
    try:
        with open(glossary_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        terms = data.get("terms", [])
        logger.info(f"Loaded {len(terms)} glossary terms from {glossary_file}")
        return terms
    except Exception as e:
        logger.warning(f"Error loading glossary: {e}. Continuing without glossary.")
        return []


def save_translated_articles(articles: List[Dict], output_dir: str = "output"):
    """
    Save translated articles to JSON files
    
    Args:
        articles: List of translated article dictionaries
        output_dir: Directory to save output files
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Save all articles to a single file
    all_articles_file = output_path / "translated_articles.json"
    with open(all_articles_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved all translated articles to {all_articles_file}")
    
    # Save individual articles
    for article in articles:
        article_id = article.get("id", "unknown")
        article_file = output_path / f"article_{article_id}.json"
        with open(article_file, 'w', encoding='utf-8') as f:
            json.dump(article, f, ensure_ascii=False, indent=2)
        logger.debug(f"Saved article {article_id} to {article_file}")


def main():
    """Main execution function"""
    logger.info("Starting Zendesk KB Translation Batch Program")
    
    # Load environment variables
    load_dotenv()
    
    # Load configuration
    config = load_config()
    
    # Get Zendesk credentials from environment
    zendesk_subdomain = os.getenv("ZENDESK_SUBDOMAIN")
    zendesk_email = os.getenv("ZENDESK_EMAIL")
    zendesk_token = os.getenv("ZENDESK_API_TOKEN")
    
    if not all([zendesk_subdomain, zendesk_email, zendesk_token]):
        logger.error("Missing Zendesk credentials. Please check your .env file.")
        sys.exit(1)
    
    # Get translation settings
    target_language = os.getenv("TARGET_LANGUAGE", 
                                 config.get("translation", {}).get("target_language", "Japanese"))
    use_azure = os.getenv("USE_AZURE", "false").lower() == "true"
    model = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Load glossary
    glossary_file = config.get("glossary_file", "glossary.yaml")
    glossary = load_glossary(glossary_file)
    
    # Initialize clients
    logger.info("Initializing Zendesk client...")
    zendesk = ZendeskClient(zendesk_subdomain, zendesk_email, zendesk_token)
    
    logger.info("Initializing translation service...")
    translator = TranslationService(
        target_language=target_language,
        glossary=glossary,
        use_azure=use_azure,
        model=model
    )
    
    # Fetch articles
    logger.info("Fetching articles from Zendesk...")
    try:
        articles = zendesk.get_articles()
        logger.info(f"Retrieved {len(articles)} articles")
    except Exception as e:
        logger.error(f"Failed to fetch articles: {e}")
        sys.exit(1)
    
    # Translate articles
    translated_articles = []
    for i, article in enumerate(articles, 1):
        article_id = article.get("id", "unknown")
        article_title = article.get("title", "Untitled")
        
        logger.info(f"Processing article {i}/{len(articles)}: {article_id} - {article_title[:50]}...")
        
        try:
            translated = translator.translate_article(article)
            translated_articles.append(translated)
            logger.info(f"Successfully translated article {article_id}")
        except Exception as e:
            logger.error(f"Failed to translate article {article_id}: {e}")
            # Continue with next article
            continue
    
    # Save results
    output_dir = config.get("output", {}).get("directory", "output")
    logger.info(f"Saving {len(translated_articles)} translated articles...")
    save_translated_articles(translated_articles, output_dir)
    
    logger.info("Translation batch program completed successfully!")
    logger.info(f"Translated {len(translated_articles)} out of {len(articles)} articles")


if __name__ == "__main__":
    main()
