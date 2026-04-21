#!/bin/bash
# Stop the running PayPulse widget. Does NOT disable auto-start.

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_lib.sh"

launchctl_stop

if is_widget_running; then
  echo "⚠️  Some widget process is still alive; force-killing ..."
  pkill -9 -f "$SCRIPT_DIR/widget.py" >/dev/null 2>&1 || true
fi

echo "✅ Widget stopped."
echo "   (auto-start on login is still configured; run uninstall-autostart.command to disable)"

close_terminal_window
