# Frequently Asked Questions

## Is my salary data sent anywhere?

**No.** PayPulse makes zero network requests. Everything is stored in your browser's `localStorage` and never leaves your device. See the [privacy policy](./privacy.md).

## My country's tax isn't supported — what do I do?

Three options:

1. **Use `simple-brackets`** — define your country's brackets manually in Settings. Works for any country with progressive tax.
2. **Use `flat-rate`** — good approximation if you're in a simple tax regime or a freelancer.
3. **Contribute a provider** — see [`tax-providers.md`](./tax-providers.md). It's ~50 lines of JavaScript.

## Can I use PayPulse offline?

Yes — 100%. Once the page is loaded, it works without internet. You can also save `index.html` anywhere on your disk and open it with File → Open.

## How accurate is the real-time ticker?

The ticker assumes linear earning: `hourly_rate × seconds_elapsed_this_shift`. It accounts for:
- Lunch break (no accrual)
- Weekends, holidays, marked sick days (no accrual)
- Extra-work days you mark manually (adds extra pay)

For salaried employees this matches your payslip at the end of the month. For hourly/gig workers, the linearity assumption may not apply.

## My salary changed mid-year. What do I do?

Currently PayPulse supports one monthly salary at a time. Workarounds:
- Change it in Settings when your raise kicks in. Past months will use the new rate unless you export → edit JSON → import.
- Upvote [issue #todo](../../issues) for multi-period salary support.

## I have bi-weekly / weekly pay, not monthly.

Not yet supported. Tracked in the roadmap. PRs welcome.

## Does the macOS widget cost CPU / battery?

Minimal. It updates once per second, does a tiny arithmetic calculation, and redraws two text labels. Actual CPU usage: < 0.1%.

## Will this work on Windows / Linux?

The **web app** works on any OS with a modern browser. The **desktop widget and menu bar app** are macOS-only (they use PyObjC / rumps). Community ports to Windows (Win32 / WinUI) or Linux (GTK) are welcome.

## Why no native app?

Because a single HTML file beats a 200MB Electron app every time. If you miss the "app feel", open in a browser and use "Add to Dock / Home Screen" as a PWA shortcut.

## Can I change currency after first setup?

Yes. Settings → Currency. All existing amounts are interpreted as the new currency (no auto-conversion). Use the optional exchange rate field if you want to convert.

## What happens at year boundary?

Everything rolls over correctly: past-year data stays in the history, the "YTD" counter resets on Jan 1, holidays for the new year are loaded (if the `HOLIDAYS` object has them).

If the new year's holidays aren't in the codebase yet, you'll see weekdays treated as workdays. Add them yourself (Settings → Holidays) or submit a PR.

## How do I back up my data?

Settings → "Export data" gives you a JSON file. Keep it safe. Import with "Import data" on a new device.

## I found a bug / have a feature idea

[Open an issue](../../issues) — we read everything.
