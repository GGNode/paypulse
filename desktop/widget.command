#!/bin/bash
# Launch the PayPulse desktop widget (foreground, for debugging).
# For background / auto-start, use start.command instead.

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_lib.sh"

ensure_venv
echo "🚀 Starting PayPulse widget (foreground)"
echo "   Quit: right-click the widget → Quit, or press Ctrl-C here"
exec ./.venv/bin/python3 widget.py
