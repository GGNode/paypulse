# PayPulse desktop · shared shell helpers
# Sourced by the .command scripts.

PLIST_LABEL="com.paypulse.widget"
PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_LABEL.plist"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Close the current Terminal window after N seconds, so scripts feel
# "headless" when double-clicked from Finder.
close_terminal_window() {
  local delay="${1:-1.5}"
  (
    sleep "$delay"
    osascript <<'APPLESCRIPT' >/dev/null 2>&1
tell application "Terminal"
  try
    close front window
  end try
end tell
APPLESCRIPT
  ) &
  disown $! 2>/dev/null || true
}

# Make sure the venv exists; auto-run setup.sh if not.
ensure_venv() {
  cd "$PROJECT_DIR"
  if [ ! -f ".venv/bin/python3" ]; then
    echo "🔧 First run — installing dependencies (≈30s) ..."
    bash ./setup.sh
  fi
}

is_widget_running() {
  pgrep -f "paypulse.*widget.py" >/dev/null 2>&1 \
    || pgrep -f "$PROJECT_DIR/widget.py" >/dev/null 2>&1
}

is_agent_installed() {
  [ -f "$PLIST_PATH" ]
}

write_plist() {
  mkdir -p "$(dirname "$PLIST_PATH")"
  cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>$PLIST_LABEL</string>

  <key>ProgramArguments</key>
  <array>
    <string>$PROJECT_DIR/.venv/bin/python3</string>
    <string>$PROJECT_DIR/widget.py</string>
  </array>

  <key>WorkingDirectory</key>
  <string>$PROJECT_DIR</string>

  <key>RunAtLoad</key>
  <true/>

  <!-- KeepAlive=false: if user quits the widget manually, don't re-spawn. -->
  <key>KeepAlive</key>
  <false/>

  <key>ProcessType</key>
  <string>Interactive</string>

  <key>StandardOutPath</key>
  <string>$PROJECT_DIR/.widget.log</string>
  <key>StandardErrorPath</key>
  <string>$PROJECT_DIR/.widget.log</string>
</dict>
</plist>
EOF
}

launchctl_start() {
  launchctl unload "$PLIST_PATH" >/dev/null 2>&1 || true
  launchctl load "$PLIST_PATH" >/dev/null 2>&1 || true
}

launchctl_stop() {
  launchctl unload "$PLIST_PATH" >/dev/null 2>&1 || true
  pkill -f "$PROJECT_DIR/widget.py" >/dev/null 2>&1 || true
}

launchctl_restart() {
  launchctl_stop
  sleep 0.3
  if is_agent_installed; then
    launchctl load "$PLIST_PATH" >/dev/null 2>&1 || true
  fi
}
