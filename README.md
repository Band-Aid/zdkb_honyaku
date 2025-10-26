# zdkb_honyaku

Translate Zendesk Knowledge Base articles with OpenAI to another language while maintaining consistent terminology through translation memory.

## Overview

This program scrapes articles from Zendesk Help Center web pages and translates them using OpenAI (or Azure OpenAI) APIs. The system includes:

- **Web scraping** of Zendesk Help Center articles (no API credentials needed)
- **Automatic markdown conversion** from HTML content
- **Smart translation detection** - uses existing Japanese translations when available
- **AI-powered translation** using GPT-4 or Azure OpenAI for missing translations
- **Translation memory/glossary** to keep terminology consistent across articles
- **Markdown output** for easy editing and version control
- **Batch processing** of multiple articles with error handling

## Features

- ✅ Scrape articles from Zendesk Help Center web pages
- ✅ Convert HTML content to clean Markdown format
- ✅ Detect existing Japanese translations automatically
- ✅ Translate using OpenAI GPT-4 or Azure OpenAI when needed
- ✅ Maintain terminology consistency with glossary/translation memory
- ✅ Save articles as markdown files (separate English and Japanese files)
- ✅ Comprehensive logging and error handling
- ✅ Support for both standard OpenAI and Azure OpenAI
- ✅ **NEW: Web scraping approach (no Zendesk API credentials required)**
- ✅ **NEW: Vue.js Web UI for batch management and translation review**
- ✅ **NEW: Interactive translation quality checker with side-by-side comparison**
- ✅ **NEW: Translation editor for refining translations**
- ✅ **NEW: Glossary management interface**

## Web UI Preview

