// TikTok Bot Web Interface - Client-side JavaScript
let socket;
let currentTaskId = null;
let statsInterval = null;
let startTime = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeSocketIO();
    loadProxyCount();
    setupEventListeners();
    loadActiveTasks();
});

// Initialize Socket.IO connection
function initializeSocketIO() {
    socket = io();
    
    socket.on('connect', function() {
        updateConnectionStatus(true);
        showNotification('Connected to server', 'success');
    });
    
    socket.on('disconnect', function() {
        updateConnectionStatus(false);
        showNotification('Disconnected from server', 'warning');
    });
    
    socket.on('progress_update', function(data) {
        if (data.task_id === currentTaskId) {
            updateStats(data);
        }
    });
    
    socket.on('task_completed', function(data) {
        if (data.task_id === currentTaskId) {
            handleTaskCompleted(data);
        }
    });
}

// Update connection status indicator
function updateConnectionStatus(connected) {
    const statusBadge = document.getElementById('connectionStatus');
    if (connected) {
        statusBadge.classList.add('connected');
        statusBadge.querySelector('span:last-child').textContent = 'Connected';
    } else {
        statusBadge.classList.remove('connected');
        statusBadge.querySelector('span:last-child').textContent = 'Disconnected';
    }
}

// Setup event listeners
function setupEventListeners() {
    document.getElementById('startBtn').addEventListener('click', startBot);
    document.getElementById('stopBtn').addEventListener('click', stopBot);
}

// Load proxy count
async function loadProxyCount() {
    try {
        const response = await fetch('/api/proxies/count');
        const data = await response.json();
        
        const proxyCountEl = document.getElementById('proxyCount');
        if (data.available && data.count > 0) {
            proxyCountEl.innerHTML = `<strong style="color: var(--success-color)">${data.count.toLocaleString()}</strong> proxies loaded and ready`;
        } else {
            proxyCountEl.innerHTML = `<strong style="color: var(--danger-color)">No proxies available</strong> - Add proxies to Data/Proxies.txt`;
        }
    } catch (error) {
        console.error('Error loading proxy count:', error);
        document.getElementById('proxyCount').textContent = 'Error loading proxies';
    }
}

// Start bot
async function startBot() {
    const videoUrl = document.getElementById('videoUrl').value.trim();
    const amount = parseInt(document.getElementById('amount').value);
    const threads = parseInt(document.getElementById('threads').value);
    const sendType = document.getElementById('sendType').value;
    const proxyType = document.getElementById('proxyType').value;
    
    // Validation
    if (!videoUrl) {
        showNotification('Please enter a TikTok video URL', 'error');
        return;
    }
    
    if (threads < 1 || threads > 10000) {
        showNotification('Threads must be between 1 and 10000', 'error');
        return;
    }
    
    // Disable start button, enable stop button
    document.getElementById('startBtn').disabled = true;
    document.getElementById('stopBtn').disabled = false;
    
    try {
        const response = await fetch('/api/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                video_uri: videoUrl,
                amount: amount,
                threads: threads,
                send_type: sendType,
                proxy_type: proxyType
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentTaskId = data.task_id;
            startTime = Date.now();
            showNotification('Bot started successfully! 🚀', 'success');
            updateStatusMessage('Bot is running...', 'active');
            
            // Start stats polling
            startStatsPolling();
            
            // Subscribe to real-time updates
            socket.emit('subscribe_task', { task_id: currentTaskId });
        } else {
            throw new Error(data.error || 'Failed to start bot');
        }
    } catch (error) {
        showNotification(error.message, 'error');
        document.getElementById('startBtn').disabled = false;
        document.getElementById('stopBtn').disabled = true;
    }
}

// Stop bot
async function stopBot() {
    if (!currentTaskId) return;
    
    try {
        const response = await fetch(`/api/stop/${currentTaskId}`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Bot stopped', 'warning');
            handleTaskCompleted({ status: 'stopped' });
        }
    } catch (error) {
        showNotification('Error stopping bot: ' + error.message, 'error');
    }
}

