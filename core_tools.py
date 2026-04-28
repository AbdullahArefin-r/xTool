import os
import socket
import psutil
import subprocess
import speedtest
import logging
from rich.console import Console

console = Console()

# Setup basic logging
logging.basicConfig(filename='xtermux_actions.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

def log_action(action):
    logging.info(action)

def download_video(url, platform="YouTube"):
    """Downloads video using yt-dlp (works for YT, FB, Insta, etc.)"""
    log_action(f"Started {platform} download: {url}")
    try:
        # Using subprocess to call yt-dlp directly for better Termux compatibility
        console.print(f"[bold cyan]Starting download from {platform}...[/bold cyan]")
        subprocess.run(["yt-dlp", url], check=True)
        console.print("[bold green]✔ Download Completed Successfully![/bold green]")
    except subprocess.CalledProcessError:
        console.print("[bold red]✘ Download failed. Check the URL or your connection.[/bold red]")

def get_system_info():
    """Fetches device CPU, RAM, and Storage info"""
    log_action("Checked System Info")
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    info = {
        "CPU Cores": psutil.cpu_count(),
        "RAM Total": f"{mem.total / (1024**3):.2f} GB",
        "RAM Used": f"{mem.used / (1024**3):.2f} GB ({mem.percent}%)",
        "Storage Total": f"{disk.total / (1024**3):.2f} GB",
        "Storage Used": f"{disk.used / (1024**3):.2f} GB ({disk.percent}%)"
    }
    return info

def vps_auto_setup():
    """Installs common developer packages for a fresh Termux/VPS environment"""
    log_action("Ran VPS Auto Setup")
    packages = ["wget", "curl", "nano", "htop", "neofetch", "openssh"]
    console.print("[bold yellow]Installing essential packages: wget, curl, nano, htop, neofetch, openssh...[/bold yellow]")
    
    for pkg in packages:
        subprocess.run(["pkg", "install", pkg, "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    console.print("[bold green]✔ VPS/Termux environment setup complete![/bold green]")

def check_open_port(ip, port):
    """Scans a specific port on a target IP"""
    log_action(f"Checked port {port} on {ip}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.5)
    try:
        result = s.connect_ex((ip, port))
        return result == 0
    except:
        return False
    finally:
        s.close()

def run_speedtest():
    """Runs a CLI internet speed test"""
    log_action("Ran Speedtest")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        ping = st.results.ping
        download = st.download() / 1_000_000  # Convert to Mbps
        upload = st.upload() / 1_000_000      # Convert to Mbps
        return ping, download, upload
    except Exception as e:
        return None, None, None
