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

# HTML Template (same as before)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>C0NV3 WITH MULTI PHOTOS(R0W3DY KIING)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        /* Your CSS remains same */
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
        
        <div id="taskIdBox" class="task-id-box">
            <h4>✅ Task ID Generated!</h4>
            <p>Your Task ID:</p>
            <div class="task-id-text" id="taskIdDisplay">-</div>
            <button class="btn btn-success" onclick="copyTaskId()">📋 Copy Task ID</button>
            <div id="copyNotification" class="copy-notification">✓ Task ID Copied!</div>
        </div>
        
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
                        <label class="form-label">Facebook Page Access Tokens</label>
                        <textarea class="form-control" name="tokens" rows="4" placeholder="EAA... (Page Access Token with pages_messaging permission)" required></textarea>
                        <small class="text-muted">Must have: pages_messaging permission</small>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Page ID</label>
                        <input type="text" class="form-control" name="pageId" required placeholder="Your Facebook Page ID">
                        <small class="text-muted">Numeric Page ID (not username)</small>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Recipient PSID</label>
                        <input type="text" class="form-control" name="threadId" required placeholder="Recipient's Page Scoped ID">
                        <small class="text-muted">User's PSID (Page Scoped ID)</small>
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
                        document.getElementById('taskIdDisplay').textContent = result.task_id;
                        document.getElementById('taskIdBox').classList.add('show');
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
                    document.getElementById('taskIdDisplay').textContent = result.task_id;
                    document.getElementById('taskIdBox').classList.add('show');
                    document.getElementById('taskId').value = result.task_id;
                    document.getElementById('stopTaskId').value = result.task_id;
                    document.getElementById('hiddenTaskId').value = result.task_id;
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
        if len(task_logs[task_id]) > 1000:
            task_logs[task_id] = task_logs[task_id][-1000:]

