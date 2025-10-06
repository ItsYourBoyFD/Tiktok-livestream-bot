# 🌐 TikTok Bot - Web Interface Guide

Complete guide to using the modern web interface for TikTok Bot.

---

## 🚀 Quick Start

### Start the Web Server

**Linux/Mac:**
```bash
./start.sh
```

**Windows:**
```bash
start.bat
```

**Or manually:**
```bash
pip install -r requirements.txt
python web_app.py
```

Then open your browser to: **http://localhost:5000**

---

## 📱 Web Interface Features

### 🎮 Control Panel

The control panel allows you to configure and start bot tasks:

1. **TikTok Video URL**
   - Paste any TikTok video URL
   - Supports short URLs (vm.tiktok.com) and full URLs
   - Example: `https://www.tiktok.com/@username/video/123456789`

2. **Amount**
   - Number of requests to send
   - Set to `0` for unlimited (runs until manually stopped)
   - Default: 1000

3. **Threads**
   - Number of concurrent threads
   - More threads = faster but more resource intensive
   - Recommended: 100-500
   - Maximum: 10,000

4. **Action Type**
   - 👁️ **Views**: Increases video view count
   - 🔄 **Shares**: Increases video share count

5. **Proxy Type**
   - HTTP, SOCKS4, or SOCKS5
   - Must match the proxies in your `Data/Proxies.txt` file

### 📊 Live Statistics

Real-time monitoring of your bot's performance:

- **Sent Requests**: Total number of successful requests
- **Requests/sec**: Current request rate
- **Elapsed Time**: How long the bot has been running
- **Progress**: Percentage complete (for non-unlimited tasks)

### 📋 Task History

View all your bot tasks:
- Current and past tasks
- Task status (running, completed, stopped, error)
- Performance metrics for each task
- Thread count and proxy type used

---

## 🎯 How to Use

### Step 1: Add Proxies

Before starting, add proxies to `Data/Proxies.txt`:

```
http://proxy1.example.com:8080
http://user:pass@proxy2.example.com:8080
socks5://proxy3.example.com:1080
```

**Proxy format:**
- One proxy per line
- Format: `protocol://host:port` or `protocol://user:pass@host:port`

### Step 2: Configure Bot

1. Open the web interface at http://localhost:5000
2. Enter the TikTok video URL
3. Set your desired amount (or 0 for unlimited)
4. Choose number of threads
5. Select action type (Views or Shares)
6. Select proxy type matching your proxies

### Step 3: Start Bot

1. Click the **"🚀 Start Bot"** button
2. Watch real-time statistics update
3. Monitor progress in the stats panel
4. View the task appear in Task History

### Step 4: Stop Bot (Optional)

- Click **"⛔ Stop Bot"** to stop the current task
- Or wait for it to complete automatically (if amount > 0)

---

## 🔧 API Endpoints

The web application provides a REST API for automation:

### Start a Bot Task

```bash
POST /api/start
Content-Type: application/json

{
  "video_uri": "https://www.tiktok.com/@user/video/123",
  "amount": 1000,
  "threads": 100,
  "send_type": "view",
  "proxy_type": "http"
}
```

**Response:**
```json
{
  "success": true,
  "task_id": "task_1_1234567890",
  "message": "Bot started successfully"
}
```

### Get Task Status

```bash
GET /api/status/{task_id}
```

**Response:**
```json
{
  "task_id": "task_1_1234567890",
  "video_uri": "https://www.tiktok.com/@user/video/123",
  "amount": 1000,
  "threads": 100,
  "send_type": "view",
  "proxy_type": "http",
  "sent_requests": 450,
  "completed": false,
  "status": "running",
  "elapsed_seconds": 45.2,
  "requests_per_second": 9.95
}
```

### Get All Tasks

```bash
GET /api/tasks
```

**Response:**
```json
{
  "tasks": [
    {
      "task_id": "task_1_1234567890",
      "sent_requests": 1000,
      "status": "completed",
      ...
    }
  ]
}
```

### Stop a Task

```bash
POST /api/stop/{task_id}
```

**Response:**
```json
{
  "success": true,
  "message": "Task stopped"
}
```

### Get Proxy Count

```bash
GET /api/proxies/count
```

**Response:**
```json
{
  "count": 150,
  "available": true
}
```

