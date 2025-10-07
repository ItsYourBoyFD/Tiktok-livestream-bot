#!/bin/bash
# Local deployment script - runs server in background

echo "🚀 Deploying TikTok Bot Web Application locally..."
echo ""

# Kill any existing instances
pkill -f web_app.py 2>/dev/null || true

# Ensure dependencies are installed
pip install -q -r requirements.txt 2>&1 | grep -v "already satisfied" || true

# Create Data directory
mkdir -p Data
touch Data/Proxies.txt

# Get network info
echo "📡 Network Information:"
echo "   Local: http://localhost:5000"
echo "   LAN:   http://$(hostname -I | awk '{print $1}'):5000"
echo ""

# Start server in background
nohup python3 web_app.py > server.log 2>&1 &
SERVER_PID=$!

echo "✅ Server started (PID: $SERVER_PID)"
echo ""
echo "📊 Access your bot at:"
echo "   🌐 http://localhost:5000"
echo ""
echo "📝 View logs: tail -f server.log"
echo "⛔ Stop server: kill $SERVER_PID"
echo ""
echo "Saving PID to .server.pid..."
echo $SERVER_PID > .server.pid

sleep 3

# Check if server is running
if ps -p $SERVER_PID > /dev/null; then
    echo "✅ Server is running successfully!"
    echo ""
    echo "🎉 Your TikTok Bot is now LIVE!"
else
    echo "❌ Server failed to start. Check server.log for errors."
    cat server.log
fi
