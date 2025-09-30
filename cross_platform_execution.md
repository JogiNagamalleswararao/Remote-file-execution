**Problem: Script Path Format**
```python
import os
import platform

def normalize_path(path):
    """Convert path to OS-appropriate format"""
    if platform.system() == "Windows":
        # Convert forward slashes to backslashes
        return path.replace('/', '\\')
    else:
        # Convert backslashes to forward slashes
        return path.replace('\\', '/')

# Usage
script_path = normalize_path("/home/user/script.py")  # Linux
script_path = normalize_path("C:\\Scripts\\script.py")  # Windows
```

**Problem: Line Ending Differences**
```python
def fix_line_endings(file_path, target_os='unix'):
    """Fix line endings for target OS"""
    with open(file_path, 'rb') as f:
        content = f.read()
    
    # Replace all line endings with target
    if target_os == 'unix':
        content = content.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    elif target_os == 'windows':
        content = content.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
        content = content.replace(b'\n', b'\r\n')
    
    with open(file_path, 'wb') as f:
        f.write(content)

# Or use dos2unix/unix2dos
# Linux: dos2unix script.py
# Windows: unix2dos script.py
```

**Problem: Character Encoding**
```python
def read_cross_platform(file_path):
    """Read file with proper encoding"""
    try:
        # Try UTF-8 first
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Fallback to latin-1
        with open(file_path, 'r', encoding='latin-1') as f:
            return f.read()

def write_cross_platform(file_path, content):
    """Write file with UTF-8 encoding"""
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
```

**Problem: Network Discovery**
```python
import socket
import subprocess
import platform

def find_machines_on_network(ip_range="192.168.1"):
    """Scan network for active machines"""
    active_hosts = []
    
    for i in range(1, 255):
        ip = f"{ip_range}.{i}"
        try:
            # Quick ping test
            param = '-n' if platform.system() == 'Windows' else '-c'
            command = ['ping', param, '1', '-w', '100', ip]
            result = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=1
            )
            
            if result.returncode == 0:
                # Try to get hostname
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except:
                    hostname = "Unknown"
                
                active_hosts.append({
                    'ip': ip,
                    'hostname': hostname
                })
                print(f"Found: {ip} ({hostname})")
        except:
            continue
    
    return active_hosts

# Usage
print("Scanning network...")
hosts = find_machines_on_network("192.168.1")
print(f"Found {len(hosts)} active hosts")
```

---

## Comparison Matrix

### Method Comparison

| Method | Win→Win | Win→Linux | Linux→Win | Complexity | Security | Speed |
|--------|---------|-----------|-----------|------------|----------|-------|
| **PowerShell Remoting** | ✅ | ❌ | ❌ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **SSH (OpenSSH)** | ✅ | ✅ | ✅ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **WinRM** | ✅ | ❌ | ✅ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **HTTP/REST API** | ✅ | ✅ | ✅ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **MQTT** | ✅ | ✅ | ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **gRPC** | ✅ | ✅ | ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Task Scheduler** | ✅ | ❌ | ❌ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

### Performance Benchmarks

**Latency (Average execution time for "Hello World" script)**

```
Local Network (1 Gbps):
├─ PowerShell Remoting:  150-250ms
├─ SSH:                  100-200ms
├─ WinRM:                200-300ms
├─ HTTP API:             50-150ms
├─ MQTT:                 20-80ms
└─ gRPC:                 30-100ms

Remote Network (Over Internet):
├─ SSH (VPN):            300-500ms
├─ HTTP API (HTTPS):     200-400ms
└─ MQTT (TLS):           100-300ms
```

**Resource Usage (Server-side)**

```
Memory Consumption:
├─ SSH Daemon:           5-15 MB
├─ Flask API:            30-60 MB
├─ MQTT Broker:          10-30 MB
├─ gRPC Server:          20-40 MB
└─ WinRM Service:        15-25 MB

CPU Usage (Idle):
├─ SSH:                  <1%
├─ API Server:           1-2%
├─ MQTT:                 <1%
└─ gRPC:                 <1%
```

### Use Case Recommendations

**Scenario 1: Simple Script Execution**
- **Best Choice:** SSH
- **Why:** Simple, secure, built-in to most systems
- **Implementation Time:** 10-15 minutes

**Scenario 2: Windows-Only Environment**
- **Best Choice:** PowerShell Remoting
- **Why:** Native Windows support, no extra software
- **Implementation Time:** 5-10 minutes

**Scenario 3: Mixed OS Environment**
- **Best Choice:** HTTP REST API or SSH
- **Why:** Universal compatibility, easy to implement
- **Implementation Time:** 30-60 minutes

**Scenario 4: IoT/Multiple Devices**
- **Best Choice:** MQTT
- **Why:** Scalable, asynchronous, lightweight
- **Implementation Time:** 60-90 minutes

**Scenario 5: High-Performance Requirements**
- **Best Choice:** gRPC
- **Why:** Fast, efficient, type-safe
- **Implementation Time:** 90-120 minutes

**Scenario 6: Legacy Systems**
- **Best Choice:** HTTP API
- **Why:** Broad compatibility, simple integration
- **Implementation Time:** 30-45 minutes

---

## Advanced Scenarios

### Scenario 1: Multi-Machine Orchestration

Execute scripts on multiple machines in parallel:

```python
# multi_executor.py
import concurrent.futures
import paramiko
import time

class MultiMachineExecutor:
    def __init__(self):
        self.machines = []
    
    def add_machine(self, name, host, username, password, os_type):
        """Add machine to execution pool"""
        self.machines.append({
            'name': name,
            'host': host,
            'username': username,
            'password': password,
            'os_type': os_type
        })
    
    def execute_on_machine(self, machine, script_path):
        """Execute script on a single machine"""
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                machine['host'],
                username=machine['username'],
                password=machine['password']
            )
            
            # Adjust command based on OS
            if machine['os_type'] == 'Windows':
                command = f'python "{script_path}"'
            else:
                command = f'python3 {script_path}'
            
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            exit_code = stdout.channel.recv_exit_status()
            
            client.close()
            
            return {
                'machine': machine['name'],
                'host': machine['host'],
                'success': exit_code == 0,
                'output': output,
                'error': error
            }
        except Exception as e:
            return {
                'machine': machine['name'],
                'host': machine['host'],
                'success': False,
                'error': str(e)
            }
    
    def execute_parallel(self, script_paths):
        """Execute scripts on all machines in parallel"""
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            for machine in self.machines:
                # Get appropriate script path for this machine
                if machine['os_type'] == 'Windows':
                    script = script_paths.get('windows', script_paths.get('default'))
                else:
                    script = script_paths.get('linux', script_paths.get('default'))
                
                future = executor.submit(self.execute_on_machine, machine, script)
                futures.append(future)
            
            # Wait for all to complete
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
        
        return results
    
    def execute_sequential(self, script_paths):
        """Execute scripts sequentially"""
        results = []
        
        for machine in self.machines:
            if machine['os_type'] == 'Windows':
                script = script_paths.get('windows', script_paths.get('default'))
            else:
                script = script_paths.get('linux', script_paths.get('default'))
            
            result = self.execute_on_machine(machine, script)
            results.append(result)
            
            # Optional: Stop on first failure
            if not result['success']:
                print(f"Execution failed on {machine['name']}, stopping...")
                break
        
        return results

# Usage
if __name__ == "__main__":
    executor = MultiMachineExecutor()
    
    # Add Windows machines
    executor.add_machine(
        name="Windows-1",
        host="192.168.1.10",
        username="admin",
        password="pass123",
        os_type="Windows"
    )
    
    executor.add_machine(
        name="Windows-2",
        host="192.168.1.20",
        username="admin",
        password="pass123",
        os_type="Windows"
    )
    
    # Add Linux machines
    executor.add_machine(
        name="RedHat-1",
        host="192.168.1.30",
        username="root",
        password="pass123",
        os_type="Linux"
    )
    
    # Execute same script on all machines
    print("Executing in parallel...")
    results = executor.execute_parallel({
        'windows': 'C:\\Scripts\\deploy.py',
        'linux': '/opt/scripts/deploy.py'
    })
    
    # Print results
    for result in results:
        print(f"\n=== {result['machine']} ({result['host']}) ===")
        if result['success']:
            print("✓ Success")
            print(f"Output: {result['output']}")
        else:
            print("✗ Failed")
            print(f"Error: {result['error']}")
```

