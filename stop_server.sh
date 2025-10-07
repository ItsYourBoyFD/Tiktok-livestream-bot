#!/bin/bash
# Stop the running server

echo "⛔ Stopping TikTok Bot server..."

if [ -f .server.pid ]; then
    PID=$(cat .server.pid)
    if ps -p $PID > /dev/null; then
        kill $PID
        echo "✅ Server stopped (PID: $PID)"
        rm .server.pid
    else
        echo "⚠️  Server not running (PID $PID not found)"
        rm .server.pid
    fi
else
    # Try to kill by process name
    pkill -f web_app.py && echo "✅ Server stopped" || echo "⚠️  No server found"
fi
