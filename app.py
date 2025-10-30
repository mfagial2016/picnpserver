from flask import Flask, request, jsonify, render_template_string
import threading
import time
import random
import os
import uuid
import json
from datetime import datetime
import requests

app = Flask(__name__)

# Store active tasks
active_tasks = {}
task_logs = {}
user_count = 0

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>C0NV3 WITH MULTI PHOTOS(R0W3DY KIING)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-image: url('https://i.postimg.cc/Z5wmsr9W/f7c75ce99a9e6bd368e3c2433dc6048a.gif');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: white;
            min-height: 100vh;
        }
        .user-counter {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(78, 205, 196, 0.9);
            color: white;
            padding: 15px 25px;
            border-radius: 50px;
            font-weight: bold;
            font-size: 18px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .user-counter .pulse {
            width: 12px;
            height: 12px;
            background: #00ff00;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.2); }
        }
        .container {
            max-width: 900px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-top: 50px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        .form-control {
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            border-radius: 10px;
            padding: 12px;
        }
        .form-control::placeholder { color: rgba(255, 255, 255, 0.7); }
        .form-control:focus {
            background: rgba(255, 255, 255, 0.3);
            border-color: #4ecdc4;
            color: white;
        }
        .btn-primary {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            border: none;
            border-radius: 10px;
            padding: 12px 30px;
            font-weight: bold;
        }
        .btn-danger {
            background: linear-gradient(45deg, #ff4757, #ff3838);
            border: none;
            border-radius: 10px;
            padding: 12px 30px;
            font-weight: bold;
        }
        .btn-success {
            background: linear-gradient(45deg, #26de81, #20bf6b);
            border: none;
            border-radius: 10px;
            padding: 8px 20px;
            font-weight: bold;
        }
        .console-output {
            background: #000;
            color: #00ff00;
            padding: 15px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 12px;
            height: 300px;
            overflow-y: auto;
        }
        h1 {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
            text-align: center;
        }
        .daddys-logo {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            margin: 0 auto 20px;
            display: block;
            border: 3px solid #4ecdc4;
            object-fit: cover;
        }
        .alert {
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .feature-badge {
            display: inline-block;
            background: rgba(78, 205, 196, 0.3);
            padding: 5px 10px;
            border-radius: 5px;
            margin: 5px;
            font-size: 12px;
        }
        .task-id-box {
            display: none;
            background: rgba(78, 205, 196, 0.2);
            border: 2px solid #4ecdc4;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            text-align: center;
            animation: slideDown 0.5s ease-out;
        }
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .task-id-box.show {
            display: block;
        }
        .task-id-text {
            font-size: 24px;
            font-weight: bold;
            color: #4ecdc4;
            margin: 10px 0;
            font-family: monospace;
        }
        .copy-notification {
            display: none;
            color: #26de81;
            font-weight: bold;
            margin-top: 10px;
            animation: fadeIn 0.3s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .copy-notification.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="user-counter">
        <div class="pulse"></div>
        <span id="userCount">👥 0 Users</span>
    </div>
    
    <audio id="bgMusic" loop>
        <source src="/static/bgmusic.mp3" type="audio/mpeg">
    </audio>
    
    <div class="container">
        <img src="https://i.postimg.cc/QMNQhrxk/459c85fcaa5d9f0762479bf382225ac6.jpg" alt="Prince" class="daddys-logo">
        <h1>CONVO WITH MULTI IMAGE (R0W3DY KIING)</h1>
        <p class="text-center">
            <span class="feature-badge">🔄 Photo Cycling Mode</span>
            <span class="feature-badge">🖼️ Multi-Photo Upload</span>
            <span class="feature-badge">👤 राजस्थान सरकार</span>
            <span class="feature-badge">⚡ Smart server</span>
        </p>
        
        <!-- Task ID Display Box -->
        <div id="taskIdBox" class="task-id-box">
            <h4>✅ Task ID Generated!</h4>
            <p>Your Task ID:</p>
            <div class="task-id-text" id="taskIdDisplay">-</div>
            <button class="btn btn-success" onclick="copyTaskId()">📋 Copy Task ID</button>
            <div id="copyNotification" class="copy-notification">✓ Task ID Copied!</div>
        </div>
        
        <!-- Generate Task ID Button -->
        <div class="text-center mb-4">
            <button class="btn btn-primary" onclick="generateTaskId()" style="font-size: 18px; padding: 15px 40px;">
                Generate Task ID
            </button>
            <p class="mt-2" style="font-size: 14px;">Click to generate Task ID before starting</p>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <form method="post" action="/start" enctype="multipart/form-data" id="mainForm">
                    <input type="hidden" name="taskId" id="hiddenTaskId" value="">
                    
                    <div class="mb-3">
                        <label class="form-label">Access Tokens</label>
                        <textarea class="form-control" name="tokens" rows="4" placeholder="Enter tokens (one per line)..."></textarea>
                        <small class="text-muted">Or upload a token file below</small>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Or Upload Token File (.txt)</label>
                        <input type="file" class="form-control" name="tokenFile" accept=".txt">
                        <small class="text-muted">if not used one token</small>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Thread/Conversation ID</label>
                        <input type="text" class="form-control" name="threadId" required>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Message Prefix</label>
                        <input type="text" class="form-control" name="prefix" required>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Time Interval (seconds)</label>
                        <input type="number" class="form-control" name="interval" min="1" value="30" required>
                        <small class="text-muted">±10 second jitter will be added automatically</small>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Messages File (.txt)</label>
                        <input type="file" class="form-control" name="messagesFile" accept=".txt" required>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Images (Optional - Multiple)</label>
                        <input type="file" class="form-control" name="imageFiles" accept="image/*" multiple>
                        <small class="text-muted">📷 1 photo: Repeats with every msg | Multiple: Cycles (Photo→Msg→Photo→Msg)</small>
                    </div>
                    
                    <button type="submit" class="btn btn-primary w-100" id="startBtn">🚀 Start Sending</button>
                </form>
            </div>
            
            <div class="col-md-6">
                <h4>Console Output</h4>
                <div class="mb-2">
                    <input type="text" class="form-control" id="taskId" placeholder="Enter Task ID">
                    <button class="btn btn-primary mt-2" onclick="loadConsole()">Load Console</button>
                </div>
                <div id="console" class="console-output">Console output will appear here...</div>
                
                <div class="mt-3">
                    <h5>Stop Task</h5>
                    <form method="post" action="/stop">
                        <input type="text" class="form-control mb-2" name="taskId" placeholder="Task ID" required>
                        <button type="submit" class="btn btn-danger w-100">⏹️ Stop</button>
                    </form>
                </div>
            </div>
        </div>
        
        <div class="text-center mt-4">
            <p>DEVELOPED BY ROWEDY KING </p>
        </div>
    </div>
    
    <script>
        let musicStarted = false;
        const bgMusic = document.getElementById('bgMusic');
        
        function startMusic() {
            if (!musicStarted && bgMusic) {
                bgMusic.volume = 0.5;
                const playPromise = bgMusic.play();
                
                if (playPromise !== undefined) {
                    playPromise
                        .then(() => {
                            musicStarted = true;
                            console.log('Music started successfully');
                        })
                        .catch(e => {
                            console.log('Music play failed:', e);
                        });
                }
            }
        }
        
        ['click', 'touchstart', 'keydown', 'mousemove'].forEach(eventType => {
            document.addEventListener(eventType, startMusic, { once: true });
        });
        
        function updateUserCount() {
            fetch('/api/user-count')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('userCount').textContent = `👮🏻 ${data.count} User${data.count !== 1 ? 's' : ''}`;
                })
                .catch(e => console.log('Error updating user count:', e));
        }
        
        updateUserCount();
        setInterval(updateUserCount, 3000);
        
        function loadConsole() {
            const taskId = document.getElementById('taskId').value;
            if (!taskId) return;
            
            fetch(`/console/${taskId}`)
                .then(r => r.json())
                .then(data => {
                    const output = data.map(log => `[${log.timestamp}] ${log.message}`).join('\\n');
                    document.getElementById('console').innerHTML = output || 'No output';
                    const consoleDiv = document.getElementById('console');
                    consoleDiv.scrollTop = consoleDiv.scrollHeight;
                });
        }
        
        setInterval(() => {
            const taskId = document.getElementById('taskId').value;
            if (taskId) loadConsole();
        }, 2000);
        
        // Handle form submission with AJAX
        const mainForm = document.getElementById('mainForm');
        const startBtn = document.getElementById('startBtn');
        
        if (mainForm) {
            mainForm.addEventListener('submit', async function(e) {
                e.preventDefault();
                
                startBtn.disabled = true;
                startBtn.innerHTML = '⏳ Starting...';
                
                const formData = new FormData(mainForm);
                
                try {
                    const response = await fetch('/start', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (result.success && result.task_id) {
                        // Show Task ID on same page
                        document.getElementById('taskIdDisplay').textContent = result.task_id;
                        document.getElementById('taskIdBox').classList.add('show');
                        
                        // Auto-load console for this task
                        document.getElementById('taskId').value = result.task_id;
                        loadConsole();
                        
                        startBtn.disabled = false;
                        startBtn.innerHTML = '🚀 Start Sending';
                    } else {
                        alert('Error: ' + (result.error || 'Failed to start task'));
                        startBtn.disabled = false;
                        startBtn.innerHTML = '🚀 Start Sending';
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('Failed to start task. Please try again.');
                    startBtn.disabled = false;
                    startBtn.innerHTML = '🚀 Start Sending';
                }
            });
        }
        
        function copyTaskId() {
            const taskId = document.getElementById('taskIdDisplay').textContent;
            navigator.clipboard.writeText(taskId).then(() => {
                const notification = document.getElementById('copyNotification');
                notification.classList.add('show');
                setTimeout(() => {
                    notification.classList.remove('show');
                }, 2000);
            });
        }
        
        async function generateTaskId() {
            try {
                const response = await fetch('/generate-task-id', {
                    method: 'POST'
                });
                
                const result = await response.json();
                
                if (result.success && result.task_id) {
                    // Show Task ID on same page
                    document.getElementById('taskIdDisplay').textContent = result.task_id;
                    document.getElementById('taskIdBox').classList.add('show');
                    
                    // Auto-fill in console input
                    document.getElementById('taskId').value = result.task_id;
                    
                    // Store in hidden field for form submission
                    document.getElementById('hiddenTaskId').value = result.task_id;
                    
                    // Store in session for later use
                    sessionStorage.setItem('currentTaskId', result.task_id);
                } else {
                    alert('Error generating Task ID');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to generate Task ID');
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/user-count')
def user_count_api():
    return jsonify({"count": user_count})

@app.route('/generate-task-id', methods=['POST'])
def generate_task_id():
    task_id = str(uuid.uuid4())[:8]
    task_logs[task_id] = []
    return jsonify({"success": True, "task_id": task_id})

def log(task_id, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if task_id in task_logs:
        task_logs[task_id].append({"timestamp": timestamp, "message": message})
        # Keep only last 1000 logs
        if len(task_logs[task_id]) > 1000:
            task_logs[task_id] = task_logs[task_id][-1000:]

def send_message(token, thread_id, message, image_path=None):
    url = f"https://graph.facebook.com/v18.0/{thread_id}/messages"
    
    if image_path:
        # Send image with message as caption
        files = {
            'filedata': open(image_path, 'rb')
        }
        data = {
            "messaging_type": "UPDATE",
            "recipient": json.dumps({"id": thread_id}),
            "message": json.dumps({"attachment": {"type": "image", "payload": {}}}),
            "access_token": token
        }
    else:
        # Send text message only
        files = None
        data = {
            "messaging_type": "UPDATE",
            "recipient": json.dumps({"id": thread_id}),
            "message": json.dumps({"text": message}),
            "access_token": token
        }

    try:
        if files:
            response = requests.post(url, data=data, files=files, timeout=30)
        else:
            response = requests.post(url, data=data, timeout=30)
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending message: {e}")
        return False
    finally:
        if files:
            for file in files.values():
                if hasattr(file, 'close'):
                    file.close()

def worker(task_id):
    data = active_tasks[task_id]
    tokens = data['tokens']
    thread_id = data['thread_id']
    prefix = data['prefix']
    interval = data['interval']
    messages = data['messages']
    images = data['images']
    
    token_idx = 0
    msg_idx = 0
    img_idx = 0
    
    log(task_id, f"🚀 Worker started with {len(tokens)} tokens, {len(messages)} messages, {len(images)} images")
    
    while active_tasks.get(task_id):
        try:
            # Get current token, message and image
            token = tokens[token_idx % len(tokens)]
            message = f"{prefix} {messages[msg_idx % len(messages)]}".strip()
            
            # Decide which image to use
            image_path = None
            if images:
                if len(images) == 1:
                    # Single image: use with every message
                    image_path = images[0]
                else:
                    # Multiple images: cycle through them
                    image_path = images[img_idx % len(images)]
                    img_idx += 1
            
            # Send message
            success = send_message(token, thread_id, message, image_path)
            
            # Log result
            status = "✅ Sent" if success else "❌ Failed"
            log_type = "📷 Image+Text" if image_path else "💬 Text"
            log(task_id, f"[{token[:8]}...] {log_type}: {message[:50]}... {status}")
            
            # Move to next token and message
            token_idx += 1
            msg_idx += 1
            
            # Sleep with jitter
            sleep_time = interval + random.randint(-10, 10)
            time.sleep(max(1, sleep_time))
            
        except Exception as e:
            log(task_id, f"❌ Error in worker: {str(e)}")
            time.sleep(10)
    
    log(task_id, "🛑 Task stopped by user")

@app.route('/start', methods=['POST'])
def start():
    global user_count
    user_count += 1

    task_id = request.form.get('taskId')
    if not task_id or task_id not in task_logs:
        return jsonify({"success": False, "error": "Invalid Task ID. Please generate Task ID first."})

    # Handle tokens
    tokens = request.form.get('tokens', '').strip().splitlines()
    
    # Handle token file upload
    if 'tokenFile' in request.files and request.files['tokenFile'].filename:
        file = request.files['tokenFile']
        if file.filename.endswith('.txt'):
            file_tokens = file.read().decode().splitlines()
            tokens.extend(file_tokens)

    # Filter valid tokens
    tokens = [t.strip() for t in tokens if t.strip() and 'EA' in t]
    
    if not tokens:
        return jsonify({"success": False, "error": "No valid tokens found. Tokens should contain 'EA'."})

    # Handle messages file
    if 'messagesFile' not in request.files or not request.files['messagesFile'].filename:
        return jsonify({"success": False, "error": "Messages file is required"})
    
    messages_file = request.files['messagesFile']
    if not messages_file.filename.endswith('.txt'):
        return jsonify({"success": False, "error": "Messages file must be a .txt file"})
    
    messages = messages_file.read().decode().splitlines()
    messages = [m.strip() for m in messages if m.strip()]

    if not messages:
        return jsonify({"success": False, "error": "No valid messages found in the file"})

    # Handle images
    images = []
    if 'imageFiles' in request.files:
        for file in request.files.getlist('imageFiles'):
            if file.filename and file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # Create uploads directory if not exists
                os.makedirs('uploads', exist_ok=True)
                
                # Save file with unique name
                filename = f"{task_id}_{uuid.uuid4().hex[:8]}_{file.filename}"
                file_path = os.path.join('uploads', filename)
                file.save(file_path)
                images.append(file_path)

    # Get other form data
    thread_id = request.form.get('threadId', '').strip()
    prefix = request.form.get('prefix', '').strip()
    
    try:
        interval = int(request.form.get('interval', 30))
    except ValueError:
        interval = 30

    if not thread_id:
        return jsonify({"success": False, "error": "Thread ID is required"})

    # Store task data and start worker
    active_tasks[task_id] = {
        'tokens': tokens,
        'thread_id': thread_id,
        'prefix': prefix,
        'interval': interval,
        'messages': messages,
        'images': images
    }

    # Start worker thread
    thread = threading.Thread(target=worker, args=(task_id,), daemon=True)
    thread.start()

    log(task_id, f"✅ Task started successfully!")
    log(task_id, f"📊 Stats: {len(tokens)} tokens, {len(messages)} messages, {len(images)} images")
    log(task_id, f"⏰ Interval: {interval} seconds (±10s jitter)")
    
    return jsonify({"success": True, "task_id": task_id})

@app.route('/stop', methods=['POST'])
def stop():
    task_id = request.form.get('taskId')
    if task_id in active_tasks:
        del active_tasks[task_id]
        log(task_id, "🛑 Task stopped by user")
        return jsonify({"success": True, "message": "Task stopped"})
    return jsonify({"success": False, "error": "Task not found"})

@app.route('/console/<task_id>')
def console(task_id):
    return jsonify(task_logs.get(task_id, []))

# Create necessary directories
os.makedirs('uploads', exist_ok=True)

if __name__ == '__main__':
    print("🚀 R0W3DY KIING Tool Starting...")
    print("📧 Developed by Rowedy King")
    print("🌐 Server running on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
