import subprocess
import sys
import os
from pathlib import Path
import shutil

def check_command_exists(command):
    """Check if a command is available in PATH"""
    return shutil.which(command) is not None

def check_venv_ready():
    """Check if virtual environment is properly created"""
    venv_path = Path(".venv")
    if os.name == 'nt':
        python_path = venv_path / "Scripts" / "python.exe"
    else:
        python_path = venv_path / "bin" / "python"
    return python_path.exists()

def run_command(command):
    """Run a command and return its output"""
    try:
        print(f"Running: {' '.join(command)}")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

def activate_venv():
    """Activate the virtual environment"""
    venv_path = Path(".venv")
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate.bat"
        os.environ['PATH'] = str(venv_path / "Scripts") + os.pathsep + os.environ['PATH']
    else:  # Unix
        activate_script = venv_path / "bin" / "activate"
        os.environ['PATH'] = str(venv_path / "bin") + os.pathsep + os.environ['PATH']
    
    # Set environment variables for virtual environment
    os.environ['VIRTUAL_ENV'] = str(venv_path)
    print(f"Activated virtual environment at {venv_path}")

def setup_environment():
    # Install UV
    print("Installing UV...")
    if not run_command([sys.executable, "-m", "pip", "install", "uv"]):
        return False
    
    # Wait for UV to be available
    attempts = 0
    while not check_command_exists("uv") and attempts < 30:
        attempts += 1
    if not check_command_exists("uv"):
        print("Error: UV installation failed or not found in PATH")
        return False

    # Create virtual environment
    print("Creating virtual environment...")
    if not run_command(["uv", "venv"]):
        return False
    
    # Wait for venv to be ready
    attempts = 0
    while not check_venv_ready() and attempts < 30:
        attempts += 1
    if not check_venv_ready():
        print("Error: Virtual environment creation failed")
        return False

    # Activate the virtual environment
    activate_venv()

    # Install dependencies
    print("Installing dependencies...")
    if not run_command(["uv", "sync"]):
        return False

    print("\nSetup completed successfully!")
    return True

if __name__ == "__main__":
    if not setup_environment():
        print("Setup failed!")
        sys.exit(1)
    sys.exit(0)
