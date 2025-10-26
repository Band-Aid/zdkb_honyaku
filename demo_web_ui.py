#!/usr/bin/env python3
"""
Demo script to show the web UI capabilities
This creates a sample batch without requiring real Zendesk/OpenAI credentials
"""
import json
from datetime import datetime

# Sample data for demonstration
sample_articles = [
    {
        "id": 12345,
        "title": "How to Get Started with Our Product",
        "body": "<h1>Getting Started</h1><p>Welcome to our <strong>Knowledge Base</strong>. This guide will help you get started quickly.</p>",
        "locale": "en-us",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-15T12:30:00Z"
    },
    {
        "id": 12346,
        "title": "Frequently Asked Questions",
        "body": "<h1>FAQ</h1><ul><li>What is this product?</li><li>How do I get Support?</li></ul>",
        "locale": "en-us",
        "created_at": "2025-01-02T00:00:00Z",
        "updated_at": "2025-01-16T10:00:00Z"
    },
    {
        "id": 12347,
        "title": "Troubleshooting Guide",
        "body": "<h1>Troubleshooting</h1><p>If you encounter issues, check our <em>Support</em> section.</p>",
        "locale": "en-us",
        "created_at": "2025-01-03T00:00:00Z",
        "updated_at": "2025-01-17T14:30:00Z"
    }
]

sample_translated_articles = [
    {
        "id": 12345,
        "title": "製品を始める方法",
        "body": "<h1>はじめに</h1><p><strong>ナレッジベース</strong>へようこそ。このガイドはすぐに始めるのに役立ちます。</p>",
        "locale": "en-us",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-15T12:30:00Z",
        "translation_status": "completed"
    },
    {
        "id": 12346,
        "title": "よくある質問",
        "body": "<h1>よくある質問</h1><ul><li>この製品は何ですか？</li><li>サポートを受けるにはどうすればよいですか？</li></ul>",
        "locale": "en-us",
        "created_at": "2025-01-02T00:00:00Z",
        "updated_at": "2025-01-16T10:00:00Z",
        "translation_status": "completed"
    },
    {
        "id": 12347,
        "title": "トラブルシューティングガイド",
        "body": "<h1>トラブルシューティング</h1><p>問題が発生した場合は、<em>サポート</em>セクションを確認してください。</p>",
        "locale": "en-us",
        "created_at": "2025-01-03T00:00:00Z",
        "updated_at": "2025-01-17T14:30:00Z",
        "translation_status": "completed"
    }
]

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def main():
    print("\n╔════════════════════════════════════════════════════════════════════╗")
    print("║          WEB UI CAPABILITIES DEMONSTRATION                         ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    print_section("1. BATCH CREATION")
    print("When you create a batch via the web UI:")
    print(f"  • Articles are fetched from Zendesk Help Center")
    print(f"  • Batch is created with ID and metadata")
    print(f"  • Status is set to 'pending'")
    print(f"\nExample batch data:")
    batch = {
        "id": 1,
        "locale": "en-us",
        "created_at": datetime.now().isoformat(),
        "status": "pending",
        "total_articles": len(sample_articles),
        "translated_articles": 0,
        "articles": sample_articles
    }
    print(json.dumps(batch, indent=2)[:500] + "...")
    
    print_section("2. TRANSLATION PROCESSING")
    print("When you start a batch translation:")
    print(f"  • Status changes to 'processing'")
    print(f"  • Each article is translated using OpenAI/Azure")
    print(f"  • Glossary terms are applied for consistency")
    print(f"  • HTML formatting is preserved")
    print(f"  • Progress is tracked")
    print(f"\nTranslation features:")
    print(f"  ✓ Title translation")
    print(f"  ✓ Body translation with HTML preservation")
    print(f"  ✓ Glossary term application")
    print(f"  ✓ Error handling and retry")
    
    print_section("3. TRANSLATION REVIEW UI")
    print("The batch detail page provides:")
    print(f"  • List of all articles with translation status")
    print(f"  • Search functionality to find specific articles")
    print(f"  • Article preview with truncated body")
    print(f"  • One-click access to view/edit any article")
    print(f"\nExample article list entry:")
    for article in sample_articles[:1]:
        print(f"  ID: {article['id']}")
        print(f"  Title: {article['title']}")
        print(f"  Preview: {article['body'][:60]}...")
    
    print_section("4. SIDE-BY-SIDE COMPARISON")
    print("The article editor modal shows:")
    print(f"  • Original content (left column, read-only)")
    print(f"  • Translated content (right column, editable)")
    print(f"  • Both title and body fields")
    print(f"  • Save/cancel buttons")
    print(f"\nExample comparison:")
    print(f"\n  Original Title:")
    print(f"    {sample_articles[0]['title']}")
    print(f"\n  Translated Title:")
    print(f"    {sample_translated_articles[0]['title']}")
    
    print_section("5. GLOSSARY MANAGEMENT")
    print("The glossary manager allows you to:")
    print(f"  • View all translation memory terms")
    print(f"  • Search for specific terms")
    print(f"  • Add new terms via a modal dialog")
    print(f"  • Terms are stored in glossary.yaml")
    print(f"\nExample glossary terms:")
    terms = [
        {"source": "Knowledge Base", "target": "ナレッジベース"},
        {"source": "Support", "target": "サポート"},
        {"source": "FAQ", "target": "よくある質問"}
    ]
    for term in terms:
        print(f"  '{term['source']}' → '{term['target']}'")
    
    print_section("6. KEY WEB UI FEATURES")
    features = [
        ("Batch Dashboard", "Monitor all translation batches at a glance"),
        ("Progress Tracking", "Real-time progress bars and status updates"),
        ("Quality Review", "Side-by-side comparison of original and translation"),
        ("Interactive Editing", "Edit translations directly in the browser"),
        ("Glossary Management", "Maintain consistent terminology"),
        ("Search & Filter", "Find specific articles quickly"),
        ("Responsive Design", "Works on desktop and tablet devices"),
        ("REST API", "Programmatic access to all functionality")
    ]
    
    for feature, description in features:
        print(f"  ✓ {feature:25} - {description}")
    
    print_section("7. TECHNOLOGY STACK")
    print("Frontend:")
    print(f"  • Vue 3 - Progressive JavaScript framework")
    print(f"  • Vue Router - Client-side routing")
    print(f"  • Axios - HTTP client for API requests")
    print(f"  • Vite - Fast build tool and dev server")
    print(f"\nBackend:")
    print(f"  • Flask - Python web framework")
    print(f"  • Flask-CORS - Cross-origin resource sharing")
    print(f"  • OpenAI API - Translation service")
    print(f"  • Zendesk API - Article fetching")
    
    print_section("GETTING STARTED")
    print("To use the web UI:")
    print(f"\n  1. Configure credentials in .env file")
    print(f"  2. Run: ./start_web_ui.sh")
    print(f"  3. Open: http://localhost:5000")
    print(f"  4. Create a batch")
    print(f"  5. Start translation")
    print(f"  6. Review and edit results")
    
    print("\n" + "="*70)
    print("  For more details, see WEB_UI_GUIDE.md")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