### Scenario 2: Scheduled Cross-Platform Tasks

Create a scheduler that works across platforms:

```python
# cross_platform_scheduler.py
import schedule
import time
import platform
from datetime import datetime
import json

class CrossPlatformScheduler:
    def __init__(self, config_file='schedule_config.json'):
        self.config_file = config_file
        self.tasks = []
        self.load_config()
    
    def load_config(self):
        """Load scheduling configuration"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.tasks = config.get('tasks', [])
        except FileNotFoundError:
            print("Config file not found, using empty schedule")
    
    def execute_remote_script(self, task):
        """Execute script on remote machine"""
        from universal_client import UniversalExecutor
        
        executor = UniversalExecutor(
            host=task['host'],
            api_key=task.get('api_key')
        )
        
        result = executor.execute_script(
            script_path=task['script_path'],
            args=task.get('args', [])
        )
        
        # Log result
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'task': task['name'],
            'host': task['host'],
            'success': result.get('success', False),
            'output': result.get('stdout', '')[:200]  # First 200 chars
        }
        
        with open('scheduler.log', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        return result
    
    def schedule_task(self, task):
        """Schedule a task based on its schedule type"""
        schedule_type = task.get('schedule_type')
        
        if schedule_type == 'interval':
            # Run every X minutes/hours
            interval = task.get('interval', 60)
            unit = task.get('unit', 'minutes')
            
            if unit == 'minutes':
                schedule.every(interval).minutes.do(
                    self.execute_remote_script, task
                )
            elif unit == 'hours':
                schedule.every(interval).hours.do(
                    self.execute_remote_script, task
                )
        
        elif schedule_type == 'daily':
            # Run daily at specific time
            time_str = task.get('time', '00:00')
            schedule.every().day.at(time_str).do(
                self.execute_remote_script, task
            )
        
        elif schedule_type == 'weekly':
            # Run weekly on specific day
            day = task.get('day', 'monday')
            time_str = task.get('time', '00:00')
            
            getattr(schedule.every(), day).at(time_str).do(
                self.execute_remote_script, task
            )
        
        print(f"Scheduled task: {task['name']} ({schedule_type})")
    
    def start(self):
        """Start the scheduler"""
        # Schedule all tasks
        for task in self.tasks:
            if task.get('enabled', True):
                self.schedule_task(task)
        
        print(f"Scheduler started on {platform.system()}")
        print(f"Total scheduled tasks: {len(schedule.jobs)}")
        
        # Run scheduler loop
        while True:
            schedule.run_pending()
            time.sleep(1)

# Example configuration file: schedule_config.json
"""
{
    "tasks": [
        {
            "name": "Daily Backup - Windows",
            "host": "192.168.1.10",
            "api_key": "secret-key",
            "script_path": "C:\\Scripts\\backup.py",
            "args": ["--full"],
            "schedule_type": "daily",
            "time": "02:00",
            "enabled": true
        },
        {
            "name": "Hourly Health Check - Linux",
            "host": "192.168.1.30",
            "api_key": "secret-key",
            "script_path": "/opt/scripts/health_check.py",
            "schedule_type": "interval",
            "interval": 1,
            "unit": "hours",
            "enabled": true
        },
        {
            "name": "Weekly Report - Windows",
            "host": "192.168.1.20",
            "api_key": "secret-key",
            "script_path": "C:\\Scripts\\report.py",
            "schedule_type": "weekly",
            "day": "monday",
            "time": "09:00",
            "enabled": true
        }
    ]
}
"""

# Usage
if __name__ == "__main__":
    scheduler = CrossPlatformScheduler('schedule_config.json')
    scheduler.start()
```

### Scenario 3: File Synchronization Before Execution

```python
# sync_and_execute.py
import os
import hashlib
import paramiko
from pathlib import Path

class SyncExecutor:
    def __init__(self, host, username, password, os_type):
        self.host = host
        self.username = username
        self.password = password
        self.os_type = os_type
        self.client = None
    
    def connect(self):
        """Establish SSH connection"""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(
            self.host,
            username=self.username,
            password=self.password
        )
    
    def calculate_file_hash(self, file_path):
        """Calculate MD5 hash of file"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def get_remote_file_hash(self, remote_path):
        """Get hash of remote file"""
        try:
            if self.os_type == 'Windows':
                command = f'certutil -hashfile "{remote_path}" MD5'
            else:
                command = f'md5sum "{remote_path}"'
            
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode('utf-8')
            
            if self.os_type == 'Windows':
                # Parse certutil output
                lines = output.split('\n')
                if len(lines) >= 2:
                    return lines[1].strip().replace(' ', '')
            else:
                # Parse md5sum output
                return output.split()[0]
        except:
            return None
    
    def sync_file(self, local_path, remote_path):
        """Sync file only if different"""
        local_hash = self.calculate_file_hash(local_path)
        remote_hash = self.get_remote_file_hash(remote_path)
        
        if local_hash != remote_hash:
            print(f"File changed, uploading: {local_path}")
            sftp = self.client.open_sftp()
            
            # Create remote directory if needed
            remote_dir = os.path.dirname(remote_path)
            if self.os_type != 'Windows':
                try:
                    sftp.mkdir(remote_dir)
                except:
                    pass
            
            sftp.put(local_path, remote_path)
            sftp.close()
            print(f"✓ Uploaded to {remote_path}")
            return True
        else:
            print(f"File unchanged, skipping: {local_path}")
            return False
    
    def sync_directory(self, local_dir, remote_dir):
        """Sync entire directory"""
        uploaded = []
        
        for root, dirs, files in os.walk(local_dir):
            for file in files:
                local_path = os.path.join(root, file)
                
                # Calculate relative path
                rel_path = os.path.relpath(local_path, local_dir)
                
                # Convert to remote path format
                if self.os_type == 'Windows':
                    remote_path = os.path.join(remote_dir, rel_path).replace('/', '\\')
                else:
                    remote_path = os.path.join(remote_dir, rel_path).replace('\\', '/')
                
                if self.sync_file(local_path, remote_path):
                    uploaded.append(remote_path)
        
        return uploaded
    
    def execute_script(self, script_path, args=None):
        """Execute script on remote machine"""
        if self.os_type == 'Windows':
            command = f'python "{script_path}"'
        else:
            command = f'python3 {script_path}'
        
        if args:
            command += f" {' '.join(args)}"
        
        stdin, stdout, stderr = self.client.exec_command(command)
        
        return {
            'stdout': stdout.read().decode('utf-8'),
            'stderr': stderr.read().decode('utf-8'),
            'exit_code': stdout.channel.recv_exit_status()
        }
    
    def close(self):
        """Close connection"""
        if self.client:
            self.client.close()

# Usage
if __name__ == "__main__":
    # Sync and execute on Windows
    executor = SyncExecutor(
        host="192.168.1.10",
        username="admin",
        password="pass123",
        os_type="Windows"
    )
    
    executor.connect()
    
    # Sync entire project directory
    executor.sync_directory(
        local_dir="./project",
        remote_dir="C:\\Projects\\myproject"
    )
    
    # Execute main script
    result = executor.execute_script("C:\\Projects\\myproject\\main.py")
    print("Output:", result['stdout'])
    
    executor.close()
```

### Scenario 4: Load Balancing Across Machines

