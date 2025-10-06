"""Gunicorn configuration for production deployment."""

import multiprocessing

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = 1  # Use 1 worker with eventlet for WebSocket support
worker_class = "eventlet"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "tiktok_bot_web"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (configure if needed)
# keyfile = "/path/to/key.pem"
# certfile = "/path/to/cert.pem"

# Development vs Production
raw_env = [
    "FLASK_ENV=production",
]

# Server hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    print("🚀 Starting TikTok Bot Web Server...")

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    print("🔄 Reloading workers...")

def when_ready(server):
    """Called just after the server is started."""
    print("✅ Server is ready to accept connections")
    print(f"📡 Listening on {bind}")

def on_exit(server):
    """Called just before exiting."""
    print("👋 Shutting down TikTok Bot Web Server...")
