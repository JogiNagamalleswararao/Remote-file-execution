# Remote Python Script Execution on Raspberry Pi

## Table of Contents
1. [Overview](#overview)
2. [Network Setup](#network-setup)
3. [Method 1: SSH Remote Execution](#method-1-ssh-remote-execution)
4. [Method 2: SCP + SSH](#method-2-scp--ssh)
5. [Method 3: Paramiko (Python Library)](#method-3-paramiko-python-library)
6. [Method 4: HTTP API with Flask](#method-4-http-api-with-flask)
7. [Method 5: MQTT Protocol](#method-5-mqtt-protocol)
8. [Security Best Practices](#security-best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Performance Comparison](#performance-comparison)

---

## Overview

This documentation provides comprehensive methods to execute Python scripts on a Raspberry Pi IoT device from a remote system.

**Environment:**
- **Local System (Controller)**: IP 192.168.1.1, Script: `in.py`
- **Raspberry Pi (Target)**: IP 192.168.1.2, Script: `out.py`

**Use Cases:**
- Remote IoT device control
- Automated script execution
- Data collection from sensors
- Remote monitoring and management

---

## Network Setup

### Prerequisites

1. **Both devices on same network**
   ```bash
   # Verify connectivity
   ping 192.168.1.2
   ```

2. **SSH enabled on Raspberry Pi**
   ```bash
   # On Raspberry Pi
   sudo raspi-config
   # Navigate: Interface Options → SSH → Enable
   # Or via command line:
   sudo systemctl enable ssh
   sudo systemctl start ssh
   ```

3. **Firewall configuration (if applicable)**
   ```bash
   # On Raspberry Pi
   sudo ufw allow 22/tcp  # For SSH
   sudo ufw allow 5000/tcp  # For HTTP API (if using)
   ```

---

## Method 1: SSH Remote Execution

### Description
Direct remote command execution using SSH protocol. Best for simple, one-time script execution.

### Advantages
- ✅ No additional libraries required
- ✅ Secure and encrypted
- ✅ Built into most Linux/Mac systems
- ✅ Simple and straightforward

### Disadvantages
- ❌ Requires SSH service running
- ❌ May need password or key setup
- ❌ Less flexible for complex interactions

### Implementation

#### Step 1: Test SSH Connection
```bash
ssh pi@192.168.1.2
```

Default Raspberry Pi credentials:
- Username: `pi`
- Password: `raspberry` (change this immediately!)

#### Step 2: Execute Remote Script
```bash
# Basic execution
ssh pi@192.168.1.2 "python3 /home/pi/out.py"

# With arguments
ssh pi@192.168.1.2 "python3 /home/pi/out.py --arg1 value1 --arg2 value2"

# With environment variables
ssh pi@192.168.1.2 "export VAR=value && python3 /home/pi/out.py"

# Run in background
ssh pi@192.168.1.2 "nohup python3 /home/pi/out.py > output.log 2>&1 &"
```

#### Step 3: Setup SSH Key Authentication (Recommended)
```bash
# On your local system (192.168.1.1)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Copy key to Raspberry Pi
ssh-copy-id pi@192.168.1.2

# Test passwordless login
ssh pi@192.168.1.2
```

#### Step 4: Create Bash Script for Automation
```bash
#!/bin/bash
# remote_execute.sh

PI_HOST="pi@192.168.1.2"
SCRIPT_PATH="/home/pi/out.py"

echo "Executing script on Raspberry Pi..."
ssh $PI_HOST "python3 $SCRIPT_PATH"

if [ $? -eq 0 ]; then
    echo "Script executed successfully"
else
    echo "Script execution failed"
    exit 1
fi
```

Make it executable:
```bash
chmod +x remote_execute.sh
./remote_execute.sh
```

---

## Method 2: SCP + SSH

### Description
Copy files to Raspberry Pi then execute them. Ideal when you need to transfer the script first.

### Advantages
- ✅ Updates script on remote device
- ✅ Good for development workflow
- ✅ Can transfer multiple files
- ✅ Preserves file permissions

### Disadvantages
- ❌ Two-step process
- ❌ Slower for frequent executions
- ❌ Creates file copies

### Implementation

#### Step 1: Copy Script to Raspberry Pi
```bash
# Copy single file
scp /path/to/in.py pi@192.168.1.2:/home/pi/

# Copy with different name
scp /path/to/in.py pi@192.168.1.2:/home/pi/out.py

# Copy entire directory
scp -r /path/to/project/ pi@192.168.1.2:/home/pi/

# Copy with compression (faster for large files)
scp -C /path/to/large_file.py pi@192.168.1.2:/home/pi/
```

#### Step 2: Execute the Script
```bash
ssh pi@192.168.1.2 "python3 /home/pi/out.py"
```

#### Step 3: Combined Script
```bash
#!/bin/bash
# deploy_and_run.sh

LOCAL_SCRIPT="./in.py"
REMOTE_PATH="/home/pi/out.py"
PI_HOST="pi@192.168.1.2"

echo "Copying script to Raspberry Pi..."
scp $LOCAL_SCRIPT $PI_HOST:$REMOTE_PATH

if [ $? -eq 0 ]; then
    echo "Executing script..."
    ssh $PI_HOST "python3 $REMOTE_PATH"
else
    echo "Failed to copy script"
    exit 1
fi
```

#### Step 4: Sync Entire Project with rsync
```bash
# Sync project directory (more efficient than scp)
rsync -avz --delete /path/to/project/ pi@192.168.1.2:/home/pi/project/

# Sync and execute
rsync -avz ./in.py pi@192.168.1.2:/home/pi/out.py && \
ssh pi@192.168.1.2 "python3 /home/pi/out.py"
```

---

## Method 3: Paramiko (Python Library)

### Description
Python library for SSH protocol automation. Best for programmatic control and integration.

### Advantages
- ✅ Pure Python solution
- ✅ Platform independent
- ✅ Programmable and scriptable
- ✅ Can handle SFTP transfers
- ✅ Good for CI/CD pipelines

### Disadvantages
- ❌ Requires external library
- ❌ More code complexity
- ❌ Need to handle connections manually

### Implementation

#### Step 1: Install Paramiko
```bash
pip install paramiko
```

#### Step 2: Basic Remote Execution Script
```python
# remote_executor.py
import paramiko
import sys

class RemoteExecutor:
    def __init__(self, host, username, password=None, key_file=None):
        self.host = host
        self.username = username
        self.password = password
        self.key_file = key_file
        self.client = None
    
    def connect(self):
        """Establish SSH connection"""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            if self.key_file:
                self.client.connect(
                    self.host,
                    username=self.username,
                    key_filename=self.key_file
                )
            else:
                self.client.connect(
                    self.host,
                    username=self.username,
                    password=self.password
                )
            print(f"✓ Connected to {self.host}")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def execute_script(self, script_path, args=None):
        """Execute remote Python script"""
        if not self.client:
            print("Not connected. Call connect() first.")
            return None
        
        command = f"python3 {script_path}"
        if args:
            command += f" {args}"
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            exit_code = stdout.channel.recv_exit_status()
            
            return {
                'output': output,
                'error': error,
                'exit_code': exit_code
            }
        except Exception as e:
            print(f"Execution error: {e}")
            return None
    
    def upload_and_execute(self, local_path, remote_path):
        """Upload script then execute it"""
        if not self.client:
            print("Not connected. Call connect() first.")
            return None
        
        try:
            # Upload file
            sftp = self.client.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            print(f"✓ Uploaded {local_path} to {remote_path}")
            
            # Execute
            return self.execute_script(remote_path)
        except Exception as e:
            print(f"Upload/Execute error: {e}")
            return None
    
    def close(self):
        """Close SSH connection"""
        if self.client:
            self.client.close()
            print("✓ Connection closed")

# Usage example
if __name__ == "__main__":
    # Configuration
    PI_HOST = "192.168.1.2"
    PI_USER = "pi"
    PI_PASS = "raspberry"  # Or use key_file parameter
    REMOTE_SCRIPT = "/home/pi/out.py"
    
    # Create executor
    executor = RemoteExecutor(PI_HOST, PI_USER, password=PI_PASS)
    
    # Connect
    if executor.connect():
        # Execute remote script
        result = executor.execute_script(REMOTE_SCRIPT)
        
        if result:
            print("\n--- Output ---")
            print(result['output'])
            
            if result['error']:
                print("\n--- Errors ---")
                print(result['error'])
            
            print(f"\nExit Code: {result['exit_code']}")
        
        # Close connection
        executor.close()
```

#### Step 3: Advanced Features
```python
# With SSH key authentication
executor = RemoteExecutor(
    host="192.168.1.2",
    username="pi",
    key_file="/home/user/.ssh/id_rsa"
)

# Upload and execute
result = executor.upload_and_execute(
    local_path="./in.py",
    remote_path="/home/pi/out.py"
)

# Execute with arguments
result = executor.execute_script(
    "/home/pi/out.py",
    args="--mode production --verbose"
)
```

---

## Method 4: HTTP API with Flask

### Description
Create a REST API on Raspberry Pi that can be triggered remotely. Best for web-based integrations.

### Advantages
- ✅ Language agnostic (any HTTP client)
- ✅ Easy to integrate with web apps
- ✅ Can add authentication
- ✅ RESTful and scalable
- ✅ Can return JSON responses

### Disadvantages
- ❌ Requires Flask server running
- ❌ Less secure than SSH (needs HTTPS)
- ❌ More complex setup
- ❌ Firewall configuration needed

### Implementation

#### Step 1: Install Flask on Raspberry Pi
```bash
ssh pi@192.168.1.2
pip3 install flask flask-cors
```

#### Step 2: Create API Server on Raspberry Pi
```python
# /home/pi/api_server.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Store running processes
running_processes = {}

@app.route('/')
def home():
    return jsonify({
        'status': 'online',
        'message': 'Raspberry Pi API Server',
        'version': '1.0'
    })

@app.route('/execute', methods=['POST'])
def execute_script():
    """Execute a Python script"""
    data = request.get_json()
    script_path = data.get('script', '/home/pi/out.py')
    args = data.get('args', [])
    
    try:
        # Execute script
        command = ['python3', script_path] + args
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return jsonify({
            'success': True,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
            'script': script_path
        })
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Script execution timed out'
        }), 408
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/execute/async', methods=['POST'])
def execute_async():
    """Execute script asynchronously"""
    data = request.get_json()
    script_path = data.get('script', '/home/pi/out.py')
    args = data.get('args', [])
    
    # Generate unique ID
    task_id = str(int(time.time() * 1000))
    
    def run_script():
        try:
            command = ['python3', script_path] + args
            result = subprocess.run(command, capture_output=True, text=True)
            running_processes[task_id] = {
                'status': 'completed',
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except Exception as e:
            running_processes[task_id] = {
                'status': 'failed',
                'error': str(e)
            }
    
    # Start in background
    running_processes[task_id] = {'status': 'running'}
    thread = threading.Thread(target=run_script)
    thread.start()
    
    return jsonify({
        'success': True,
        'task_id': task_id,
        'message': 'Script execution started'
    })

@app.route('/status/<task_id>')
def check_status(task_id):
    """Check status of async task"""
    if task_id in running_processes:
        return jsonify(running_processes[task_id])
    else:
        return jsonify({
            'error': 'Task not found'
        }), 404

@app.route('/system/info')
def system_info():
    """Get system information"""
    try:
        cpu_temp = subprocess.run(
            ['vcgencmd', 'measure_temp'],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        return jsonify({
            'cpu_temp': cpu_temp,
            'uptime': subprocess.run(['uptime'], capture_output=True, text=True).stdout.strip()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting API Server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)
```

#### Step 3: Run Server as Service
```bash
# Create systemd service
sudo nano /etc/systemd/system/pi-api.service
```

Add this content:
```ini
[Unit]
Description=Raspberry Pi API Server
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 /home/pi/api_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable pi-api.service
sudo systemctl start pi-api.service
sudo systemctl status pi-api.service
```

#### Step 4: Client Script on Local System
```python
# in.py (on 192.168.1.1)
import requests
import json
import time

class PiAPIClient:
    def __init__(self, pi_ip, port=5000):
        self.base_url = f"http://{pi_ip}:{port}"
    
    def check_status(self):
        """Check if API is online"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            return response.json()
        except Exception as e:
            print(f"Connection error: {e}")
            return None
    
    def execute_script(self, script_path, args=None):
        """Execute script synchronously"""
        payload = {
            'script': script_path,
            'args': args or []
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/execute",
                json=payload,
                timeout=60
            )
            return response.json()
        except Exception as e:
            print(f"Execution error: {e}")
            return None
    
    def execute_async(self, script_path, args=None):
        """Execute script asynchronously"""
        payload = {
            'script': script_path,
            'args': args or []
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/execute/async",
                json=payload
            )
            return response.json()
        except Exception as e:
            print(f"Execution error: {e}")
            return None
    
    def check_task(self, task_id):
        """Check async task status"""
        try:
            response = requests.get(f"{self.base_url}/status/{task_id}")
            return response.json()
        except Exception as e:
            print(f"Status check error: {e}")
            return None
    
    def get_system_info(self):
        """Get system information"""
        try:
            response = requests.get(f"{self.base_url}/system/info")
            return response.json()
        except Exception as e:
            print(f"Info error: {e}")
            return None

# Usage
if __name__ == "__main__":
    client = PiAPIClient("192.168.1.2")
    
    # Check connection
    print("Checking connection...")
    status = client.check_status()
    print(status)
    
    # Execute script
    print("\nExecuting script...")
    result = client.execute_script("/home/pi/out.py")
    
    if result and result.get('success'):
        print("Output:", result['stdout'])
    else:
        print("Error:", result.get('error'))
    
    # Async execution
    print("\nExecuting async...")
    async_result = client.execute_async("/home/pi/out.py")
    
    if async_result and async_result.get('success'):
        task_id = async_result['task_id']
        print(f"Task ID: {task_id}")
        
        # Poll for completion
        while True:
            task_status = client.check_task(task_id)
            print(f"Status: {task_status.get('status')}")
            
            if task_status.get('status') != 'running':
                print("Output:", task_status.get('stdout'))
                break
            
            time.sleep(1)
```

---

## Method 5: MQTT Protocol

### Description
Message-based communication using MQTT broker. Ideal for IoT deployments and real-time communication.

### Advantages
- ✅ Lightweight protocol
- ✅ Asynchronous communication
- ✅ Scalable to multiple devices
- ✅ Pub/Sub architecture
- ✅ Good for unstable networks

### Disadvantages
- ❌ Requires MQTT broker
- ❌ More complex architecture
- ❌ Learning curve for MQTT
- ❌ Additional infrastructure

### Implementation

#### Step 1: Install MQTT Library
```bash
# On both devices
pip3 install paho-mqtt
```

#### Step 2: Raspberry Pi Subscriber
```python
# /home/pi/mqtt_executor.py
import paho.mqtt.client as mqtt
import subprocess
import json
import time

class MQTTExecutor:
    def __init__(self, broker, port=1883):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(client_id="raspberry_pi_executor")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback when connected"""
        if rc == 0:
            print("✓ Connected to MQTT Broker")
            # Subscribe to command topic
            self.client.subscribe("pi/execute/command")
            self.client.subscribe("pi/execute/status")
        else:
            print(f"✗ Connection failed with code {rc}")
    
    def on_message(self, client, userdata, message):
        """Callback when message received"""
        topic = message.topic
        payload = message.payload.decode('utf-8')
        
        print(f"Received message on {topic}")
        
        if topic == "pi/execute/command":
            self.execute_command(payload)
        elif topic == "pi/execute/status":
            self.send_status()
    
    def execute_command(self, payload):
        """Execute command from MQTT message"""
        try:
            data = json.loads(payload)
            script = data.get('script', '/home/pi/out.py')
            args = data.get('args', [])
            
            print(f"Executing: {script}")
            
            # Execute script
            command = ['python3', script] + args
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Publish result
            response = {
                'success': True,
                'script': script,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'timestamp': time.time()
            }
            
            self.client.publish(
                "pi/execute/result",
                json.dumps(response)
            )
            
            print("✓ Execution complete")
            
        except json.JSONDecodeError:
            print("✗ Invalid JSON payload")
        except subprocess.TimeoutExpired:
            error_response = {
                'success': False,
                'error': 'Execution timeout',
                'timestamp': time.time()
            }
            self.client.publish(
                "pi/execute/result",
                json.dumps(error_response)
            )
        except Exception as e:
            error_response = {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
            self.client.publish(
                "pi/execute/result",
                json.dumps(error_response)
            )
    
    def send_status(self):
        """Send system status"""
        try:
            cpu_temp = subprocess.run(
                ['vcgencmd', 'measure_temp'],
                capture_output=True,
                text=True
            ).stdout.strip()
            
            status = {
                'online': True,
                'cpu_temp': cpu_temp,
                'timestamp': time.time()
            }
            
            self.client.publish(
                "pi/status/info",
                json.dumps(status)
            )
        except Exception as e:
            print(f"Status error: {e}")
    
    def start(self):
        """Start MQTT client"""
        try:
            self.client.connect(self.broker, self.port, keepalive=60)
            print(f"Connecting to MQTT Broker at {self.broker}:{self.port}")
            self.client.loop_forever()
        except Exception as e:
            print(f"Connection error: {e}")

if __name__ == "__main__":
    # Using public broker (for testing only)
    BROKER = "broker.hivemq.com"
    # Or use local broker: BROKER = "192.168.1.1"
    
    executor = MQTTExecutor(BROKER)
    executor.start()
```

#### Step 3: Local System Publisher
```python
# in.py (on 192.168.1.1)
import paho.mqtt.client as mqtt
import json
import time

class MQTTController:
    def __init__(self, broker, port=1883):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(client_id="local_controller")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.result_received = False
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback when connected"""
        if rc == 0:
            print("✓ Connected to MQTT Broker")
            # Subscribe to result topic
            self.client.subscribe("pi/execute/result")
            self.client.subscribe("pi/status/info")
        else:
            print(f"✗ Connection failed with code {rc}")
    
    def on_message(self, client, userdata, message):
        """Callback when message received"""
        topic = message.topic
        payload = message.payload.decode('utf-8')
        
        try:
            data = json.loads(payload)
            
            if topic == "pi/execute/result":
                print("\n--- Execution Result ---")
                if data.get('success'):
                    print("Status: Success ✓")
                    print(f"Output:\n{data.get('stdout')}")
                    if data.get('stderr'):
                        print(f"Errors:\n{data.get('stderr')}")
                else:
                    print("Status: Failed ✗")
                    print(f"Error: {data.get('error')}")
                
                self.result_received = True
            
            elif topic == "pi/status/info":
                print("\n--- System Status ---")
                print(f"Online: {data.get('online')}")
                print(f"CPU Temp: {data.get('cpu_temp')}")
        
        except json.JSONDecodeError:
            print("✗ Invalid JSON response")
    
    def execute_script(self, script_path, args=None):
        """Send execution command"""
        command = {
            'script': script_path,
            'args': args or []
        }
        
        self.result_received = False
        self.client.publish(
            "pi/execute/command",
            json.dumps(command)
        )
        
        print(f"Sent command to execute: {script_path}")
        
        # Wait for result
        timeout = 30
        start_time = time.time()
        while not self.result_received and (time.time() - start_time) < timeout:
            time.sleep(0.1)
        
        if not self.result_received:
            print("⚠ Timeout waiting for result")
    
    def request_status(self):
        """Request system status"""
        self.client.publish("pi/execute/status", "request")
        print("Requested system status")
    
    def start(self):
        """Connect to broker"""
        try:
            self.client.connect(self.broker, self.port, keepalive=60)
            self.client.loop_start()
            print(f"✓ Connected to MQTT Broker at {self.broker}:{self.port}")
            return True
        except Exception as e:
            print(f"✗ Connection error: {e}")
            return False
    
    def stop(self):
        """Disconnect from broker"""
        self.client.loop_stop()
        self.client.disconnect()

# Usage
if __name__ == "__main__":
    # Using public broker (for testing)
    BROKER = "broker.hivemq.com"
    # Or use local broker: BROKER = "192.168.1.1"
    
    controller = MQTTController(BROKER)
    
    if controller.start():
        time.sleep(2)  # Wait for connection
        
        # Request status
        controller.request_status()
        time.sleep(2)
        
        # Execute script
        controller.execute_script("/home/pi/out.py", ["--verbose"])
        
        time.sleep(2)
        controller.stop()
```

#### Step 4: Setup Local MQTT Broker (Optional)
```bash
# Install Mosquitto on local system
sudo apt-get install mosquitto mosquitto-clients

# Start broker
sudo systemctl start mosquitto
sudo systemctl enable mosquitto

# Test broker
mosquitto_pub -h localhost -t test -m "hello"
mosquitto_sub -h localhost -t test
```

---

## Security Best Practices

### SSH Security

1. **Change Default Password**
```bash
passwd
```

2. **Disable Root Login**
```bash
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
sudo systemctl restart sshd
```

3. **Use SSH Keys Only**
```bash
# In sshd_config
PasswordAuthentication no
PubkeyAuthentication yes
```

4. **Change Default SSH Port**
```bash
# In sshd_config
Port 2222  # Choose any port above 1024
```

5. **Install Fail2Ban**
```bash
sudo apt-get install fail2ban
sudo systemctl enable fail2ban
```

### API Security

1. **Use HTTPS with SSL Certificate**
```python
# Use Let's Encrypt or self-signed certificate
app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
```

2. **Implement API Authentication**
```python
from functools import wraps
from flask import request, jsonify

API_KEY = "your-secret-key-here"

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-API-Key') != API_KEY:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/execute', methods=['POST'])
@require_api_key
def execute_script():
    # Your code here
    pass
```

3. **Rate Limiting**
```bash
pip3 install flask-limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)
```

### MQTT Security

1. **Use Authentication**
```bash
# Create password file
mosquitto_passwd -c /etc/mosquitto/passwd username

# Edit mosquitto.conf
allow_anonymous false
password_file /etc/mosquitto/passwd
```

2. **Use TLS/SSL**
```python
# MQTT client with TLS
client.tls_set(
    ca_certs="/path/to/ca.crt",
    certfile="/path/to/client.crt",
    keyfile="/path/to/client.key"
)
```

3. **Use Unique Topics**
```python
# Instead of generic topics, use device-specific
DEVICE_ID = "pi_001"
COMMAND_TOPIC = f"devices/{DEVICE_ID}/execute/command"
RESULT_TOPIC = f"devices/{DEVICE_ID}/execute/result"
```

### Network Security

1. **Configure Firewall**
```bash
# On Raspberry Pi
sudo ufw enable
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 5000/tcp    # API (if needed)
sudo ufw deny from any to any
```

2. **Use VPN for Remote Access**
```bash
# Install WireGuard
sudo apt-get install wireguard

# Or use OpenVPN
sudo apt-get install openvpn
```

3. **Network Isolation**
- Place IoT devices on separate VLAN
- Use network segmentation
- Implement firewall rules between segments

### General Security

1. **Keep System Updated**
```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
```

2. **Disable Unnecessary Services**
```bash
sudo systemctl disable bluetooth
sudo systemctl disable avahi-daemon
```

3. **Monitor Logs**
```bash
# Check auth logs
sudo tail -f /var/log/auth.log

# Check system logs
journalctl -f
```

4. **Input Validation**
```python
import os

def validate_script_path(path):
    """Validate script path to prevent path traversal"""
    # Only allow scripts in specific directory
    allowed_dir = "/home/pi/scripts/"
    abs_path = os.path.abspath(path)
    
    if not abs_path.startswith(allowed_dir):
        raise ValueError("Invalid script path")
    
    if not os.path.exists(abs_path):
        raise ValueError("Script not found")
    
    return abs_path
```

---

## Troubleshooting

### SSH Connection Issues

**Problem: Connection Refused**
```bash
# Check if SSH is running
sudo systemctl status ssh

# Start SSH service
sudo systemctl start ssh

# Check if port 22 is open
sudo netstat -tlnp | grep :22
```

**Problem: Permission Denied**
```bash
# Check SSH key permissions
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 700 ~/.ssh

# Check authorized_keys on Pi
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

**Problem: Host Key Verification Failed**
```bash
# Remove old host key
ssh-keygen -R 192.168.1.2

# Or edit known_hosts
nano ~/.ssh/known_hosts
```

### Script Execution Issues

**Problem: Python Not Found**
```bash
# Check Python location
which python3

# Use full path
ssh pi@192.168.1.2 "/usr/bin/python3 /home/pi/out.py"

# Or set PATH
ssh pi@192.168.1.2 "export PATH=/usr/bin:$PATH && python3 /home/pi/out.py"
```

**Problem: Module Not Found**
```bash
# Install missing module on Pi
ssh pi@192.168.1.2 "pip3 install module_name"

# Check installed modules
ssh pi@192.168.1.2 "pip3 list"

# Use virtual environment
ssh pi@192.168.1.2 "source /home/pi/venv/bin/activate && python3 out.py"
```

**Problem: Permission Denied on Script**
```bash
# Make script executable
ssh pi@192.168.1.2 "chmod +x /home/pi/out.py"

# Check file permissions
ssh pi@192.168.1.2 "ls -la /home/pi/out.py"
```

### Network Issues

**Problem: Cannot Ping Raspberry Pi**
```bash
# Check IP address on Pi
ssh pi@192.168.1.2  # If previously connected
ip addr show

# Check network configuration
ifconfig

# Restart networking
sudo systemctl restart networking
```

**Problem: Firewall Blocking**
```bash
# Check firewall status
sudo ufw status

# Allow SSH temporarily
sudo ufw allow 22/tcp

# Disable firewall (for testing only)
sudo ufw disable
```

**Problem: Network Discovery**
```bash
# Find Raspberry Pi on network
sudo nmap -sn 192.168.1.0/24

# Or use arp-scan
sudo arp-scan --localnet
```

### API Issues

**Problem: Connection Refused on Port 5000**
```bash
# Check if Flask is running
ps aux | grep python

# Check if port is listening
netstat -tlnp | grep :5000

# Start Flask server
python3 /home/pi/api_server.py
```

**Problem: Firewall Blocking Port**
```bash
# Allow port 5000
sudo ufw allow 5000/tcp

# Check firewall rules
sudo ufw status numbered
```

**Problem: CORS Errors**
```python
# Install flask-cors
pip3 install flask-cors

# Enable in Flask app
from flask_cors import CORS
CORS(app)
```

### MQTT Issues

**Problem: Cannot Connect to Broker**
```bash
# Test broker connectivity
mosquitto_pub -h broker.hivemq.com -t test -m "hello"

# Check broker status (if local)
sudo systemctl status mosquitto

# Start broker
sudo systemctl start mosquitto
```

**Problem: Messages Not Received**
```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Or enable MQTT logging
client.enable_logger()
```

**Problem: Authentication Failed**
```bash
# Test with credentials
mosquitto_pub -h localhost -t test -m "hello" -u username -P password

# Check password file
sudo cat /etc/mosquitto/passwd
```

### Performance Issues

**Problem: Slow Execution**
```bash
# Check CPU usage
top
htop

# Check memory
free -h

# Check disk space
df -h

# Check temperature
vcgencmd measure_temp
```

**Problem: Timeout Errors**
```python
# Increase timeout in requests
response = requests.post(url, json=data, timeout=120)

# Increase timeout in subprocess
result = subprocess.run(command, timeout=60)

# Increase SSH timeout
ssh -o ConnectTimeout=30 pi@192.168.1.2
```

### Debugging Tips

1. **Enable Verbose Output**
```bash
# SSH verbose mode
ssh -v pi@192.168.1.2

# Python verbose mode
python3 -v script.py
```

2. **Check Logs**
```bash
# System logs
journalctl -xe

# Auth logs
sudo tail -f /var/log/auth.log

# Custom logs
tail -f /var/log/myapp.log
```

3. **Test Connectivity**
```bash
# Test network
ping 192.168.1.2

# Test port
nc -zv 192.168.1.2 22

# Test HTTP
curl http://192.168.1.2:5000/
```

---

## Performance Comparison

### Method Comparison Table

| Method | Speed | Security | Complexity | Best Use Case |
|--------|-------|----------|------------|---------------|
| **SSH Direct** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | Quick scripts, one-time tasks |
| **SCP + SSH** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Development, script updates |
| **Paramiko** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Automation, CI/CD pipelines |
| **HTTP API** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | Web integration, REST APIs |
| **MQTT** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | IoT networks, async messaging |

### Latency Benchmarks

Typical latencies for executing a simple "Hello World" script:

```
SSH Direct:        ~100-200ms
SCP + SSH:         ~500-800ms (includes file transfer)
Paramiko:          ~150-300ms
HTTP API:          ~50-150ms
MQTT:              ~10-50ms (broker dependent)
```

### Resource Usage

**SSH (sshd):**
- Memory: ~5-10 MB
- CPU: Minimal (<1%)
- Network: Encrypted overhead

**Flask API:**
- Memory: ~30-50 MB
- CPU: 1-5% (idle), 10-30% (processing)
- Network: HTTP overhead

**MQTT Client:**
- Memory: ~2-5 MB
- CPU: Minimal (<1%)
- Network: Very lightweight

### Scalability

**SSH:**
- ✓ Good for 1-10 devices
- ✗ Connection overhead per device
- ✗ Sequential execution

**HTTP API:**
- ✓ Good for 10-100 devices
- ✓ Parallel requests possible
- ✗ Server resource intensive

**MQTT:**
- ✓ Excellent for 100+ devices
- ✓ Pub/Sub architecture scales well
- ✓ Minimal per-device overhead

---

## Advanced Topics

### Executing Scripts with Virtual Environments

```bash
# Create virtual environment on Pi
ssh pi@192.168.1.2 "python3 -m venv /home/pi/myenv"

# Install packages
ssh pi@192.168.1.2 "/home/pi/myenv/bin/pip install requests numpy"

# Execute script in venv
ssh pi@192.168.1.2 "/home/pi/myenv/bin/python /home/pi/out.py"
```

### Handling Long-Running Scripts

**Using nohup:**
```bash
ssh pi@192.168.1.2 "nohup python3 /home/pi/out.py > output.log 2>&1 &"
```

**Using screen:**
```bash
ssh pi@192.168.1.2 "screen -dmS mysession python3 /home/pi/out.py"

# Check status
ssh pi@192.168.1.2 "screen -ls"

# Attach to session
ssh pi@192.168.1.2 "screen -r mysession"
```

**Using systemd service:**
```bash
# Create service file
sudo nano /etc/systemd/system/myscript.service
```

```ini
[Unit]
Description=My Python Script
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 /home/pi/out.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable myscript.service
sudo systemctl start myscript.service

# Check status
sudo systemctl status myscript.service
```

### Scheduling Execution

**Using Cron:**
```bash
# Edit crontab on Pi
ssh pi@192.168.1.2 "crontab -e"

# Add scheduled task
# Run every day at 2 AM
0 2 * * * /usr/bin/python3 /home/pi/out.py >> /home/pi/cron.log 2>&1

# Run every 5 minutes
*/5 * * * * /usr/bin/python3 /home/pi/out.py
```

**From Local System:**
```python
import schedule
import time
from remote_executor import RemoteExecutor

def job():
    executor = RemoteExecutor("192.168.1.2", "pi", key_file="~/.ssh/id_rsa")
    if executor.connect():
        executor.execute_script("/home/pi/out.py")
        executor.close()

# Schedule
schedule.every(10).minutes.do(job)
schedule.every().day.at("02:00").do(job)

# Run scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
```

### Passing Data Between Scripts

**Using Command Line Arguments:**
```python
# in.py (local)
import subprocess
data = "sensor_data"
subprocess.run(f"ssh pi@192.168.1.2 'python3 /home/pi/out.py {data}'", shell=True)

# out.py (Pi)
import sys
data = sys.argv[1]
print(f"Received: {data}")
```

**Using Files:**
```bash
# Create data file locally
echo '{"temp": 25, "humidity": 60}' > data.json

# Copy to Pi
scp data.json pi@192.168.1.2:/home/pi/

# Execute with file
ssh pi@192.168.1.2 "python3 /home/pi/out.py /home/pi/data.json"
```

**Using Environment Variables:**
```bash
ssh pi@192.168.1.2 "TEMP=25 HUMIDITY=60 python3 /home/pi/out.py"
```

**Using Shared Database:**
```python
# Both scripts connect to shared database
import sqlite3

# Local script writes data
conn = sqlite3.connect('//192.168.1.2/shared/db.sqlite')
cursor = conn.cursor()
cursor.execute("INSERT INTO tasks VALUES (?, ?)", (task_id, data))
conn.commit()

# Pi script reads data
conn = sqlite3.connect('/shared/db.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT * FROM tasks WHERE processed = 0")
tasks = cursor.fetchall()
```

### Error Handling and Retry Logic

```python
import time
from typing import Optional

class ResilientExecutor:
    def __init__(self, max_retries=3, retry_delay=5):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    def execute_with_retry(self, func, *args, **kwargs) -> Optional[dict]:
        """Execute function with retry logic"""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                result = func(*args, **kwargs)
                print(f"✓ Success on attempt {attempt + 1}")
                return result
            except Exception as e:
                last_error = e
                print(f"✗ Attempt {attempt + 1} failed: {e}")
                
                if attempt < self.max_retries - 1:
                    print(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
        
        print(f"✗ All {self.max_retries} attempts failed")
        raise last_error

# Usage
executor = ResilientExecutor(max_retries=3, retry_delay=5)

def execute_remote():
    # Your execution logic here
    pass

result = executor.execute_with_retry(execute_remote)
```

### Monitoring and Logging

```python
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('remote_execution.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('RemoteExecutor')

class MonitoredExecutor:
    def execute(self, script_path):
        """Execute with comprehensive logging"""
        start_time = datetime.now()
        logger.info(f"Starting execution of {script_path}")
        
        try:
            # Your execution logic
            result = self._execute_script(script_path)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"Execution completed in {execution_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Execution failed: {e}", exc_info=True)
            raise
```

### Web Dashboard for Monitoring

```python
# dashboard.py
from flask import Flask, render_template, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/devices')
def get_devices():
    """Get status of all devices"""
    devices = []
    
    # Check Raspberry Pi
    try:
        result = subprocess.run(
            ['ping', '-c', '1', '192.168.1.2'],
            capture_output=True,
            timeout=2
        )
        status = 'online' if result.returncode == 0 else 'offline'
    except:
        status = 'offline'
    
    devices.append({
        'name': 'Raspberry Pi',
        'ip': '192.168.1.2',
        'status': status
    })
    
    return jsonify(devices)

@app.route('/api/execute/<device>')
def execute_on_device(device):
    """Execute script on device"""
    # Implementation here
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

---

## Conclusion

This documentation covered five comprehensive methods for remote Python script execution on Raspberry Pi:

1. **SSH Direct Execution** - Simple and secure for basic needs
2. **SCP + SSH** - Good for development workflows
3. **Paramiko** - Python-based automation solution
4. **HTTP API** - Web-friendly RESTful approach
5. **MQTT** - Scalable IoT messaging protocol

**Recommendations:**

- **For beginners:** Start with SSH direct execution
- **For development:** Use SCP + SSH method
- **For automation:** Use Paramiko or HTTP API
- **For IoT networks:** Use MQTT protocol
- **For production:** Combine methods based on requirements

**Next Steps:**

1. Choose the method that fits your use case
2. Implement security best practices
3. Set up monitoring and logging
4. Test thoroughly in development environment
5. Document your specific implementation
6. Plan for scaling and maintenance

**Additional Resources:**

- Raspberry Pi Documentation: https://www.raspberrypi.org/documentation/
- Paramiko Documentation: https://www.paramiko.org/
- Flask Documentation: https://flask.palletsprojects.com/
- MQTT Protocol: https://mqtt.org/
- SSH Security: https://www.ssh.com/academy/ssh/security

---

**Version:** 1.0  
**Last Updated:** September 30, 2025  
**Maintained By:** Cadfem IT  
**Author:** Naga Malleswara Rao