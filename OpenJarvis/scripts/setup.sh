#!/bin/bash

# OpenJarvis Setup Script
# This script sets up the development environment for OpenJarvis

set -e

echo "🚀 OpenJarvis Setup"
echo "=================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "\n${YELLOW}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "Python version: $python_version"

# Check if Python 3.10+
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo -e "${RED}Error: Python 3.10 or higher is required${NC}"
    exit 1
fi

# Create virtual environment with uv
echo -e "\n${YELLOW}Setting up Python environment with uv...${NC}"
if command -v uv &> /dev/null; then
    uv sync
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
else
    echo -e "${YELLOW}uv not found, using pip...${NC}"
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e .
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
fi

# Install Node.js dependencies
echo -e "\n${YELLOW}Setting up Node.js environment...${NC}"
if command -v npm &> /dev/null; then
    npm install
    echo -e "${GREEN}✅ Node.js dependencies installed${NC}"
else
    echo -e "${RED}npm not found. Please install Node.js first.${NC}"
    echo "Visit: https://nodejs.org/"
fi

# Create necessary directories
echo -e "\n${YELLOW}Creating directories...${NC}"
mkdir -p logs
mkdir -p memory/context
echo -e "${GREEN}✅ Directories created${NC}"

# Copy .env example if not exists
if [ ! -f .env ]; then
    echo -e "\n${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env 2>/dev/null || true
    echo -e "${GREEN}✅ .env file created${NC}"
fi

# Check Ollama
echo -e "\n${YELLOW}Checking Ollama installation...${NC}"
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✅ Ollama is installed${NC}"
    
    # Check if model is available
    if ollama list | grep -q "deepseek-coder"; then
        echo -e "${GREEN}✅ deepseek-coder model is available${NC}"
    else
        echo -e "${YELLOW}deepseek-coder model not found. Pulling...${NC}"
        ollama pull deepseek-coder
        echo -e "${GREEN}✅ Model pulled successfully${NC}"
    fi
else
    echo -e "${YELLOW}Ollama not found. You can install it from: https://ollama.ai${NC}"
    echo "Or use OpenAI by setting OPENAI_API_KEY in .env"
fi

# Final instructions
echo -e "\n${GREEN}================================${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${GREEN}================================${NC}"

echo -e "\n${YELLOW}Next steps:${NC}"
echo "1. Edit .env file with your API keys if using OpenAI"
echo "2. Start Ollama: ollama serve"
echo "3. Run Jarvis: uv run jarvis ask \"your question\""
echo "4. Start WhatsApp bot: npm start"

echo -e "\n${YELLOW}Example usage:${NC}"
echo "  uv run jarvis ask \"Create a Python file that prints hello world\""
echo "  uv run jarvis ask \"List all files in current directory\""

echo ""
