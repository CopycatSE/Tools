import sys
#!/usr/bin/env python3

import os
import sys
import time
import subprocess
import getpass
import platform
import shutil

# Terminal colors
GREEN = '\033[0;32m'
RED = '\033[0;31m'
CYAN = '\033[0;36m'
YELLOW = '\033[1;33m'
NC = '\033[0m'

def typewriter(text, delay=0.03):
    """Print text with a typewriter effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def loading_animation(duration=3):
    """Display a loading animation with a progress bar and Japanese message."""
    bar_length = 24
    fill_char = "▓"
    empty_char = "░"
    msg = "     スクリプトを読み込み中... "
    color_bar = '\033[1;36m'  # Cyan
    color_msg = '\033[1;33m'  # Yellow
    color_reset = '\033[0m'

    steps = duration * 10
    for i in range(steps + 1):
        filled = int(i * bar_length / steps)
        bar = fill_char * filled + empty_char * (bar_length - filled)
        percent = int(100 * i / steps)
        print(f"\r{color_msg}{msg}{color_bar}[{bar}] {percent:3d}%{color_reset}", end='', flush=True)
        time.sleep(0.05)
    print()

def check_cmd(cmd, label):
    """
    Check if a command is available.
    If missing, attempt to install it via Homebrew (on macOS).
    """
    if shutil.which(cmd):
        print(f"   ☑ {label} ... OK")
        return True
    else:
        print(f"   ☒ {label} ... MISSING")
        if not shutil.which("brew"):
            print(f"{RED}✗ Homebrewが見つかりません。https://brew.sh を確認してください。{NC}")
            return False
        print(f"{YELLOW}➤ {label} を Homebrew からインストールします...{NC}")
        time.sleep(1)
        if cmd == "awk":
            os.system("brew install gawk")
        else:
            os.system(f"brew install {cmd}")
        if shutil.which(cmd):
            print(f"{GREEN}✓ {label} が正常にインストールされました！{NC}")
            return True
        else:
            print(f"{RED}✗ {label} のインストールに失敗しました。手動で確認してください。{NC}")
            return False

def print_banner():
    """Print the ASCII art banner with cyan color."""
    banner = f"""{CYAN}
  ██████╗ ██╗██████╗ ███████╗ █████╗ ██████╗ ██████╗ ██╗   ██╗
  ██╔══██╗██║██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝
  ██████╔╝██║██████╔╝█████╗  ███████║██████╔╝██████╔╝ ╚████╔╝ 
  ██╔═══╝ ██║██╔═══╝ ██╔══╝  ██╔══██║██╔═══╝ ██╔═══╝   ╚██╔╝  
  ██║     ██║██║     ███████╗██║  ██║██║     ██║        ██║   
  ╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝        ╚═╝   {NC}
"""
    print(banner)

def print_warning():
    """Print a warning message about scanning all devices in the local network."""
    print()
    print(f"{YELLOW}          ⚠ このスクリプトはネットワーク内の全デバイスをスキャンします。⚠{NC}")
    print(f"{YELLOW}         ⚠ WARNING: This script scans all devices in your local network ⚠{NC}")
    print()
    time.sleep(5)

def system_info():
    """Fetch and display system information with a typewriter effect."""
    print()
    print(f"{CYAN}  ╭───────────────────────╮╭────────────────────────╮{NC}")
    print(f"{CYAN}≡ │ システム情報取得中... ││ (Fetching system info) │{NC}")
    print(f"{CYAN}  ╰───────────────────────╯╰────────────────────────╯{NC}")
    user = getpass.getuser()
    hostname = platform.node()
    os_str = f"{platform.system()} {platform.release()}"
    # IP detection for macOS
    local_ip = subprocess.getoutput("ipconfig getifaddr en0 2>/dev/null") or "N/A"
    gateway = subprocess.getoutput("netstat -rn | awk '/default/ {print $2}' | head -n 1")
    wifi = subprocess.getoutput("networksetup -getairportnetwork en0 2>/dev/null | cut -d ':' -f2 | xargs") or "N/A"
    typewriter(f"    ○ ユーザー (User):        {user}", 0.005)
    typewriter(f"    ○ ホスト名 (Hostname):    {hostname}", 0.005)
    typewriter(f"    ○ OS:                     {os_str}", 0.005)
    typewriter(f"    ○ 内部IP (Local IP):      {local_ip}", 0.005)
    typewriter(f"    ○ ゲートウェイ (Gateway): {gateway}", 0.005)
    typewriter(f"    ○ ネットワーク (Wi-Fi):   {wifi}", 0.005)

def check_tools():
    """Check for required tools and attempt installation if missing."""
    print()
    print(f"{CYAN}  ╭─────────────────────────────╮{NC}")
    print(f"{CYAN}≡ │ 必要なツールをチェック中... │{NC}")
    print(f"{CYAN}  ╰─────────────────────────────╯{NC}")
    missing = 0
    for cmd, label in [("python3", "Python3"), ("ping", "Ping"), ("awk", "Awk")]:
        if not check_cmd(cmd, label):
            missing += 1
    return missing

def clear_screen():
    """Clear the terminal screen."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def main():
    """Main function to orchestrate the script execution."""
    clear_screen()
    print("\n" * 7)
    print_warning()
    clear_screen()
    print_banner()
    time.sleep(1)
    typewriter(" このスクリプトは、ネットワーク内のすべてのデバイスをスキャンします", 0.01)
    typewriter(" スキャン結果として、IPアドレスのレポートを表示します。", 0.01)
    time.sleep(1)
    print()
    system_info()
    if check_tools():
        sys.exit(1)
    print()
    loading_animation(3)
    # Import and run the main logic from finder_logic module
    try:
        from config.finder_logic import main as finder_main
    except ImportError:
        print("Error: Failed to import finder_logic. Please check the project structure.")
        sys.exit(1)
    # Directly call finder_logic main function
    finder_main()

if __name__ == "__main__":
    main()