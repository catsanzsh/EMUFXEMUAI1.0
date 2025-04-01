import platform
import subprocess
import os
import shutil
import requests
from pathlib import Path

# Constants
MUPEN_VERSION = "2.6.0"  # Latest stable release as of July 2024
BASE_URL = f"https://github.com/mupen64plus/mupen64plus-core/releases/download/{MUPEN_VERSION}"

def detect_os():
    """Detect the operating system."""
    os_name = platform.system()
    if os_name == "Windows":
        return "Windows"
    elif os_name == "Darwin":
        return "MacOS"
    elif os_name == "Linux":
        if "chrome" in platform.uname().release.lower():
            return "ChromeOS"
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("ID="):
                        distro = line.strip().split("=")[1].lower().strip('"')
                        return {"debian": "Debian", "arch": "Arch"}.get(distro, "Linux (Unknown)")
        except FileNotFoundError:
            return "Linux (Unknown)"
    return "Unsupported"

def download_file(url, dest):
    """Download a file from a URL to a destination path."""
    print(f"Downloading from {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded to {dest}")

def check_mupen_running():
    """Check if Mupen64Plus is running."""
    os_name = detect_os()
    try:
        if os_name == "Windows":
            output = subprocess.check_output("tasklist", shell=True, text=True, stderr=subprocess.STDOUT)
            return "mupen64plus" in output.lower()
        elif os_name in ["MacOS", "Debian", "Arch", "ChromeOS"]:
            try:
                subprocess.check_output(["pgrep", "-f", "mupen64plus"], text=True)
                return True
            except subprocess.CalledProcessError:
                return False
    except subprocess.CalledProcessError as e:
        print(f"Error checking processes: {e}")
        return False
    return False

def install_mupen_windows():
    """Download and set up Mupen64Plus on Windows."""
    url = f"{BASE_URL}/mupen64plus-bundle-win64-{MUPEN_VERSION}.zip"
    dest_dir = Path("C:/Mupen64Plus")
    zip_path = Path.home() / f"mupen64plus-bundle-win64-{MUPEN_VERSION}.zip"

    # Download
    download_file(url, zip_path)

    # Extract
    print("Extracting archive...")
    shutil.unpack_archive(zip_path, dest_dir)
    zip_path.unlink()  # Remove the zip file

    print(f"Installation complete! Run 'mupen64plus-ui-console.exe' from {dest_dir}")

def install_mupen_macos():
    """Download and set up Mupen64Plus on macOS."""
    url = f"{BASE_URL}/mupen64plus-bundle-osx-{MUPEN_VERSION}.zip"
    dest_dir = Path("/Applications/Mupen64Plus")
    zip_path = Path.home() / f"mupen64plus-bundle-osx-{MUPEN_VERSION}.zip"

    # Download
    download_file(url, zip_path)

    # Extract
    print("Extracting archive...")
    shutil.unpack_archive(zip_path, dest_dir)
    zip_path.unlink()

    print(f"Installation complete! Run 'mupen64plus' from {dest_dir}")

def install_mupen_debian():
    """Install Mupen64Plus on Debian using apt or binary download."""
    try:
        # Prefer package manager if available
        print("Updating package list...")
        subprocess.run(["sudo", "apt", "update"], check=True)
        print("Installing Mupen64Plus via apt...")
        subprocess.run(["sudo", "apt", "install", "-y", "mupen64plus"], check=True)
        print("Installation complete! Run 'mupen64plus' from the terminal.")
    except subprocess.CalledProcessError:
        # Fallback to binary download
        url = f"{BASE_URL}/mupen64plus-bundle-linux64-{MUPEN_VERSION}.tar.gz"
        dest_dir = Path("/usr/local/mupen64plus")
        tar_path = Path.home() / f"mupen64plus-bundle-linux64-{MUPEN_VERSION}.tar.gz"

        download_file(url, tar_path)
        print("Extracting archive...")
        os.makedirs(dest_dir, exist_ok=True)
        subprocess.run(["tar", "-xzf", tar_path, "-C", dest_dir], check=True)
        tar_path.unlink()
        print(f"Installation complete! Run 'mupen64plus' from {dest_dir}/bin")

if __name__ == "__main__":
    os_type = detect_os()
    print(f"Detected OS: {os_type}")
    if os_type == "Windows":
        install_mupen_windows()
    elif os_type == "MacOS":
        install_mupen_macos()
    elif os_type == "Debian":
        install_mupen_debian()
    elif os_type in ["Arch", "ChromeOS", "Linux (Unknown)"]:
        print("Installation for this Linux variant is not fully supported by this script. Please install manually or update the script for your distribution.")
    else:
        print("Unsupported operating system.")
