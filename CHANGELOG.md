# Changelog

All notable changes to PayPulse will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Mainland China tax provider `cn-iit`** — full Individual Income Tax on
  comprehensive income: 7-level progressive annual brackets, basic allowance
  (¥60,000 / yr), all 7 categories of special additional deductions
  (子女教育 / 婴幼儿 / 继续教育 / 住房贷款 / 住房租金 / 赡养老人 / 大病医疗),
  other deductions, charitable donations (30 % cap), and year-end bonus
  taxation with switchable **separate (全年一次性奖金)** vs **combined** method.
- **Mainland China pension provider `cn-social-insurance`** — "五险一金":
  pension / medical / unemployment / work-injury / maternity + housing fund,
  with independent base-range clamps and employee / employer rates, Beijing
  2025 defaults. Employee share is automatically deducted from pre-tax income.
- **调休 make-up workdays** — `HOLIDAYS` entries now accept
  `type: 'workday'` so that weekends shifted to working days (e.g. China's
  `2026-02-14`, `2026-02-28`, `2026-04-26`, `2026-09-27`, `2026-10-11`)
  count as normal workdays while actual public holidays still don't.
- **Pension provider config UI** — `flat-percent` and `cn-social-insurance`
  now expose `renderConfig` / `readConfig` so users can tweak rates and
  bases right from the Settings tab (on par with tax providers).
- **Export JSON** — `holidays` and `makeupWorkdays` are now exported as two
  separate arrays so downstream tooling can tell the difference.
- **Desktop tools** — `menubar.py` and `widget.py` both honour the new
  `makeupWorkdays` list when counting workdays in a month.
- **Docs overhaul** — `README.md` / `README.zh-CN.md` / `README.zh-HK.md` and
  `desktop/README.md` rewritten with a hero banner, a 6-tile feature grid,
  side-by-side region comparison (HK vs. CN), onboarding walkthrough, tax
  engine showcase, macOS widget/menu-bar mockups and dark/light previews —
  ~20 screenshots total, all in `assets/`.

### Changed
- `REGIONS.CN` now uses `cn-iit` / `cn-social-insurance` / `holidayKey: 'CN'`
  out of the box.
- 2026 holiday data populated for HK, CN, US, UK, SG, JP (CN includes the
  full 调休 schedule from the State Council notice).
- macOS desktop widget fullscreen handling is now Space-aware: it keeps hidden
  during browser/video fullscreen even when Quartz temporarily misses the
  fullscreen window, handles localized macOS system owners (e.g. `程序坞`), and
  restores normal-window mode behind the active app instead of jumping to the
  front.

## [1.0.0] — 2026-04-21

### Added
- Real-time salary ticker (updates every second)
- Today / this month / year-to-date / cumulative earnings
- Workday calendar with public holiday support
- Multi-language support: English, 简体中文, 繁體中文
- Multi-currency support: HKD, CNY, USD, EUR, JPY, GBP, SGD, AUD
- Pluggable tax providers: `hk-salaries-tax`, `simple-brackets`, `flat-rate`, `none`
- Pluggable pension providers: `hk-mpf`, `flat-percent`, `none`
- First-run onboarding wizard (5 steps)
- Side income tracking (stock P&L, freelance gigs, etc.)
- Annual goal tracker
- Tax breakdown visualization
- TVC (Tax-Deductible Voluntary Contributions) savings calculator
- JSON import / export
- Dark mode
- macOS desktop widget (Python + PyObjC)
- macOS menu bar app (Python + rumps)
- LaunchAgent-based autostart for the widget
