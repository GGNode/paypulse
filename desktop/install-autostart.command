#!/bin/bash
# Install the LaunchAgent so the widget auto-starts on login.

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_lib.sh"

ensure_venv
write_plist
launchctl_start

sleep 0.5
echo "-----------------------------------"
if is_widget_running; then
  echo "✅ Auto-start installed and widget is running now."
else
  echo "⚠️  LaunchAgent installed, but widget didn't appear yet."
  echo "    Check: $SCRIPT_DIR/.widget.log"
fi
echo ""
echo "   LaunchAgent: $PLIST_PATH"
echo "   Uninstall any time with uninstall-autostart.command"

close_terminal_window 2.5
