#!/usr/bin/env python3
"""
PayPulse · macOS menu bar app 💰
================================
Shows your real-time earnings in the macOS menu bar.
Click the menu bar item to see details or open the full dashboard.

Usage:
  1. bash setup.sh          (one-time, creates .venv with deps)
  2. Double-click menubar.command

Config file: ./paypulse-config.json  (auto-created on first run)

You can also import your web-app data: in the web app go to
Settings → Export, then place the downloaded JSON here as
`paypulse-config.json`.
"""

import json
import os
import sys
import webbrowser
from datetime import date, datetime, timedelta

try:
    import rumps
except ImportError:
    print("❌ Missing 'rumps'. Please run: bash setup.sh")
    sys.exit(1)

# ================= Paths =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "paypulse-config.json")
DASHBOARD = os.path.abspath(os.path.join(BASE_DIR, "..", "index.html"))

# ================= Defaults =================
DEFAULT_CONFIG = {
    "salary": 0,
    "bonusMonths": 0,
    "startDate": "",           # YYYY-MM-DD, empty = from today
    "workStart": "09:00",
    "workEnd":   "18:00",
    "lunchStart": "12:00",
    "lunchEnd":   "13:00",
    "currency": "USD",
    "currencySymbol": "$",
    "fxRate": 1.0,
    "decimals": 2,
    "holidays": [],            # list of "YYYY-MM-DD" — public holidays
    "makeupWorkdays": [],      # list of "YYYY-MM-DD" — weekends turned into
                               # working days (e.g. China 调休). A date in
                               # this list is ALWAYS a workday, even on a
                               # Saturday / Sunday.
}


# ================= Config loading =================
def _flatten_web_export(obj: dict) -> dict:
    """Accept both a raw config dict and a web-app export of form
    {config: {...}, daily: {...}}."""
    if isinstance(obj, dict) and "config" in obj and isinstance(obj["config"], dict):
        cfg = dict(obj["config"])
        # Map currency → symbol if possible
        cur = cfg.get("currency")
        SYM = {
            "HKD": "HK$", "CNY": "¥", "USD": "$", "EUR": "€",
            "JPY": "¥", "GBP": "£", "SGD": "S$", "AUD": "A$",
            "CAD": "C$", "KRW": "₩", "TWD": "NT$", "INR": "₹",
        }
        if cur and "currencySymbol" not in cfg:
            cfg["currencySymbol"] = SYM.get(cur, cur + " ")
        return cfg
    return dict(obj) if isinstance(obj, dict) else {}


def load_config() -> dict:
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                raw = json.load(f)
            flat = _flatten_web_export(raw)
            return {**DEFAULT_CONFIG, **flat}
        except Exception as e:
            print(f"⚠️  Config parse failed: {e}, using defaults.")
            return dict(DEFAULT_CONFIG)
    else:
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
        return dict(DEFAULT_CONFIG)


# ================= Utils =================
def parse_time(s: str):
    h, m = s.split(":")
    return int(h), int(m)


def today_at(h: int, m: int) -> datetime:
    n = datetime.now()
    return n.replace(hour=h, minute=m, second=0, microsecond=0)


def is_work_day(d: date, holiday_set: set, makeup_set: set) -> bool:
    key = d.strftime("%Y-%m-%d")
    if key in makeup_set:
        return True                # 调休上班 — weekend shifted to working day
    if d.weekday() >= 5:
        return False
    return key not in holiday_set


def count_workdays_in_month(year: int, month: int,
                            holiday_set: set, makeup_set: set) -> int:
    if month == 12:
        nxt = date(year + 1, 1, 1)
    else:
        nxt = date(year, month + 1, 1)
    last_day = (nxt - timedelta(days=1)).day
    return sum(1 for d in range(1, last_day + 1)
               if is_work_day(date(year, month, d), holiday_set, makeup_set))


def fmt_money(cfg: dict, amount: float) -> str:
    dec = int(cfg.get("decimals", 2) or 0)
    fx = float(cfg.get("fxRate", 1) or 1)
    sym = cfg.get("currencySymbol") or cfg.get("currency", "") + " "
    v = (float(amount) or 0) * fx
    return f"{sym}{v:,.{dec}f}"


