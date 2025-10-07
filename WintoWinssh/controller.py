
# controller.py using Paramiko
import paramiko
import os
from typing import Optional

class WindowsSSHExecutor:
    def __init__(self, host, username, password=None, key_file=None):
        # Connection parameters
        # - host: target machine (IP/hostname) running an SSH server
        # - username: account used to authenticate on the remote host
        # - password: optional; used only if key_file is not provided
        # - key_file: path to an OpenSSH private key; preferred over password
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
                # Authenticate using an OpenSSH private key file
                resolved_key_path = self._resolve_private_key_path(self.key_file)
                self.client.connect(
                    self.host,
                    username=self.username,
                    key_filename=resolved_key_path,
                    allow_agent=False,
                    look_for_keys=False
                )
            else:
                # Authenticate using username/password
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

    def _resolve_private_key_path(self, path: str) -> str:
        r"""Return a usable private key file path.
        - If a directory is provided (e.g., %USERPROFILE%\.ssh), try common key filenames.
        - If a file is provided, validate it exists and return as-is.
        """
        expanded_path = os.path.expandvars(os.path.expanduser(path))

        if os.path.isdir(expanded_path):
            candidate_names = [
                "id_ed25519",
                "id_rsa",
                "windows_key",
                "winkey",
            ]
            for name in candidate_names:
                candidate = os.path.join(expanded_path, name)
                if os.path.isfile(candidate):
                    return candidate
            raise FileNotFoundError(
                f"No private key found in directory: {expanded_path}. "
                "Looked for id_ed25519, id_rsa, windows_key, winkey"
            )

        if os.path.isfile(expanded_path):
            # Detect PuTTY .ppk keys by extension OR file header content
            # Paramiko cannot read PuTTY .ppk files. They must be converted
            # to OpenSSH format (PEM) via PuTTYgen.
            if expanded_path.lower().endswith(".ppk"):
                raise ValueError(
                    "PuTTY .ppk keys are not supported. Convert to OpenSSH format "
                    "(PuTTYgen: Load .ppk -> Conversions -> Export OpenSSH key) "
                    f"and use that file instead. Provided: {expanded_path}"
                )
            try:
                with open(expanded_path, "r", encoding="utf-8", errors="ignore") as f:
                    first_line: str = f.readline().strip()
                if first_line.startswith("PuTTY-User-Key-File"):
                    raise ValueError(
                        "Detected PuTTY key format. Convert to OpenSSH format "
                        "(PuTTYgen: Load .ppk -> Conversions -> Export OpenSSH key) "
                        f"and use that file instead. Provided: {expanded_path}"
                    )
            except OSError:
                # If we cannot read the file to inspect header, let Paramiko try and surface error
                pass
            return expanded_path

        # If the file does not exist, check if a sibling .ppk exists to give a clearer hint
        ppk_candidate = expanded_path + ".ppk" if not expanded_path.lower().endswith(".ppk") else expanded_path
        if os.path.isfile(ppk_candidate):
            raise ValueError(
                "PuTTY .ppk key detected adjacent to the requested path. Convert to OpenSSH format "
                "(PuTTYgen: Load .ppk -> Conversions -> Export OpenSSH key) and use that file instead. "
                f"Found: {ppk_candidate}"
            )

        raise FileNotFoundError(f"Private key not found: {expanded_path}")
    
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

# # Usage
# executor = WindowsSSHExecutor(
#     host="192.168.16.105",
#     username="Administrator",
#     password="123456"
# )

# Use SSH Keys (Most Secure - No Password Needed!)
# ==============================================================================
# Generate SSH key pair on your local machine:
# Windows: ssh-keygen -t rsa -b 4096 -f %USERPROFILE%\.ssh\windows_key
# Copy public key to Windows server

# Configure the executor
# - For key-based auth: set key_file to your OpenSSH private key path
# - For password auth: omit key_file and provide password=...
executor = WindowsSSHExecutor(
    host="192.168.16.105",
    username="Administrator",
    key_file=r"C:\\Users\\Malli\\.ssh\\private_key_openssh"
)

if executor.connect():
    # result = executor.execute_script("C:\\Scripts\\target.py")
    result = executor.execute_script("C:\\Users\\Administrator\\Desktop\\Malli\\target.py", args=["hello", "123"])

    print("Output:", result['stdout'])
    executor.close()
