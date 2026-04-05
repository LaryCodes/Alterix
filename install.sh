#!/bin/bash

# Alterix Quick Installation Script
# This script sets up both backend and frontend

set -e  # Exit on error

echo "🚀 Starting Alterix Installation..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "📋 Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
if (( $(echo "$PYTHON_VERSION < 3.10" | bc -l) )); then
    echo -e "${RED}❌ Python 3.10+ is required (found $PYTHON_VERSION)${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python $PYTHON_VERSION${NC}"

# Check Node.js version
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if (( NODE_VERSION < 18 )); then
    echo -e "${RED}❌ Node.js 18+ is required (found v$NODE_VERSION)${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Node.js v$NODE_VERSION${NC}"

echo ""
echo "🐍 Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt --quiet

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    if [ -f ".env.example" ]; then
        echo "Creating .env from .env.example..."
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Please edit backend/.env with your configuration${NC}"
    else
        echo -e "${RED}❌ .env.example not found${NC}"
    fi
fi

echo -e "${GREEN}✅ Backend setup complete${NC}"

cd ..

echo ""
echo "⚛️  Setting up Frontend..."
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install --silent

# Check for .env.local file
if [ ! -f ".env.local" ]; then
    echo -e "${YELLOW}⚠️  .env.local file not found${NC}"
    if [ -f ".env.local.example" ]; then
        echo "Creating .env.local from .env.local.example..."
        cp .env.local.example .env.local
        echo -e "${YELLOW}⚠️  Please edit frontend/.env.local with your configuration${NC}"
    else
        echo -e "${RED}❌ .env.local.example not found${NC}"
    fi
fi

echo -e "${GREEN}✅ Frontend setup complete${NC}"

cd ..

echo ""
echo -e "${GREEN}🎉 Installation Complete!${NC}"
echo ""
echo "📝 Next Steps:"
echo "1. Configure backend/.env with your Supabase and API keys"
echo "2. Configure frontend/.env.local with your API URL"
echo "3. Set up your database schema (see SETUP_GUIDE.md)"
echo ""
echo "🚀 To start the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source .venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then visit: http://localhost:3000"
echo ""
