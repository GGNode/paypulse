#!/usr/bin/env python3
"""
PayPulse · macOS Desktop Widget
===============================
A floating desktop card that shows your live earnings in real time.

• Refreshes every second
• Click → open the full web dashboard
• Right-click → menu (mode / reload config / reset position / quit)
• Drag anywhere on the card to reposition (position is remembered)

Display modes (switch via right-click menu):

  💻 Normal window (default, recommended)
     Behaves like a normal app window: can be clicked/dragged.
     Hidden behind other apps but visible on "Show desktop".
     Does NOT appear in the Dock.
  📌 Always on top
     Floats above all other windows. Always visible.
  🏖️ Desktop-wallpaper layer (advanced)
     Sits at the same layer as desktop icons.
     ⚠ Clicks/drags may not work in this mode (macOS limitation).

When any app is in fullscreen mode, the widget auto-hides, so it
doesn't pop up over fullscreen videos.

Usage:
  python3 widget.py            # or double-click widget.command
"""

import os
import sys
import json
import webbrowser
from datetime import datetime

try:
    import objc
    from AppKit import (
        NSApplication, NSApp, NSWindow, NSView, NSColor, NSFont, NSEvent,
        NSTextField, NSBackingStoreBuffered, NSMenu, NSMenuItem,
        NSVisualEffectView, NSVisualEffectMaterialHUDWindow,
        NSVisualEffectBlendingModeBehindWindow, NSVisualEffectStateActive,
        NSScreen, NSFontWeightBold, NSFontWeightRegular, NSTextAlignmentLeft,
        NSApplicationActivationPolicyAccessory, NSWorkspace,
        NSWindowCollectionBehaviorCanJoinAllSpaces,
        NSWindowCollectionBehaviorStationary,
        NSWindowCollectionBehaviorIgnoresCycle,
    )
    from Foundation import NSObject, NSTimer, NSMakeRect, NSMakePoint
    from PyObjCTools import AppHelper
    from Quartz import (
        CGWindowLevelForKey, kCGDesktopWindowLevelKey,
        CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly,
        kCGNullWindowID,
    )
except ImportError as e:
    print(f"❌ Missing dependency: {e}\nPlease run: bash setup.sh")
    sys.exit(1)

# Reuse menubar compute logic
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from menubar import compute_now, load_config, fmt_money, CONFIG_PATH, DASHBOARD  # noqa: E402


# ================= Constants =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, ".widget_state.json")

WIDGET_W, WIDGET_H = 280, 130

LEVEL_NORMAL = 0         # NSNormalWindowLevel
LEVEL_FLOATING = 3       # NSFloatingWindowLevel
LEVEL_DESKTOP = CGWindowLevelForKey(kCGDesktopWindowLevelKey)

MODE_DEFS = {
    "normal":   ("💻 Normal window (recommended)", LEVEL_NORMAL),
    "floating": ("📌 Always on top",               LEVEL_FLOATING),
    "desktop":  ("🏖️ Desktop-wallpaper layer",     LEVEL_DESKTOP),
}
DEFAULT_MODE = "normal"


# ================= State persistence =================
def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


# ================= Fullscreen detection =================
_FULLSCREEN_EXCLUDE = {
    "Window Server", "Dock", "SystemUIServer", "Control Center",
    "Notification Center", "Spotlight", "TextInputMenuAgent", "Finder",
    # macOS localized owner names.
    "程序坞", "系统用户界面服务器", "控制中心", "通知中心", "访达",
}
_MY_PID = os.getpid()
_FULLSCREEN_EDGE_TOLERANCE = 12
_FULLSCREEN_RESTORE_GRACE_SECONDS = 5.0


def _log(message):
    print(
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}",
        flush=True,
    )


def _screen_rects():
    rects = []
    for screen in NSScreen.screens():
        frame = screen.frame()
        rects.append((
            float(frame.origin.x),
            float(frame.origin.y),
            float(frame.size.width),
            float(frame.size.height),
        ))
    return rects


def _covers_screen(bounds, screen):
    """Return True when a Quartz window bounds rect covers a full screen."""
    sx, sy, sw, sh = screen
    x = float(bounds.get("X", 0))
    y = float(bounds.get("Y", 0))
    w = float(bounds.get("Width", 0))
    h = float(bounds.get("Height", 0))
    tol = _FULLSCREEN_EDGE_TOLERANCE

    if w < 200 or h < 200:
        return False

    return (
        x <= sx + tol
        and y <= sy + tol
        and x + w >= sx + sw - tol
        and y + h >= sy + sh - tol
    )


