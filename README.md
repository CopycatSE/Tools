# Network Scanner Tools

A collection of scripts to scan your local network for active devices and generate a detailed IP report with a flashy terminal UI.

## 🚀 Features

- **Fast, full-range scan** of all IPs in your subnet
- **Colorful, animated** progress bar and summary headers
- **Bash wrapper** with typewriter effect, system info dump, and pre-flight checks
- **Python core** (`finder-logic.py`) for platform‑agnostic ICMP ping scanning
- **Auto-install** missing tools via Homebrew (optional `--yes` flag)
- **Customizable** timings, color schemes, and output formatting

## 🛠️ Prerequisites

- macOS or Linux with:
  - Python 3.x
  - Bash
  - Homebrew (for auto-install functionality)
- Terminal that supports ANSI escape codes and UTF-8 encoding

## ⚙️ Installation

1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd Tools
   ```
2. Make the Bash script executable:
   ```bash
   chmod +x raspberryIPfinder.sh
   ```
3. Ensure Python script is executable (if needed):
   ```bash
   chmod +x config/finder-logic.py
   ```

## 📖 Usage

### Bash Wrapper

```bash
./raspberryIPfinder.sh [--yes]
```

- `--yes` – skip confirmation prompt and proceed automatically.
- The script will:
  1. Display a typewriter‑style description and system info.
  2. Check for required tools and offer auto-install via Homebrew.
  3. Animate a pastel‑pink, ASCII-art banner and a cyan summary header.
  4. Invoke the Python scanner to ping every IP in `prefix`.
  5. Render a blue progress bar with percentage.
  6. Show final Japanese summary with total IPs scanned and elapsed time.

### Python Core

```bash
python3 config/finder-logic.py
```

You can call the Python script directly if you prefer manual orchestration.

## 🔧 Configuration

- **Subnet prefix** is auto-detected via `hostname -I` (Linux) or `ipconfig getifaddr en0` (macOS).
- **Timing**: Adjust `MAX_DURATION` in `find_raspberry()` for total scan duration.
- **Colors**: Modify ANSI codes in both scripts to suit your theme.
- **Typewriter speed**: Tweak `delay` parameters in `typewriter()` functions.

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.
