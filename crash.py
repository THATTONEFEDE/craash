import os
import sys
import subprocess
import time

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def install_pip():
    try:
        subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
    except Exception:
        print("Failed to install pip using ensurepip. Attempting to download get-pip.py...")
        url = "https://bootstrap.pypa.io/get-pip.py"
        response = subprocess.check_output(["curl", "-O", url])
        subprocess.check_call([sys.executable, "get-pip.py"])

def check_and_install_packages():
    global psutil
    try:
        import psutil
    except ImportError:
        print("psutil not found. Installing...")
        install("psutil")
        import psutil  # Import again after installation

def close_all_programs():
    for proc in psutil.process_iter():
        try:
            if proc.name() not in ["System", "System Idle Process", "services.exe", "winlogon.exe", "csrss.exe"]:
                print(f"Terminating: {proc.name()} (PID: {proc.pid})")
                proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def reboot_system():
    os.system("shutdown /r /t 0")

if __name__ == "__main__":
    try:
        import pip
    except ImportError:
        print("pip not found. Installing...")
        install_pip()

    check_and_install_packages()
    close_all_programs()
    time.sleep(2)
    reboot_system()