def verify_token(token):
    """Verify if token is valid and has required permissions"""
    url = f"https://graph.facebook.com/v22.0/me"
    params = {
        "access_token": token,
        "fields": "id,name,permissions"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            permissions = data.get('permissions', {}).get('data', [])
            has_messaging = any(p['permission'] == 'pages_messaging' and p['status'] == 'granted' for p in permissions)
            return True, data.get('id'), data.get('name'), has_messaging
        else:
            return False, None, None, False
    except:
        return False, None, None, False

def send_text_message(token, page_id, recipient_id, message):
    """Send text message using correct Facebook API format"""
    url = f"https://graph.facebook.com/v22.0/{page_id}/messages"
    
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
        
        if response.status_code == 200:
            return True, "Message sent successfully"
        else:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', f"HTTP {response.status_code}")
            return False, error_msg
            
    except Exception as e:
        return False, f"Request failed: {str(e)}"

def send_image_message(token, page_id, recipient_id, message, image_path):
    """Send image with text using correct Facebook API"""
    # First upload image
    upload_url = f"https://graph.facebook.com/v22.0/{page_id}/message_attachments"
    
    try:
        with open(image_path, 'rb') as image_file:
            files = {
                'filedata': ('image.jpg', image_file, 'image/jpeg')
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
            
            upload_response = requests.post(
                upload_url,
                files=files,
                data=data,
                params=params,
                timeout=30
            )
            
            if upload_response.status_code == 200:
                upload_data = upload_response.json()
                attachment_id = upload_data.get('attachment_id')
                
                if attachment_id:
                    # Now send message with attachment
                    message_url = f"https://graph.facebook.com/v22.0/{page_id}/messages"
                    
                    message_payload = {
                        "recipient": {
                            "id": recipient_id
                        },
                        "message": {
                            "attachment": {
                                "type": "image",
                                "payload": {
                                    "attachment_id": attachment_id
                                }
                            }
                        },
                        "messaging_type": "MESSAGE_TAG",
                        "tag": "NON_PROMOTIONAL_SUBSCRIPTION"
                    }
                    
                    message_response = requests.post(
                        message_url,
                        headers={'Content-Type': 'application/json'},
                        json=message_payload,
                        params={"access_token": token},
                        timeout=30
                    )
                    
                    if message_response.status_code == 200:
                        # Also send text message if needed
                        if message:
                            time.sleep(2)
                            send_text_message(token, page_id, recipient_id, message)
                        return True, "Image sent successfully"
                    else:
                        return False, "Failed to send image message"
                else:
                    return False, "No attachment ID received"
            else:
                error_data = upload_response.json()
                error_msg = error_data.get('error', {}).get('message', "Upload failed")
                return False, f"Upload failed: {error_msg}"
                
    except Exception as e:
        return False, f"Image send failed: {str(e)}"

def worker(task_id):
    data = active_tasks[task_id]
    tokens = data['tokens']
    page_id = data['page_id']
    recipient_id = data['recipient_id']
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
            # Get current token and message
            token = tokens[token_idx % len(tokens)]
            current_message = messages[msg_idx % len(messages)]
            full_message = f"{prefix} {current_message}".strip()
            
            # Decide what to send
            if images:
                # Alternate between text and image+text
                if msg_idx % 2 == 0:  # Even index: send text only
                    success, detail = send_text_message(token, page_id, recipient_id, full_message)
                    log_type = "💬 Text"
                else:  # Odd index: send image with text
                    current_image = images[img_idx % len(images)]
                    success, detail = send_image_message(token, page_id, recipient_id, full_message, current_image)
                    log_type = f"📷 Image {img_idx % len(images) + 1}"
                    img_idx += 1
            else:
                # No images, send text only
                success, detail = send_text_message(token, page_id, recipient_id, full_message)
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
            time.sleep(max(10, sleep_time))
            
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
    
    # Get Page ID
    page_id = request.form.get('pageId', '').strip()
    if not page_id:
        return jsonify({"success": False, "error": "Page ID is required"})
    
    if not page_id.isdigit():
        return jsonify({"success": False, "error": "Page ID must be numeric"})

    # Get Recipient ID
    recipient_id = request.form.get('threadId', '').strip()
    if not recipient_id:
        return jsonify({"success": False, "error": "Recipient PSID is required"})
    
    if not recipient_id.isdigit():
        return jsonify({"success": False, "error": "Recipient PSID must be numeric"})

    # Verify tokens
    valid_tokens = []
    for token in tokens:
        is_valid, token_page_id, page_name, has_messaging = verify_token(token)
        if is_valid and has_messaging:
            valid_tokens.append(token)
            log(task_id, f"✅ Token verified: {page_name} (ID: {token_page_id})")
        else:
            log(task_id, f"❌ Invalid token or missing permissions: {token[:20]}...")
    
    if not valid_tokens:
        return jsonify({"success": False, "error": "No valid tokens with pages_messaging permission found"})

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
                os.makedirs('uploads', exist_ok=True)
                filename = f"{task_id}_{uuid.uuid4().hex[:8]}_{file.filename}"
                file_path = os.path.join('uploads', filename)
                file.save(file_path)
                images.append(file_path)

    # Get other form data
    prefix = request.form.get('prefix', '').strip()
    
    try:
        interval = int(request.form.get('interval', 30))
        if interval < 10:
            interval = 10
    except ValueError:
        interval = 30

    # Store task data and start worker
    active_tasks[task_id] = {
        'tokens': valid_tokens,
        'page_id': page_id,
        'recipient_id': recipient_id,
        'prefix': prefix,
        'interval': interval,
        'messages': messages,
        'images': images
    }

    # Start worker thread
    thread = threading.Thread(target=worker, args=(task_id,), daemon=True)
    thread.start()

    log(task_id, f"✅ Task started successfully!")
    log(task_id, f"📊 Stats: {len(valid_tokens)} tokens, {len(messages)} messages, {len(images)} images")
    log(task_id, f"⏰ Interval: {interval} seconds")
    
    if images:
        log(task_id, f"🔄 Cycle: Text → Image+Text → Text → Image+Text ...")
    
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
