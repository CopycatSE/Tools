import sys
import os
import platform
import subprocess
import re
import time


# Dynamically add root project directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def run_deep_ssh_scan(ssh_ip_list):
    try:
        from config.ssh_tester_logic import scan_ssh_ports
        if ssh_ip_list:
            print()
            typewriter("    === DEEP SCAN CODE EXECUTION ===")
            scan_ssh_ports(ssh_ip_list)
    except ImportError:
        typewriter("[!] [!] Failed to import scan_ssh_ports from config.ssh_tester_logic. SSH check skipped [!] [!].", 0.01)

def run_common_ssh_scan(ssh_ip_list):
    try:
        from config.ssh_tester_logic_lite import scan_ssh_ports
        if ssh_ip_list:
            print()
            typewriter("    === COMMON SCAN CODE EXECUTION  ===")
            scan_ssh_ports(ssh_ip_list)
    except ImportError:
        typewriter("[!] [!] Failed to import scan_ssh_ports from config.ssh_tester_logic. SSH check skipped [!] [!]..", 0.01)

def select_button():
    import sys
    import termios
    import tty

    buttons = [ "DEEP PORT SCAN", "COMMON PORT SCAN", "CANCEL" ]
    selected = 0

    def print_buttons():
        sys.stdout.write("\r    ")
        for i, btn in enumerate(buttons):
            if i == selected:
                sys.stdout.write(f"\033[7m {btn} \033[0m ")  # Inverse for selected
            else:
                sys.stdout.write(f" {btn} ")
        sys.stdout.flush()

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        print_buttons()
        while True:
            ch = sys.stdin.read(1)
            if ch == '\x1b':  # escape sequence
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    if ch3 == 'C':  # right arrow
                        selected = (selected + 1) % len(buttons)
                        print_buttons()
                    elif ch3 == 'D':  # left arrow
                        selected = (selected - 1) % len(buttons)
                        print_buttons()
            elif ch == '\r' or ch == '\n':  # Enter key
                print()
                return selected
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def typewriter(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()

def get_local_ip_prefix():
    try:
        result = subprocess.check_output("ipconfig getifaddr en0", shell=True).decode().strip()
    except subprocess.CalledProcessError:
        result = subprocess.check_output("ipconfig getifaddr en1", shell=True).decode().strip()
    ip = result
    prefix = '.'.join(ip.split('.')[:3]) + '.'
    return prefix

def ping_device(ip):
    try:
        import time
        start = time.time()
        subprocess.check_output(['ping', '-c', '1', ip], stderr=subprocess.DEVNULL, timeout=0.1)
        return True, time.time() - start
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False, 0

def get_hostname(ip):
    try:
        output = subprocess.check_output(["nslookup", ip], stderr=subprocess.DEVNULL).decode()
        match = re.search(r'name = ([\w\-\.]+)', output)
        return match.group(1) if match else ""
    except Exception:
        return ""

def find_raspberry():
    prefix = get_local_ip_prefix()
    # Determine the full IP of this machine to exclude from the report
    try:
        local_full_ip = subprocess.check_output("ipconfig getifaddr en0", shell=True).decode().strip()
    except subprocess.CalledProcessError:
        local_full_ip = subprocess.check_output("ipconfig getifaddr en1", shell=True).decode().strip()
    start_time = time.time()
    
    print(f"\n\033[38;5;218m   ☰ [INFO] SCANNING NETWORK: {prefix}0/24...\033[0m", flush=True)

    last_bar = ""
    found_devices = []

    total_ips = 254

    for i in range(1, 255):
        ip = f"{prefix}{i}"
        success, ping_time = ping_device(ip)
        if success:
            hostname = get_hostname(ip)
            found_devices.append((ip, hostname))
        progress = int((i / 254) * 40)
        bar = "▓" * progress + "░" * (40 - progress)
        percent = int((i / 254) * 100)
        print(f"\r\033[1;34m    [ローディング] スキャン中: [{bar}] {percent}%\033[0m", end="", flush=True)
        # Only after the last update, do newline
        if i == 254:
            print()
            print()
   
    print("\033[36m\n☰    [SUMMARY] Scan complete! \033[0m")

    if found_devices:
        for ip, hostname in found_devices:
            if ip == local_full_ip:
                continue
            typewriter(f" ●●●●●● Device: {ip} — Hostname: {hostname}")
    else:
        typewriter("      ✗ No active devices found.")
    duration = time.time() - start_time
    total_scanned = 254
    network_range = f"{prefix}0/24"
    # Japanese summary: scanned X IPs in network Y in Z seconds
    print()
    typewriter(f"⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤", 0.001)
    print()
    typewriter(f"   {total_scanned} 個のIPアドレスをスキャンしました。ネットワーク: {network_range}。所要時間: {duration:.2f}秒。", 0.005)
    typewriter(f"⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤", 0.001)
    sys.stdout.flush()

    ssh_ip_list = [ip for ip, hostname in found_devices if ip != local_full_ip]
    return ssh_ip_list


def main():
    print()
    print("\033[36m\n       スキャンの種類を選択してください  \033[0m")
    print()

    choice = select_button()
    if choice == 0:
        print()
        typewriter(f"         EXECUTING DEEP PORT SCAN SEQUENCE...", 0.005)
        print()
        ssh_ip_list = find_raspberry()
        run_deep_ssh_scan(ssh_ip_list)
    elif choice == 1:
        print()
        typewriter(f"         EXECUTING COMMON PORT SCAN SEQUENCE...", 0.005)
        print()
        ssh_ip_list = find_raspberry()
        run_common_ssh_scan(ssh_ip_list)
    else:
        print("Bye!")
        sys.exit(0)


if __name__ == "__main__":
    main()