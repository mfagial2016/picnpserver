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
                <form id="mainForm" enctype="multipart/form-data">
                    <input type="hidden" name="taskId" id="hiddenTaskId" value="">
                    
                    <div class="mb-3">
                        <label class="form-label">Access Tokens</label>
                        <textarea class="form-control" name="tokens" rows="4" placeholder="Enter Facebook Page Access Tokens (one per line)..."></textarea>
                        <small class="text-muted">Use Facebook Page Access Tokens only</small>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Or Upload Token File (.txt)</label>
                        <input type="file" class="form-control" name="tokenFile" accept=".txt">
                        <small class="text-muted">Each token on new line</small>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Thread/Conversation ID</label>
                        <input type="text" class="form-control" name="threadId" required placeholder="Facebook Page Scoped ID (PSID)">
                        <small class="text-muted">User's Page Scoped ID (PSID)</small>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Message Prefix</label>
                        <input type="text" class="form-control" name="prefix" required placeholder="Hi! ">
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Time Interval (seconds)</label>
                        <input type="number" class="form-control" name="interval" min="10" value="30" required>
                        <small class="text-muted">Minimum 10 seconds recommended</small>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Messages File (.txt)</label>
                        <input type="file" class="form-control" name="messagesFile" accept=".txt" required>
                        <small class="text-muted">One message per line</small>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Images (Optional - Multiple)</label>
                        <input type="file" class="form-control" name="imageFiles" accept="image/*" multiple>
                        <small class="text-muted">📷 Cycle: Text → Image+Text → Text → Image+Text</small>
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
                    <input type="text" class="form-control mb-2" id="stopTaskId" placeholder="Task ID" required>
                    <button class="btn btn-danger w-100" onclick="stopTask()">⏹️ Stop Task</button>
                </div>
            </div>
        </div>
        
        <div class="text-center mt-4">
            <p>DEVELOPED BY ROWEDY KING</p>
        </div>
    </div>
    
    <script>
        function updateUserCount() {
            fetch('/api/user-count')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('userCount').textContent = `👥 ${data.count} User${data.count !== 1 ? 's' : ''}`;
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
                        document.getElementById('stopTaskId').value = result.task_id;
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
        
        async function stopTask() {
            const taskId = document.getElementById('stopTaskId').value;
            if (!taskId) {
                alert('Please enter Task ID');
                return;
            }
            
            try {
                const response = await fetch('/stop', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ taskId: taskId })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    alert('Task stopped successfully!');
                    loadConsole();
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to stop task');
            }
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
                    document.getElementById('stopTaskId').value = result.task_id;
                    
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

def send_text_message(token, recipient_id, message):
    """Send text message using Facebook Graph API v22.0"""
    url = f"https://graph.facebook.com/v22.0/me/messages"
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    payload = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message
        },
        "messaging_type": "MESSAGE_TAG",
        "tag": "NON_PROMOTIONAL_SUBSCRIPTION"
    }
    
    params = {
        "access_token": token
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            params=params,
            timeout=30
        )
        
        response_data = response.json()
        
        if response.status_code == 200:
            return True, "Message sent successfully"
        else:
            error_msg = f"HTTP {response.status_code}"
            if 'error' in response_data:
                error_msg = response_data['error'].get('message', error_msg)
            return False, error_msg
            
    except Exception as e:
        return False, f"Request failed: {str(e)}"

def send_image_message(token, recipient_id, message, image_url):
    """Send image with text using Facebook Graph API v22.0"""
    url = f"https://graph.facebook.com/v22.0/me/messages"
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    payload = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": image_url,
                    "is_reusable": True
                }
            }
        },
        "messaging_type": "MESSAGE_TAG",
        "tag": "NON_PROMOTIONAL_SUBSCRIPTION"
    }
    
    params = {
        "access_token": token
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            params=params,
            timeout=30
        )
        
        response_data = response.json()
        
        if response.status_code == 200:
            # Send text message separately after image
            time.sleep(2)
            text_success, text_msg = send_text_message(token, recipient_id, message)
            if text_success:
                return True, "Image and text sent successfully"
            else:
                return False, f"Image sent but text failed: {text_msg}"
        else:
            error_msg = f"HTTP {response.status_code}"
            if 'error' in response_data:
                error_msg = response_data['error'].get('message', error_msg)
            return False, error_msg
            
    except Exception as e:
        return False, f"Request failed: {str(e)}"

