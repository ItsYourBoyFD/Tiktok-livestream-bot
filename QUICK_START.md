# 🚀 Quick Start Guide

Get your TikTok Bot running in **under 2 minutes**!

---

## ⚡ Super Quick Start

### 1️⃣ Add Proxies

Create/edit `Data/Proxies.txt` and add proxies (one per line):

```
http://proxy1.example.com:8080
http://user:pass@proxy2.example.com:3128
socks5://proxy3.example.com:1080
```

### 2️⃣ Start the Web Server

**On Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**On Windows:**
```bash
start.bat
```

**Or manually:**
```bash
pip install -r requirements.txt
python web_app.py
```

### 3️⃣ Open Your Browser

Navigate to: **http://localhost:5000**

### 4️⃣ Start Botting!

1. Enter TikTok video URL
2. Set amount and threads
3. Click "🚀 Start Bot"
4. Watch real-time stats!

---

## 🐳 Docker Quick Start

Even faster with Docker:

```bash
# One command to rule them all
docker-compose up -d

# Access at http://localhost
```

---

## 📝 First Time Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Proxies added to `Data/Proxies.txt`
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Web server started (`python web_app.py`)
- [ ] Browser open at http://localhost:5000
- [ ] Ready to bot! 🎉

---

## 💡 Quick Tips

**Best Settings for Beginners:**
- Amount: `1000`
- Threads: `100`
- Type: `Views`
- Proxy: Match your proxy type

**Proxy Quality Matters:**
- More proxies = better
- Fresh proxies = faster
- Residential > Datacenter

**Performance:**
- Start small (50-100 threads)
- Gradually increase
- Monitor system resources

---

## 🔍 Troubleshooting

**"No proxies available"**
→ Add proxies to `Data/Proxies.txt`

**"Bot not starting"**
→ Check browser console (F12) for errors

**"Slow performance"**
→ Reduce threads or get better proxies

**"Can't access web interface"**
→ Make sure port 5000 is not blocked

---

## 📚 Next Steps

- Read [WEB_INTERFACE_GUIDE.md](WEB_INTERFACE_GUIDE.md) for API docs
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- Check [PERFORMANCE_OPTIMIZATIONS.md](PERFORMANCE_OPTIMIZATIONS.md) for details

---

## 🎯 Usage Examples

### Example 1: Small Test Run

```
URL: https://www.tiktok.com/@user/video/123
Amount: 100
Threads: 50
Type: Views
Proxy: http
```

### Example 2: Large Campaign

```
URL: https://www.tiktok.com/@user/video/456
Amount: 10000
Threads: 500
Type: Shares
Proxy: socks5
```

### Example 3: Continuous Running

```
URL: https://www.tiktok.com/@user/video/789
Amount: 0 (unlimited)
Threads: 200
Type: Views
Proxy: http
```

---

## 🌐 Access from Other Devices

**On Local Network:**

Find your IP address:
```bash
# Linux/Mac
hostname -I

# Windows
ipconfig
```

Then access from other devices:
```
http://YOUR_IP:5000
```

**Example:**
```
http://192.168.1.100:5000
```

---

## ✅ That's It!

You're ready to start botting! If you need help, check the Discord: **discord.gg/devcenter**

<p align="center">
  <b>Happy Botting! 🚀</b>
</p>