![Batch Management UI](https://github.com/user-attachments/assets/d1ef7149-7e48-431d-91f1-92cd9d44da1d)

The web interface provides an intuitive dashboard for managing translation batches, reviewing translations, and maintaining your glossary.

## Prerequisites

- Python 3.7 or higher
- OpenAI API key or Azure OpenAI credentials (for translation)
- Internet access to Zendesk Help Center

**Note:** Zendesk API credentials are no longer required. The system now scrapes articles directly from the web.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Band-Aid/zdkb_honyaku.git
cd zdkb_honyaku
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up configuration:
```bash
cp .env.example .env
```

4. Edit `.env` file with your credentials:
```
# Zendesk base URL (no credentials needed)
ZENDESK_BASE_URL=https://support.pendo.io

# Article IDs to process (comma-separated)
ARTICLE_IDS=27240321140763,27240321140764

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4

TARGET_LANGUAGE=Japanese
USE_AZURE=false
```

For Azure OpenAI, set `USE_AZURE=true` and provide:
```
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_azure_api_key
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
AZURE_OPENAI_API_VERSION=2023-05-15
```

## Configuration

### config.yaml

Configure translation settings and output preferences:

```yaml
# Zendesk Help Center settings
zendesk:
  base_url: "https://support.pendo.io"

# Glossary/Translation Memory
glossary_file: "glossary.yaml"

# Translation settings
translation:
  target_language: "Japanese"
  preserve_html: true
  
# Output settings
output:
  directory: "output"
  format: "markdown"  # Articles saved as .md files
```

### glossary.yaml

Define terminology for consistent translation:

```yaml
terms:
  - source: "Knowledge Base"
    target: "ナレッジベース"
  - source: "Support"
    target: "サポート"
  - source: "FAQ"
    target: "よくある質問"
```

Add more terms specific to your domain to ensure consistent terminology across all translated articles.

## Usage

### Command Line (Batch Mode)

Run the translation program:

```bash
python main.py
```

The program will:
1. Load configuration and glossary
2. Scrape English articles from Zendesk Help Center
3. Check if Japanese translations exist on Zendesk
4. If Japanese exists, save both English and Japanese as markdown
5. If not, translate using OpenAI and save both versions
6. Apply glossary terms for consistent terminology
7. Save all files to the output directory

**Specifying Article IDs:**

Set the `ARTICLE_IDS` environment variable with comma-separated article IDs:

```bash
export ARTICLE_IDS="27240321140763,27240321140764,27240321140765"
python main.py
```

Or add to your `.env` file:
```
ARTICLE_IDS=27240321140763,27240321140764,27240321140765
```

### Web UI (Interactive Mode)

Start the web interface for interactive batch management and translation review:

```bash
# Start the API server
python api_server.py
```

Then open your browser to `http://localhost:5000`

Or run in development mode:

```bash
# Terminal 1: Start API server
python api_server.py

# Terminal 2: Start Vue dev server
cd frontend
npm install  # First time only
npm run dev
```

Then open your browser to `http://localhost:3000`

The web UI provides:
- **Batch Management**: Create and monitor translation batches
- **Translation Review**: Side-by-side comparison of original and translated content
- **Translation Editor**: Edit and refine translations
- **Glossary Manager**: Manage translation memory terms

## Output

Articles are saved in the `output/` directory as markdown files:

- `article_{id}_en.md` - English version in markdown
- `article_{id}_ja.md` - Japanese version in markdown
- `processing_summary.json` - Summary of all processed articles

Each markdown file contains:
- Article title as h1 heading
- Full article body converted from HTML to markdown
- Preserved formatting and structure

The summary JSON includes:
- Article IDs processed
- Status of each article (existing_translation, translated, error)
- File paths for English and Japanese versions
- Translation source (zendesk or openai)

## Logging

The program generates detailed logs in:
- Console output (stdout)
- `translation.log` file

Log levels:
- INFO: General progress information
- DEBUG: Detailed processing information
- WARNING: Non-critical issues
- ERROR: Failed operations

## Error Handling

The program includes robust error handling:
- Articles not found (404) are logged and skipped
- Network errors are caught and reported
- Failed translations are logged with error details
- Missing configuration triggers clear error messages
- The batch continues processing even if individual articles fail

## Project Structure

```
zdkb_honyaku/
├── main.py                   # Main program (CLI)
├── zendesk_scraper.py        # Web scraper for Zendesk articles
├── article_service.py        # Article processing workflow
├── translation_service.py    # OpenAI/Azure translation service
├── zendesk_client.py         # Legacy Zendesk API client (deprecated)
├── api_server.py             # Flask API server for web UI
├── example_usage.py          # Example usage scripts
├── config.yaml               # Configuration file
├── glossary.yaml             # Translation memory/glossary
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── test_scraper.py           # Tests for web scraper
├── test_translation.py       # Tests for translation service
├── .gitignore                # Git ignore patterns
├── frontend/                 # Vue.js web UI
│   ├── src/
│   │   ├── views/           # Page components
│   │   ├── services/        # API client
│   │   └── App.vue          # Root component
│   ├── package.json         # Frontend dependencies
│   └── README.md            # Frontend documentation
└── README.md                 # This file
```

## How It Works

### Article Processing Workflow

1. **Scrape English Article**: The scraper fetches the article from `https://support.pendo.io/hc/en-us/articles/{article_id}`
2. **Convert to Markdown**: HTML content is converted to clean markdown format
3. **Check for Japanese**: The scraper attempts to fetch from `https://support.pendo.io/hc/ja/articles/{article_id}`
4. **Save or Translate**:
   - If Japanese exists: Both versions are saved as markdown files
   - If not: English is translated via OpenAI, then both are saved
5. **Apply Glossary**: Translation uses glossary terms for consistency

### URL Structure

- English: `https://support.pendo.io/hc/en-us/articles/{article_id}-{title-slug}` → Use just the ID
- Japanese: `https://support.pendo.io/hc/ja/articles/{article_id}` → Change locale from `en-us` to `ja`

## Development

### Running Tests

```bash
# Run all tests
python -m unittest test_scraper.py test_translation.py -v

# Run specific test file
python -m unittest test_scraper.py -v
```

### Adding New Glossary Terms

Edit `glossary.yaml` and add new term pairs:

```yaml
terms:
  - source: "Your English Term"
    target: "対応する日本語訳"
```

### Customizing Translation

Modify the system prompt in `translation_service.py` to adjust translation behavior:

```python
def _build_system_prompt(self) -> str:
    # Customize the prompt here
    prompt = f"You are a professional translator..."
```

### Testing with Specific Articles

To test scraping a specific article:

```python
from zendesk_scraper import ZendeskScraper

scraper = ZendeskScraper(base_url="https://support.pendo.io")
article = scraper.get_article("27240321140763", locale="en-us")
if article:
    print(f"Title: {article['title']}")
    print(f"Body length: {len(article['body'])} chars")
```

To test the complete workflow:

```bash
python example_usage.py
```

## Troubleshooting

### Network/Connection Errors
- Ensure you have internet access to the Zendesk Help Center
- Check that the base URL is correct in config.yaml or .env
- Verify the article ID exists at the URL

### Article Not Found (404)
- Verify the article ID is correct
- Check if the article is published and publicly accessible
- Try accessing the URL directly in a browser

### Translation Issues
- Review `translation.log` for detailed error messages
- Check API rate limits and quotas
- Verify OpenAI/Azure API keys are valid
- Ensure glossary file format is valid YAML

### Scraping/Parsing Issues
- If article body is empty, the HTML structure may have changed
- Check the browser's inspector to verify the article HTML structure
- Update CSS selectors in `zendesk_scraper.py` if needed
- The scraper looks for common Zendesk class names

### Markdown Formatting Problems
- Verify the HTML source is valid
- Adjust html2text settings in `zendesk_scraper.py` if needed
- Review converted markdown output for structure integrity

## License

This project is provided as-is for translating Zendesk Knowledge Base articles.

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing style
- Add appropriate error handling
- Update documentation for new features
- Test with real Zendesk articles before submitting

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review log files for error details
3. Open an issue on GitHub with relevant log excerpts
