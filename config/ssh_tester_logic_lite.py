import socket

def check_ssh(ip, port=22, timeout=0.5):
    """Проверяет, открыт ли порт 22 на указанном IP."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, port))
        s.close()
        return True
    except (socket.timeout, socket.error):
        return False

import sys
import time

def typewriter(text, delay=0.015):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()

def scan_ssh_ports(ip_list):
    GREEN = '\033[1;32m'
    RED = '\033[1;31m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[1;36m'
    RESET = '\033[0m'
    BOX = '═' * 34

    open_total = 0
    closed_total = 0

    print(f"{CYAN}      ╔{BOX}╗{RESET}")
    print(f"{CYAN}≡     ║      SSH PORT SCAN REPORT        ║{RESET}")
    print(f"{CYAN}      ╚{BOX}╝{RESET}")
    print()

    for ip in ip_list:
        if ip == "192.168.8.1":
            continue
        open_ports = []
        common_ports = [
            22, 21, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995,
            1723, 3306, 3389, 5900, 8080
        ]
        extra_ports = list(range(3300, 3401))
        all_ports = sorted(set(common_ports + extra_ports))
        total_ports = len(all_ports)
        bar_length = 28

        for idx, port in enumerate(all_ports, 1):
            if check_ssh(ip, port=port):
                open_ports.append(port)
                open_total += 1
            # Draw progress bar every 5 ports or at the end
            if idx % 5 == 0 or idx == total_ports:
                progress = int((idx / total_ports) * bar_length)
                bar = "▓" * progress + "░" * (bar_length - progress)
                percent = int((idx / total_ports) * 100)
                print(f"\r      [{bar}] {percent}% ({ip})", end="", flush=True)
        print()  # Newline after each IP's progress bar
        # Reporting
        if open_ports:
            typewriter(f"{GREEN}                    ✓ {ip} — open: {', '.join(map(str, open_ports))}{RESET}", delay=0.001)
            print()
        else:
            typewriter(f"{RED}                      ✗ {ip} — open: none{RESET}", delay=0.005)
            print()
    print()
    typewriter(f"{YELLOW}           --- SUMMARY ---{RESET}")
    typewriter(f"{GREEN}    ✓ OPEN PORTS:{RESET} {open_total}   {RED}✗ CLOSED PORTS:{RESET} {closed_total}", delay=0.02)
    print()
    typewriter(f"{CYAN}     Scan complete for {len(ip_list)} hosts.{RESET}", delay=0.012)
    print()
    print()
