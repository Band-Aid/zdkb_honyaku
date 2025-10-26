"""
Translation Service
Handles translation using OpenAI or Azure OpenAI APIs
"""
import os
from typing import List, Dict, Optional
import logging
from openai import OpenAI, AzureOpenAI

logger = logging.getLogger(__name__)


class TranslationService:
    """Service for translating text using OpenAI or Azure OpenAI"""
    
    def __init__(self, 
                 target_language: str,
                 glossary: Optional[List[Dict[str, str]]] = None,
                 use_azure: bool = False,
                 model: str = "gpt-4"):
        """
        Initialize translation service
        
        Args:
            target_language: Target language for translation
            glossary: List of term dictionaries with 'source' and 'target' keys
            use_azure: Whether to use Azure OpenAI instead of standard OpenAI
            model: Model name to use (for standard OpenAI) or deployment name (for Azure)
        """
        self.target_language = target_language
        self.glossary = glossary or []
        self.model = model
        
        if use_azure:
            self.client = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
            )
            self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", model)
        else:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.deployment = model
            
    def _build_system_prompt(self) -> str:
        """
        Build the system prompt including glossary/translation memory
        
        Returns:
            System prompt string
        """
        prompt = f"You are a professional translator. Translate the following text to {self.target_language}. "
        prompt += "Preserve all HTML formatting, tags, and structure exactly as they appear in the original text. "
        prompt += "Only translate the content within the tags, not the tags themselves.\n\n"
        
        if self.glossary:
            prompt += "Use the following glossary for consistent terminology:\n"
            for term in self.glossary:
                source = term.get("source", "")
                target = term.get("target", "")
                if source and target:
                    prompt += f"- '{source}' should be translated as '{target}'\n"
            prompt += "\n"
            
        prompt += "Maintain the original formatting and structure. Return only the translated text."
        return prompt
    
    def translate_text(self, text: str) -> str:
        """
        Translate a single text string
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text
        """
        if not text or not text.strip():
            return text
            
        system_prompt = self._build_system_prompt()
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.3  # Lower temperature for more consistent translations
            )
            
            translated = response.choices[0].message.content
            logger.debug(f"Translated text (first 100 chars): {translated[:100]}...")
            return translated
            
        except Exception as e:
            logger.error(f"Error translating text: {e}")
            raise
    
    def translate_article(self, article: Dict) -> Dict:
        """
        Translate an article's title and body
        
        Args:
            article: Article dictionary with 'title' and 'body' fields
            
        Returns:
            Dictionary with translated title and body
        """
        translated_article = article.copy()
        
        # Translate title
        if article.get("title"):
            logger.info(f"Translating title: {article['title'][:50]}...")
            translated_article["title"] = self.translate_text(article["title"])
            
        # Translate body
        if article.get("body"):
            logger.info(f"Translating body (length: {len(article['body'])} chars)...")
            translated_article["body"] = self.translate_text(article["body"])
            
        return translated_article
