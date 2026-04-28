import sys
import json
import os
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich import print as rprint
import core_tools as tools

console = Console()
CONFIG_FILE = "config.json"

def load_config():
    """Loads or creates the configuration file"""
    if not os.path.exists(CONFIG_FILE):
        default_config = {"version": "1.0", "theme": "dark", "auto_update": True}
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_config, f)
        return default_config
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def update_tool():
    """Pulls the latest code from GitHub"""
    try:
        with console.status("[bold cyan]Checking for updates from GitHub...[/bold cyan]", spinner="dots"):
            subprocess.run(["git", "pull"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        console.print("[bold green]✔ Toolkit is up to date![/bold green]\n")
    except Exception:
        console.print("[bold yellow]⚠ Could not check for updates. Are you in a git repository?[/bold yellow]\n")

def clear_screen():
    os.system("clear")

def display_banner():
    banner = """[bold cyan]
 ██╗  ██╗       ████████╗███████╗██████╗ ███╗   ███╗██╗   ██╗██╗  ██╗
 ╚██╗██╔╝       ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║   ██║╚██╗██╔╝
  ╚███╔╝  █████╗   ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║ ╚███╔╝ 
  ██╔██╗  ╚════╝   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║ ██╔██╗ 
 ██╔╝ ██╗          ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝██╔╝ ██╗
 ╚═╝  ╚═╝          ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝
                    [bold yellow]Premium CLI Utilities | V 1.0[/bold yellow][/bold cyan]
    """
    console.print(banner, justify="center")

def main_menu():
    config = load_config()
    
    if config.get("auto_update"):
        update_tool()

    while True:
        display_banner()
        
        menu_text = """
[bold green][1][/bold green] YouTube Video Downloader    [bold green][4][/bold green] VPS/Termux Auto Setup
[bold green][2][/bold green] Facebook/Reels Downloader   [bold green][5][/bold green] Open Ports Checker
[bold green][3][/bold green] System Info Viewer          [bold green][6][/bold green] Internet Speed Test
        
[bold red][0][/bold red] Exit Toolkit
        """
        console.print(Panel(menu_text, title="[bold magenta]Main Menu[/bold magenta]", border_style="cyan", expand=False))
        
        choice = Prompt.ask("[bold yellow]Select an option[/bold yellow]", choices=["0", "1", "2", "3", "4", "5", "6"])
        
        if choice == "1":
            url = Prompt.ask("\n[bold cyan]Enter YouTube Video URL[/bold cyan]")
            tools.download_video(url, "YouTube")
            
        elif choice == "2":
            url = Prompt.ask("\n[bold cyan]Enter Facebook Video/Reel URL[/bold cyan]")
            tools.download_video(url, "Facebook")
            
        elif choice == "3":
            with console.status("[bold cyan]Gathering system information...[/bold cyan]", spinner="bouncingBar"):
                info = tools.get_system_info()
                
            table = Table(title="System Information", show_header=True, header_style="bold magenta")
            table.add_column("Component", style="cyan")
            table.add_column("Details", style="green")
            
            for key, value in info.items():
                table.add_row(key, str(value))
            console.print(table)
            
        elif choice == "4":
            tools.vps_auto_setup()
            
        elif choice == "5":
            ip = Prompt.ask("\n[bold cyan]Enter Target IP/Domain[/bold cyan]")
            port = int(Prompt.ask("[bold cyan]Enter Port Number[/bold cyan]"))
            with console.status(f"[bold cyan]Scanning {ip}:{port}...[/bold cyan]", spinner="dots"):
                is_open = tools.check_open_port(ip, port)
            if is_open:
                console.print(f"[bold green]✔ Port {port} on {ip} is OPEN[/bold green]")
            else:
                console.print(f"[bold red]✘ Port {port} on {ip} is CLOSED or FILTERED[/bold red]")
                
        elif choice == "6":
            with console.status("[bold cyan]Running Speedtest (This may take a minute)...[/bold cyan]", spinner="earth"):
                ping, dl, ul = tools.run_speedtest()
            if ping:
                console.print(f"\n[bold green]Ping:[/bold green] {ping:.2f} ms")
                console.print(f"[bold green]Download:[/bold green] {dl:.2f} Mbps")
                console.print(f"[bold green]Upload:[/bold green] {ul:.2f} Mbps")
            else:
                console.print("[bold red]✘ Speedtest failed. Check your connection.[/bold red]")
                
        elif choice == "0":
            console.print("\n[bold magenta]Thank you for using X-TERMUX PRO TOOLKIT. Exiting safely...[/bold magenta]")
            sys.exit(0)
            
        Prompt.ask("\n[bold dim]Press Enter to return to the main menu...[/bold dim]")
        clear_screen()

if __name__ == "__main__":
    clear_screen()
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold red]Program interrupted by user. Exiting safely...[/bold red]")
        sys.exit(0)
