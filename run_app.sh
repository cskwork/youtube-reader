#!/bin/bash

# YouTube Transcript Reader - Quick Start Script

echo "🚀 YouTube Transcript Reader - Starting..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install/upgrade pip
echo "📋 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp env.example .env
    echo "📝 Please edit .env file and add your API keys!"
    echo "   You need at least one LLM API key for summarization features."
    echo ""
    read -p "Press Enter to continue after adding API keys..."
fi

# Run the Flask app
echo "🌐 Starting Flask application..."
echo "🔗 The app will be available at http://localhost:5000"
echo ""
python app.py 