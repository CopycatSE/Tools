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
    local chars="/-\|"
    end=$((SECONDS + duration))
    while [ $SECONDS -lt $end ]; do
        for ((i=0; i<${#chars}; i++)); do
            printf "\r${YELLOW}🔎 Raspberry Pi をスキャン中... %s${NC}" "${chars:$i:1}"
            sleep 0.1
        done
    done
    printf "\r"
}

# Check for --yes flag to auto-confirm
AUTO_YES=false
for arg in "$@"; do
    if [[ "$arg" == "--yes" ]]; then
        AUTO_YES=true
    fi
done

echo -e "${YELLOW}⚠ このスクリプトはネットワーク内の全デバイスをスキャンします。${NC}"
echo -e "${YELLOW}(WARNING: This script scans all devices in your local network.)${NC}"
if [ "$AUTO_YES" = false ]; then
    read -p "続行しますか？ (Proceed? y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo -e "${RED}✗ キャンセルされました。スキャンは実行されませんでした。${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ --yes フラグ検出。スキャンを自動で続行します。${NC}"
fi

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

loading_animation 3

python3 "$(dirname "$0")/config/finder-logic.py"