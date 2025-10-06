# ⚡ Quick Reference Card

## 🚀 Start Commands

```bash
# Web Interface (Recommended)
./start.sh              # Linux/Mac
start.bat               # Windows

# CLI Mode
python main.py

# Docker
docker-compose up -d

# Production (systemd)
sudo systemctl start tiktok-bot
```

## 🌐 URLs

| Service | URL |
|---------|-----|
| Web Interface | http://localhost:5000 |
| API Health | http://localhost:5000/health |
| API Docs | See WEB_INTERFACE_GUIDE.md |

## 📊 API Quick Reference

```bash
# Start bot
curl -X POST http://localhost:5000/api/start \
  -H "Content-Type: application/json" \
  -d '{"video_uri":"URL","amount":1000,"threads":100,"send_type":"view","proxy_type":"http"}'

# Get status
curl http://localhost:5000/api/status/TASK_ID

# Get all tasks
curl http://localhost:5000/api/tasks

# Stop task
curl -X POST http://localhost:5000/api/stop/TASK_ID

# Proxy count
curl http://localhost:5000/api/proxies/count

# Health check
curl http://localhost:5000/health
```

## 🎯 Recommended Settings

| Purpose | Threads | Amount | Proxy Type |
|---------|---------|--------|------------|
| Testing | 10-50 | 100 | HTTP |
| Normal Use | 100-200 | 1000 | HTTP/SOCKS5 |
| High Speed | 500-1000 | 0 (unlimited) | SOCKS5 |
| VPS | 1000+ | 0 | Mixed |

## 📁 Important Files

```
Data/Proxies.txt        - Your proxies (REQUIRED)
web_app.py              - Web server
main.py                 - CLI version
requirements.txt        - Dependencies
docker-compose.yml      - Docker config
```

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| No proxies | Add to Data/Proxies.txt |
| Port in use | Change port in web_app.py |
| Slow performance | Reduce threads |
| WebSocket error | Check firewall/nginx |

## 📞 Support

- **Docs**: WEB_INTERFACE_GUIDE.md, DEPLOYMENT.md
- **Discord**: discord.gg/devcenter
- **Issues**: GitHub Issues

## 🎨 File Structure

```
tiktok-bot/
├── web_app.py          ← Web server
├── main.py             ← CLI version
├── templates/          ← HTML
├── static/             ← CSS/JS
├── Data/Proxies.txt    ← YOUR PROXIES
└── *.md                ← Documentation
```

## 💡 Quick Tips

1. ✅ Add proxies FIRST
2. ✅ Start with 100 threads
3. ✅ Use web interface for ease
4. ✅ Monitor requests/second
5. ✅ Use VPS for best speed

---

**Need help? Read:** [WEB_INTERFACE_GUIDE.md](WEB_INTERFACE_GUIDE.md)