```python
# load_balancer.py
import time
import threading
from queue import Queue
from universal_client import UniversalExecutor

class LoadBalancer:
    def __init__(self):
        self.machines = []
        self.task_queue = Queue()
        self.results = []
        self.lock = threading.Lock()
    
    def add_machine(self, name, host, api_key):
        """Add machine to the pool"""
        self.machines.append({
            'name': name,
            'host': host,
            'api_key': api_key,
            'executor': UniversalExecutor(host, api_key=api_key),
            'busy': False,
            'tasks_completed': 0
        })
    
    def worker(self, machine):
        """Worker thread for each machine"""
        while True:
            task = self.task_queue.get()
            
            if task is None:  # Poison pill to stop worker
                break
            
            machine['busy'] = True
            
            try:
                print(f"[{machine['name']}] Executing: {task['script']}")
                result = machine['executor'].execute_script(
                    script_path=task['script'],
                    args=task.get('args', [])
                )
                
                with self.lock:
                    self.results.append({
                        'task_id': task['id'],
                        'machine': machine['name'],
                        'result': result
                    })
                    machine['tasks_completed'] += 1
                
                print(f"[{machine['name']}] Completed task {task['id']}")
            
            except Exception as e:
                print(f"[{machine['name']}] Error: {e}")
            
            finally:
                machine['busy'] = False
                self.task_queue.task_done()
    
    def add_task(self, task_id, script_path, args=None):
        """Add task to queue"""
        self.task_queue.put({
            'id': task_id,
            'script': script_path,
            'args': args or []
        })
    
    def start(self):
        """Start worker threads"""
        threads = []
        
        for machine in self.machines:
            thread = threading.Thread(
                target=self.worker,
                args=(machine,),
                daemon=True
            )
            thread.start()
            threads.append(thread)
        
        return threads
    
    def stop(self):
        """Stop all workers"""
        for _ in self.machines:
            self.task_queue.put(None)
    
    def wait_completion(self):
        """Wait for all tasks to complete"""
        self.task_queue.join()
    
    def get_statistics(self):
        """Get load balancer statistics"""
        stats = {
            'total_tasks': len(self.results),
            'machines': []
        }
        
        for machine in self.machines:
            stats['machines'].append({
                'name': machine['name'],
                'host': machine['host'],
                'busy': machine['busy'],
                'tasks_completed': machine['tasks_completed']
            })
        
        return stats

# Usage
if __name__ == "__main__":
    balancer = LoadBalancer()
    
    # Add machines
    balancer.add_machine(
        name="Windows-1",
        host="192.168.1.10",
        api_key="secret-key"
    )
    
    balancer.add_machine(
        name="Windows-2",
        host="192.168.1.20",
        api_key="secret-key"
    )
    
    balancer.add_machine(
        name="Linux-1",
        host="192.168.1.30",
        api_key="secret-key"
    )
    
    # Start workers
    balancer.start()
    
    # Add tasks
    for i in range(20):
        if i % 2 == 0:
            balancer.add_task(
                task_id=f"task-{i}",
                script_path="C:\\Scripts\\process_data.py",
                args=[f"--batch={i}"]
            )
        else:
            balancer.add_task(
                task_id=f"task-{i}",
                script_path="/opt/scripts/process_data.py",
                args=[f"--batch={i}"]
            )
    
    # Wait for completion
    print("Processing tasks...")
    balancer.wait_completion()
    
    # Get statistics
    stats = balancer.get_statistics()
    print("\n=== Statistics ===")
    print(f"Total tasks completed: {stats['total_tasks']}")
    for machine in stats['machines']:
        print(f"{machine['name']}: {machine['tasks_completed']} tasks")
    
    balancer.stop()
```

---

## Best Practices Summary

### 1. Security
- ✅ Always use SSH keys instead of passwords
- ✅ Implement API authentication
- ✅ Use HTTPS/TLS for API communication
- ✅ Validate and sanitize all inputs
- ✅ Use firewalls to restrict access
- ✅ Log all execution attempts
- ✅ Regularly update all systems

### 2. Reliability
- ✅ Implement retry logic
- ✅ Handle timeouts gracefully
- ✅ Log errors comprehensively
- ✅ Monitor system health
- ✅ Use connection pooling
- ✅ Implement failover mechanisms

### 3. Performance
- ✅ Use parallel execution when possible
- ✅ Cache connections
- ✅ Minimize data transfer
- ✅ Use compression for large files
- ✅ Implement load balancing
- ✅ Monitor resource usage

### 4. Maintainability
- ✅ Document all configurations
- ✅ Use configuration files
- ✅ Implement proper logging
- ✅ Version control scripts
- ✅ Use descriptive naming
- ✅ Comment complex logic

### 5. Cross-Platform Compatibility
- ✅ Use platform-agnostic methods
- ✅ Handle path separators correctly
- ✅ Check OS before executing
- ✅ Test on all target platforms
- ✅ Use appropriate Python commands (python vs python3)

---

## Quick Reference Commands

### Windows Commands
```powershell
# Check connectivity
Test-Connection 192.168.1.30

# Enable PowerShell Remoting
Enable-PSRemoting -Force

# Install OpenSSH
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Start SSH service
Start-Service sshd

# Test SSH
ssh user@192.168.1.30

# Execute remote PowerShell
Invoke-Command -ComputerName 192.168.1.20 -ScriptBlock { python script.py }
```

### Linux Commands
```bash
# Check connectivity
ping 192.168.1.10

# Install SSH
sudo yum install -y openssh-server

# Start SSH
sudo systemctl start sshd

# Test SSH
ssh user@192.168.1.10

# Execute remote command
ssh user@192.168.1.10 "python3 /path/to/script.py"

# Copy file
scp local.py user@192.168.1.10:/remote/path/
```

### Python Quick Commands
```python
# SSH execution
import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('192.168.1.30', username='user', password='pass')
stdin, stdout, stderr = client.exec_command('python3 script.py')
print(stdout.read().decode())
client.close()

# HTTP API call
import requests
response = requests.post(
    'http://192.168.1.30:5000/execute',
    json={'script': '/path/to/script.py'},
    headers={'X-API-Key': 'your-key'}
)
print(response.json())
```

---

## Conclusion

This guide provides comprehensive methods for executing Python scripts across different operating systems and IP addresses. Choose the method that best fits your requirements:

- **For simplicity:** Use SSH
- **For Windows-only:** Use PowerShell Remoting
- **For flexibility:** Use HTTP REST API
- **For scale:** Use MQTT or gRPC
- **For performance:** Use gRPC or native tools

Always prioritize security, test thoroughly, and document your implementation for future reference.

---

**Version:** 1.0  
**Last Updated:** September 30, 2025  
**Maintained By:** Cadfem IT  
**Author:** Naga Malleswara Rao# Cross-Platform Remote Script Execution Guide

