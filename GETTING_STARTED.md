# 🎯 Getting Started with TikTok Bot Web Interface

**Your bot is ready! Follow these steps to get started.**

---

## ⚡ 60-Second Quick Start

### Step 1: Add Proxies (30 seconds)

Edit `Data/Proxies.txt` and add your proxies (one per line):

```
http://proxy1.example.com:8080
socks5://proxy2.example.com:1080
```

### Step 2: Start Server (15 seconds)

**Linux/Mac:**
```bash
./start.sh
```

**Windows:**
```bash
start.bat
```

### Step 3: Open Browser (15 seconds)

Navigate to: **http://localhost:5000**

---

## 🎮 Using the Web Interface

### Starting Your First Bot

1. **Enter TikTok Video URL**
   - Example: `https://www.tiktok.com/@username/video/123456789`

2. **Configure Settings**
   - Amount: `1000` (or `0` for unlimited)
   - Threads: `100` (recommended for beginners)
   - Type: `Views` or `Shares`
   - Proxy Type: Match your proxies (http/socks4/socks5)

3. **Click "🚀 Start Bot"**

4. **Watch Live Stats**
   - Sent requests
   - Requests per second
   - Progress percentage
   - Elapsed time

---

## 🐳 Docker Deployment (Production)

If you have Docker installed:

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

**Access at:** http://localhost

---

## 📱 Access from Phone/Other Devices

1. Find your computer's IP address:
   ```bash
   # Linux/Mac
   hostname -I
   
   # Windows
   ipconfig
   ```

2. On other device, open browser to:
   ```
   http://YOUR_IP:5000
   ```
   
   Example: `http://192.168.1.100:5000`

---

## 💡 Recommended Settings

### For Testing (First Time)
```
Amount: 100
Threads: 50
Type: Views
```

### For Normal Use
```
Amount: 1000
Threads: 100-200
Type: Views or Shares
```

### For Maximum Speed
```
Amount: 10000
Threads: 500-1000
Type: Views
Proxies: 100+ high-quality
```

---

## 🔧 Troubleshooting

### "No proxies available"
**Solution:** Add proxies to `Data/Proxies.txt`

### "Port 5000 already in use"
**Solution:** Stop other apps using port 5000, or edit `web_app.py` to use different port

### "Module not found"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Web interface not loading
**Solution:** 
1. Check if server is running
2. Try `http://127.0.0.1:5000` instead
3. Check firewall settings

### Bot starts but no progress
**Solution:**
1. Check proxy quality
2. Verify TikTok URL is correct
3. Look at browser console (F12) for errors

---

## 📊 Understanding the Stats

- **Sent Requests**: Total successful requests sent
- **Requests/sec**: Current speed (higher is better)
- **Elapsed Time**: How long bot has been running
- **Progress**: Percentage complete (only if amount > 0)

**Good Performance:**
- 50+ requests/sec with 50 threads
- 100+ requests/sec with 100 threads
- 500+ requests/sec with 500 threads

**Poor Performance:**
- Less than 10 requests/sec → Check proxies
- 0 requests/sec → Verify URL and proxies

---

## 🎓 Next Steps

### For Casual Users
1. ✅ Add proxies
2. ✅ Start web server
3. ✅ Use the web interface
4. ✅ Done!

### For Power Users
- Read [WEB_INTERFACE_GUIDE.md](WEB_INTERFACE_GUIDE.md) for API usage
- Use REST API to automate tasks
- Run multiple instances

### For Production Deployment
- Read [DEPLOYMENT.md](DEPLOYMENT.md)
- Set up Docker deployment
- Configure nginx reverse proxy
- Enable HTTPS/SSL
- Set up monitoring

---

## 🔒 Safety Tips

1. **Start Small**
   - Test with 50-100 threads first
   - Gradually increase based on results

2. **Use Quality Proxies**
   - Fresh proxies work better
   - Residential proxies > Datacenter
   - Rotate proxies regularly

3. **Monitor Resources**
   - Watch CPU/RAM usage
   - Don't exceed your system limits

4. **Be Respectful**
   - Don't overload target servers
   - Use reasonable amounts
   - Follow TikTok's Terms of Service

---

## 📚 Documentation Reference

- **QUICK_START.md** → 2-minute setup
- **WEB_INTERFACE_GUIDE.md** → Complete API docs
- **DEPLOYMENT.md** → Production deployment
- **PERFORMANCE_OPTIMIZATIONS.md** → Technical details

---

## 💬 Getting Help

**Need help?**
- Check documentation above
- Join Discord: **discord.gg/devcenter**
- Read troubleshooting section

**Common Issues:**
- Proxies not loading → Check file path and format
- Slow performance → Improve proxy quality
- Connection errors → Verify TikTok URL

---

## ✨ Pro Tips

1. **Proxy Management**
   - Keep proxies in separate files by type
   - Test proxies before using
   - Rotate regularly

2. **Performance**
   - More threads ≠ always better
   - Sweet spot: 100-500 threads
   - Quality > Quantity for proxies

3. **Strategy**
   - Run multiple small tasks vs one large task
   - Mix view and share botting
   - Vary thread counts

4. **Monitoring**
   - Watch requests/second rate
   - Check browser console for errors
   - Monitor system resources

---

## 🎯 Quick Commands Cheat Sheet

```bash
# Start web server
./start.sh              # Linux/Mac
start.bat               # Windows

# Start with Docker
docker-compose up -d

# View logs
docker-compose logs -f

# Stop Docker
docker-compose down

# Check if running
curl http://localhost:5000/health

# Install dependencies
pip install -r requirements.txt

# Run CLI mode (classic)
python main.py
```

---

## 🎉 You're All Set!

Your TikTok Bot is ready to use. Start the server and begin botting!

**Questions?** Join our Discord: **discord.gg/devcenter**

<p align="center">
  <b>Happy Botting! 🚀</b>
</p>
