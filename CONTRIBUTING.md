# Contributing to PayPulse

PayPulse is a zero-dependency, single-file web app. There's no build tool, no framework version to pin, no `npm install`. You edit HTML, reload the browser, see the result. That makes it pretty easy to contribute to.

## 🌐 Adding a language

1. Open `index.html`.
2. Find the `const I18N = {` block near the top of the `<script>` section.
3. Copy the `'en'` block and rename the key to your locale code (e.g. `'fr'`, `'ja'`, `'de'`).
4. Translate each value. Leave the keys unchanged.
5. Add your language to the language selector in the header (look for `<select id="lang">`).

Test by switching to your language in the UI — every visible string should change.

## 🏛️ Adding tax logic for a new country

1. Open `index.html` and find the `const TAX_PROVIDERS = {` block.
2. Add a new entry:

```js
'my-country-tax': {
  name: {
    'en': 'My Country Income Tax',
    'zh-CN': '我国个人所得税',
  },
  defaultConfig: {
    // Any user-configurable fields, e.g. marital status, allowances
  },
  compute(grossAnnual, options) {
    // Return { tax, net, breakdown: [{label, amount, note}] }
    // tax = total annual tax
    // net = grossAnnual - tax
    // breakdown = array of line items for display
    return { tax: 0, net: grossAnnual, breakdown: [] };
  },
},
```

3. Add your provider to the region → provider mapping in `REGIONS`.
4. Add relevant `i18n` strings for any UI labels you introduce.

See [`docs/tax-providers.md`](./docs/tax-providers.md) for a worked example.

## 📅 Adding public holidays

1. Find `const HOLIDAYS = {` in `index.html`.
2. Add or extend an entry keyed by ISO country code:

```js
'JP': {
  '2026-01-01': { 'en': "New Year's Day", 'ja': '元日' },
  '2026-01-12': { 'en': 'Coming of Age Day', 'ja': '成人の日' },
  // ...
},
```

## 💼 Adding a pension/retirement provider

Edit `const PENSION_PROVIDERS = {` and follow the same pattern as `TAX_PROVIDERS`.

Return shape:

```js
{
  employee: Number,       // monthly employee contribution
  employer: Number,       // monthly employer contribution (goes to user's asset)
  taxDeductible: Number,  // annual amount that reduces taxable income
}
```

## 🎨 UI / theme contributions

Themes live in CSS variables at the top of the `<style>` block. Add a new theme:

```css
[data-theme="ocean"] {
  --bg: #0a2540;
  --fg: #e6f1ff;
  /* ... */
}
```

Then register it in the theme dropdown.

## 🐛 Bug reports

Please include:
- Browser + version
- Language / region settings
- Steps to reproduce
- Expected vs actual behaviour
- Screenshot (if visual)

## 💡 Feature requests

Open an issue with the `enhancement` label. Explain the use case — "I want to see X because Y" is more useful than "add feature X".

## 🧪 Testing your changes

No test framework. Just:
1. Open `index.html` in a browser.
2. Hard-reload (`Cmd+Shift+R` / `Ctrl+Shift+R`).
3. Walk through the onboarding wizard.
4. Try edge cases: holidays, weekends, year boundaries.

## 📝 Commit style

```
feat(i18n): add French translation
fix(tax): correct HK marginal rate for bonus
docs: update quick start section
```

## 🙏 Code of Conduct

Be kind. We're all just trying to make watching our paychecks more fun.
