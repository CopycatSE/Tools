import os
import sys

print("=== PYTHON IMPORT TEST ===\n")

print("Current working directory (os.getcwd()):")
print(os.getcwd())
print()

print("sys.path:")
for p in sys.path:
    print("  ", p)
print()

print("Contents of config/:")
print(os.listdir("config"))
print()

try:
    from config.ssh_tester_logic_lite import scan_ssh_ports
    print("SUCCESS: scan_ssh_ports imported from config.ssh_tester_logic_lite!")
    print("Function object:", scan_ssh_ports)
except Exception as e:
    print("FAIL: Could not import scan_ssh_ports from config.ssh_tester_logic_lite")
    print("Error:", e)
print()

try:
    from config.ssh_tester_logic import scan_ssh_ports as deep_scan_ports
    print("SUCCESS: scan_ssh_ports imported from config.ssh_tester_logic!")
    print("Function object:", deep_scan_ports)
except Exception as e:
    print("FAIL: Could not import scan_ssh_ports from config.ssh_tester_logic")
    print("Error:", e)
print("\n=== DONE ===")