def upload_image_to_facebook(token, image_path):
    """Upload image to Facebook and get attachment ID"""
    upload_url = f"https://graph.facebook.com/v22.0/me/message_attachments"
    
    try:
        with open(image_path, 'rb') as image_file:
            files = {
                'filedata': image_file
            }
            data = {
                'message': json.dumps({
                    'attachment': {
                        'type': 'image',
                        'payload': {
                            'is_reusable': True
                        }
                    }
                })
            }
            params = {
                'access_token': token
            }
            
            response = requests.post(
                upload_url,
                files=files,
                data=data,
                params=params,
                timeout=30
            )
            
            response_data = response.json()
            
            if response.status_code == 200:
                attachment_id = response_data.get('attachment_id')
                if attachment_id:
                    return True, attachment_id
                else:
                    return False, "No attachment ID in response"
            else:
                error_msg = f"Upload failed: HTTP {response.status_code}"
                if 'error' in response_data:
                    error_msg = response_data['error'].get('message', error_msg)
                return False, error_msg
                
    except Exception as e:
        return False, f"Upload failed: {str(e)}"

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
    
    # Pre-upload images and get their Facebook URLs
    image_urls = []
    if images:
        log(task_id, "📤 Uploading images to Facebook...")
        for i, image_path in enumerate(images):
            success, result = upload_image_to_facebook(tokens[0], image_path)
            if success:
                image_urls.append(f"https://graph.facebook.com/v22.0/{result}")
                log(task_id, f"✅ Image {i+1} uploaded successfully")
            else:
                log(task_id, f"❌ Failed to upload image {i+1}: {result}")
    
    while active_tasks.get(task_id):
        try:
            # Get current token and message
            token = tokens[token_idx % len(tokens)]
            current_message = messages[msg_idx % len(messages)]
            full_message = f"{prefix} {current_message}".strip()
            
            # Decide what to send
            if images and image_urls:
                # Alternate between text and image+text
                if msg_idx % 2 == 0:  # Even index: send text only
                    success, detail = send_text_message(token, thread_id, full_message)
                    log_type = "💬 Text"
                else:  # Odd index: send image with text
                    current_image_url = image_urls[img_idx % len(image_urls)]
                    success, detail = send_image_message(token, thread_id, full_message, current_image_url)
                    log_type = f"📷 Image {img_idx % len(image_urls) + 1}"
                    img_idx += 1
            else:
                # No images, send text only
                success, detail = send_text_message(token, thread_id, full_message)
                log_type = "💬 Text"
            
            # Log result
            if success:
                status = "✅ Sent"
            else:
                status = f"❌ Failed: {detail}"
            
            log(task_id, f"[{token[:12]}...] {log_type}: {full_message[:40]}... {status}")
            
            # Move to next token and message
            token_idx += 1
            msg_idx += 1
            
            # Sleep with jitter
            sleep_time = interval + random.randint(-5, 5)
            time.sleep(max(10, sleep_time))  # Minimum 10 seconds
            
        except Exception as e:
            log(task_id, f"❌ Worker error: {str(e)}")
            time.sleep(10)
    
    log(task_id, "🛑 Task stopped")

@app.route('/start', methods=['POST'])
def start():
    global user_count
    user_count += 1

    task_id = request.form.get('taskId')
    if not task_id or task_id not in task_logs:
        return jsonify({"success": False, "error": "Invalid Task ID. Please generate Task ID first."})

    # Handle tokens
    tokens_text = request.form.get('tokens', '')
    tokens = [t.strip() for t in tokens_text.splitlines() if t.strip()]
    
    # Handle token file upload
    if 'tokenFile' in request.files:
        file = request.files['tokenFile']
        if file and file.filename and file.filename.endswith('.txt'):
            file_tokens = file.read().decode('utf-8', errors='ignore').splitlines()
            tokens.extend([t.strip() for t in file_tokens if t.strip()])

    # Filter valid Facebook Page Access Tokens
    tokens = [t for t in tokens if t and len(t) > 100 and ('EA' in t or 'EAA' in t)]
    
    if not tokens:
        return jsonify({"success": False, "error": "No valid Facebook Page Access Tokens found. Tokens should start with EA and be long strings."})

    # Handle messages file
    if 'messagesFile' not in request.files:
        return jsonify({"success": False, "error": "Messages file is required"})
    
    messages_file = request.files['messagesFile']
    if not messages_file.filename:
        return jsonify({"success": False, "error": "Messages file is required"})
    
    messages = messages_file.read().decode('utf-8', errors='ignore').splitlines()
    messages = [m.strip() for m in messages if m.strip()]

    if not messages:
        return jsonify({"success": False, "error": "No valid messages found in the file"})

    # Handle images
    images = []
    if 'imageFiles' in request.files:
        for file in request.files.getlist('imageFiles'):
            if file and file.filename:
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
        if interval < 10:
            interval = 10  # Minimum interval
    except ValueError:
        interval = 30

    if not thread_id:
        return jsonify({"success": False, "error": "Thread ID is required"})

    if not thread_id.isdigit():
        return jsonify({"success": False, "error": "Thread ID must be numeric (Facebook PSID)"})

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
    log(task_id, f"⏰ Interval: {interval} seconds")
    
    if images:
        log(task_id, f"🔄 Cycle: Text → Image+Text → Text → Image+Text ...")
    else:
        log(task_id, f"📝 Mode: Text messages only")
    
    return jsonify({"success": True, "task_id": task_id})

@app.route('/stop', methods=['POST'])
def stop():
    try:
        data = request.get_json()
        task_id = data.get('taskId') if data else request.form.get('taskId')
        
        if task_id in active_tasks:
            del active_tasks[task_id]
            log(task_id, "🛑 Task stopped by user")
            return jsonify({"success": True, "message": "Task stopped"})
        return jsonify({"success": False, "error": "Task not found"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/console/<task_id>')
def console(task_id):
    return jsonify(task_logs.get(task_id, []))

# Create necessary directories
os.makedirs('uploads', exist_ok=True)

if __name__ == '__main__':
    print("🚀 R0W3DY KIING Facebook Messenger Tool Starting...")
    print("📧 Developed by Rowedy King")
    print("🔗 Using Facebook Graph API v22.0")
    print("🌐 Server running on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
