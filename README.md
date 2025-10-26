# zdkb_honyaku

Translate Zendesk Knowledge Base articles with OpenAI to another language while maintaining consistent terminology through translation memory.

## Overview

This batch program fetches articles from Zendesk Help Center and translates them using OpenAI (or Azure OpenAI) APIs. The system includes:

- **Automatic article fetching** from Zendesk Help Center API
- **AI-powered translation** using GPT-4 or Azure OpenAI
- **Translation memory/glossary** to keep terminology consistent across articles
- **Format preservation** to maintain original HTML formatting and structure
- **Batch processing** of multiple articles with error handling

## Features

- ✅ Fetch all articles from Zendesk Help Center
- ✅ Translate using OpenAI GPT-4 or Azure OpenAI
- ✅ Maintain terminology consistency with glossary/translation memory
- ✅ Preserve HTML formatting and structure
- ✅ Save translated articles in JSON format
- ✅ Comprehensive logging and error handling
- ✅ Support for both standard OpenAI and Azure OpenAI
- ✅ **NEW: Vue.js Web UI for batch management and translation review**
- ✅ **NEW: Interactive translation quality checker with side-by-side comparison**
- ✅ **NEW: Translation editor for refining translations**
- ✅ **NEW: Glossary management interface**

## Web UI Preview

![Batch Management UI](https://github.com/user-attachments/assets/d1ef7149-7e48-431d-91f1-92cd9d44da1d)

The web interface provides an intuitive dashboard for managing translation batches, reviewing translations, and maintaining your glossary.

## Prerequisites

- Python 3.7 or higher
- Zendesk account with API access
- OpenAI API key or Azure OpenAI credentials

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
ZENDESK_SUBDOMAIN=your_subdomain
ZENDESK_EMAIL=your_email@example.com
ZENDESK_API_TOKEN=your_api_token

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
# Glossary/Translation Memory
glossary_file: "glossary.yaml"

# Translation settings
translation:
  target_language: "Japanese"
  preserve_html: true
  
# Output settings
output:
  directory: "output"
  format: "json"
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

Run the translation batch program:

```bash
python main.py
```

The program will:
1. Load configuration and glossary
2. Connect to Zendesk and fetch all articles
3. Translate each article using OpenAI/Azure OpenAI
4. Apply glossary terms for consistent terminology
5. Save translated articles to the output directory

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

Translated articles are saved in the `output/` directory:

- `translated_articles.json` - All articles in a single file
- `article_{id}.json` - Individual article files

Each translated article contains:
- Original article metadata
- Translated title
- Translated body (with preserved HTML formatting)

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
- Failed article translations are logged and skipped
- Network errors are caught and reported
- Missing configuration triggers clear error messages
- The batch continues processing even if individual articles fail

## Project Structure

```
zdkb_honyaku/
├── main.py                 # Main batch program (CLI)
├── api_server.py           # Flask API server for web UI
├── zendesk_client.py       # Zendesk API client
├── translation_service.py  # OpenAI/Azure translation service
├── config.yaml             # Configuration file
├── glossary.yaml           # Translation memory/glossary
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore patterns
├── frontend/               # Vue.js web UI
│   ├── src/
│   │   ├── views/         # Page components
│   │   ├── services/      # API client
│   │   └── App.vue        # Root component
│   ├── package.json       # Frontend dependencies
│   └── README.md          # Frontend documentation
└── README.md               # This file
```

## Development

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

### Testing

To test with a specific article:

```python
from zendesk_client import ZendeskClient

zendesk = ZendeskClient(subdomain, email, token)
article = zendesk.get_article(article_id)
```

## Troubleshooting

### Authentication Errors
- Verify Zendesk credentials in `.env`
- Ensure API token has correct permissions
- Check OpenAI/Azure API keys are valid

### Translation Issues
- Review `translation.log` for detailed error messages
- Check API rate limits and quotas
- Verify glossary file format is valid YAML

### HTML Formatting Problems
- The system prompt instructs the model to preserve formatting
- Check if source HTML is valid
- Review translated output for structure integrity

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
