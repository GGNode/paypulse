# Privacy Policy

**Last updated: 2026-04-21**

## TL;DR

PayPulse runs **entirely in your browser**. It makes **zero network requests**. None of your data ever leaves your device.

## What data does PayPulse handle?

When you use PayPulse, it stores the following on **your device only**, inside your browser's `localStorage`:

- Monthly salary amount
- Working hours (e.g. 9:00 – 18:00 with 1h lunch)
- Start date (when you began this job)
- Year-end bonus months
- Language, currency, region, tax provider, pension provider preferences
- Theme preference (light / dark)
- Daily override records (sick leave, extra work days, stock P&L notes)
- Annual income goal

That's it. There is no cloud, no account, no sync.

## What does PayPulse NOT do?

- ❌ No analytics (no Google Analytics, Plausible, Mixpanel, nothing)
- ❌ No telemetry — we don't know you exist
- ❌ No ads, no trackers, no pixel beacons
- ❌ No server API calls
- ❌ No user accounts
- ❌ No cookies except what `localStorage` technically is (browser-only key/value store)
- ❌ No external fonts (all rendering uses your system fonts)
- ❌ No external scripts or frameworks loaded from CDN

You can verify this yourself:
1. Open `index.html` in a browser
2. Open DevTools → Network tab
3. Reload the page
4. **You will see zero requests after the initial page load.**

## Sharing / exporting data

You can manually export your data as JSON via the **Settings → Export** button, and import it elsewhere. That's the only time your data "moves" — and only by your own hand.

## The macOS desktop tools

The optional `desktop/` tools (widget + menu bar app) are also fully offline. They read the same `paypulse-config.json` file locally and never make any network requests.

## Deleting your data

Two ways:
1. **In-app:** Settings → "Clear all data"
2. **Manual:** In your browser, open DevTools → Application → Local Storage → delete the `paypulse` key

For the desktop tools: delete `~/Documents/paypulse/desktop/paypulse-config.json` and `~/Documents/paypulse/desktop/.widget_state.json`.

## Contact

Open an [issue](../../issues) if you have any privacy questions.