def find_fullscreen_window():
    """Return the app window that looks fullscreen, or None.

    Browser video fullscreen windows are not always reported consistently by
    Quartz, and they are not guaranteed to be layer 0. The reliable signal is
    a non-system, visible app-owned window covering an entire screen.
    """
    try:
        windows = CGWindowListCopyWindowInfo(
            kCGWindowListOptionOnScreenOnly, kCGNullWindowID
        )
    except Exception:
        return None
    if not windows:
        return None

    screens = _screen_rects()
    for window in windows:
        if window.get("kCGWindowOwnerPID") == _MY_PID:
            continue
        owner = window.get("kCGWindowOwnerName", "") or ""
        if owner in _FULLSCREEN_EXCLUDE:
            continue
        layer = int(window.get("kCGWindowLayer", 0) or 0)
        # Dock, menu bar and system overlays may cover the screen in Quartz's
        # list. Real app/video fullscreen surfaces live below those layers.
        if layer < 0 or layer >= 20:
            continue
        if float(window.get("kCGWindowAlpha", 1) or 0) <= 0:
            continue
        bounds = window.get("kCGWindowBounds") or {}
        if any(_covers_screen(bounds, screen) for screen in screens):
            return window
    return None


def is_any_app_fullscreen():
    """Return True if any non-system app window covers a full screen."""
    return find_fullscreen_window() is not None


# ================= Pass-through subviews =================
class PassThroughEffect(NSVisualEffectView):
    """Background blur layer that doesn't intercept mouse events."""
    def hitTest_(self, point):
        return None


class PassThroughLabel(NSTextField):
    """Read-only label that doesn't intercept mouse events."""
    def hitTest_(self, point):
        return None


# ================= Content view (receives click / drag / right-click) =================
class WidgetView(NSView):
    _click_cb = None
    _drag_start_window_origin = None
    _drag_start_mouse = None
    _did_drag = False
    DRAG_THRESHOLD = 4

    def setClickCallback_(self, cb):
        self._click_cb = cb

    def acceptsFirstMouse_(self, event):
        return True

    def mouseDown_(self, event):
        win = self.window()
        if win is None:
            return
        self._drag_start_mouse = NSEvent.mouseLocation()
        self._drag_start_window_origin = win.frame().origin
        self._did_drag = False

    def mouseDragged_(self, event):
        if self._drag_start_mouse is None:
            return
        now = NSEvent.mouseLocation()
        dx = now.x - self._drag_start_mouse.x
        dy = now.y - self._drag_start_mouse.y
        if not self._did_drag and (abs(dx) > self.DRAG_THRESHOLD or abs(dy) > self.DRAG_THRESHOLD):
            self._did_drag = True
        if self._did_drag:
            self.window().setFrameOrigin_(NSMakePoint(
                self._drag_start_window_origin.x + dx,
                self._drag_start_window_origin.y + dy,
            ))

    def mouseUp_(self, event):
        if not self._did_drag and self._click_cb is not None:
            self._click_cb()
        if self._did_drag and self.window():
            origin = self.window().frame().origin
            st = load_state()
            st["x"] = float(origin.x)
            st["y"] = float(origin.y)
            save_state(st)
        self._drag_start_mouse = None
        self._drag_start_window_origin = None


