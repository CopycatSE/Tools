import socket
import sys
import time

def check_ssh(ip, port=22, timeout=0.5):
    """Checks if port 22 is open on the specified IP."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, port))
        s.close()
        return True
    except (socket.timeout, socket.error):
        return False

def typewriter(text, delay=0.015):
    # Print text with a typewriter effect
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()

def scan_ssh_ports(ip_list):
    # Define color codes for terminal output
    GREEN = '\033[1;32m'
    RED = '\033[1;31m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[1;36m'
    RESET = '\033[0m'
    BOX = '═' * 34

    open_total = 0
    closed_total = 0

    # Print header with styling
    print(f"{CYAN}      ╔{BOX}╗{RESET}")
    print(f"{CYAN}≡     ║      SSH PORT SCAN REPORT        ║{RESET}")
    print(f"{CYAN}      ╚{BOX}╝{RESET}")
    print()

    # Iterate over each IP address in the list
    for ip in ip_list:
        if ip == "192.168.8.1":
            # Skip this specific IP
            continue

        open_ports = []
        total_ports = 65535
        bar_length = 28

        # Scan all ports from 1 to 65535
        for idx, port in enumerate(range(1, 65536), 1):
            if check_ssh(ip, port=port):
                open_ports.append(port)
                open_total += 1

            # Update progress bar every 500 ports or at the end
            if idx % 500 == 0 or idx == total_ports:
                progress = int((idx / total_ports) * bar_length)
                bar = "▓" * progress + "░" * (bar_length - progress)
                percent = int((idx / total_ports) * 100)
                print(f"\r      [{bar}] {percent}% ({ip})", end="", flush=True)

        print()  # Newline after each IP's progress bar

        # Report open ports or none found
        if open_ports:
            typewriter(f"{GREEN}                    ✓ {ip} — open: {', '.join(map(str, open_ports))}{RESET}", delay=0.001)
            print()
        else:
            typewriter(f"{RED}                      ✗ {ip} — open: none{RESET}", delay=0.005)
            print()

    print()
    # Print summary of scan results
    typewriter(f"{YELLOW}           --- SUMMARY ---{RESET}")
    typewriter(f"{GREEN}    ✓ OPEN PORTS:{RESET} {open_total}   {RED}✗ CLOSED PORTS:{RESET} {closed_total}", delay=0.02)
    print()
    typewriter(f"{CYAN}     Scan complete for {len(ip_list)} hosts.{RESET}", delay=0.012)
    print()
    print()

if __name__ == "__main__":
    pass