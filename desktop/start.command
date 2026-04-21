#!/bin/bash
# Start the PayPulse widget in the background (no visible terminal).

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_lib.sh"

ensure_venv

if is_widget_running; then
  echo "ℹ️  Widget is already running."
else
  echo "🚀 Launching widget in background ..."
  nohup ./.venv/bin/python3 widget.py >> .widget.log 2>&1 &
  disown $! 2>/dev/null || true
  sleep 0.5
  if is_widget_running; then
    echo "✅ Widget running. Logs: $SCRIPT_DIR/.widget.log"
  else
    echo "❌ Widget failed to start. Check $SCRIPT_DIR/.widget.log"
  fi
fi

close_terminal_window
