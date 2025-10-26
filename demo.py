#!/usr/bin/env python3
"""
Demo script showing how the translation program works
This demonstrates the key features without requiring real API credentials
"""
import json
from translation_service import TranslationService
from zendesk_client import ZendeskClient


def demo_system_prompt():
    """Demonstrate the system prompt generation with glossary"""
    print("=" * 70)
    print("DEMO: System Prompt Generation with Translation Memory")
    print("=" * 70)
    
    glossary = [
        {"source": "Knowledge Base", "target": "ナレッジベース"},
        {"source": "Support", "target": "サポート"},
        {"source": "FAQ", "target": "よくある質問"}
    ]
    
    translator = TranslationService(
        target_language="Japanese",
        glossary=glossary
    )
    
    prompt = translator._build_system_prompt()
    print("\nGenerated System Prompt:")
    print("-" * 70)
    print(prompt)
    print("-" * 70)
    print("\nKey Features:")
    print("✓ Target language specified: Japanese")
    print("✓ HTML formatting preservation instruction included")
    print("✓ Translation memory/glossary integrated")
    print(f"✓ {len(glossary)} glossary terms loaded\n")


def demo_article_structure():
    """Demonstrate the expected article structure"""
    print("=" * 70)
    print("DEMO: Article Structure")
    print("=" * 70)
    
    sample_article = {
        "id": 123456789,
        "title": "How to Use the Knowledge Base",
        "body": """
        <h1>Welcome to our Support Center</h1>
        <p>This is a <strong>Knowledge Base</strong> article with <em>formatted text</em>.</p>
        <ul>
            <li>Find answers in our FAQ</li>
            <li>Get Support from our team</li>
            <li>Access Tutorial videos</li>
        </ul>
        """,
        "locale": "en-us",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-15T12:30:00Z"
    }
    
    print("\nSample Zendesk Article:")
    print("-" * 70)
    print(json.dumps(sample_article, indent=2))
    print("-" * 70)
    print("\nStructure Details:")
    print("✓ Article ID for tracking")
    print("✓ Title to be translated")
    print("✓ Body with HTML formatting (preserved during translation)")
    print("✓ Metadata (locale, timestamps)\n")


def demo_translation_workflow():
    """Demonstrate the translation workflow"""
    print("=" * 70)
    print("DEMO: Translation Workflow")
    print("=" * 70)
    
    print("\nWorkflow Steps:")
    print("-" * 70)
    print("1. Load Configuration")
    print("   - Read config.yaml for settings")
    print("   - Load glossary.yaml for translation memory")
    print("   - Load .env for API credentials")
    print()
    print("2. Initialize Services")
    print("   - Create Zendesk API client")
    print("   - Create Translation service with glossary")
    print()
    print("3. Fetch Articles")
    print("   - Connect to Zendesk Help Center API")
    print("   - Fetch all articles (paginated)")
    print("   - Log progress")
    print()
    print("4. Translate Each Article")
    print("   - Send title to OpenAI/Azure with system prompt")
    print("   - Send body to OpenAI/Azure with system prompt")
    print("   - Apply glossary terms for consistency")
    print("   - Preserve HTML formatting")
    print()
    print("5. Save Results")
    print("   - Save all articles to translated_articles.json")
    print("   - Save individual articles to article_{id}.json")
    print("   - Log completion summary")
    print("-" * 70)
    print()


def demo_glossary_usage():
    """Demonstrate glossary term matching"""
    print("=" * 70)
    print("DEMO: Glossary/Translation Memory Usage")
    print("=" * 70)
    
    glossary = [
        {"source": "Knowledge Base", "target": "ナレッジベース"},
        {"source": "Support", "target": "サポート"},
        {"source": "FAQ", "target": "よくある質問"},
        {"source": "Tutorial", "target": "チュートリアル"},
        {"source": "Documentation", "target": "ドキュメント"}
    ]
    
    print("\nLoaded Glossary Terms:")
    print("-" * 70)
    for term in glossary:
        print(f"  {term['source']:20} → {term['target']}")
    print("-" * 70)
    
    print("\nHow It Works:")
    print("✓ Glossary terms are included in every API call's system prompt")
    print("✓ OpenAI/Azure model uses these as translation references")
    print("✓ Ensures consistent terminology across all articles")
    print("✓ Can be extended with domain-specific terms")
    print()


def demo_configuration():
    """Demonstrate configuration structure"""
    print("=" * 70)
    print("DEMO: Configuration Files")
    print("=" * 70)
    
    print("\n1. config.yaml:")
    print("-" * 70)
    config_example = """
glossary_file: "glossary.yaml"

translation:
  target_language: "Japanese"
  preserve_html: true
  
output:
  directory: "output"
  format: "json"
"""
    print(config_example)
    
    print("\n2. .env (environment variables):")
    print("-" * 70)
    env_example = """
# Zendesk
ZENDESK_SUBDOMAIN=your_subdomain
ZENDESK_EMAIL=your_email@example.com
ZENDESK_API_TOKEN=your_api_token

# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4
TARGET_LANGUAGE=Japanese
"""
    print(env_example)
    
    print("\n3. glossary.yaml:")
    print("-" * 70)
    glossary_example = """
terms:
  - source: "Knowledge Base"
    target: "ナレッジベース"
  - source: "Support"
    target: "サポート"
"""
    print(glossary_example)
    print("-" * 70)
    print()


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 10 + "ZENDESK KB TRANSLATION SYSTEM DEMO" + " " * 24 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    demo_configuration()
    demo_glossary_usage()
    demo_system_prompt()
    demo_article_structure()
    demo_translation_workflow()
    
    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print("\nTo run the actual translation:")
    print("  1. Configure your credentials in .env")
    print("  2. Update glossary.yaml with your terms")
    print("  3. Run: python main.py")
    print()


if __name__ == "__main__":
    main()
