# Quick Start Guide

## 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## 2. Configuration

Copy and configure the environment file:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```bash
# Zendesk Configuration
ZENDESK_SUBDOMAIN=yourcompany
ZENDESK_EMAIL=admin@yourcompany.com
ZENDESK_API_TOKEN=your_zendesk_token

# OpenAI Configuration
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
TARGET_LANGUAGE=Japanese
```

## 3. Customize Glossary

Edit `glossary.yaml` to add your domain-specific terms:

```yaml
terms:
  - source: "Product Name"
    target: "製品名"
  - source: "Feature X"
    target: "機能X"
```

## 4. Run Translation

```bash
python main.py
```

## 5. View Results

Translated articles will be in the `output/` directory:
- `output/translated_articles.json` - All articles
- `output/article_123.json` - Individual articles

## Using Azure OpenAI Instead

Set these in your `.env`:

```bash
USE_AZURE=true
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_DEPLOYMENT=gpt-4
AZURE_OPENAI_API_VERSION=2023-05-15
```

## Testing

Run the demo to see how it works:

```bash
python demo.py
```

Run unit tests:

```bash
python test_translation.py
```

## Common Issues

### Missing API Credentials
Error: `Missing Zendesk credentials`
Solution: Ensure all required variables in `.env` are set

### OpenAI API Errors
Error: `The api_key client option must be set`
Solution: Check `OPENAI_API_KEY` in `.env`

### Rate Limiting
If you hit API rate limits, the program will log errors for specific articles but continue processing others.
