#!/bin/bash
# Quick start script for TikTok Bot Web Application

set -e

echo "🚀 Starting TikTok Bot Web Application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Create Data directory
if [ ! -d "Data" ]; then
    echo "📁 Creating Data directory..."
    mkdir -p Data
fi

# Create empty Proxies.txt if it doesn't exist
if [ ! -f "Data/Proxies.txt" ]; then
    echo "📝 Creating Proxies.txt..."
    touch Data/Proxies.txt
    echo "⚠️  Please add proxies to Data/Proxies.txt (one per line)"
fi

# Count proxies
PROXY_COUNT=$(wc -l < Data/Proxies.txt | tr -d ' ')
if [ "$PROXY_COUNT" -eq 0 ]; then
    echo "⚠️  WARNING: No proxies found in Data/Proxies.txt"
    echo "   Add proxies before starting the bot for best results"
else
    echo "✅ Found $PROXY_COUNT proxies"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 TikTok Bot Web Application is starting..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📡 Web Interface: http://localhost:5000"
echo "🔧 API Health: http://localhost:5000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run the application
python web_app.py
