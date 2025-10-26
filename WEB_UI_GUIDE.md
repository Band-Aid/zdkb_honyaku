# Web UI User Guide

This guide explains how to use the web interface for managing Zendesk KB translations.

## Web UI Overview

![Batch Management Interface](https://github.com/user-attachments/assets/d1ef7149-7e48-431d-91f1-92cd9d44da1d)

The web interface provides a clean, modern dashboard for managing all aspects of your translation workflow.

## Getting Started

### Starting the Web UI

Run the startup script:
```bash
./start_web_ui.sh
```

Or manually:
```bash
python api_server.py
```

Then open your browser to: **http://localhost:5000**

## Features Overview

### 1. Batch Management

#### Creating a New Batch

1. Navigate to the **Batches** page (default landing page)
2. Click the **"+ New Batch"** button
3. Select the source locale (e.g., "en-us" for English US)
4. Click **"Create Batch"**

The system will fetch all articles from your Zendesk Help Center for that locale.

#### Viewing Batches

The Batches page displays all translation batches with:
- Batch ID and status (pending, processing, completed, failed)
- Source locale
- Creation timestamp
- Article count and translation progress
- Progress bar showing completion percentage

#### Starting Translation

1. Locate a batch with status "pending"
2. Click the **"Start Translation"** button
3. Confirm the action
4. The system will translate all articles in the batch
5. Progress updates automatically as articles are translated

**Note:** Translation may take time depending on the number of articles and API response times.

### 2. Translation Quality Review

#### Viewing Batch Details

1. From the Batches page, click **"View Details"** on any batch
2. You'll see:
   - Batch information (locale, dates, article counts)
   - List of all articles in the batch
   - Translation status for each article

#### Reviewing Individual Articles

1. In the batch detail page, use the search box to find specific articles
2. Click **"View/Edit"** on any article
3. A side-by-side comparison modal opens showing:
   - **Left column:** Original article (title and body)
   - **Right column:** Translated article (editable)

#### Quality Checking

Compare the original and translation side-by-side:
- Check terminology consistency
- Verify HTML formatting is preserved
- Ensure context and meaning are accurate
- Look for any translation errors or awkward phrasing

### 3. Translation Editing

#### Making Edits

1. In the side-by-side comparison view:
   - Edit the translated title in the input field
   - Edit the translated body in the textarea
2. Changes are tracked automatically
3. Click **"Save Changes"** to save your edits
4. Click **"Close"** to discard changes

**Tips:**
- The original content remains visible for reference
- You can edit both title and body
- HTML formatting should be preserved in your edits
- Changes are saved to the batch (not to Zendesk directly)

### 4. Glossary Management

#### Viewing the Glossary

1. Click **"Glossary"** in the navigation bar
2. View all translation memory terms
3. Use the search box to find specific terms

#### Adding New Terms

1. Click **"+ Add Term"**
2. Enter the source term (English)
3. Enter the target translation
4. Click **"Add Term"**

**Example:**
- Source: "Knowledge Base"
- Target: "ナレッジベース"

#### How Glossary Works

- Terms are included in the system prompt for all translations
- Ensures consistent terminology across all articles
- New terms apply to future translations
- Domain-specific terms improve translation quality

## Workflow Example

### Typical Translation Workflow

1. **Setup:**
   - Configure `.env` with your credentials
   - Add common terms to the glossary

2. **Create Batch:**
   - Create a new batch for your source locale
   - System fetches all articles from Zendesk

3. **Translate:**
   - Start the translation process
   - Wait for completion (monitor progress)

4. **Review:**
   - Open batch details
   - Review articles one by one
   - Check translation quality

5. **Edit:**
   - Make corrections where needed
   - Refine translations for accuracy
   - Ensure terminology consistency

6. **Export:**
   - Use the API or batch program to export results
   - Results are saved in the `output/` directory

## Tips and Best Practices

### Translation Quality

- Review at least a sample of translations for quality
- Pay special attention to:
  - Technical terms
  - Product names
  - UI labels
  - Code snippets and examples

### Glossary Management

- Add terms before running large batches
- Include:
  - Product names
  - Feature names
  - Common technical terms
  - Company-specific terminology

### Performance

- Large batches may take time to translate
- Monitor progress from the batches list
- You can work on completed batches while others process

### Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- JavaScript must be enabled
- Recommended screen resolution: 1280x720 or higher

## Troubleshooting

### "Failed to create batch"

- Check `.env` file has correct Zendesk credentials
- Verify API token has proper permissions
- Ensure subdomain is correct

### "Failed to start batch"

- Check `.env` file has correct OpenAI/Azure credentials
- Verify API key is valid
- Check API rate limits

### Translation Quality Issues

- Review and update glossary terms
- Consider adjusting the model (GPT-4 vs GPT-3.5)
- Check source articles for HTML formatting issues

### Changes Not Saving

- Check browser console for errors
- Verify API server is running
- Check file permissions on output directory

## Keyboard Shortcuts

- `Ctrl+Enter` in glossary modal: Add term
- `Esc`: Close modals
- `Ctrl+F`: Search (in articles list)

## API Integration

The web UI communicates with the Flask API server. You can also use the API directly:

- `GET /api/batches` - List batches
- `POST /api/batches` - Create batch
- `POST /api/batches/:id/start` - Start translation
- `GET /api/glossary` - Get glossary
- `POST /api/glossary` - Add term

See `frontend/README.md` for complete API documentation.
