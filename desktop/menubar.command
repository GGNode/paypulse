#!/bin/bash
# Launch the PayPulse menu-bar app (foreground).

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_lib.sh"

ensure_venv
echo "🚀 Starting PayPulse menu-bar app"
exec ./.venv/bin/python3 menubar.py