# ================= Core compute =================
def compute_now(cfg: dict):
    """Return (today_earned, month_earned, status, daily_rate)."""
    now = datetime.now()
    today = now.date()

    try:
        ws_h, ws_m = parse_time(cfg["workStart"])
        we_h, we_m = parse_time(cfg["workEnd"])
        ls_h, ls_m = parse_time(cfg["lunchStart"])
        le_h, le_m = parse_time(cfg["lunchEnd"])
    except Exception:
        return 0.0, 0.0, "bad_config", 0

    work_sec = ((we_h * 3600 + we_m * 60) - (ws_h * 3600 + ws_m * 60)
                - ((le_h * 3600 + le_m * 60) - (ls_h * 3600 + ls_m * 60)))
    if work_sec <= 0:
        return 0.0, 0.0, "bad_config", 0

    holiday_set = set(cfg.get("holidays") or [])
    makeup_set = set(cfg.get("makeupWorkdays") or [])
    month_days = count_workdays_in_month(
        today.year, today.month, holiday_set, makeup_set
    )
    if month_days == 0:
        return 0.0, 0.0, "no_workday", 0

    salary = float(cfg.get("salary", 0) or 0)
    daily = salary / month_days
    per_sec = daily / work_sec

    ws = today_at(ws_h, ws_m)
    we = today_at(we_h, we_m)
    ls = today_at(ls_h, ls_m)
    le = today_at(le_h, le_m)

    start_str = cfg.get("startDate") or ""
    if start_str:
        try:
            start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        except Exception:
            start_date = today
    else:
        start_date = today

        if today < start_date:
            return 0.0, 0.0, "not_yet", daily
        if not is_work_day(today, holiday_set, makeup_set):
            status = "weekend" if today.weekday() >= 5 else "holiday"
            month_earned = _month_so_far(
                cfg, today, 0.0, daily, holiday_set, makeup_set, start_date
            )
            return 0.0, month_earned, status, daily

    worked_sec = 0
    if now > ws:
        end = min(now, we)
        morning_end = min(end, ls)
        if morning_end > ws:
            worked_sec += (morning_end - ws).total_seconds()
        if end > le:
            worked_sec += (end - le).total_seconds()

    today_earned = worked_sec * per_sec

    if now < ws:
        status = "before"
    elif ls <= now < le:
        status = "lunch"
    elif now >= we:
        status = "off"
    else:
        status = "working"

        month_earned = _month_so_far(
            cfg, today, today_earned, daily, holiday_set, makeup_set, start_date
        )
        return today_earned, month_earned, status, daily


def _month_so_far(cfg, today, today_earned, daily,
                  holiday_set, makeup_set, start_date):
    month_first = date(today.year, today.month, 1)
    count_start = max(month_first, start_date)
    completed = 0
    cur = count_start
    prev_day = today - timedelta(days=1)
    while cur <= prev_day:
        if is_work_day(cur, holiday_set, makeup_set):
            completed += 1
        cur += timedelta(days=1)
    return completed * daily + today_earned


# ================= UI =================
STATUS_ICONS = {
    "working":    "💼",
    "lunch":      "🍜",
    "before":     "☕",
    "off":        "✅",
    "weekend":    "🛌",
    "holiday":    "🏖️",
    "not_yet":    "🗓️",
    "bad_config": "⚠️",
    "no_workday": "📭",
}
STATUS_LABEL = {
    "working":    "Working — numbers ticking 📈",
    "lunch":      "Lunch break (no pay)",
    "before":     "Before work",
    "off":        "Done for today 🎉",
    "weekend":    "Weekend",
    "holiday":    "Public holiday",
    "not_yet":    "Before start date",
    "bad_config": "Config error",
    "no_workday": "No workday this month",
}


class PayPulseApp(rumps.App):
    def __init__(self):
        super().__init__("💰 —", quit_button=None)
        self.cfg = load_config()
        self.menu = [
            rumps.MenuItem("📊 Open full dashboard", callback=self.open_dashboard),
            rumps.MenuItem("🔄 Reload config",        callback=self.reload_cfg),
            rumps.MenuItem("📁 Open config folder",   callback=self.open_folder),
            None,
            rumps.MenuItem("— details —"),
            None,
            rumps.MenuItem("❌ Quit",                 callback=rumps.quit_application),
        ]
        self._details_item = self.menu["— details —"]
        self._details_item.state = -1
        rumps.Timer(self._tick, 1).start()
        self._tick(None)

    def _tick(self, _sender):
        try:
            today, month, status, daily = compute_now(self.cfg)
        except Exception as e:
            self.title = f"⚠️ {e}"
            return
        icon = STATUS_ICONS.get(status, "💰")
        if status in ("weekend", "holiday", "not_yet", "bad_config", "no_workday"):
            self.title = f"{icon} {STATUS_LABEL.get(status, '')}"
        else:
            self.title = f"{icon} {fmt_money(self.cfg, today)}"
        self._details_item.title = (
            f"Today {fmt_money(self.cfg, today)}  ·  "
            f"Month {fmt_money(self.cfg, month)}  ·  "
            f"Daily {fmt_money(self.cfg, daily)}"
        )

    def open_dashboard(self, _):
        if os.path.exists(DASHBOARD):
            webbrowser.open(f"file://{DASHBOARD}")
        else:
            rumps.alert("Dashboard not found", f"Expected at:\n{DASHBOARD}")

    def reload_cfg(self, _):
        self.cfg = load_config()
        self._tick(None)
        rumps.notification("PayPulse", "Config reloaded", "")

    def open_folder(self, _):
        os.system(f'open "{BASE_DIR}"')


if __name__ == "__main__":
    PayPulseApp().run()
