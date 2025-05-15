# Network Scanner & SSH Tools

Scan your local network for active devices and open ports — with options for a deep or common scan, including SSH checks.

## Requirements

- macOS or Linux (may work on Windows with Python 3)
- Python 3 (only required if running the Python script)

## Installation

Clone this repo:

```bash
git clone <repo-url>
cd Tools
```

## Usage

### Running the Python script (interactive button selection):

```bash
python3 config/finder_logic.py
```

### Running the standalone binary (no Python required):

```bash
./pipeappyIPfinder
```

Or with the `--yes` option:

```bash
./pipeappyIPfinder --yes
```

All required Python dependencies are installed automatically if using the Python script.

## Scan Modes

- **Deep Scan:** Scans all detected IP addresses in your network, checks a wide range of ports, and provides SSH accessibility reports.
- **Common Scan:** Scans only popular ports and the 3300–3400 range for each active host.
- **End:** Exits the app.

## Example Output

```
スキャンの種類を選択してください
  [ DEEP PORT SCAN ] [ COMMON PORT SCAN ] [ END ]

   ☰ [INFO] SCANNING NETWORK: 192.168.8.0/24...
    [ローディング] スキャン中: [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] 100%

☰    [SUMMARY] Scan complete!
 ●●●●●● Device: 192.168.8.1 — Hostname: homerouter.cpe.
 ●●●●●● Device: 192.168.8.41 — Hostname: iPhone.
 ●●●●●● Device: 192.168.8.70 — Hostname: copycat-pi-riga.

=== SSH PORT SCAN ===
192.168.8.41: SSH open
192.168.8.70: SSH closed
```

## License

MIT
