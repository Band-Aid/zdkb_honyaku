# Vue.js Frontend for Zendesk KB Translation Manager

This is the frontend interface for managing translation batches and reviewing translation quality.

## Features

- **Batch Management**: Create and monitor translation batches
- **Translation Quality Review**: Side-by-side comparison of original and translated content
- **Translation Editor**: Edit and refine translations with live preview
- **Glossary Management**: Manage translation memory terms for consistent terminology

## Setup

### Prerequisites

- Node.js 18+ and npm
- Python 3.7+ (for backend API)

### Installation

1. Install frontend dependencies:
```bash
cd frontend
npm install
```

2. Install backend dependencies:
```bash
cd ..
pip install -r requirements.txt
```

### Development

1. Start the backend API server:
```bash
python api_server.py
```
The API will run on http://localhost:5000

2. In a separate terminal, start the Vue development server:
```bash
cd frontend
npm run dev
```
The frontend will run on http://localhost:3000

### Production Build

Build the frontend for production:
```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/` and will be served by the Flask API server.

## API Endpoints

The backend provides the following REST API endpoints:

### Configuration
- `GET /api/health` - Health check
- `GET /api/config` - Get current configuration
- `GET /api/glossary` - Get glossary terms
- `POST /api/glossary` - Add new glossary term

### Batches
- `GET /api/batches` - List all batches
- `POST /api/batches` - Create new batch
- `GET /api/batches/:id` - Get batch details
- `POST /api/batches/:id/start` - Start translating a batch

### Articles
- `POST /api/articles/:id/translate` - Translate single article
- `PUT /api/articles/:id` - Update article translation

### Output
- `GET /api/output/list` - List output files
- `GET /api/output/:filename` - Get output file contents

## Project Structure

```
frontend/
├── src/
│   ├── components/        # Reusable Vue components
│   ├── views/            # Page components
│   │   ├── BatchList.vue        # List all batches
│   │   ├── BatchDetail.vue      # View batch and articles
│   │   ├── ArticleEditor.vue    # Edit article translations
│   │   └── GlossaryManager.vue  # Manage glossary terms
│   ├── services/
│   │   └── api.js        # API client
│   ├── App.vue           # Root component
│   └── main.js           # Entry point
├── index.html            # HTML template
├── vite.config.js        # Vite configuration
└── package.json          # Dependencies
```

## Usage

### Creating a Batch

1. Navigate to "Batches" in the navigation
2. Click "New Batch"
3. Select source locale
4. Click "Create Batch"

### Translating a Batch

1. From the batch list, click "Start Translation" on a pending batch
2. Wait for the translation to complete
3. Click "View Details" to see translated articles

### Reviewing Translations

1. Open a completed batch
2. Click "View/Edit" on any article
3. Compare original and translated content side-by-side
4. Edit the translation as needed
5. Click "Save Changes"

### Managing Glossary

1. Navigate to "Glossary" in the navigation
2. Click "Add Term" to add new terminology
3. Enter source and target terms
4. Terms will be automatically applied in future translations

## Technology Stack

- **Vue 3**: Progressive JavaScript framework
- **Vue Router**: Official router for Vue.js
- **Axios**: HTTP client for API requests
- **Vite**: Fast build tool and dev server
- **Flask**: Python web framework for backend API
- **Flask-CORS**: Cross-origin resource sharing for API

## Development Tips

- The frontend proxies API requests to the backend during development
- Use browser DevTools to inspect API requests
- Check browser console for errors
- Backend logs are written to `translation.log`