## Table of Contents
1. [Overview](#overview)
2. [Network Configuration](#network-configuration)
3. [Windows to Windows Execution](#windows-to-windows-execution)
4. [Windows to Linux (Red Hat)](#windows-to-linux-red-hat)
5. [Linux to Windows Execution](#linux-to-windows-execution)
6. [Universal Methods (Cross-Platform)](#universal-methods-cross-platform)
7. [Security Best Practices](#security-best-practices)
8. [Troubleshooting](#troubleshooting)
9. [Comparison Matrix](#comparison-matrix)

---

## Overview

This guide covers remote script execution across different operating systems with different IP addresses.

### Sample Network Setup

```
┌─────────────────────────────────────────────────────────┐
│                    Network: 192.168.1.0/24              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Windows Machine 1        Windows Machine 2            │
│  IP: 192.168.1.10         IP: 192.168.1.20            │
│  Script: controller.py    Script: target.py           │
│                                                         │
│  Red Hat Linux            Windows Machine 3            │
│  IP: 192.168.1.30         IP: 192.168.1.40            │
│  Script: server.py        Script: worker.py           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Network Configuration

### Prerequisites for All Systems

1. **Ensure Network Connectivity**
```bash
# Test from any machine
ping 192.168.1.10
ping 192.168.1.20
ping 192.168.1.30
```

2. **Configure Firewalls**
- Allow necessary ports
- Add firewall exceptions
- Configure network profiles

3. **Install Python**
- Ensure Python is installed on all systems
- Add Python to PATH

---

## Windows to Windows Execution

### Method 1: PowerShell Remoting (Recommended)

#### Setup on Target Windows (192.168.1.20)

**Step 1: Enable PowerShell Remoting**
```powershell
# Run as Administrator
Enable-PSRemoting -Force

# Configure trusted hosts (if not in domain)
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "192.168.1.10" -Force

# Restart WinRM service
Restart-Service WinRM

# Verify configuration
Get-PSSessionConfiguration
```

**Step 2: Configure Firewall**
```powershell
# Allow WinRM
New-NetFirewallRule -Name "WinRM-HTTP" -DisplayName "Windows Remote Management (HTTP-In)" -Enabled True -Direction Inbound -Protocol TCP -LocalPort 5985

# Or use the built-in rule
Enable-NetFirewallRule -Name "WINRM-HTTP-In-TCP"
```

**Step 3: Create User Account (if needed)**
```powershell
# Create user for remote access
net user remoteuser Password123! /add
net localgroup Administrators remoteuser /add
```

#### Execution from Controller Windows (192.168.1.10)

**Basic Remote Execution:**
```powershell
# Create credentials
$username = "remoteuser"
$password = ConvertTo-SecureString "Password123!" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential($username, $password)

# Execute Python script remotely
Invoke-Command -ComputerName 192.168.1.20 -Credential $cred -ScriptBlock {
    python C:\Scripts\target.py
}

# Execute with arguments
Invoke-Command -ComputerName 192.168.1.20 -Credential $cred -ScriptBlock {
    param($arg1, $arg2)
    python C:\Scripts\target.py $arg1 $arg2
} -ArgumentList "value1", "value2"

# Capture output
$result = Invoke-Command -ComputerName 192.168.1.20 -Credential $cred -ScriptBlock {
    python C:\Scripts\target.py 2>&1 | Out-String
}
Write-Host $result
```

**Python Script for PowerShell Remoting:**
```python
# controller.py (Windows 192.168.1.10)
import subprocess
import json

class WindowsRemoteExecutor:
    def __init__(self, target_ip, username, password):
        self.target_ip = target_ip
        self.username = username
        self.password = password
    
    def execute_script(self, script_path, args=None):
        """Execute Python script on remote Windows machine"""
        # Build PowerShell command
        ps_command = f"""
        $password = ConvertTo-SecureString '{self.password}' -AsPlainText -Force
        $cred = New-Object System.Management.Automation.PSCredential('{self.username}', $password)
        
        Invoke-Command -ComputerName {self.target_ip} -Credential $cred -ScriptBlock {{
            python {script_path}
        }}
        """
        
        try:
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def upload_and_execute(self, local_path, remote_path):
        """Upload script then execute"""
        # Copy file first
        copy_command = f"""
        $password = ConvertTo-SecureString '{self.password}' -AsPlainText -Force
        $cred = New-Object System.Management.Automation.PSCredential('{self.username}', $password)
        
        $session = New-PSSession -ComputerName {self.target_ip} -Credential $cred
        Copy-Item -Path '{local_path}' -Destination '{remote_path}' -ToSession $session
        Remove-PSSession $session
        """
        
        try:
            # Upload file
            subprocess.run(
                ["powershell", "-Command", copy_command],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Execute
            return self.execute_script(remote_path)
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Usage
if __name__ == "__main__":
    executor = WindowsRemoteExecutor(
        target_ip="192.168.1.20",
        username="remoteuser",
        password="Password123!"
    )
    
    # Execute remote script
    result = executor.execute_script("C:\\Scripts\\target.py")
    
    if result['success']:
        print("Output:", result['stdout'])
    else:
        print("Error:", result.get('error', result['stderr']))
```

### Method 2: SSH on Windows (OpenSSH)

**Step 1: Install OpenSSH on Target Windows (192.168.1.20)**
```powershell
# Check if OpenSSH is available
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'

# Install OpenSSH Server
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Start and configure SSH service
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

# Configure firewall
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

**Step 2: Execute from Controller Windows (192.168.1.10)**
```python
# controller.py using Paramiko
import paramiko

class WindowsSSHExecutor:
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
        """Execute Python script via SSH"""
        if not self.client:
            return None
        
        command = f"python {script_path}"
        if args:
            command += f" {' '.join(args)}"
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            
            return {
                'stdout': stdout.read().decode('utf-8'),
                'stderr': stderr.read().decode('utf-8'),
                'exit_code': stdout.channel.recv_exit_status()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def close(self):
        """Close connection"""
        if self.client:
            self.client.close()

# Usage
executor = WindowsSSHExecutor(
    host="192.168.1.20",
    username="remoteuser",
    password="Password123!"
)

if executor.connect():
    result = executor.execute_script("C:\\Scripts\\target.py")
    print("Output:", result['stdout'])
    executor.close()
```

### Method 3: Task Scheduler Remote Execution

**Step 1: Create Task on Target Windows (192.168.1.20)**
```powershell
# Create scheduled task that runs on demand
$action = New-ScheduledTaskAction -Execute "python" -Argument "C:\Scripts\target.py"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date)
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

Register-ScheduledTask -TaskName "RemoteExecution" -Action $action -Trigger $trigger -Principal $principal
```

**Step 2: Trigger from Controller Windows (192.168.1.10)**
```python
# controller.py
import subprocess

class TaskSchedulerExecutor:
    def __init__(self, target_ip, username, password):
        self.target_ip = target_ip
        self.username = username
        self.password = password
    
    def execute_task(self, task_name):
        """Trigger scheduled task remotely"""
        command = [
            "schtasks",
            "/Run",
            "/S", self.target_ip,
            "/U", self.username,
            "/P", self.password,
            "/TN", task_name
        ]
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def check_task_status(self, task_name):
        """Check task status"""
        command = [
            "schtasks",
            "/Query",
            "/S", self.target_ip,
            "/U", self.username,
            "/P", self.password,
            "/TN", task_name,
            "/FO", "LIST",
            "/V"
        ]
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )
            return result.stdout
        except Exception as e:
            return str(e)

# Usage
executor = TaskSchedulerExecutor(
    target_ip="192.168.1.20",
    username="remoteuser",
    password="Password123!"
)

result = executor.execute_task("RemoteExecution")
if result['success']:
    print("Task executed successfully")
else:
    print("Error:", result['error'])
```

---

## Windows to Linux (Red Hat)

### Method 1: SSH from Windows to Linux

**Setup on Red Hat Linux (192.168.1.30)**

**Step 1: Install and Configure OpenSSH**
```bash
# Install OpenSSH server
sudo yum install -y openssh-server

# Start and enable SSH
sudo systemctl start sshd
sudo systemctl enable sshd

# Check status
sudo systemctl status sshd
```

**Step 2: Configure Firewall**
```bash
# Allow SSH through firewall
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload

# Verify
sudo firewall-cmd --list-all
```

**Step 3: Create User (if needed)**
```bash
# Create user
sudo useradd -m remoteuser
sudo passwd remoteuser

# Add to sudoers (optional)
sudo usermod -aG wheel remoteuser
```

#### Execution from Windows (192.168.1.10)

**Method A: Using Paramiko (Python)**
```python
# controller.py (Windows)
import paramiko
import os

class LinuxRemoteExecutor:
    def __init__(self, host, username, password=None, key_file=None):
        self.host = host
        self.username = username
        self.password = password
        self.key_file = key_file
        self.client = None
    
    def connect(self):
        """Connect to Linux machine"""
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
            print(f"✓ Connected to Linux host {self.host}")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def execute_script(self, script_path, args=None):
        """Execute Python script on Linux"""
        if not self.client:
            return None
        
        command = f"python3 {script_path}"
        if args:
            command += f" {' '.join(args)}"
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            exit_code = stdout.channel.recv_exit_status()
            
            return {
                'success': exit_code == 0,
                'stdout': output,
                'stderr': error,
                'exit_code': exit_code
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def upload_and_execute(self, local_path, remote_path):
        """Upload script from Windows to Linux and execute"""
        if not self.client:
            return None
        
        try:
            # Upload using SFTP
            sftp = self.client.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.chmod(remote_path, 0o755)  # Make executable
            sftp.close()
            
            print(f"✓ Uploaded {local_path} to {remote_path}")
            
            # Execute
            return self.execute_script(remote_path)
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def execute_bash_command(self, command):
        """Execute bash command"""
        if not self.client:
            return None
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            
            return {
                'stdout': stdout.read().decode('utf-8'),
                'stderr': stderr.read().decode('utf-8'),
                'exit_code': stdout.channel.recv_exit_status()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def close(self):
        """Close connection"""
        if self.client:
            self.client.close()
            print("✓ Connection closed")

# Usage
if __name__ == "__main__":
    executor = LinuxRemoteExecutor(
        host="192.168.1.30",
        username="remoteuser",
        password="Password123!"
    )
    
    if executor.connect():
        # Execute existing script on Linux
        result = executor.execute_script("/home/remoteuser/server.py")
        
        if result['success']:
            print("Output:", result['stdout'])
        else:
            print("Error:", result.get('error', result['stderr']))
        
        # Upload and execute
        result = executor.upload_and_execute(
            local_path="C:\\Scripts\\controller.py",
            remote_path="/home/remoteuser/uploaded_script.py"
        )
        
        executor.close()
```

**Method B: Using PuTTY/Plink (Command Line)**
```python
# controller.py using plink
import subprocess

class PlinkExecutor:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        # Download plink.exe from PuTTY website
        self.plink_path = "C:\\Tools\\plink.exe"
    
    def execute_script(self, script_path):
        """Execute script using plink"""
        command = [
            self.plink_path,
            "-ssh",
            f"{self.username}@{self.host}",
            "-pw", self.password,
            f"python3 {script_path}"
        ]
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Usage
executor = PlinkExecutor(
    host="192.168.1.30",
    username="remoteuser",
    password="Password123!"
)

result = executor.execute_script("/home/remoteuser/server.py")
print(result)
```

### Method 2: HTTP API (Cross-Platform)

**Setup Flask API on Red Hat Linux (192.168.1.30)**
```python
# api_server.py on Linux
from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)
CORS(app)

# Configuration
API_KEY = "secure-api-key-12345"
ALLOWED_SCRIPTS_DIR = "/scripts" if platform.system() != "Windows" else "C:\\Scripts"

def verify_api_key():
    """Verify API key from request header"""
    key = request.headers.get('X-API-Key')
    return key == API_KEY

def get_python_command():
    """Get appropriate Python command for OS"""
    return "python" if platform.system() == "Windows" else "python3"

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'platform': platform.system(),
        'hostname': platform.node(),
        'python_version': platform.python_version()
    })

@app.route('/execute', methods=['POST'])
def execute_script():
    """Execute script on any OS"""
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    script_path = data.get('script')
    args = data.get('args', [])
    working_dir = data.get('working_dir', None)
    
    if not script_path:
        return jsonify({'error': 'No script specified'}), 400
    
    # Security: Validate script path
    if not os.path.exists(script_path):
        return jsonify({'error': 'Script not found'}), 404
    
    try:
        python_cmd = get_python_command()
        command = [python_cmd, script_path] + args
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=working_dir
        )
        
        return jsonify({
            'success': True,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
            'platform': platform.system()
        })
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Execution timeout'
        }), 408
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/system/info', methods=['GET'])
def system_info():
    """Get system information"""
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        return jsonify({
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'hostname': platform.node(),
            'processor': platform.processor(),
            'python_version': platform.python_version()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/files/list', methods=['POST'])
def list_files():
    """List files in directory"""
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    directory = data.get('directory', ALLOWED_SCRIPTS_DIR)
    
    try:
        files = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            files.append({
                'name': item,
                'path': item_path,
                'is_file': os.path.isfile(item_path),
                'is_dir': os.path.isdir(item_path)
            })
        
        return jsonify({
            'success': True,
            'directory': directory,
            'files': files
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print(f"Starting Universal API Server on {platform.system()}")
    print(f"Platform: {platform.system()} {platform.release()}")
    app.run(host='0.0.0.0', port=5000, debug=False)
```

**Universal Client (Works on any OS)**
```python
# universal_client.py
import requests
import platform
import json

class UniversalExecutor:
    def __init__(self, host, port=5000, api_key=None):
        self.base_url = f"http://{host}:{port}"
        self.api_key = api_key
        self.headers = {
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        } if api_key else {'Content-Type': 'application/json'}
    
    def health_check(self):
        """Check server health"""
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def execute_script(self, script_path, args=None, working_dir=None):
        """Execute script on remote machine"""
        payload = {
            'script': script_path,
            'args': args or [],
            'working_dir': working_dir
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/execute",
                json=payload,
                headers=self.headers,
                timeout=120
            )
            
            return response.json()
        except requests.Timeout:
            return {
                'success': False,
                'error': 'Request timeout'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_system_info(self):
        """Get remote system information"""
        try:
            response = requests.get(
                f"{self.base_url}/system/info",
                headers=self.headers,
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def list_files(self, directory):
        """List files in remote directory"""
        payload = {'directory': directory}
        
        try:
            response = requests.post(
                f"{self.base_url}/files/list",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {'error': str(e)}

# Usage Examples
if __name__ == "__main__":
    print(f"Running on: {platform.system()}")
    
    # Example 1: Windows to Windows
    if platform.system() == "Windows":
        executor = UniversalExecutor(
            host="192.168.1.20",
            api_key="secure-api-key-12345"
        )
        
        result = executor.execute_script("C:\\Scripts\\target.py")
        print("Windows Result:", result)
    
    # Example 2: Windows to Linux
    if platform.system() == "Windows":
        executor = UniversalExecutor(
            host="192.168.1.30",
            api_key="secure-api-key-12345"
        )
        
        result = executor.execute_script("/home/remoteuser/server.py")
        print("Linux Result:", result)
    
    # Example 3: Linux to Windows
    if platform.system() == "Linux":
        executor = UniversalExecutor(
            host="192.168.1.40",
            api_key="secure-api-key-12345"
        )
        
        result = executor.execute_script("C:\\Scripts\\worker.py")
        print("Windows Result:", result)
    
    # Example 4: Get system info
    executor = UniversalExecutor(
        host="192.168.1.30",
        api_key="secure-api-key-12345"
    )
    
    info = executor.get_system_info()
    print("System Info:", json.dumps(info, indent=2))
```

### Method 2: MQTT (Message Queue for IoT)

**Install MQTT Broker (Mosquitto) - Can run on any OS**

**On Windows:**
```powershell
# Download from https://mosquitto.org/download/
# Install and start service
net start mosquitto
```

**On Red Hat Linux:**
```bash
sudo yum install -y mosquitto mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
sudo firewall-cmd --permanent --add-port=1883/tcp
sudo firewall-cmd --reload
```

**Universal MQTT Client**
```python
# mqtt_universal_client.py
import paho.mqtt.client as mqtt
import json
import subprocess
import platform
import time

class UniversalMQTTExecutor:
    def __init__(self, broker, port=1883, client_id=None):
        self.broker = broker
        self.port = port
        self.client_id = client_id or f"{platform.node()}_{int(time.time())}"
        self.client = mqtt.Client(client_id=self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.system_type = platform.system()
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback when connected"""
        if rc == 0:
            print(f"✓ Connected to MQTT Broker [{self.system_type}]")
            # Subscribe to execution commands for this machine
            self.client.subscribe(f"execute/{self.client_id}")
            self.client.subscribe("execute/broadcast")
        else:
            print(f"✗ Connection failed with code {rc}")
    
    def on_message(self, client, userdata, message):
        """Callback when message received"""
        try:
            payload = json.loads(message.payload.decode('utf-8'))
            command_type = payload.get('type')
            
            if command_type == 'execute':
                self.handle_execute(payload)
            elif command_type == 'status':
                self.send_status()
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def handle_execute(self, payload):
        """Handle script execution request"""
        script_path = payload.get('script')
        args = payload.get('args', [])
        
        print(f"Executing: {script_path}")
        
        try:
            python_cmd = "python" if self.system_type == "Windows" else "python3"
            command = [python_cmd, script_path] + args
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            response = {
                'client_id': self.client_id,
                'platform': self.system_type,
                'success': True,
                'script': script_path,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'timestamp': time.time()
            }
            
        except Exception as e:
            response = {
                'client_id': self.client_id,
                'platform': self.system_type,
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
        
        # Publish result
        self.client.publish(
            f"result/{self.client_id}",
            json.dumps(response)
        )
    
    def send_status(self):
        """Send system status"""
        status = {
            'client_id': self.client_id,
            'platform': self.system_type,
            'hostname': platform.node(),
            'online': True,
            'timestamp': time.time()
        }
        
        self.client.publish(
            f"status/{self.client_id}",
            json.dumps(status)
        )
    
    def start(self):
        """Connect and start listening"""
        try:
            self.client.connect(self.broker, self.port, keepalive=60)
            print(f"Connecting to MQTT Broker at {self.broker}:{self.port}")
            self.client.loop_forever()
        except Exception as e:
            print(f"Connection error: {e}")

# Usage - Run this on each machine
if __name__ == "__main__":
    # Use local broker or public broker
    BROKER = "192.168.1.10"  # Or "broker.hivemq.com" for testing
    
    executor = UniversalMQTTExecutor(BROKER)
    executor.start()
```

**MQTT Controller (Send commands from any machine)**
```python
# mqtt_controller.py
import paho.mqtt.client as mqtt
import json
import time

class MQTTController:
    def __init__(self, broker, port=1883):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(client_id="controller")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.results = {}
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback when connected"""
        if rc == 0:
            print("✓ Controller connected to MQTT Broker")
            # Subscribe to all results
            self.client.subscribe("result/#")
            self.client.subscribe("status/#")
        else:
            print(f"✗ Connection failed with code {rc}")
    
    def on_message(self, client, userdata, message):
        """Handle responses"""
        try:
            data = json.loads(message.payload.decode('utf-8'))
            
            if message.topic.startswith("result/"):
                print("\n--- Execution Result ---")
                print(f"Client: {data.get('client_id')}")
                print(f"Platform: {data.get('platform')}")
                
                if data.get('success'):
                    print(f"Status: Success ✓")
                    print(f"Output:\n{data.get('stdout')}")
                else:
                    print(f"Status: Failed ✗")
                    print(f"Error: {data.get('error')}")
                
                self.results[data.get('client_id')] = data
            
            elif message.topic.startswith("status/"):
                print(f"\n--- Status: {data.get('client_id')} ---")
                print(f"Platform: {data.get('platform')}")
                print(f"Hostname: {data.get('hostname')}")
                print(f"Online: {data.get('online')}")
        
        except Exception as e:
            print(f"Error processing response: {e}")
    
    def execute_on_client(self, client_id, script_path, args=None):
        """Send execution command to specific client"""
        command = {
            'type': 'execute',
            'script': script_path,
            'args': args or []
        }
        
        topic = f"execute/{client_id}"
        self.client.publish(topic, json.dumps(command))
        print(f"Sent command to {client_id}: {script_path}")
    
    def broadcast_execute(self, script_path, args=None):
        """Broadcast execution command to all clients"""
        command = {
            'type': 'execute',
            'script': script_path,
            'args': args or []
        }
        
        self.client.publish("execute/broadcast", json.dumps(command))
        print(f"Broadcast command: {script_path}")
    
    def request_status(self, client_id=None):
        """Request status from client(s)"""
        command = {'type': 'status'}
        
        if client_id:
            self.client.publish(f"execute/{client_id}", json.dumps(command))
        else:
            self.client.publish("execute/broadcast", json.dumps(command))
    
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
        """Disconnect"""
        self.client.loop_stop()
        self.client.disconnect()

# Usage Examples
if __name__ == "__main__":
    BROKER = "192.168.1.10"
    
    controller = MQTTController(BROKER)
    
    if controller.start():
        time.sleep(2)  # Wait for connection
        
        # Example 1: Execute on Windows machine
        controller.execute_on_client(
            client_id="WINDOWS-PC_1234567890",
            script_path="C:\\Scripts\\target.py"
        )
        
        # Example 2: Execute on Linux machine
        controller.execute_on_client(
            client_id="redhat-server_1234567891",
            script_path="/home/remoteuser/server.py",
            args=["--verbose"]
        )
        
        # Example 3: Broadcast to all machines
        # controller.broadcast_execute("/scripts/universal_task.py")
        
        # Example 4: Request status from all
        # controller.request_status()
        
        # Keep running to receive responses
        time.sleep(10)
        
        controller.stop()
```

### Method 3: gRPC (High Performance RPC)

**Install gRPC**
```bash
# On all systems
pip install grpcio grpcio-tools
```

**Define Protocol (proto file)**
```protobuf
// execution.proto
syntax = "proto3";

service ExecutionService {
    rpc ExecuteScript (ExecuteRequest) returns (ExecuteResponse);
    rpc GetSystemInfo (Empty) returns (SystemInfo);
}

message ExecuteRequest {
    string script_path = 1;
    repeated string args = 2;
    string working_dir = 3;
}

message ExecuteResponse {
    bool success = 1;
    string stdout = 2;
    string stderr = 3;
    int32 return_code = 4;
    string error = 5;
}

message Empty {}

message SystemInfo {
    string platform = 1;
    string hostname = 2;
    string python_version = 3;
}
```

**Generate Python code:**
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. execution.proto
```

**gRPC Server (Run on any OS)**
```python
# grpc_server.py
import grpc
from concurrent import futures
import subprocess
import platform
import execution_pb2
import execution_pb2_grpc

class ExecutionService(execution_pb2_grpc.ExecutionServiceServicer):
    def ExecuteScript(self, request, context):
        """Execute script"""
        try:
            python_cmd = "python" if platform.system() == "Windows" else "python3"
            command = [python_cmd, request.script_path] + list(request.args)
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=request.working_dir if request.working_dir else None
            )
            
            return execution_pb2.ExecuteResponse(
                success=True,
                stdout=result.stdout,
                stderr=result.stderr,
                return_code=result.returncode
            )
        except Exception as e:
            return execution_pb2.ExecuteResponse(
                success=False,
                error=str(e)
            )
    
    def GetSystemInfo(self, request, context):
        """Get system information"""
        return execution_pb2.SystemInfo(
            platform=platform.system(),
            hostname=platform.node(),
            python_version=platform.python_version()
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    execution_pb2_grpc.add_ExecutionServiceServicer_to_server(
        ExecutionService(), server
    )
    server.add_insecure_port('[::]:50051')
    print(f"gRPC Server started on port 50051 [{platform.system()}]")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
```

**gRPC Client (Run on any OS)**
```python
# grpc_client.py
import grpc
import execution_pb2
import execution_pb2_grpc

class GRPCExecutor:
    def __init__(self, host, port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = execution_pb2_grpc.ExecutionServiceStub(self.channel)
    
    def execute_script(self, script_path, args=None, working_dir=None):
        """Execute script on remote machine"""
        try:
            request = execution_pb2.ExecuteRequest(
                script_path=script_path,
                args=args or [],
                working_dir=working_dir or ""
            )
            
            response = self.stub.ExecuteScript(request)
            
            return {
                'success': response.success,
                'stdout': response.stdout,
                'stderr': response.stderr,
                'return_code': response.return_code,
                'error': response.error
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_system_info(self):
        """Get remote system info"""
        try:
            response = self.stub.GetSystemInfo(execution_pb2.Empty())
            return {
                'platform': response.platform,
                'hostname': response.hostname,
                'python_version': response.python_version
            }
        except Exception as e:
            return {'error': str(e)}
    
    def close(self):
        """Close channel"""
        self.channel.close()

# Usage
if __name__ == "__main__":
    # Connect to any machine
    executor = GRPCExecutor("192.168.1.30")
    
    # Get system info
    info = executor.get_system_info()
    print("System Info:", info)
    
    # Execute script
    result = executor.execute_script("/home/remoteuser/server.py")
    
    if result['success']:
        print("Output:", result['stdout'])
    else:
        print("Error:", result['error'])
    
    executor.close()
```

---

## Security Best Practices

### 1. Authentication

**API Key Authentication**
```python
import secrets
import hashlib

def generate_api_key():
    """Generate secure API key"""
    return secrets.token_urlsafe(32)

def hash_api_key(api_key):
    """Hash API key for storage"""
    return hashlib.sha256(api_key.encode()).hexdigest()

# Store hashed keys, never plain text
API_KEYS = {
    hash_api_key("key1"): "user1",
    hash_api_key("key2"): "user2"
}
```

**JWT Token Authentication**
```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"

def generate_token(username):
    """Generate JWT token"""
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
```

### 2. Encryption

**SSH Key-Based Authentication (Recommended)**

**On Windows:**
```powershell
# Generate SSH key
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Copy to Linux
type $env:USERPROFILE\.ssh\id_rsa.pub | ssh user@192.168.1.30 "cat >> ~/.ssh/authorized_keys"
```

**On Linux:**
```bash
# Generate SSH key
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Copy to Windows
ssh-copy-id user@192.168.1.40

# Or manually
cat ~/.ssh/id_rsa.pub | ssh user@192.168.1.40 "type >> C:\Users\user\.ssh\authorized_keys"
```

**HTTPS/TLS for API**
```python
from flask import Flask
import ssl

app = Flask(__name__)

# Create self-signed certificate (for testing)
# openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', port=5000, ssl_context=context)
```

### 3. Input Validation

```python
import os
import re

def validate_script_path(script_path, allowed_dirs):
    """Validate script path to prevent path traversal"""
    # Resolve to absolute path
    abs_path = os.path.abspath(script_path)
    
    # Check if path is in allowed directories
    if not any(abs_path.startswith(allowed_dir) for allowed_dir in allowed_dirs):
        raise ValueError("Script path not in allowed directories")
    
    # Check if file exists
    if not os.path.exists(abs_path):
        raise ValueError("Script not found")
    
    # Check if it's a file (not directory)
    if not os.path.isfile(abs_path):
        raise ValueError("Path is not a file")
    
    return abs_path

def validate_arguments(args):
    """Validate command arguments"""
    # Remove dangerous characters
    safe_args = []
    for arg in args:
        # Allow only alphanumeric, dash, underscore, slash, backslash, dot
        if re.match(r'^[a-zA-Z0-9\-_/\\.]+

# Security: Add authentication
API_KEY = "your-secret-key-12345"

def verify_api_key():
    """Verify API key"""
    key = request.headers.get('X-API-Key')
    return key == API_KEY

@app.route('/execute', methods=['POST'])
def execute_script():
    """Execute Python script"""
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    script_path = data.get('script')
    args = data.get('args', [])
    
    if not script_path:
        return jsonify({'error': 'No script specified'}), 400
    
    try:
        command = ['python3', script_path] + args
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.path.dirname(script_path)
        )
        
        return jsonify({
            'success': True,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Run as systemd service:**
```bash
# Create service file
sudo nano /etc/systemd/system/api-server.service
```

```ini
[Unit]
Description=Python API Server
After=network.target

[Service]
Type=simple
User=remoteuser
WorkingDirectory=/home/remoteuser
ExecStart=/usr/bin/python3 /home/remoteuser/api_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable api-server
sudo systemctl start api-server

# Configure firewall
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

**Client on Windows (192.168.1.10)**
```python
# controller.py on Windows
import requests
import json

class HTTPAPIExecutor:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        }
    
    def health_check(self):
        """Check if API is accessible"""
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def execute_script(self, script_path, args=None):
        """Execute script via API"""
        payload = {
            'script': script_path,
            'args': args or []
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/execute",
                json=payload,
                headers=self.headers,
                timeout=60
            )
            
            return response.json()
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Usage
if __name__ == "__main__":
    executor = HTTPAPIExecutor(
        base_url="http://192.168.1.30:5000",
        api_key="your-secret-key-12345"
    )
    
    # Health check
    health = executor.health_check()
    print("Health:", health)
    
    # Execute script
    result = executor.execute_script(
        script_path="/home/remoteuser/server.py",
        args=["--mode", "production"]
    )
    
    if result.get('success'):
        print("Output:", result['stdout'])
    else:
        print("Error:", result.get('error'))
```

---

## Linux to Windows Execution

### Method 1: SSH from Linux to Windows

**Prerequisite: OpenSSH Server on Windows (192.168.1.40)**
```powershell
# On Windows target
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
```

**Execute from Red Hat Linux (192.168.1.30)**
```python
# executor.py on Linux
import paramiko

class WindowsExecutor:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.client = None
    
    def connect(self):
        """Connect to Windows via SSH"""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            self.client.connect(
                self.host,
                username=self.username,
                password=self.password,
                look_for_keys=False,
                allow_agent=False
            )
            print(f"✓ Connected to Windows host {self.host}")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def execute_script(self, script_path, args=None):
        """Execute Python script on Windows"""
        if not self.client:
            return None
        
        # Windows uses backslashes and 'python' command
        command = f'python "{script_path}"'
        if args:
            command += f" {' '.join(args)}"
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            
            return {
                'stdout': stdout.read().decode('utf-8'),
                'stderr': stderr.read().decode('utf-8'),
                'exit_code': stdout.channel.recv_exit_status()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def execute_powershell(self, ps_command):
        """Execute PowerShell command"""
        if not self.client:
            return None
        
        command = f'powershell.exe -Command "{ps_command}"'
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            
            return {
                'stdout': stdout.read().decode('utf-8'),
                'stderr': stderr.read().decode('utf-8'),
                'exit_code': stdout.channel.recv_exit_status()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def upload_and_execute(self, local_path, remote_path):
        """Upload Linux script to Windows and execute"""
        if not self.client:
            return None
        
        try:
            sftp = self.client.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            
            print(f"✓ Uploaded to Windows: {remote_path}")
            
            return self.execute_script(remote_path)
        except Exception as e:
            return {'error': str(e)}
    
    def close(self):
        if self.client:
            self.client.close()

# Usage
if __name__ == "__main__":
    executor = WindowsExecutor(
        host="192.168.1.40",
        username="windowsuser",
        password="Password123!"
    )
    
    if executor.connect():
        # Execute existing Windows script
        result = executor.execute_script("C:\\Scripts\\worker.py")
        print("Output:", result['stdout'])
        
        # Execute PowerShell command
        ps_result = executor.execute_powershell("Get-Process | Select-Object -First 5")
        print("PowerShell:", ps_result['stdout'])
        
        executor.close()
```

### Method 2: WMI from Linux to Windows

**Install Required Packages on Linux**
```bash
sudo yum install -y python3-pip
pip3 install pywinrm
```

**Execute from Linux**
```python
# wmi_executor.py on Linux
import winrm

class WinRMExecutor:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.session = None
    
    def connect(self):
        """Establish WinRM connection"""
        try:
            self.session = winrm.Session(
                f'http://{self.host}:5985/wsman',
                auth=(self.username, self.password),
                transport='ntlm'
            )
            # Test connection
            result = self.session.run_cmd('whoami')
            if result.status_code == 0:
                print(f"✓ Connected to {self.host}")
                return True
            return False
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def execute_script(self, script_path, args=None):
        """Execute Python script via WinRM"""
        if not self.session:
            return None
        
        command = f'python "{script_path}"'
        if args:
            command += f" {' '.join(args)}"
        
        try:
            result = self.session.run_cmd(command)
            
            return {
                'success': result.status_code == 0,
                'stdout': result.std_out.decode('utf-8'),
                'stderr': result.std_err.decode('utf-8'),
                'status_code': result.status_code
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def execute_powershell(self, ps_script):
        """Execute PowerShell script"""
        if not self.session:
            return None
        
        try:
            result = self.session.run_ps(ps_script)
            
            return {
                'success': result.status_code == 0,
                'stdout': result.std_out.decode('utf-8'),
                'stderr': result.std_err.decode('utf-8'),
                'status_code': result.status_code
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Usage
executor = WinRMExecutor(
    host="192.168.1.40",
    username="windowsuser",
    password="Password123!"
)

if executor.connect():
    # Execute Python script
    result = executor.execute_script("C:\\Scripts\\worker.py")
    print("Output:", result['stdout'])
    
    # Execute PowerShell
    ps_result = executor.execute_powershell("Get-ComputerInfo | Select-Object OsName, OsVersion")
    print("PS Output:", ps_result['stdout'])
```

**Enable WinRM on Windows Target (192.168.1.40)**
```powershell
# Run as Administrator on Windows
Enable-PSRemoting -Force

# Configure WinRM
winrm quickconfig

# Set trusted hosts (if not in domain)
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "*" -Force

# Configure firewall
netsh advfirewall firewall add rule name="WinRM-HTTP" dir=in action=allow protocol=TCP localport=5985
```

---

## Universal Methods (Cross-Platform)

### Method 1: RESTful API (Best for Heterogeneous Environments)

This works for any combination: Windows-Windows, Windows-Linux, Linux-Windows, Linux-Linux

**Server (Can run on any OS)**
```python
# universal_server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import platform
import os

app = Flask(__name__), arg):
            safe_args.append(arg)
        else:
            raise ValueError(f"Invalid argument: {arg}")
    
    return safe_args
```

### 4. Firewall Configuration

**Windows Firewall:**
```powershell
# Allow specific port
New-NetFirewallRule -DisplayName "API Server" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow

# Allow from specific IP only
New-NetFirewallRule -DisplayName "API Server" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow -RemoteAddress 192.168.1.10

# Remove rule
Remove-NetFirewallRule -DisplayName "API Server"
```

**Red Hat Firewall:**
```bash
# Allow port
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload

# Allow from specific IP
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.10" port port="5000" protocol="tcp" accept'
sudo firewall-cmd --reload

# List rules
sudo firewall-cmd --list-all
```

### 5. Logging and Monitoring

```python
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('execution.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('RemoteExecution')

def log_execution(client_ip, script_path, success, error=None):
    """Log execution attempts"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'client_ip': client_ip,
        'script_path': script_path,
        'success': success,
        'error': error
    }
    
    if success:
        logger.info(f"Execution successful: {json.dumps(log_entry)}")
    else:
        logger.error(f"Execution failed: {json.dumps(log_entry)}")
```

---

## Troubleshooting

### Common Windows Issues

**Problem: PowerShell Remoting Not Working**
```powershell
# Check WinRM service
Get-Service WinRM

# Test WinRM
Test-WSMan -ComputerName 192.168.1.20

# Check trusted hosts
Get-Item WSMan:\localhost\Client\TrustedHosts

# Reset WinRM configuration
winrm quickconfig
```

**Problem: OpenSSH Not Starting**
```powershell
# Check service status
Get-Service sshd

# Check event logs
Get-EventLog -LogName Application -Source sshd -Newest 10

# Reinstall
Remove-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
```

**Problem: Python Not Found**
```powershell
# Add Python to PATH
$env:Path += ";C:\Python39"

# Or use full path
C:\Python39\python.exe script.py

# Verify
where python
python --version
```

### Common Linux Issues

**Problem: SSH Connection Refused**
```bash
# Check if SSH is running
sudo systemctl status sshd

# Start SSH
sudo systemctl start sshd

# Check if port 22 is listening
sudo netstat -tlnp | grep :22

# Check SELinux (Red Hat)
sudo getenforce
sudo setenforce 0  # Temporary disable for testing
```

**Problem: Permission Denied**
```bash
# Fix SSH directory permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# Check file ownership
ls -la ~/.ssh/

# Fix ownership
chown -R $USER:$USER ~/.ssh/
```

**Problem: Firewall Blocking**
```bash
# Check firewall status
sudo firewall-cmd --state

# List rules
sudo firewall-cmd --list-all

# Add port
sudo firewall-cmd --permanent --add-port=22/tcp
sudo firewall-cmd --reload

# Disable firewall (testing only)
sudo systemctl stop firewalld
```

### Cross-Platform Issues

**Problem: Script Path Format**

# Security: Add authentication
API_KEY = "your-secret-key-12345"

def verify_api_key():
    """Verify API key"""
    key = request.headers.get('X-API-Key')
    return key == API_KEY

@app.route('/execute', methods=['POST'])
def execute_script():
    """Execute Python script"""
    if not verify_api_key():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    script_path = data.get('script')
    args = data.get('args', [])
    
    if not script_path:
        return jsonify({'error': 'No script specified'}), 400
    
    try:
        command = ['python3', script_path] + args
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.path.dirname(script_path)
        )
        
        return jsonify({
            'success': True,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Run as systemd service:**
```bash
# Create service file
sudo nano /etc/systemd/system/api-server.service
```

```ini
[Unit]
Description=Python API Server
After=network.target

[Service]
Type=simple
User=remoteuser
WorkingDirectory=/home/remoteuser
ExecStart=/usr/bin/python3 /home/remoteuser/api_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable api-server
sudo systemctl start api-server

# Configure firewall
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

**Client on Windows (192.168.1.10)**
```python
# controller.py on Windows
import requests
import json

class HTTPAPIExecutor:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        }
    
    def health_check(self):
        """Check if API is accessible"""
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def execute_script(self, script_path, args=None):
        """Execute script via API"""
        payload = {
            'script': script_path,
            'args': args or []
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/execute",
                json=payload,
                headers=self.headers,
                timeout=60
            )
            
            return response.json()
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Usage
if __name__ == "__main__":
    executor = HTTPAPIExecutor(
        base_url="http://192.168.1.30:5000",
        api_key="your-secret-key-12345"
    )
    
    # Health check
    health = executor.health_check()
    print("Health:", health)
    
    # Execute script
    result = executor.execute_script(
        script_path="/home/remoteuser/server.py",
        args=["--mode", "production"]
    )
    
    if result.get('success'):
        print("Output:", result['stdout'])
    else:
        print("Error:", result.get('error'))
```

---

## Linux to Windows Execution

### Method 1: SSH from Linux to Windows

**Prerequisite: OpenSSH Server on Windows (192.168.1.40)**
```powershell
# On Windows target
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
```

**Execute from Red Hat Linux (192.168.1.30)**
```python
# executor.py on Linux
import paramiko

class WindowsExecutor:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.client = None
    
    def connect(self):
        """Connect to Windows via SSH"""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            self.client.connect(
                self.host,
                username=self.username,
                password=self.password,
                look_for_keys=False,
                allow_agent=False
            )
            print(f"✓ Connected to Windows host {self.host}")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def execute_script(self, script_path, args=None):
        """Execute Python script on Windows"""
        if not self.client:
            return None
        
        # Windows uses backslashes and 'python' command
        command = f'python "{script_path}"'
        if args:
            command += f" {' '.join(args)}"
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            
            return {
                'stdout': stdout.read().decode('utf-8'),
                'stderr': stderr.read().decode('utf-8'),
                'exit_code': stdout.channel.recv_exit_status()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def execute_powershell(self, ps_command):
        """Execute PowerShell command"""
        if not self.client:
            return None
        
        command = f'powershell.exe -Command "{ps_command}"'
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            
            return {
                'stdout': stdout.read().decode('utf-8'),
                'stderr': stderr.read().decode('utf-8'),
                'exit_code': stdout.channel.recv_exit_status()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def upload_and_execute(self, local_path, remote_path):
        """Upload Linux script to Windows and execute"""
        if not self.client:
            return None
        
        try:
            sftp = self.client.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            
            print(f"✓ Uploaded to Windows: {remote_path}")
            
            return self.execute_script(remote_path)
        except Exception as e:
            return {'error': str(e)}
    
    def close(self):
        if self.client:
            self.client.close()

# Usage
if __name__ == "__main__":
    executor = WindowsExecutor(
        host="192.168.1.40",
        username="windowsuser",
        password="Password123!"
    )
    
    if executor.connect():
        # Execute existing Windows script
        result = executor.execute_script("C:\\Scripts\\worker.py")
        print("Output:", result['stdout'])
        
        # Execute PowerShell command
        ps_result = executor.execute_powershell("Get-Process | Select-Object -First 5")
        print("PowerShell:", ps_result['stdout'])
        
        executor.close()
```

### Method 2: WMI from Linux to Windows

**Install Required Packages on Linux**
```bash
sudo yum install -y python3-pip
pip3 install pywinrm
```

**Execute from Linux**
```python
# wmi_executor.py on Linux
import winrm

class WinRMExecutor:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.session = None
    
    def connect(self):
        """Establish WinRM connection"""
        try:
            self.session = winrm.Session(
                f'http://{self.host}:5985/wsman',
                auth=(self.username, self.password),
                transport='ntlm'
            )
            # Test connection
            result = self.session.run_cmd('whoami')
            if result.status_code == 0:
                print(f"✓ Connected to {self.host}")
                return True
            return False
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def execute_script(self, script_path, args=None):
        """Execute Python script via WinRM"""
        if not self.session:
            return None
        
        command = f'python "{script_path}"'
        if args:
            command += f" {' '.join(args)}"
        
        try:
            result = self.session.run_cmd(command)
            
            return {
                'success': result.status_code == 0,
                'stdout': result.std_out.decode('utf-8'),
                'stderr': result.std_err.decode('utf-8'),
                'status_code': result.status_code
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def execute_powershell(self, ps_script):
        """Execute PowerShell script"""
        if not self.session:
            return None
        
        try:
            result = self.session.run_ps(ps_script)
            
            return {
                'success': result.status_code == 0,
                'stdout': result.std_out.decode('utf-8'),
                'stderr': result.std_err.decode('utf-8'),
                'status_code': result.status_code
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Usage
executor = WinRMExecutor(
    host="192.168.1.40",
    username="windowsuser",
    password="Password123!"
)

if executor.connect():
    # Execute Python script
    result = executor.execute_script("C:\\Scripts\\worker.py")
    print("Output:", result['stdout'])
    
    # Execute PowerShell
    ps_result = executor.execute_powershell("Get-ComputerInfo | Select-Object OsName, OsVersion")
    print("PS Output:", ps_result['stdout'])
```

**Enable WinRM on Windows Target (192.168.1.40)**
```powershell
# Run as Administrator on Windows
Enable-PSRemoting -Force

# Configure WinRM
winrm quickconfig

# Set trusted hosts (if not in domain)
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "*" -Force

# Configure firewall
netsh advfirewall firewall add rule name="WinRM-HTTP" dir=in action=allow protocol=TCP localport=5985
```

---

## Universal Methods (Cross-Platform)

### Method 1: RESTful API (Best for Heterogeneous Environments)

This works for any combination: Windows-Windows, Windows-Linux, Linux-Windows, Linux-Linux

**Server (Can run on any OS)**
```python
# universal_server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import platform
import os

app = Flask(__name__)