// Start stats polling
function startStatsPolling() {
    if (statsInterval) clearInterval(statsInterval);
    
    statsInterval = setInterval(async () => {
        if (!currentTaskId) return;
        
        try {
            const response = await fetch(`/api/status/${currentTaskId}`);
            const data = await response.json();
            
            updateStats(data);
            
            if (data.completed) {
                handleTaskCompleted(data);
            }
        } catch (error) {
            console.error('Error polling stats:', error);
        }
    }, 1000);
}

// Update statistics display
function updateStats(data) {
    // Update sent requests
    document.getElementById('sentRequests').textContent = data.sent_requests?.toLocaleString() || '0';
    
    // Update requests per second
    const rps = Math.round(data.requests_per_second || 0);
    document.getElementById('requestsPerSec').textContent = rps.toLocaleString();
    
    // Update elapsed time
    const elapsed = data.elapsed_seconds || 0;
    document.getElementById('elapsed').textContent = formatTime(elapsed);
    
    // Update progress
    if (data.amount > 0) {
        const progress = Math.min(100, (data.sent_requests / data.amount) * 100);
        document.getElementById('progress').textContent = progress.toFixed(1) + '%';
        document.getElementById('progressBar').style.width = progress + '%';
    } else {
        document.getElementById('progress').textContent = '∞';
        document.getElementById('progressBar').style.width = '100%';
    }
}

// Handle task completion
function handleTaskCompleted(data) {
    clearInterval(statsInterval);
    statsInterval = null;
    currentTaskId = null;
    
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
    
    if (data.status === 'completed') {
        updateStatusMessage(`✓ Completed! ${data.sent_requests?.toLocaleString() || 0} requests sent`, 'success');
        showNotification('Task completed successfully! 🎉', 'success');
    } else if (data.status === 'error') {
        updateStatusMessage('✗ Error: ' + (data.error || 'Unknown error'), 'error');
        showNotification('Task failed: ' + (data.error || 'Unknown error'), 'error');
    } else {
        updateStatusMessage('Task stopped', 'warning');
    }
    
    loadActiveTasks();
}

// Update status message
function updateStatusMessage(message, type = '') {
    const statusEl = document.getElementById('statusMessage');
    statusEl.textContent = message;
    statusEl.className = 'status-message';
    if (type) statusEl.classList.add(type);
}

// Load active tasks
async function loadActiveTasks() {
    try {
        const response = await fetch('/api/tasks');
        const data = await response.json();
        
        const tasksList = document.getElementById('tasksList');
        
        if (data.tasks && data.tasks.length > 0) {
            tasksList.innerHTML = data.tasks.map(task => createTaskHTML(task)).join('');
        } else {
            tasksList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">📭</div>
                    <p>No tasks yet. Start a bot to see it here!</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

// Create task HTML
function createTaskHTML(task) {
    const statusClass = task.status === 'running' ? 'running' : 
                       task.status === 'completed' ? 'completed' : 'error';
    
    const icon = task.send_type === 'view' ? '👁️' : '🔄';
    
    return `
        <div class="task-item">
            <div class="task-icon">${icon}</div>
            <div class="task-details">
                <h4>${task.send_type === 'view' ? 'View Bot' : 'Share Bot'} - ${task.sent_requests.toLocaleString()} requests</h4>
                <div class="task-meta">
                    <span>⚡ ${task.threads} threads</span>
                    <span>🌐 ${task.proxy_type}</span>
                    <span>⏱️ ${formatTime(task.elapsed_seconds)}</span>
                    <span>📊 ${Math.round(task.requests_per_second)}/s</span>
                </div>
            </div>
            <div class="task-status ${statusClass}">
                ${task.status.toUpperCase()}
            </div>
        </div>
    `;
}

// Format time
function formatTime(seconds) {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hrs > 0) {
        return `${hrs}h ${mins}m ${secs}s`;
    } else if (mins > 0) {
        return `${mins}m ${secs}s`;
    } else {
        return `${secs}s`;
    }
}

// Show notification
function showNotification(message, type = 'info') {
    // Simple console log for now - you can enhance this with a toast library
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    // Update status message
    updateStatusMessage(message, type);
}
