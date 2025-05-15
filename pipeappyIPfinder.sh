#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

function typewriter() {
    text="$1"
    delay="${2:-0.03}"
    while IFS= read -n1 char; do
        printf "%s" "$char"
        sleep "$delay"
    done <<< "$text"
    echo
}

function loading_animation() {
    local duration="${1:-3}"
    local bar_length=24
    local fill_char="▓"
    local empty_char="░"
    local msg="     スクリプトを読み込み中... "
    local color_bar='\033[1;36m'  # Cyan
    local color_msg='\033[1;33m'  # Yellow
    local color_reset='\033[0m'

    local steps=$((duration * 10))
    for ((i=0; i<=steps; i++)); do
        local filled=$((i * bar_length / steps))
        local bar=""
        for ((j=0; j<bar_length; j++)); do
            if [ $j -lt $filled ]; then
                bar+="$fill_char"
            else
                bar+="$empty_char"
            fi
        done
        printf "\r${color_msg}%s${color_bar}[%s] %3d%%${color_reset}" "$msg" "$bar" "$((100 * i / steps))"
        sleep 0.05
    done
    printf "\n"
}

# Check for --yes flag to auto-confirm
AUTO_YES=false
for arg in "$@"; do
    if [[ "$arg" == "--yes" ]]; then
        AUTO_YES=true
    fi
done
clear
echo 
echo 
echo 
echo 
echo 
echo 
echo 
echo -e "${YELLOW}          ⚠ このスクリプトはネットワーク内の全デバイスをスキャンします。${NC}"
echo -e "${YELLOW}(         WARNING: This script scans all devices in your local network.)${NC}"
echo
echo 
echo 
echo 
echo 
echo 
echo 


sleep 5

clear
echo -e "${CYAN}"
echo "  ██████╗ ██╗██████╗ ███████╗ █████╗ ██████╗ ██████╗ ██╗   ██╗"
echo "  ██╔══██╗██║██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝"
echo "  ██████╔╝██║██████╔╝█████╗  ███████║██████╔╝██████╔╝ ╚████╔╝ "
echo "  ██╔═══╝ ██║██╔═══╝ ██╔══╝  ██╔══██║██╔═══╝ ██╔═══╝   ╚██╔╝  "
echo "  ██║     ██║██║     ███████╗██║  ██║██║     ██║        ██║   "
echo "  ╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝        ╚═╝   "
echo -e "${NC}"
sleep 1


typewriter " このスクリプトは、ネットワーク内のすべてのデバイスをスキャンします" 0.01
typewriter " スキャン結果として、IPアドレスのレポートを表示します。" 0.01
sleep 1
echo
echo -e "${CYAN}  ╭───────────────────────╮╭────────────────────────╮${NC}"
echo -e "${CYAN}≡ │ システム情報取得中... ││ (Fetching system info) │${NC}"
echo -e "${CYAN}  ╰───────────────────────╯╰────────────────────────╯${NC}"
typewriter "    ○ ユーザー (User):        $(whoami)" 0.005
typewriter "    ○ ホスト名 (Hostname):    $(hostname)" 0.005
typewriter "    ○ OS:                     $(uname -s) $(uname -r)" 0.005
typewriter "    ○ 内部IP (Local IP):      $(ipconfig getifaddr en0 2>/dev/null || echo 'N/A')" 0.005
typewriter "    ○ ゲートウェイ (Gateway): $(netstat -rn | awk '/default/ {print $2}' | head -n 1)" 0.005
typewriter "    ○ ネットワーク (Wi-Fi):   $(networksetup -getairportnetwork en0 2>/dev/null | cut -d ':' -f2 | xargs || echo 'N/A')" 0.005

if ! command -v python3 &> /dev/null 
then
    typewriter "Python3 が見つかりません！インストールしてください！" 0.005
    exit 1
fi

echo
echo -e "${CYAN}  ╭─────────────────────────────╮${NC}"
echo -e "${CYAN}≡ │ 必要なツールをチェック中... │${NC}"
echo -e "${CYAN}  ╰─────────────────────────────╯${NC}"
missing=0

function check_cmd() {
    local cmd="$1"
    local label="$2"
    if command -v "$cmd" &> /dev/null; then
        echo -e "   ☑ ${label} ... OK"
    else
        echo -e "   ☒ ${label} ... MISSING"
        if ! command -v brew &> /dev/null; then
            echo -e "${RED}✗ Homebrewが見つかりません。https://brew.sh を確認してください。${NC}"
            missing=1
            return
        fi

        echo -e "${YELLOW}➤ ${label} を Homebrew からインストールします...${NC}"
        sleep 1
        if [[ "$cmd" == "awk" ]]; then
            brew install gawk
        else
            brew install "$cmd"
        fi

        if command -v "$cmd" &> /dev/null; then
            echo -e "${GREEN}✓ ${label} が正常にインストールされました！${NC}"
        else
            echo -e "${RED}✗ ${label} のインストールに失敗しました。手動で確認してください。${NC}"
            missing=1
        fi
    fi
}

check_cmd "python3" "Python3"
check_cmd "ping" "Ping"
check_cmd "awk" "Awk"


# Create venv if it does not exist
if [ ! -d "$HOME/myvenv" ]; then
    typewriter "○ Python venv が見つかりません。~/myvenv を作成します..." 0.01
    python3 -m venv "$HOME/myvenv"
    if [ $? -ne 0 ]; then
        typewriter "✗ venvの作成に失敗しました。python3 を確認してください。" 0.01
        exit 1
    fi
fi

# Activate the venv
source "$HOME/myvenv/bin/activate"
echo
typewriter "            ✓ Python venv がアクティブになりました" 0.01
echo

loading_animation 3

python3 "$(dirname "$0")/config/finder_logic.py"
