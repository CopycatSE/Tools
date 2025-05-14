import os
import platform
import subprocess
import re
import sys
import time
import sys

def typewriter(text, delay=0.03):
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
    print("\n\n\033[38;5;218m   ☰ [INFO] SCANNING NETWORK: {}0/24...\033[0m".format(prefix))
    sys.stdout.flush()

    print("\n", flush=True)
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
    print()
   
    print("\033[36m\n   ☰ [SUMMARY] Scan complete! \033[0m")

    if found_devices:
        for ip, hostname in found_devices:
            if ip == local_full_ip:
                continue
            typewriter(f"   ● Device: {ip} — Hostname: {hostname}")
    else:
        typewriter("✗ No active devices found.")
    duration = time.time() - start_time
    total_scanned = 254
    network_range = f"{prefix}0/24"
    # Japanese summary: scanned X IPs in network Y in Z seconds
    typewriter(f"{total_scanned} 個のIPアドレスをスキャンしました。ネットワーク: {network_range}。所要時間: {duration:.2f}秒。", 0.005)
    sys.stdout.flush()
    return None

if __name__ == "__main__":
    find_raspberry()