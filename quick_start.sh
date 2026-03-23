#!/bin/bash

# Medical AI Agent - Quick Start Script
# This script automates the initial setup

echo "======================================"
echo "🧠 Medical AI Agent - Quick Start"
echo "======================================"
echo ""

# Check Python installation
echo "✓ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "  Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "✓ Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  Virtual environment created"
else
    echo "  Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "✓ Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo "  Dependencies installed"

# Check .env file
echo ""
echo "✓ Checking configuration..."
if [ ! -f ".env" ]; then
    echo "  ⚠️  .env file not found"
    echo "  Creating from template..."
    cp .env.template .env
    echo ""
    echo "  🔑 IMPORTANT: Edit .env file and add your API keys:"
    echo "     - OPENAI_API_KEY"
    echo "     - TAVILY_API_KEY"
    echo "     - KAGGLE_USERNAME"
    echo "     - KAGGLE_KEY"
    echo ""
    echo "  Then run this script again."
    exit 0
else
    echo "  .env file found"
fi

# Check Kaggle credentials
echo ""
echo "✓ Checking Kaggle credentials..."
if [ ! -f "$HOME/.kaggle/kaggle.json" ]; then
    echo "  ⚠️  Kaggle credentials not found"
    echo "  Please place kaggle.json in ~/.kaggle/"
    echo "  Get it from: https://www.kaggle.com/settings/account"
    exit 1
else
    echo "  Kaggle credentials found"
fi

# All checks passed
echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "Choose how to run:"
echo ""
echo "Option 1 - Jupyter Notebook (Interactive):"
echo "  jupyter notebook medical_ai_agent.ipynb"
echo ""
echo "Option 2 - Python Script (Direct):"
echo "  python medical_agent.py"
echo ""
echo "Option 3 - Gradio Only (Web Interface):"
echo "  python -c 'from medical_agent import *; demo = create_gradio_interface(initialize_system()); demo.launch()'"
echo ""
