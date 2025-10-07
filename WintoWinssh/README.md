### End-to-End SSH Setup and Usage (Windows + PuTTYgen + Paramiko)

This guide walks you from a fresh Windows setup to connecting over SSH and running the provided Python script.

### 1) Install OpenSSH
- Windows 10/11: Open Settings → Apps → Optional Features → Add a feature.
  - Install "OpenSSH Client" and (on the server machine) "OpenSSH Server".
- Verify in PowerShell:
```powershell
ssh -V
```
- If installing on Windows Server via PowerShell:
```powershell
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
```

### 2) Generate SSH Keys with PuTTYgen (Client machine)
- Open PuTTYgen
  - Type of key: RSA
  - Number of bits: 4096
  - Click "Generate" and move the mouse to add randomness.
- Save keys under your user profile:
  - Public key: `C:\Users\<username>\.ssh\id_rsa.pub` (you may name it as you wish)
  - Private key (.ppk): `C:\Users\<username>\.ssh\id_rsa.ppk`
- Also export an OpenSSH private key (required for Python Paramiko):
  - In PuTTYgen: Conversions → Export OpenSSH key
  - Save as: `C:\Users\<username>\.ssh\id_rsa_openssh`

Notes:
- The OpenSSH private key file should start with `-----BEGIN OPENSSH PRIVATE KEY-----`.
- Keep private keys secure; never share them.

### 3) Install your public key on the server (target machine)
- Copy the public key text from PuTTYgen (or the contents of `id_rsa.pub`).
- On the server, create the `.ssh` folder for the target user (e.g., `Administrator`):
```powershell
mkdir -Force "C:\Users\<server-username>\.ssh"
notepad "C:\Users\<server-username>\.ssh\authorized_keys"
```
- Paste the public key onto a single line inside `authorized_keys`, then save.

Recommended permissions (Windows OpenSSH):
```powershell
# Run as Administrator
$USER = "<server-username>"
$sshPath = "C:\Users\$USER\.ssh"
$authKeys = Join-Path $sshPath "authorized_keys"

icacls "$sshPath" /inheritance:r
icacls "$sshPath" /grant:r "$USER:(F)" "Administrators:(F)"
icacls "$authKeys" /inheritance:r
icacls "$authKeys" /grant:r "$USER:(F)" "Administrators:(F)"
```

Ensure the OpenSSH Server is running on the server:
```powershell
Get-Service sshd
# If not running:
Start-Service sshd
Set-Service -Name sshd -StartupType Automatic
```

### 4) Test SSH login from the client
- Basic test using the OpenSSH key (not the .ppk):
```powershell
ssh -i "C:\Users\<username>\.ssh\id_rsa_openssh" <server-username>@<server-ip>
```
- If this succeeds, your key setup is correct.

### 5) Python script and dependencies
- Place the Python script (e.g., `controller.py`) in `C:\Users\<username>\Documents`.
- Create `requriment.txt` with dependencies:
```text
paramiko
```
- Install dependencies:
```powershell
pip install -r requriment.txt
```

### 6) Configure the Python script
In `controller.py`, set your connection details. Example for key-based auth:
```python
executor = WindowsSSHExecutor(
    host="<server-ip>",
    username="<server-username>",
    key_file=r"C:\\Users\\<username>\\.ssh\\id_rsa_openssh"
)
```
Alternatively, for password auth (not recommended):
```python
executor = WindowsSSHExecutor(
    host="<server-ip>",
    username="<server-username>",
    password="<your-password>"
)
```

### 7) Run the Python script
```powershell
cd C:\Users\<username>\Documents
python .\controller.py
```
Expected on success:
```
✓ Connected to <server-ip>
Output: <remote script output>
```

### Troubleshooting
- Key format error or Paramiko fails with `.ppk`:
  - Use the OpenSSH key exported from PuTTYgen (`Export OpenSSH key`).
- Connection refused / timed out:
  - Verify server IP, firewall, and that `sshd` is running on the server.
- Permission denied (publickey):
  - Ensure the public key is in `authorized_keys` for the correct user.
  - Check permissions of `.ssh` and `authorized_keys` (see commands above).
- Wrong user directory:
  - Keys must be placed under the profile of the same user you SSH as.

### Useful references
- OpenSSH on Windows: `https://learn.microsoft.com/windows-server/administration/openssh/openssh_overview`
- PuTTYgen: `https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html`
