#!/bin/bash
# PayPulse desktop tools · one-time setup
# Creates a local .venv so nothing touches your system Python.

set -e
cd "$(dirname "$0")"

echo "🔧 Creating virtualenv at $(pwd)/.venv ..."
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  echo "✅ venv created"
else
  echo "ℹ️  venv already exists, skipping"
fi

echo "📦 Installing dependencies ..."
./.venv/bin/pip install --upgrade pip --quiet
# rumps           → macOS menu-bar app
# pyobjc-framework-Quartz → window-level APIs for the widget
./.venv/bin/pip install rumps "pyobjc-framework-Quartz" --quiet

echo ""
echo "🎉 Done!"
echo ""
echo "Next steps:"
echo "  1. Open the web dashboard first (double-click ../index.html)"
echo "     and finish the onboarding wizard."
echo "  2. In the dashboard: Settings → Export, and save the JSON"
echo "     as: $(pwd)/paypulse-config.json"
echo "  3. Then launch:"
echo "       • widget.command    → desktop card"
echo "       • menubar.command   → menu-bar ticker"
echo ""