# ================= App delegate =================
class WidgetDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        self.cfg = load_config()
        self.state = load_state()
        self.mode = self.state.get("mode", DEFAULT_MODE)
        self._hidden_by_fs = False
        self._fs_missing_since = None
        self._space_generation = 0
        self._hidden_on_space_generation = None
        self._logged_same_space_missing = False
        self._build_window()
        self._apply_mode(self.mode)
        self._build_menu()
        self._refresh()

        ws_nc = NSWorkspace.sharedWorkspace().notificationCenter()
        ws_nc.addObserver_selector_name_object_(
            self, b"_spaceChanged:",
            "NSWorkspaceActiveSpaceDidChangeNotification", None,
        )
        self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            1.0, self, b"_tick:", None, True
        )
        self.fs_timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            2.0, self, b"_checkFullscreen:", None, True
        )
        self._apply_fullscreen_visibility()

    # ---------- Build window ----------
    def _build_window(self):
        screen = NSScreen.mainScreen().visibleFrame()
        default_x = screen.origin.x + 20
        default_y = screen.origin.y + 20
        x = self.state.get("x", default_x)
        y = self.state.get("y", default_y)
        frame = NSMakeRect(x, y, WIDGET_W, WIDGET_H)

        NSWindowStyleMaskBorderless = 0
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            frame, NSWindowStyleMaskBorderless, NSBackingStoreBuffered, False
        )
        self.window.setOpaque_(False)
        self.window.setBackgroundColor_(NSColor.clearColor())
        self.window.setHasShadow_(True)
        self.window.setHidesOnDeactivate_(False)
        self.window.setIgnoresMouseEvents_(False)
        self.window.setCollectionBehavior_(
            NSWindowCollectionBehaviorCanJoinAllSpaces
            | NSWindowCollectionBehaviorStationary
            | NSWindowCollectionBehaviorIgnoresCycle
        )

        self.content = WidgetView.alloc().initWithFrame_(
            NSMakeRect(0, 0, WIDGET_W, WIDGET_H)
        )
        self.content.setClickCallback_(self._open_dashboard)
        self.window.setContentView_(self.content)

        effect = PassThroughEffect.alloc().initWithFrame_(
            NSMakeRect(0, 0, WIDGET_W, WIDGET_H)
        )
        effect.setMaterial_(NSVisualEffectMaterialHUDWindow)
        effect.setBlendingMode_(NSVisualEffectBlendingModeBehindWindow)
        effect.setState_(NSVisualEffectStateActive)
        effect.setWantsLayer_(True)
        effect.layer().setCornerRadius_(16.0)
        effect.layer().setMasksToBounds_(True)
        effect.setAutoresizingMask_(18)
        self.content.addSubview_(effect)

        self.lblStatus = self._make_label(
            x=14, y=WIDGET_H - 32, w=WIDGET_W - 28, h=22,
            size=12, weight=NSFontWeightRegular,
            color=NSColor.secondaryLabelColor(),
        )
        self.content.addSubview_(self.lblStatus)

        self.lblToday = self._make_label(
            x=14, y=WIDGET_H - 84, w=WIDGET_W - 28, h=46,
            size=30, weight=NSFontWeightBold,
            color=NSColor.labelColor(),
        )
        self.content.addSubview_(self.lblToday)

        self.lblSub = self._make_label(
            x=14, y=10, w=WIDGET_W - 28, h=36,
            size=10, weight=NSFontWeightRegular,
            color=NSColor.tertiaryLabelColor(),
        )
        self.lblSub.setLineBreakMode_(0)
        self.lblSub.cell().setWraps_(True)
        self.content.addSubview_(self.lblSub)

        self.window.orderFrontRegardless()

    def _make_label(self, x, y, w, h, size, weight, color):
        lbl = PassThroughLabel.alloc().initWithFrame_(NSMakeRect(x, y, w, h))
        lbl.setBezeled_(False)
        lbl.setDrawsBackground_(False)
        lbl.setEditable_(False)
        lbl.setSelectable_(False)
        lbl.setFont_(NSFont.systemFontOfSize_weight_(size, weight))
        lbl.setTextColor_(color)
        lbl.setAlignment_(NSTextAlignmentLeft)
        return lbl

    # ---------- Right-click menu ----------
    def _build_menu(self):
        menu = NSMenu.alloc().init()
        menu.setAutoenablesItems_(False)

        info = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "— PayPulse widget —", None, ""
        )
        info.setEnabled_(False)
        menu.addItem_(info)
        menu.addItem_(NSMenuItem.separatorItem())

        mode_header = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Display mode:", None, ""
        )
        mode_header.setEnabled_(False)
        menu.addItem_(mode_header)

        self.mi_modes = {}
        for key, (label, _lv) in MODE_DEFS.items():
            mi = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                label, b"_setMode:", ""
            )
            mi.setTarget_(self)
            mi.setRepresentedObject_(key)
            menu.addItem_(mi)
            self.mi_modes[key] = mi

        menu.addItem_(NSMenuItem.separatorItem())

        mi_open = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "📊 Open full dashboard", b"_menuOpen:", ""
        )
        mi_open.setTarget_(self)
        menu.addItem_(mi_open)

        mi_reload = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "🔄 Reload config", b"_reload:", ""
        )
        mi_reload.setTarget_(self)
        menu.addItem_(mi_reload)

        mi_reset = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "↩️ Reset to bottom-left", b"_resetPos:", ""
        )
        mi_reset.setTarget_(self)
        menu.addItem_(mi_reset)

        menu.addItem_(NSMenuItem.separatorItem())

        mi_quit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "❌ Quit widget", b"_quit:", "q"
        )
        mi_quit.setTarget_(self)
        menu.addItem_(mi_quit)

        self.content.setMenu_(menu)
        self._update_mode_checks()

    def _update_mode_checks(self):
        for key, mi in self.mi_modes.items():
            mi.setState_(1 if key == self.mode else 0)

    # ---------- Mode ----------
    def _apply_mode(self, key):
        if key not in MODE_DEFS:
            key = DEFAULT_MODE
        _label, level = MODE_DEFS[key]
        self.window.setLevel_(level)
        self.mode = key
        st = load_state()
        st["mode"] = key
        save_state(st)

    def _setMode_(self, sender):
        key = sender.representedObject()
        if key in MODE_DEFS:
            self._apply_mode(key)
            self._update_mode_checks()
            self._refresh()

    # ---------- Fullscreen auto-hide ----------
    def _spaceChanged_(self, notification):
        self._space_generation += 1
        _log(f"space changed: generation={self._space_generation}")
        self._apply_fullscreen_visibility()

    def _checkFullscreen_(self, timer):
        self._apply_fullscreen_visibility()

    def _restore_after_fullscreen(self):
        """Show the widget again without stealing focus in normal mode."""
        if self.mode == "normal":
            self.window.orderBack_(None)
        else:
            self.window.orderFrontRegardless()

    def _apply_fullscreen_visibility(self):
        fullscreen_window = find_fullscreen_window()

        if fullscreen_window:
            self._fs_missing_since = None
            owner = fullscreen_window.get("kCGWindowOwnerName", "") or "unknown"
            layer = fullscreen_window.get("kCGWindowLayer", "?")
            bounds = fullscreen_window.get("kCGWindowBounds") or {}
            if not self._hidden_by_fs:
                _log(f"hide widget: fullscreen window owner={owner!r} layer={layer} bounds={bounds}")
                self.window.orderOut_(None)
                self._hidden_by_fs = True
                self._hidden_on_space_generation = self._space_generation
                self._logged_same_space_missing = False
            return

        if not self._hidden_by_fs:
            return

        # Quartz can intermittently miss browser/video fullscreen windows.
        # Once hidden inside a fullscreen Space, stay hidden until macOS reports
        # a Space change. Otherwise the widget flickers back over the video.
        if self._space_generation == self._hidden_on_space_generation:
            if not self._logged_same_space_missing:
                _log("fullscreen window missing in the same Space; keep widget hidden")
                self._logged_same_space_missing = True
            return

        now = datetime.now()
        if self._fs_missing_since is None:
            self._fs_missing_since = now
            _log("fullscreen window missing after Space change; waiting before showing widget")
            return

        missing_for = (now - self._fs_missing_since).total_seconds()
        if missing_for >= _FULLSCREEN_RESTORE_GRACE_SECONDS:
            _log(f"show widget: fullscreen window gone after Space change for {missing_for:.1f}s")
            self._restore_after_fullscreen()
            self._hidden_by_fs = False
            self._fs_missing_since = None
            self._hidden_on_space_generation = None
            self._logged_same_space_missing = False

    # ---------- Refresh ----------
    def _tick_(self, timer):
        self._refresh()

    def _refresh(self):
        try:
            today, month, status, daily = compute_now(self.cfg)
        except Exception as e:
            self.lblStatus.setStringValue_("⚠️ Config error")
            self.lblToday.setStringValue_("—")
            self.lblSub.setStringValue_(str(e))
            return

        icon_map = {
            "working": "💼", "lunch": "🍜", "before": "☕",
            "off": "✅", "weekend": "🛌", "holiday": "🏖️",
            "not_yet": "🗓️", "bad_config": "⚠️", "no_workday": "📭",
        }
        text_map = {
            "working": "Working — ticking up 📈",
            "lunch":   "Lunch break (no pay)",
            "before":  "Before work",
            "off":     "Done for today 🎉",
            "weekend": "Weekend",
            "holiday": "Public holiday",
            "not_yet": "Before start date",
            "bad_config": "Config error",
            "no_workday": "No workday this month",
        }
        icon = icon_map.get(status, "💰")
        stxt = text_map.get(status, status)
        mode_hint = {
            "normal":   "💻 normal",
            "floating": "📌 on-top",
            "desktop":  "🏖️ desktop",
        }.get(self.mode, "")

        self.lblStatus.setStringValue_(f"{icon}  {stxt}")
        self.lblToday.setStringValue_(fmt_money(self.cfg, today))
        self.lblSub.setStringValue_(
            f"Month {fmt_money(self.cfg, month)} · "
            f"Daily {fmt_money(self.cfg, daily)}\n"
            f"{mode_hint} · click to open · right-click menu · drag to move"
        )

    # ---------- Actions ----------
    def _open_dashboard(self):
        if os.path.exists(DASHBOARD):
            webbrowser.open(f"file://{DASHBOARD}")

    def _menuOpen_(self, sender):
        self._open_dashboard()

    def _reload_(self, sender):
        self.cfg = load_config()
        self._refresh()

    def _resetPos_(self, sender):
        screen = NSScreen.mainScreen().visibleFrame()
        x = screen.origin.x + 20
        y = screen.origin.y + 20
        self.window.setFrameOrigin_(NSMakePoint(x, y))
        st = load_state()
        st["x"] = x
        st["y"] = y
        save_state(st)

    def _quit_(self, sender):
        NSApp.terminate_(None)


def main():
    app = NSApplication.sharedApplication()
    delegate = WidgetDelegate.alloc().init()
    app.setDelegate_(delegate)
    app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
    app.activateIgnoringOtherApps_(True)
    AppHelper.runEventLoop()


if __name__ == "__main__":
    main()
