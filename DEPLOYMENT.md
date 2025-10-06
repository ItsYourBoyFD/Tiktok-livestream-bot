# 🚀 TikTok Bot - Production Deployment Guide

This guide covers multiple deployment options for the TikTok Bot web application.

---

## 📋 Table of Contents

1. [Quick Start (Development)](#quick-start-development)
2. [Docker Deployment](#docker-deployment)
3. [Manual Production Deployment](#manual-production-deployment)
4. [Cloud Deployment Options](#cloud-deployment-options)
5. [Security & Best Practices](#security--best-practices)

---

## 🏃 Quick Start (Development)

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create Data directory and add proxies
mkdir -p Data
# Add your proxies to Data/Proxies.txt (one per line)

# 3. Run the development server
python web_app.py
```

**Access the web interface at:** `http://localhost:5000`

---

## 🐳 Docker Deployment (Recommended)

### Option 1: Docker Compose (Easiest)

```bash
# 1. Build and start the services
docker-compose up -d

# 2. View logs
docker-compose logs -f

# 3. Stop the services
docker-compose down
```

**Access the web interface at:** `http://localhost` (nginx) or `http://localhost:5000` (direct)

### Option 2: Docker Only

```bash
# 1. Build the image
docker build -t tiktok-bot .

# 2. Run the container
docker run -d \
  --name tiktok-bot \
  -p 5000:5000 \
  -v $(pwd)/Data:/app/Data \
  --restart unless-stopped \
  tiktok-bot

# 3. View logs
docker logs -f tiktok-bot

# 4. Stop the container
docker stop tiktok-bot
docker rm tiktok-bot
```

---

## 🔧 Manual Production Deployment

### On Ubuntu/Debian Server

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python and dependencies
sudo apt install -y python3 python3-pip python3-venv nginx

# 3. Create application directory
sudo mkdir -p /opt/tiktok-bot
sudo chown $USER:$USER /opt/tiktok-bot
cd /opt/tiktok-bot

# 4. Clone/copy your application files
# (Copy all files to /opt/tiktok-bot)

# 5. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 6. Install dependencies
pip install -r requirements.txt

# 7. Create Data directory
mkdir -p Data
# Add your proxies to Data/Proxies.txt

# 8. Set up systemd service
sudo cp tiktok-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tiktok-bot
sudo systemctl start tiktok-bot

# 9. Check status
sudo systemctl status tiktok-bot
```

### Configure Nginx Reverse Proxy

```bash
# 1. Create nginx configuration
sudo nano /etc/nginx/sites-available/tiktok-bot

# Paste the following configuration:
```

```nginx
server {
    listen 80;
    server_name your-domain.com;  # Change this!

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_buffering off;
        proxy_read_timeout 86400;
    }

    location /static/ {
        alias /opt/tiktok-bot/static/;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# 2. Enable the site
sudo ln -s /etc/nginx/sites-available/tiktok-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 3. (Optional) Set up SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## ☁️ Cloud Deployment Options

### AWS EC2

```bash
# 1. Launch an EC2 instance (Ubuntu 22.04 LTS recommended)
# 2. Configure security group to allow ports: 80, 443, 5000
# 3. SSH into the instance
# 4. Follow "Manual Production Deployment" steps above
```

### DigitalOcean Droplet

```bash
# 1. Create a droplet (Ubuntu 22.04)
# 2. Use Docker deployment method:
docker-compose up -d
```

### Heroku

Create `Procfile`:
```
web: gunicorn -c gunicorn_config.py web_app:app
```

Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Railway.app

1. Connect your GitHub repository
2. Railway will auto-detect and deploy
3. Expose port 5000

### Render.com

1. Create new Web Service
2. Connect repository
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn -c gunicorn_config.py web_app:app`

---

## 🔒 Security & Best Practices

### 1. Proxy Security

```bash
# Secure your proxies file
chmod 600 Data/Proxies.txt
```

### 2. Firewall Configuration

```bash
# Ubuntu/Debian with UFW
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 3. Environment Variables

Create `.env` file:
```bash
FLASK_SECRET_KEY=your-super-secret-key-here
MAX_THREADS=1000
RATE_LIMIT=100
```

### 4. Rate Limiting

Already configured in `nginx.conf`:
- 10 requests/second per IP
- Burst up to 20 requests

### 5. HTTPS Setup

```bash
# Let's Encrypt (Free SSL)
sudo certbot --nginx -d your-domain.com
sudo certbot renew --dry-run
```

### 6. Monitoring

```bash
# View application logs
sudo journalctl -u tiktok-bot -f

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## 📊 Performance Tuning

### For High Traffic

1. **Increase worker connections** in `gunicorn_config.py`:
```python
worker_connections = 2000
```

2. **Optimize nginx**:
```nginx
worker_processes auto;
worker_connections 4096;
```

3. **Use Redis for session storage** (optional):
```bash
pip install redis flask-session
```

### For Many Concurrent Bots

1. Increase system limits:
```bash
sudo nano /etc/security/limits.conf
# Add:
* soft nofile 65536
* hard nofile 65536
```

2. Optimize kernel:
```bash
sudo nano /etc/sysctl.conf
# Add:
net.core.somaxconn = 4096
net.ipv4.tcp_max_syn_backlog = 4096
```

---

## 🔧 Maintenance

### Update Application

```bash
# Docker
docker-compose pull
docker-compose up -d

# Manual
cd /opt/tiktok-bot
git pull  # or copy new files
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart tiktok-bot
```

### Backup Proxies

```bash
# Automatic daily backup
echo "0 2 * * * cp /opt/tiktok-bot/Data/Proxies.txt /backup/proxies-$(date +\%Y\%m\%d).txt" | sudo crontab -
```

---

## 🆘 Troubleshooting

### Bot Not Starting

```bash
# Check logs
sudo journalctl -u tiktok-bot -n 50

# Check if port is in use
sudo netstat -tulpn | grep 5000

# Restart service
sudo systemctl restart tiktok-bot
```

### WebSocket Issues

```bash
# Check nginx configuration
sudo nginx -t

# Ensure WebSocket upgrade headers are set
# Check browser console for errors
```

### High Memory Usage

```bash
# Monitor resources
htop

# Reduce threads or workers in gunicorn_config.py
```

---

## 📞 Support

- GitHub Issues: [Your Repo URL]
- Discord: discord.gg/devcenter
- Documentation: See README.md

---

## 📝 Quick Command Reference

```bash
# Start service
sudo systemctl start tiktok-bot

# Stop service
sudo systemctl stop tiktok-bot

# Restart service
sudo systemctl restart tiktok-bot

# View logs
sudo journalctl -u tiktok-bot -f

# Check status
sudo systemctl status tiktok-bot

# Docker compose
docker-compose up -d          # Start
docker-compose down           # Stop
docker-compose logs -f        # View logs
docker-compose restart        # Restart
```

---

**🎉 Your TikTok Bot is now ready for production!**

Access it at your domain or server IP address.
