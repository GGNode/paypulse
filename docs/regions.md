# Adding a new region

PayPulse ships with sensible defaults for several regions (HK, CN, US, UK, SG,
JP, plus a generic `CUSTOM`). Adding a new one is a ~20-line contribution.

A **region** is a bundle of defaults:
- display language (`locale`)
- currency
- which tax provider to pre-select
- which pension provider to pre-select
- which holiday map to use

Users can still override every one of these from the Settings tab after
onboarding — regions are just friendly starting points.

---

## 1. Edit `index.html`

Open `index.html` and find the `REGIONS` object (search for `const REGIONS`).
Add a new entry. Example for Germany:

```js
const REGIONS = {
  // …existing entries…

  DE: {
    name: { en: 'Germany', 'zh-CN': '德国', 'zh-HK': '德國' },
    locale: 'en',
    currency: 'EUR',
    tax: 'simple-brackets',
    pension: 'flat-percent',
    holidayKey: 'DE',
    taxConfig: {
      currency: 'EUR',
      brackets: [
        // [upper-bound-exclusive, rate]  — last entry must be Infinity
        [11604, 0],
        [17005, 0.14],
        [66760, 0.42],
        [277825, 0.42],
        [Infinity, 0.45],
      ],
      allowance: 11604,
    },
    pensionConfig: { percent: 9.3 },   // employee share of statutory pension
  },
};
```

Key fields:

| Field | Meaning |
| --- | --- |
| `name` | Display name per locale. Fall back order is current locale → English → any key. |
| `locale` | One of `en`, `zh-CN`, `zh-HK`. Suggests the display language on first visit. |
| `currency` | Default currency code. Must be a key in the top-level `CURRENCIES` map. If yours is missing, add it (symbol + decimals). |
| `tax` | ID of a tax provider. Built-ins: `none`, `flat-rate`, `simple-brackets`, `hk-salaries-tax`, `cn-iit`. See [`tax-providers.md`](tax-providers.md). |
| `pension` | ID of a pension provider. Built-ins: `none`, `flat-percent`, `hk-mpf`, `cn-social-insurance`. |
| `holidayKey` | Which entry in `HOLIDAYS` to use. Use `CUSTOM` if you don't ship holiday data (users can still add dates manually). |
| `taxConfig` | Initial payload stored in `STATE.config.taxConfig`. Shape depends on the chosen tax provider. |
| `pensionConfig` | Same idea for the pension provider. |

## 2. Holidays (optional but nice)

If you want public holidays filled in automatically, add an entry to the
`HOLIDAYS` object:

```js
const HOLIDAYS = {
  // …existing regions…

  DE: {
    '2026-01-01': { en: 'New Year', 'zh-CN': '新年',   'zh-HK': '新年' },
    '2026-04-03': { en: 'Good Friday', 'zh-CN': '耶稣受难日', 'zh-HK': '耶穌受難日' },
    // …
  },
};
```

Each date maps to a localized-name record. At minimum include `en`; other
locales fall back to English if missing.

### Make-up working days (调休)

Some regions (most notably Mainland China) shift weekends into working days
in exchange for longer public-holiday stretches. Express this by marking the
entry with `type: 'workday'`:

```js
'2026-04-26': {
  type: 'workday',
  en: 'Labour Day make-up workday',
  'zh-CN': '劳动节调休上班',
},
```

Rules:
- An entry without `type` (or `type: 'holiday'`) counts as a **public
  holiday** — salary still accrues, but no work is done.
- An entry with `type: 'workday'` **always** counts as a working day, even
  if it falls on a Saturday or Sunday.
- Make-up workdays are excluded from the "next holiday" countdown.

Prefer official government sources for the dates. A link in your PR
description is very welcome.

## 3. Add the label(s) to the language files (optional)

If your region introduces new terminology (e.g. a regionally specific tax
line), add keys to the `I18N` dictionary. Otherwise English is fine by
default — we always accept Markdown PRs to translate later.

## 4. Test

1. Open `index.html` in a browser.
2. Clear existing data (Settings → Clear all data) to re-trigger the wizard,
   or just pick your region from the top-right dropdown.
3. Confirm the defaults look sensible and that the tax/pension numbers are in
   the right ballpark.

## 5. Submit a pull request

Include in the description:
- Region code and name
- Sources for tax brackets, allowances, and pension rates (links)
- Year of validity (tax years, e.g. "2024 / 2025")
- How you tested

One region per PR, please — that makes reviewing and merging fast.

---

## Notes & tips

- **Don't hard-code personal data.** Never submit a region that hints at a
  specific person's salary, start date, employer, etc. The whole project stays
  "your data, your device".
- **Keep tax logic conservative.** PayPulse is a *visualization*, not an
  accounting tool. When a region has two or more tax methods (e.g. standard
  rate vs progressive in HK), either pick the more common one as the default
  or write a dedicated provider (see
  [`tax-providers.md`](tax-providers.md) for the interface).
- **Holidays drift every year.** Clearly mark which year your holiday map
  covers, and add a code comment pointing to the official source.
- **Pension is optional.** If a region has no mandatory retirement deduction,
  set `pension: 'none'`.

---

## Example: Mainland China 🇨🇳 (reference implementation)

PayPulse ships a full Mainland-China bundle out of the box:

- **Holidays** — 2026 国务院办公厅《关于 2026 年部分节假日安排的通知》including
  6 public-holiday clusters **and** the corresponding 调休 make-up workdays
  (Spring Festival 2/14 + 2/28, Labour Day 4/26, National Day 9/27 + 10/11).
- **Tax provider `cn-iit`** — Individual Income Tax on comprehensive income:
  - 7-level annual progressive table with quick-deduction constants.
  - Basic allowance ¥60,000/year auto-deducted.
  - Full list of special additional deductions (专项附加扣除):
    `子女教育`, `3 岁以下婴幼儿`, `学历继续教育`, `职业资格`, `首套房贷`,
    `住房租金` (tier-1/2/3), `赡养老人`, `大病医疗` (15k floor, 80k cap).
  - Other deductions + charitable donations (capped at 30 % of taxable).
  - Year-end-bonus: choose **separate** (全年一次性奖金, monthly rate table)
    or **combined** with comprehensive income.
- **Pension provider `cn-social-insurance`** — "五险一金":
  - 6 contribution rates per side (employee + employer).
  - Independent base-range clamps for social-insurance vs housing fund.
  - Defaults mirror Beijing 2025 rates; edit for your own city.
  - Employee share automatically feeds into the IIT pre-tax deduction.

The whole bundle is derived from the config you pick in **Settings**, so no
personal data is baked in. When a new year's holiday schedule or tax change
is published, updating a single `HOLIDAYS` / provider block is enough.

---

Thanks for making PayPulse useful for more people! 🎉
