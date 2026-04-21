#!/bin/bash
# Show status of the PayPulse widget and its auto-start LaunchAgent.

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_lib.sh"

echo "📊 PayPulse widget status"
echo "-----------------------------------"

if is_widget_running; then
  echo "Process:     ✅ running"
  pgrep -lf "$SCRIPT_DIR/widget.py" || true
else
  echo "Process:     ❌ not running"
fi

if is_agent_installed; then
  echo "Auto-start:  ✅ installed ($PLIST_PATH)"
else
  echo "Auto-start:  ❌ not installed"
fi

echo ""
echo "Logs:        $SCRIPT_DIR/.widget.log"
echo ""
read -n 1 -s -r -p "Press any key to close ..."
echo ""
