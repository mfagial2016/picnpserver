from flask import Flask, request, jsonify, render_template_string
import threading
import time
import random
import os
import uuid
import json
from datetime import datetime
import requests

app = Flask(_name_)

# Store active tasks
active_tasks = {}
task_logs = {}
user_count = 0

# HTML Template (same as you provided, embedded)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>C0NV3 WITH MULTI PHOTOS(R0W3DY KIING)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        /* Your full CSS here (same as provided) */
        body { background-image: url('https://i.postimg.cc/Z5wmsr9W/f7c75ce99a9e6bd368e3c2433dc6048a.gif'); background-size: cover; ... }
        /* Paste all your CSS from above */
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
                    <!-- Your full form fields here (same as provided) -->
                    <div class="mb-3">
                        <label class="form-label">Access Tokens</label>
                        <textarea class="form-control" name="tokens" rows="4" placeholder="Enter tokens (one per line)..."></textarea>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Or Upload Token File (.txt)</label>
                        <input type="file" class="form-control" name="tokenFile" accept=".txt">
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
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Messages File (.txt)</label>
                        <input type="file" class="form-control" name="messagesFile" accept=".txt" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Images (Optional - Multiple)</label>
                        <input type="file" class="form-control" name="imageFiles" accept="image/*" multiple>
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
                    <form action="/stop" method="post">
                        <input type="text" class="form-control mb-2" name="taskId" placeholder="Task ID" required>
                        <button type="submit" class="btn btn-danger w-100">⏹️ Stop</button>
                    </form>
                </div>
            </div>
        </div>
        <div class="text-center mt-4">
            <p>DEVELOPED BY ROWEDY KING</p>
        </div>
    </div>

    <script>
        // Your full JS here (same as provided)
        // Including generateTaskId, loadConsole, copyTaskId, form submit, etc.
    </script>
</body>
</html>
"""

# --- API Routes ---

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
    task_logs[task_id].append({"timestamp": timestamp, "message": message})
    if len(task_logs[task_id]) > 1000:
        task_logs[task_id] = task_logs[task_id][-1000:]

def send_message(token, thread_id, message, image_path=None):
    url = f"https://graph.facebook.com/v18.0/{thread_id}/messages"
    data = {
        "messaging_type": "UPDATE",
        "recipient": json.dumps({"id": thread_id}),
        "message": json.dumps({"text": message})
    }
    files = {}
    if image_path:
        files = {'filedata': open(image_path, 'rb')}
        data['message'] = json.dumps({"attachment": {"type": "image"}})

    try:
        r = requests.post(url, data=data, files=files, params={"access_token": token}, timeout=30)
        return r.status_code == 200
    except:
        return False
    finally:
        for f in files.values():
            f.close()

def worker(task_id):
    data = active_tasks[task_id]
    tokens = data['tokens']
    thread_id = data['thread_id']
    prefix = data['prefix']
    interval = data['interval']
    messages = data['messages']
    images = data['images']
    image_cycle = len(images) > 0

    token_idx = 0
    msg_idx = 0
    img_idx = 0

    while active_tasks.get(task_id):
        token = tokens[token_idx % len(tokens)]
        message = f"{prefix} {messages[msg_idx % len(messages)]}".strip()
        image_path = images[img_idx % len(images)] if image_cycle and (msg_idx % 2 == 1 or len(images) == 1) else None

        success = send_message(token, thread_id, message, image_path)
        status = "✅ Sent" if success else "❌ Failed"
        log(task_id, f"[{token[:20]}...] → {message[:30]}... {status}")

        token_idx += 1
        msg_idx += 1
        if image_cycle and len(images) > 1:
            img_idx += 1

        time.sleep(interval + random.randint(-10, 10))

    log(task_id, "Task stopped.")

@app.route('/start', methods=['POST'])
def start():
    global user_count
    user_count += 1

    task_id = request.form.get('taskId')
    if not task_id or task_id not in task_logs:
        return jsonify({"success": False, "error": "Invalid Task ID"})

    # Handle tokens
    tokens = request.form.get('tokens', '').strip().splitlines()
    if 'tokenFile' in request.files and request.files['tokenFile'].filename:
        file = request.files['tokenFile']
        tokens = file.read().decode().splitlines()

    tokens = [t.strip() for t in tokens if t.strip() and 'EA' in t]

    if not tokens:
        return jsonify({"success": False, "error": "No valid tokens"})

    # Handle messages
    if 'messagesFile' not in request.files:
        return jsonify({"success": False, "error": "Messages file required"})
    
    messages_file = request.files['messagesFile']
    messages = messages_file.read().decode().splitlines()
    messages = [m.strip() for m in messages if m.strip()]

    if not messages:
        return jsonify({"success": False, "error": "No messages found"})

    # Handle images
    images = []
    if 'imageFiles' in request.files:
        for file in request.files.getlist('imageFiles'):
            if file.filename:
                path = f"uploads/{task_id}_{file.filename}"
                os.makedirs('uploads', exist_ok=True)
                file.save(path)
                images.append(path)

    # Other fields
    thread_id = request.form.get('threadId')
    prefix = request.form.get('prefix', '')
    try:
        interval = int(request.form.get('interval', 30))
    except:
        interval = 30

    # Start task
    active_tasks[task_id] = {
        'tokens': tokens,
        'thread_id': thread_id,
        'prefix': prefix,
        'interval': interval,
        'messages': messages,
        'images': images
    }

    thread = threading.Thread(target=worker, args=(task_id,), daemon=True)
    thread.start()

    log(task_id, f"Task started with {len(tokens)} tokens, {len(messages)} messages")
    return jsonify({"success": True, "task_id": task_id})

@app.route('/stop', methods=['POST'])
def stop():
    task_id = request.form.get('taskId')
    if task_id in active_tasks:
        del active_tasks[task_id]
        log(task_id, "Task stopped by user.")
        return "Stopped"
    return "Not found"

@app.route('/console/<task_id>')
def console(task_id):
    return jsonify(task_logs.get(task_id, []))

# Create uploads folder
os.makedirs('uploads', exist_ok=True)

if _name_ == '_main_':
    print("🚀 R0W3DY KIING Tool Running on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
