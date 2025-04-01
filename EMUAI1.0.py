import platform
import subprocess
import os
import sys
import time

def detect_os():
    """Detect the operating system."""
    os_name = platform.system()
    if os_name == "Windows":
        return "Windows"
    elif os_name == "Darwin":
        return "MacOS"
    elif os_name == "Linux":
        # Further distinguish Linux distros
        if "chrome" in platform.uname().release.lower():
            return "ChromeOS"
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("ID="):
                        distro = line.strip().split("=")[1].lower().strip('"')
                        if distro == "debian":
                            return "Debian"
                        elif distro == "arch":
                            return "Arch"
        except FileNotFoundError:
            pass
        return "Linux (Unknown)"
    return "Unsupported"

def check_mupen_running():
    """Simulate checking if Mupen64Plus is running (rudimentary check)."""
    os_name = detect_os()
    try:
        if os_name == "Windows":
            output = subprocess.check_output("tasklist", shell=True, text=True)
            return "mupen64plus" in output.lower()
        elif os_name in ["MacOS", "Debian", "Arch", "ChromeOS"]:
            output = subprocess.check_output("ps aux | grep [m]upen64plus", shell=True, text=True)
            return bool(output)
    except subprocess.CalledProcessError:
        return False
    return False

def install_mupen_windows():
    """Install Mupen64Plus on Windows (simulated)."""
    print("Starting Mupen64Plus installation for Windows...")
    print("Downloading Mupen64Plus binary (simulated)...")
    time.sleep(2)
    print("Extracting to C:\\Program Files\\Mupen64Plus (simulated)...")
    time.sleep(1)
    print("Installation complete! Run 'mupen64plus.exe' from C:\\Program Files\\Mupen64Plus.")

def install_mupen_macos():
    """Install Mupen64Plus on macOS using Homebrew (simulated)."""
    print("Starting Mupen64Plus installation for macOS...")
    try:
        subprocess.check_call(["brew", "--version"])
        print("Homebrew detected.")
    except FileNotFoundError:
        print("Homebrew not found. Installing Homebrew (simulated)...")
        time.sleep(2)
        print("Homebrew installed.")
    print("Installing Mupen64Plus via Homebrew (simulated)...")
    time.sleep(2)
    print("Installation complete! Run 'mupen64plus' from the terminal.")

def install_mupen_debian():
    """Install Mupen64Plus on Debian (simulated)."""
    print("Starting Mupen64Plus installation for Debian...")
    print("Updating package list (simulated)...")
    time.sleep(1)
    print("Installing Mupen64Plus via apt (simulated)...")
    # In reality: subprocess.run(["sudo", "apt", "update"])
    #          subprocess.run(["sudo", "apt", "install", "-y", "mupen64plus"])
    time.sleep(2)
    print("Installation complete! Run 'mupen64plus' from the terminal.")

def install_mupen_arch():
    """Install Mupen64Plus on Arch Linux (simulated)."""
    print("Starting Mupen64Plus installation for Arch Linux...")
    print("Updating package list and installing Mupen64Plus via pacman (simulated)...")
    # In reality: subprocess.run(["sudo", "pacman", "-Syu", "mupen64plus"])
    time.sleep(2)
    print("Installation complete! Run 'mupen64plus' from the terminal.")

def install_mupen_chromeos():
    """Install Mupen64Plus on Chrome OS (Crostini, Debian-based, simulated)."""
    print("Starting Mupen64Plus installation for Chrome OS (Crostini)...")
    print("Note: This assumes Linux (Debian) is enabled in Chrome OS settings.")
    print("Updating package list (simulated)...")
    time.sleep(1)
    print("Installing Mupen64Plus via apt (simulated)...")
    # In reality: subprocess.run(["sudo", "apt", "update"])
    #          subprocess.run(["sudo", "apt", "install", "-y", "mupen64plus"])
    time.sleep(2)
    print("Installation complete! Run 'mupen64plus' from the terminal in Crostini.")

def wizard():
    """Main wizard function."""
    print("Welcome to the Mupen64Plus Installation Wizard!")
    os_name = detect_os()
    
    if os_name == "Unsupported" or os_name == "Linux (Unknown)":
        print(f"Sorry, this wizard does not fully support {os_name} yet.")
        return
    
    print(f"Detected operating system: {os_name}")
    
    # Check if Mupen64Plus is already running (simulated)
    if check_mupen_running():
        print("Mupen64Plus appears to be running/on-screen.")
        proceed = input("Do you still want to install/reinstall it? (y/n): ").lower()
        if proceed != 'y':
            print("Installation aborted.")
            return
    
    # Ask user if they want to install
    response = input(f"Do you want to install Mupen64Plus on {os_name}? (y/n): ").lower()
    
    if response == 'y':
        print(f"Proceeding with installation for {os_name}...")
        if os_name == "Windows":
            install_mupen_windows()
        elif os_name == "MacOS":
            install_mupen_macos()
        elif os_name == "Debian":
            install_mupen_debian()
        elif os_name == "Arch":
            install_mupen_arch()
        elif os_name == "ChromeOS":
            install_mupen_chromeos()
    else:
        print("Installation cancelled by user.")
        print("Goodbye!")
        return

    print("Wizard complete! Enjoy playing N64 games.")

if __name__ == "__main__":
    wizard()
