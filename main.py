#!/usr/bin/env python3
"""
Zendesk Knowledge Base Translation Program

This program scrapes articles from Zendesk Help Center and translates them using OpenAI,
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

from article_service import ArticleTranslationService
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


def save_results(results: List[Dict], output_dir: str = "output"):
    """
    Save processing results to a JSON summary file
    
    Args:
        results: List of processing result dictionaries
        output_dir: Directory to save output files
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Save summary of all processed articles
    summary_file = output_path / "processing_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved processing summary to {summary_file}")


def main():
    """Main execution function"""
    logger.info("Starting Zendesk KB Translation Program")
    
    # Load environment variables
    load_dotenv()
    
    # Load configuration
    config = load_config()
    
    # Get Zendesk base URL from environment or config
    base_url = os.getenv("ZENDESK_BASE_URL")
    if not base_url:
        base_url = config.get("zendesk", {}).get("base_url", "https://support.pendo.io")
    
    logger.info(f"Using Zendesk base URL: {base_url}")
    
    # Get translation settings
    target_language = os.getenv("TARGET_LANGUAGE", 
                                config.get("translation", {}).get("target_language", "Japanese"))
    use_azure = os.getenv("USE_AZURE", "false").lower() == "true"
    model = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Load glossary
    glossary_file = config.get("glossary_file", "glossary.yaml")
    glossary = load_glossary(glossary_file)
    
    # Initialize translation service
    logger.info("Initializing translation service...")
    translator = TranslationService(
        target_language=target_language,
        glossary=glossary,
        use_azure=use_azure,
        model=model
    )
    
    # Get output directory
    output_dir = config.get("output", {}).get("directory", "output")
    
    # Initialize article service
    logger.info("Initializing article service...")
    article_service = ArticleTranslationService(
        base_url=base_url,
        translator=translator,
        output_dir=output_dir
    )
    
    # Get article IDs to process
    # You can modify this to read from a file or command line arguments
    article_ids_input = os.getenv("ARTICLE_IDS", "")
    if article_ids_input:
        article_ids = [aid.strip() for aid in article_ids_input.split(",") if aid.strip()]
    else:
        # Example article IDs - replace with your actual article IDs
        logger.warning("No ARTICLE_IDS environment variable set. Using example article ID.")
        article_ids = ["27240321140763"]  # Example from the problem statement
    
    logger.info(f"Processing {len(article_ids)} article(s): {', '.join(article_ids)}")
    
    # Process articles
    results = article_service.process_articles(article_ids)
    
    # Save results summary
    logger.info("Saving results summary...")
    save_results(results, output_dir)
    
    # Print summary
    logger.info("\n" + "="*60)
    logger.info("Processing Summary:")
    logger.info("="*60)
    
    for result in results:
        article_id = result.get('article_id')
        status = result.get('status')
        logger.info(f"\nArticle {article_id}: {status}")
        
        if status == "existing_translation":
            logger.info(f"  - Found existing Japanese translation")
            logger.info(f"  - English: {result.get('english_file')}")
            logger.info(f"  - Japanese: {result.get('japanese_file')}")
        elif status == "translated":
            logger.info(f"  - Translated using OpenAI")
            logger.info(f"  - English: {result.get('english_file')}")
            logger.info(f"  - Japanese: {result.get('japanese_file')}")
        elif status == "error" or status == "translation_error":
            logger.error(f"  - Error: {result.get('message', result.get('error'))}")
    
    logger.info("\n" + "="*60)
    logger.info("Translation program completed!")
    logger.info(f"Results saved to: {output_dir}")
    logger.info("="*60)


if __name__ == "__main__":
    main()
