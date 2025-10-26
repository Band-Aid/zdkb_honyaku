#!/usr/bin/env python3
"""
Flask API Server for Zendesk KB Translation Management
Provides REST API for managing translation batches and reviewing translations
"""
import os
import sys
import json
import yaml
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from zendesk_client import ZendeskClient
from translation_service import TranslationService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
CORS(app)

# Global state for batches
batches = []
batch_counter = 0


def load_config(config_file: str = "config.yaml") -> Dict:
    """Load configuration from YAML file"""
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return {}


def load_glossary(glossary_file: str) -> List[Dict[str, str]]:
    """Load glossary/translation memory from YAML file"""
    try:
        with open(glossary_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        terms = data.get("terms", [])
        return terms
    except Exception as e:
        logger.warning(f"Error loading glossary: {e}")
        return []


def get_translation_service():
    """Initialize and return translation service"""
    config = load_config()
    glossary_file = config.get("glossary_file", "glossary.yaml")
    glossary = load_glossary(glossary_file)
    
    target_language = os.getenv("TARGET_LANGUAGE", 
                                config.get("translation", {}).get("target_language", "Japanese"))
    use_azure = os.getenv("USE_AZURE", "false").lower() == "true"
    model = os.getenv("OPENAI_MODEL", "gpt-4")
    
    return TranslationService(
        target_language=target_language,
        glossary=glossary,
        use_azure=use_azure,
        model=model
    )


def get_zendesk_client():
    """Initialize and return Zendesk client"""
    subdomain = os.getenv("ZENDESK_SUBDOMAIN")
    email = os.getenv("ZENDESK_EMAIL")
    token = os.getenv("ZENDESK_API_TOKEN")
    
    if not all([subdomain, email, token]):
        raise ValueError("Missing Zendesk credentials")
    
    return ZendeskClient(subdomain, email, token)


@app.route('/')
def index():
    """Serve the Vue.js frontend"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


@app.route('/api/config')
def get_config():
    """Get current configuration"""
    config = load_config()
    return jsonify({
        "target_language": os.getenv("TARGET_LANGUAGE", config.get("translation", {}).get("target_language")),
        "use_azure": os.getenv("USE_AZURE", "false").lower() == "true",
        "model": os.getenv("OPENAI_MODEL", "gpt-4")
    })


@app.route('/api/glossary')
def get_glossary():
    """Get glossary terms"""
    config = load_config()
    glossary_file = config.get("glossary_file", "glossary.yaml")
    glossary = load_glossary(glossary_file)
    return jsonify({"terms": glossary})


@app.route('/api/glossary', methods=['POST'])
def add_glossary_term():
    """Add a new glossary term"""
    data = request.json
    source = data.get('source')
    target = data.get('target')
    
    if not source or not target:
        return jsonify({"error": "Both source and target are required"}), 400
    
    config = load_config()
    glossary_file = config.get("glossary_file", "glossary.yaml")
    
    try:
        # Load existing glossary
        with open(glossary_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        
        terms = data.get("terms", [])
        terms.append({"source": source, "target": target})
        data["terms"] = terms
        
        # Save updated glossary
        with open(glossary_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True)
        
        return jsonify({"success": True, "term": {"source": source, "target": target}})
    except Exception as e:
        logger.error(f"Error adding glossary term: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/batches')
def list_batches():
    """List all translation batches"""
    return jsonify({"batches": batches})


@app.route('/api/batches', methods=['POST'])
def create_batch():
    """Create a new translation batch"""
    global batch_counter
    
    data = request.json
    locale = data.get('locale', 'en-us')
    
    try:
        zendesk = get_zendesk_client()
        articles = zendesk.get_articles(locale=locale)
        
        batch_counter += 1
        batch = {
            "id": batch_counter,
            "locale": locale,
            "created_at": datetime.now().isoformat(),
            "status": "pending",
            "total_articles": len(articles),
            "translated_articles": 0,
            "articles": articles
        }
        batches.append(batch)
        
        logger.info(f"Created batch {batch_counter} with {len(articles)} articles")
        return jsonify({"success": True, "batch": batch})
    except Exception as e:
        logger.error(f"Error creating batch: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/batches/<int:batch_id>')
def get_batch(batch_id):
    """Get details of a specific batch"""
    batch = next((b for b in batches if b["id"] == batch_id), None)
    if not batch:
        return jsonify({"error": "Batch not found"}), 404
    return jsonify({"batch": batch})


@app.route('/api/batches/<int:batch_id>/start', methods=['POST'])
def start_batch(batch_id):
    """Start translating a batch"""
    batch = next((b for b in batches if b["id"] == batch_id), None)
    if not batch:
        return jsonify({"error": "Batch not found"}), 404
    
    if batch["status"] != "pending":
        return jsonify({"error": "Batch already started or completed"}), 400
    
    try:
        translator = get_translation_service()
        batch["status"] = "processing"
        batch["started_at"] = datetime.now().isoformat()
        
        translated_articles = []
        for i, article in enumerate(batch["articles"]):
            try:
                translated = translator.translate_article(article)
                translated["translation_status"] = "completed"
                translated_articles.append(translated)
                batch["translated_articles"] = len(translated_articles)
            except Exception as e:
                logger.error(f"Error translating article {article.get('id')}: {e}")
                article["translation_status"] = "failed"
                article["error"] = str(e)
                translated_articles.append(article)
        
        batch["articles"] = translated_articles
        batch["status"] = "completed"
        batch["completed_at"] = datetime.now().isoformat()
        
        return jsonify({"success": True, "batch": batch})
    except Exception as e:
        batch["status"] = "failed"
        batch["error"] = str(e)
        logger.error(f"Error processing batch {batch_id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/articles/<int:article_id>/translate', methods=['POST'])
def translate_article(article_id):
    """Translate a single article"""
    data = request.json
    article = data.get('article')
    
    if not article:
        return jsonify({"error": "Article data is required"}), 400
    
    try:
        translator = get_translation_service()
        translated = translator.translate_article(article)
        return jsonify({"success": True, "article": translated})
    except Exception as e:
        logger.error(f"Error translating article: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/articles/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    """Update a translated article"""
    data = request.json
    
    # Find the article in batches
    for batch in batches:
        for article in batch["articles"]:
            if article.get("id") == article_id:
                # Update fields
                if "title" in data:
                    article["title"] = data["title"]
                if "body" in data:
                    article["body"] = data["body"]
                article["last_modified"] = datetime.now().isoformat()
                return jsonify({"success": True, "article": article})
    
    return jsonify({"error": "Article not found"}), 404


@app.route('/api/output/list')
def list_output_files():
    """List all output files"""
    config = load_config()
    output_dir = Path(config.get("output", {}).get("directory", "output"))
    
    if not output_dir.exists():
        return jsonify({"files": []})
    
    files = []
    for file_path in output_dir.glob("*.json"):
        files.append({
            "name": file_path.name,
            "size": file_path.stat().st_size,
            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        })
    
    return jsonify({"files": files})


@app.route('/api/output/<filename>')
def get_output_file(filename):
    """Get contents of an output file"""
    config = load_config()
    output_dir = Path(config.get("output", {}).get("directory", "output"))
    file_path = output_dir / filename
    
    if not file_path.exists():
        return jsonify({"error": "File not found"}), 404
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error reading file {filename}: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Create output directory if it doesn't exist
    config = load_config()
    output_dir = Path(config.get("output", {}).get("directory", "output"))
    output_dir.mkdir(exist_ok=True)
    
    # Run the server
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting API server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
