"""
Article Translation Service
Handles the workflow of fetching articles, checking translations, and saving them
"""
import os
import logging
from pathlib import Path
from typing import List, Dict, Optional
from zendesk_scraper import ZendeskScraper
from translation_service import TranslationService

logger = logging.getLogger(__name__)


class ArticleTranslationService:
    """Service for managing article scraping, translation, and storage"""
    
    def __init__(self, 
                 base_url: str,
                 translator: TranslationService,
                 output_dir: str = "output"):
        """
        Initialize the article translation service
        
        Args:
            base_url: Base URL of the Zendesk Help Center
            translator: Translation service instance
            output_dir: Directory to save output files
        """
        self.scraper = ZendeskScraper(base_url=base_url)
        self.translator = translator
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def _save_markdown(self, content: str, filename: str) -> str:
        """
        Save content to a markdown file
        
        Args:
            content: Markdown content to save
            filename: Name of the file (without extension)
            
        Returns:
            Path to the saved file
        """
        filepath = self.output_dir / f"{filename}.md"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Saved markdown to {filepath}")
        return str(filepath)
    
    def _translate_markdown(self, markdown_content: str, title: str = "") -> str:
        """
        Translate markdown content using OpenAI
        
        Args:
            markdown_content: Markdown content to translate
            title: Optional title to translate and prepend
            
        Returns:
            Translated markdown content
        """
        # Build the content to translate
        content_to_translate = markdown_content
        
        # Translate the content
        translated_body = self.translator.translate_text(content_to_translate)
        
        # If title was provided, translate it separately and prepend
        if title:
            translated_title = self.translator.translate_text(title)
            return f"# {translated_title}\n\n{translated_body}"
        
        return translated_body
    
    def process_article(self, article_id: str) -> Dict:
        """
        Process a single article: fetch English, check for Japanese, translate if needed
        
        Args:
            article_id: The article ID to process
            
        Returns:
            Dictionary with processing results
        """
        logger.info(f"Processing article {article_id}")
        
        # Fetch both English and Japanese versions
        article_pair = self.scraper.get_article_pair(article_id)
        
        english_article = article_pair.get('english')
        japanese_article = article_pair.get('japanese')
        
        if not english_article:
            logger.error(f"Could not fetch English article {article_id}")
            return {
                "article_id": article_id,
                "status": "error",
                "message": "English article not found"
            }
        
        # Save English version
        english_filename = f"article_{article_id}_en"
        english_content = f"# {english_article['title']}\n\n{english_article['body']}"
        english_path = self._save_markdown(english_content, english_filename)
        
        result = {
            "article_id": article_id,
            "english_url": english_article['url'],
            "english_file": english_path,
            "english_title": english_article['title']
        }
        
        # Check if Japanese version exists
        if japanese_article:
            # Japanese version exists, save it
            logger.info(f"Japanese translation found for article {article_id}")
            japanese_filename = f"article_{article_id}_ja"
            japanese_content = f"# {japanese_article['title']}\n\n{japanese_article['body']}"
            japanese_path = self._save_markdown(japanese_content, japanese_filename)
            
            result.update({
                "status": "existing_translation",
                "japanese_url": japanese_article['url'],
                "japanese_file": japanese_path,
                "japanese_title": japanese_article['title'],
                "translation_source": "zendesk"
            })
        else:
            # No Japanese version, translate using OpenAI
            logger.info(f"No Japanese translation found for article {article_id}, translating with OpenAI...")
            try:
                # Translate the markdown content
                translated_content = self._translate_markdown(
                    english_article['body'],
                    english_article['title']
                )
                
                # Save translated version
                japanese_filename = f"article_{article_id}_ja"
                japanese_path = self._save_markdown(translated_content, japanese_filename)
                
                result.update({
                    "status": "translated",
                    "japanese_file": japanese_path,
                    "translation_source": "openai"
                })
                
                logger.info(f"Successfully translated article {article_id}")
                
            except Exception as e:
                logger.error(f"Error translating article {article_id}: {e}")
                result.update({
                    "status": "translation_error",
                    "error": str(e)
                })
        
        return result
    
    def process_articles(self, article_ids: List[str]) -> List[Dict]:
        """
        Process multiple articles
        
        Args:
            article_ids: List of article IDs to process
            
        Returns:
            List of processing results
        """
        results = []
        
        for i, article_id in enumerate(article_ids, 1):
            logger.info(f"Processing article {i}/{len(article_ids)}: {article_id}")
            result = self.process_article(article_id)
            results.append(result)
        
        return results
