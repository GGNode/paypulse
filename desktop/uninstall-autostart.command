#!/bin/bash
# Remove the LaunchAgent so the widget no longer auto-starts.

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/_lib.sh"

launchctl_stop
if [ -f "$PLIST_PATH" ]; then
  rm -f "$PLIST_PATH"
  echo "✅ Auto-start removed ($PLIST_PATH)"
else
  echo "ℹ️  Auto-start was not installed; nothing to do."
fi

close_terminal_window
