# Writing a Tax Provider

A **tax provider** is a plain JavaScript object that knows how to compute annual tax for a given gross income. PayPulse ships with a few built-in providers and makes it easy to add more.

## The interface

```js
{
  id: 'my-country-tax',                    // unique string id
  name: {                                  // i18n display name
    'en': 'My Country Income Tax',
    'zh-CN': '我国个人所得税',
  },
  defaultConfig: {
    // any user-configurable knobs, e.g. { marriedJointly: false, children: 0 }
  },
  compute(grossAnnual, options) {
    // grossAnnual: annual gross income (number, in local currency)
    // options:     { config, pension, deductions, ... } (see below)
    // must return:
    return {
      tax: Number,         // total annual tax
      net: Number,         // grossAnnual - tax (optionally minus other deductions)
      marginalRate: Number,// effective marginal rate on the next dollar (0..1)
      breakdown: [         // array of line items for display
        { label: 'Gross annual', amount: grossAnnual },
        { label: 'Standard deduction', amount: -xxxx },
        { label: 'Taxable income', amount: yyyy, emphasize: true },
        { label: 'Tax (progressive)', amount: zzzz },
      ],
    };
  },
}
```

## Minimal example — flat rate

```js
'flat-rate': {
  id: 'flat-rate',
  name: { 'en': 'Flat rate' },
  defaultConfig: { ratePercent: 20 },
  compute(gross, { config }) {
    const rate = (config.ratePercent || 0) / 100;
    const tax = gross * rate;
    return {
      tax,
      net: gross - tax,
      marginalRate: rate,
      breakdown: [
        { label: 'Gross annual', amount: gross },
        { label: `Tax (${config.ratePercent}%)`, amount: tax },
      ],
    };
  },
},
```

## Progressive brackets example

```js
'simple-brackets': {
  id: 'simple-brackets',
  name: { 'en': 'Progressive brackets (custom)' },
  defaultConfig: {
    brackets: [
      { upTo: 10000,  rate: 0.00 },
      { upTo: 50000,  rate: 0.10 },
      { upTo: 200000, rate: 0.20 },
      { upTo: null,   rate: 0.30 },  // null = infinity
    ],
    personalAllowance: 10000,
  },
  compute(gross, { config }) {
    const taxable = Math.max(0, gross - config.personalAllowance);
    let tax = 0, last = 0, marginal = 0;
    for (const b of config.brackets) {
      const ceiling = b.upTo === null ? Infinity : b.upTo;
      if (taxable > last) {
        const slice = Math.min(taxable, ceiling) - last;
        tax += slice * b.rate;
        marginal = b.rate;
      }
      last = ceiling;
      if (taxable <= ceiling) break;
    }
    return {
      tax,
      net: gross - tax,
      marginalRate: marginal,
      breakdown: [
        { label: 'Gross', amount: gross },
        { label: 'Personal allowance', amount: -config.personalAllowance },
        { label: 'Taxable', amount: taxable, emphasize: true },
        { label: 'Tax (progressive)', amount: tax },
      ],
    };
  },
},
```

## Registering your provider

Add your object to the `TAX_PROVIDERS` map in `index.html`:

```js
const TAX_PROVIDERS = {
  'none':             { /* ... */ },
  'flat-rate':        { /* ... */ },
  'simple-brackets':  { /* ... */ },
  'hk-salaries-tax':  { /* ... */ },
  'my-country-tax':   { /* your provider */ },
};
```

Then map it as the default for a region in `REGIONS`:

```js
const REGIONS = {
  'MY': {
    name: { 'en': 'Malaysia', 'zh-CN': '马来西亚' },
    currency: 'MYR',
    defaultTaxProvider: 'my-country-tax',
    defaultPensionProvider: 'flat-percent',
  },
  // ...
};
```

## Testing

No test framework required:

1. Open `index.html` in a browser.
2. Settings → Region → select yours.
3. Enter a few known salary values and compare with your country's official calculator.
4. Check edge cases: zero income, very high income, bonus months.

## Guidelines

- **Return numbers in the local currency of the provider** — no conversion.
- **`net` should be what the user gets in hand** — after tax, after pension, after anything the provider handles.
- **Keep progressive brackets in order**, lowest to highest.
- **i18n all user-visible strings** in the `breakdown` labels — use the active locale from `options.locale`.
- **Document your assumptions** with comments (filing status, tax year, etc.).