### Health Check

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "active_tasks": 2,
  "timestamp": "2025-10-06T12:00:00"
}
```

---

## 🔌 WebSocket Events

Real-time updates via Socket.IO:

### Client → Server

**Subscribe to task updates:**
```javascript
socket.emit('subscribe_task', { task_id: 'task_1_1234567890' });
```

### Server → Client

**Connection established:**
```javascript
socket.on('connected', (data) => {
  console.log(data); // { data: 'Connected to TikTok Bot Server' }
});
```

**Progress update:**
```javascript
socket.on('progress_update', (data) => {
  console.log(data);
  // {
  //   task_id: 'task_1_1234567890',
  //   sent_requests: 450,
  //   completed: false
  // }
});
```

**Task completed:**
```javascript
socket.on('task_completed', (data) => {
  console.log(data);
  // { task_id: '...', status: 'completed', sent_requests: 1000, ... }
});
```

---

## 💻 Using the API with cURL

### Start a bot task:

```bash
curl -X POST http://localhost:5000/api/start \
  -H "Content-Type: application/json" \
  -d '{
    "video_uri": "https://www.tiktok.com/@user/video/123",
    "amount": 1000,
    "threads": 100,
    "send_type": "view",
    "proxy_type": "http"
  }'
```

### Get task status:

```bash
curl http://localhost:5000/api/status/task_1_1234567890
```

### Stop a task:

```bash
curl -X POST http://localhost:5000/api/stop/task_1_1234567890
```

---

## 🐍 Using the API with Python

```python
import requests

# Start a bot task
response = requests.post('http://localhost:5000/api/start', json={
    'video_uri': 'https://www.tiktok.com/@user/video/123',
    'amount': 1000,
    'threads': 100,
    'send_type': 'view',
    'proxy_type': 'http'
})

data = response.json()
task_id = data['task_id']
print(f"Task started: {task_id}")

# Poll for status
import time
while True:
    status = requests.get(f'http://localhost:5000/api/status/{task_id}').json()
    print(f"Progress: {status['sent_requests']}/{status['amount']} "
          f"({status['requests_per_second']:.1f} req/s)")
    
    if status['completed']:
        print("Task completed!")
        break
    
    time.sleep(1)
```

---

## 🔒 Security Considerations

### Production Deployment

1. **Never expose to public internet without authentication**
   - Use nginx reverse proxy
   - Implement authentication middleware
   - Use HTTPS/SSL

2. **Rate Limiting**
   - Already configured in nginx.conf
   - 10 requests/second per IP

3. **Firewall**
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw deny 5000/tcp  # Block direct access
   ```

4. **Environment Variables**
   - Don't commit API keys or secrets
   - Use .env files (not committed to git)

---

## 🎨 Customization

### Change Port

Edit `web_app.py`:
```python
socketio.run(app, host='0.0.0.0', port=8080)  # Change 5000 to 8080
```

### Change Theme Colors

Edit `static/css/style.css`:
```css
:root {
    --primary-color: #00ff00;  /* Change to your color */
    --secondary-color: #0000ff;
    /* ... */
}
```

### Add Authentication

```python
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username == "admin" and password == "secret":
        return username

@app.route('/api/start', methods=['POST'])
@auth.login_required
def start_bot():
    # ... existing code
```

---

## 📈 Performance Tips

### For Maximum Speed

1. **Use more threads** (if you have good hardware):
   - Start with 100, gradually increase
   - Monitor CPU/memory usage

2. **Use high-quality proxies**:
   - Residential proxies > Datacenter proxies
   - Fresh proxies > Old proxies

3. **Optimize thread count**:
   - Too few = slow
   - Too many = resource exhaustion
   - Sweet spot: usually 100-500

### For Stability

1. **Use fewer threads** (50-100)
2. **Set amount limit** (don't use unlimited)
3. **Monitor resource usage**
4. **Use quality proxies**

---

## 🐛 Troubleshooting

### Bot Not Starting

**Check proxy count:**
- Open browser console (F12)
- Look for proxy count at top of page
- Ensure proxies are loaded

**Check browser console:**
```javascript
// Open browser console (F12) and check for errors
```

### WebSocket Disconnecting

**Check firewall settings:**
```bash
sudo ufw status
```

**Ensure nginx is configured for WebSockets** (if using nginx)

### Slow Performance

**Reduce threads:**
- Start with 50 threads
- Gradually increase

**Check proxy quality:**
- Bad proxies = slow performance
- Test proxies individually

### No Progress Updates

**Check WebSocket connection:**
- Browser console should show "Connected to server"
- Reload page if disconnected

---

## 📞 Support

- **Documentation**: See DEPLOYMENT.md for production setup
- **Performance**: See PERFORMANCE_OPTIMIZATIONS.md
- **Discord**: discord.gg/devcenter

---

## ✨ Features Showcase

### 🎯 Smart URL Parsing
- Automatically extracts video ID
- Handles short URLs (vm.tiktok.com)
- Cached for performance

### ⚡ Real-time Updates
- WebSocket-based live stats
- No page refresh needed
- Instant progress feedback

### 📊 Professional UI
- Modern dark theme
- Responsive design
- Mobile-friendly

### 🔧 Production-Ready
- Docker support
- Nginx reverse proxy
- Systemd service
- Health checks
- Logging

---

**🎉 Enjoy using the TikTok Bot Web Interface!**

For advanced deployment options, see [DEPLOYMENT.md](DEPLOYMENT.md)
