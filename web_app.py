"""
TikTok Bot Web Application
Production-ready Flask application with real-time updates
"""
import os
import time
import queue
import threading
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import secrets

# Import optimized bot functions
from main import (
    sendView, sendShare, clearURL, create_session,
    APP_NAMES, DEVICE_ID_MIN, DEVICE_ID_MAX, BASE_HEADERS
)
from utils import readProxiesFile

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global state management
active_tasks = {}
task_counter = 0
task_lock = threading.Lock()

class BotTask:
    """Represents a running bot task with stats tracking."""
    
    def __init__(self, task_id, video_uri, amount, threads, send_type, proxy_type):
        self.task_id = task_id
        self.video_uri = video_uri
        self.amount = amount
        self.threads = threads
        self.send_type = send_type  # 'view' or 'share'
        self.proxy_type = proxy_type
        
        self.item_id = None
        self.sent_requests = 0
        self.completed = False
        self.started_at = datetime.now()
        self.count_queue = queue.Queue(maxsize=10000)
        
        self.worker_threads = []
        self.status = 'initializing'
        self.error = None
    
    def to_dict(self):
        """Convert task to dictionary for JSON serialization."""
        elapsed = (datetime.now() - self.started_at).total_seconds()
        
        return {
            'task_id': self.task_id,
            'video_uri': self.video_uri,
            'amount': self.amount,
            'threads': self.threads,
            'send_type': self.send_type,
            'proxy_type': self.proxy_type,
            'sent_requests': self.sent_requests,
            'completed': self.completed,
            'status': self.status,
            'error': self.error,
            'started_at': self.started_at.isoformat(),
            'elapsed_seconds': elapsed,
            'requests_per_second': self.sent_requests / elapsed if elapsed > 0 else 0
        }

def process_requests(task):
    """Process requests in background thread."""
    try:
        # Get proxy list
        proxy_list = readProxiesFile()
        if not proxy_list:
            task.error = "No proxies available"
            task.status = 'error'
            return
        
        # Parse video URL
        try:
            task.item_id = clearURL(task.video_uri)
            task.status = 'running'
        except Exception as e:
            task.error = f"Invalid video URL: {str(e)}"
            task.status = 'error'
            return
        
        # Determine send function
        send_func = sendView if task.send_type == 'view' else sendShare
        
        # Create global variables for the worker threads
        import main
        main.itemID = task.item_id
        main.proxyType = task.proxy_type
        main.proxyList = proxy_list
        main.amount = task.amount
        main.completed = False
        main.sentRequests = 0
        main.countQueue = task.count_queue
        
        def worker():
            """Worker thread that sends requests."""
            while not task.completed and not main.completed:
                try:
                    if send_func():
                        task.count_queue.put(1, block=False)
                except queue.Full:
                    time.sleep(0.001)
                except Exception:
                    pass
        
        def counter():
            """Count successful requests."""
            while not task.completed:
                try:
                    task.count_queue.get(timeout=1)
                    task.sent_requests += 1
                    main.sentRequests = task.sent_requests
                    
                    # Emit progress update via SocketIO
                    socketio.emit('progress_update', {
                        'task_id': task.task_id,
                        'sent_requests': task.sent_requests,
                        'completed': task.completed
                    })
                    
                    if task.amount > 0 and task.sent_requests >= task.amount:
                        task.completed = True
                        main.completed = True
                        task.status = 'completed'
                        break
                except queue.Empty:
                    if task.completed:
                        break
        
        # Start counter thread
        counter_thread = threading.Thread(target=counter, daemon=True)
        counter_thread.start()
        
        # Start worker threads
        for i in range(task.threads):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            task.worker_threads.append(t)
        
        # Wait for completion or timeout
        counter_thread.join()
        
        if not task.error:
            task.status = 'completed'
        
    except Exception as e:
        task.error = str(e)
        task.status = 'error'
    finally:
        task.completed = True
        socketio.emit('task_completed', task.to_dict())

@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start_bot():
    """Start a new bot task."""
    global task_counter
    
    try:
        data = request.json
        
        # Validate input
        video_uri = data.get('video_uri', '').strip()
        amount = int(data.get('amount', 0))
        threads = int(data.get('threads', 100))
        send_type = data.get('send_type', 'view')  # 'view' or 'share'
        proxy_type = data.get('proxy_type', 'http')  # 'http', 'socks4', 'socks5'
        
        if not video_uri:
            return jsonify({'error': 'Video URI is required'}), 400
        
        if threads < 1 or threads > 10000:
            return jsonify({'error': 'Threads must be between 1 and 10000'}), 400
        
        if send_type not in ['view', 'share']:
            return jsonify({'error': 'Invalid send type'}), 400
        
        if proxy_type not in ['http', 'socks4', 'socks5']:
            return jsonify({'error': 'Invalid proxy type'}), 400
        
        # Create new task
        with task_lock:
            task_counter += 1
            task_id = f"task_{task_counter}_{int(time.time())}"
        
        task = BotTask(task_id, video_uri, amount, threads, send_type, proxy_type)
        active_tasks[task_id] = task
        
        # Start background processing
        threading.Thread(target=process_requests, args=(task,), daemon=True).start()
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': 'Bot started successfully'
        })
    
    except ValueError as e:
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status/<task_id>')
def get_status(task_id):
    """Get status of a specific task."""
    task = active_tasks.get(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task.to_dict())

@app.route('/api/tasks')
def get_tasks():
    """Get all active tasks."""
    return jsonify({
        'tasks': [task.to_dict() for task in active_tasks.values()]
    })

@app.route('/api/stop/<task_id>', methods=['POST'])
def stop_task(task_id):
    """Stop a running task."""
    task = active_tasks.get(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    task.completed = True
    task.status = 'stopped'
    
    return jsonify({
        'success': True,
        'message': 'Task stopped'
    })

@app.route('/api/proxies/count')
def proxy_count():
    """Get number of available proxies."""
    try:
        proxies = readProxiesFile()
        return jsonify({
            'count': len(proxies),
            'available': len(proxies) > 0
        })
    except Exception as e:
        return jsonify({
            'count': 0,
            'available': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'active_tasks': len(active_tasks),
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print('Client connected')
    emit('connected', {'data': 'Connected to TikTok Bot Server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print('Client disconnected')

@socketio.on('subscribe_task')
def handle_subscribe(data):
    """Subscribe to task updates."""
    task_id = data.get('task_id')
    if task_id in active_tasks:
        emit('subscribed', {'task_id': task_id})

if __name__ == '__main__':
    # Create Data directory if it doesn't exist
    os.makedirs('Data', exist_ok=True)
    
    # Create empty proxies file if it doesn't exist
    if not os.path.exists('Data/Proxies.txt'):
        with open('Data/Proxies.txt', 'w') as f:
            f.write('')
    
    print("🚀 Starting TikTok Bot Web Application...")
    print("📡 Access the web interface at: http://localhost:5000")
    print("🔧 API documentation available at: http://localhost:5000/health")
    
    # Run with SocketIO
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
