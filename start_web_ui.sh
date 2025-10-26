#!/bin/bash
# Startup script for the Zendesk KB Translation Manager

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Zendesk KB Translation Manager - Web UI      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${BLUE}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓${NC} .env file created. Please edit it with your credentials."
    echo ""
    echo "Press Enter to continue or Ctrl+C to exit and configure .env first..."
    read
fi

# Install Python dependencies if needed
if ! python -c "import flask" 2>/dev/null; then
    echo -e "${BLUE}Installing Python dependencies...${NC}"
    pip install -q -r requirements.txt
    echo -e "${GREEN}✓${NC} Python dependencies installed"
fi

# Check if frontend is built
if [ ! -d "frontend/dist" ]; then
    echo -e "${BLUE}Frontend not built. Building now...${NC}"
    cd frontend
    npm install
    npm run build
    cd ..
    echo -e "${GREEN}✓${NC} Frontend built successfully"
fi

# Start the API server
echo ""
echo -e "${BLUE}Starting API server...${NC}"
echo -e "${GREEN}✓${NC} Server will be available at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python api_server.py
