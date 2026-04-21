<div align="center">

<img src="./assets/banner.png" alt="PayPulse — 睇住份糧每秒跳動" width="100%">

# 💰 PayPulse

### *睇住份糧每秒跳動*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![HTML](https://img.shields.io/badge/built%20with-vanilla%20HTML-orange)](./index.html)
[![No Backend](https://img.shields.io/badge/backend-none%20%F0%9F%94%92-blue)](./docs/privacy.md)
[![i18n](https://img.shields.io/badge/i18n-EN%20%7C%20%E7%AE%80%E4%B8%AD%20%7C%20%E7%B9%81%E4%B8%AD-red)](#語言--貨幣--地區)
[![Regions](https://img.shields.io/badge/%E5%9C%B0%E5%8D%80-HK%20%7C%20CN%20%7C%20US%20%7C%20UK%20%7C%20SG%20%7C%20JP-purple)](./docs/regions.md)

[🇬🇧 English](./README.md) · [🇨🇳 简体中文](./README.zh-CN.md) · [🇭🇰 繁體中文](./README.zh-HK.md)

[**線上試用**](https://ggnode.github.io/paypulse/) · [**文件**](./docs/) · [**報 Bug**](https://github.com/GGNode/paypulse/issues)

</div>

---

大部分薪金計算器都係填個數、計一次、就算係。PayPulse 唔同，佢係**即時俾你睇住份糧一秒一秒噉跳上去**。

星期五下晝打開嚟，望住個數字由兩點跳到放工，幾解壓㗎。

冇後端、唔使登記、唔需要 build，就係一個 `index.html`，瀏覽器打開就用得。

---

## 截圖預覽

<table>
<tr>
<td align="center" width="33%">
<img src="./assets/home-hero-en.png" alt="首頁 — 秒級跳動"><br>
<b>秒級跳動</b><br>
<sub>大個數字每秒跳，下面係日薪進度條、放工倒數同下個假期。</sub>
</td>
<td align="center" width="33%">
<img src="./assets/home-cards-en.png" alt="今日/本月/年度目標卡片"><br>
<b>本月 & 年度目標</b><br>
<sub>四張卡片——今日到手、本月累計、年度目標、當前進度，實時更新。</sub>
</td>
<td align="center" width="33%">
<img src="./assets/details-chart-en.png" alt="累計收入曲線"><br>
<b>收入走勢圖</b><br>
<sub>手寫 SVG 曲線，冇 Chart.js，冇依賴，就係純數學。</sub>
</td>
</tr>
<tr>
<td align="center">
<img src="./assets/details-financials-en.png" alt="每月財務明細"><br>
<b>每月財務明細</b><br>
<sub>稅前、稅款、強積金、淨到手、資產增長，逐月列清楚。</sub>
</td>
<td align="center">
<img src="./assets/tax-breakdown-en.png" alt="薪俸稅明細"><br>
<b>稅務明細</b><br>
<sub>每一項扣除、每一條免稅額、邊際稅率，仲有 TVC 慳稅試算。</sub>
</td>
<td align="center">
<img src="./assets/settings-providers-en.png" alt="插件化稅務同強積金"><br>
<b>稅 & 強積金插件化</b><br>
<sub>一個下拉菜單，由香港薪俸稅換成大陸個稅，或者自己定稅率表。</sub>
</td>
</tr>
</table>

---

## 快速上手

### 瀏覽器直接開

```bash
git clone https://github.com/GGNode/paypulse.git
cd paypulse
open index.html
```

第一次打開會有個設定嚮導，幾個問題答完就搞掂：

<table>
<tr>
<td align="center" width="33%"><img src="./assets/onboarding-en.png" alt="第一步 — 揀語言"><br><sub>揀語言</sub></td>
<td align="center" width="33%"><img src="./assets/onboarding-region.png" alt="第二步 — 揀地區"><br><sub>揀地區，稅/強積金/假期自動填入</sub></td>
<td align="center" width="33%"><img src="./assets/onboarding-salary.png" alt="第三步 — 填月薪"><br><sub>填月薪同返工日期</sub></td>
</tr>
</table>

### 線上試用

👉 [ggnode.github.io/paypulse](https://ggnode.github.io/paypulse/)

### macOS 桌面部件（可選）

想要個數字掛喺桌面，唔想切瀏覽器窗口嘅話：

```bash
cd desktop
bash setup.sh                     # 一次性安裝，整好 .venv，裝好依賴
./install-autostart.command       # 裝 LaunchAgent，開機自啟
```

詳情睇 [`desktop/README.md`](./desktop/README.md)。

---

## 語言 / 貨幣 / 地區

### 語言

| 代碼 | 語言 | 狀態 |
|------|------|------|
| `en` | English | ✅ 完整 |
| `zh-CN` | 简体中文 | ✅ 完整 |
| `zh-HK` | 繁體中文（香港） | ✅ 完整 |
| 其他 | — | 歡迎 PR，翻譯一個 JS 對象就得 |

<table>
<tr>
<td align="center" width="33%"><img src="./assets/home-hero-en.png" alt="英文介面"><br><sub>English</sub></td>
<td align="center" width="33%"><img src="./assets/home-hero-zh.png" alt="简体中文（香港地區）"><br><sub>简体中文（香港地區）</sub></td>
<td align="center" width="33%"><img src="./assets/home-hero-cn.png" alt="简体中文（中國大陸）"><br><sub>简体中文（中國大陸，CNY）</sub></td>
</tr>
</table>

### 貨幣

`HKD` · `CNY` · `USD` · `EUR` · `JPY` · `GBP` · `SGD` · `AUD`，自訂符號都得。

### 稅務插件

| 提供者 | 涵蓋內容 |
|--------|---------|
| `hk-salaries-tax` | **香港薪俸稅 2025/26** — 累進稅率/標準稅率，個人/已婚/子女/供養父母免稅額，MPF/TVC/住宅按揭扣除，年終花紅，TVC 慳稅試算 |
| `cn-iit` | **中國大陸個人所得稅** — 綜合所得 7 級超額累進，¥60,000 基本減除，全部 7 類專項附加扣除可配置，年終獎單獨計稅/併入綜合所得兩種方式，與五險一金稅前扣除聯動 |
| `simple-brackets` | 通用累進稅率表，自己填區間和稅率，適合任何地方 |
| `flat-rate` | 固定比率，適合自由工作者或外派 |
| `none` | 只顯示稅前，唔做稅務計算 |

<table>
<tr>
<td align="center" width="50%"><img src="./assets/tax-breakdown-en.png" alt="香港薪俸稅明細"><br><sub>香港薪俸稅，含 TVC 慳稅試算</sub></td>
<td align="center" width="50%"><img src="./assets/tax-breakdown-cn.png" alt="中國大陸個稅明細"><br><sub>中國大陸 — 綜合所得，年終獎單獨計稅</sub></td>
</tr>
</table>

想加你所在地區嘅稅務邏輯，大概 100 行代碼。睇 [`docs/tax-providers.md`](./docs/tax-providers.md)。

### 強積金 / 退休金插件

| 提供者 | 涵蓋內容 |
|--------|---------|
| `hk-mpf` | **香港強積金** — 僱員 5% + 僱主 5%，上限 HK$1,500/月 |
| `cn-social-insurance` | **中國大陸五險一金** — 養老/醫療/失業/工傷/生育+公積金，基數上下限同各項比率全部可調 |
| `flat-percent` | 固定比率，美國 401(k) 或自願供款 |
| `none` | 唔扣強積金 |

<p align="center">
  <img src="./assets/settings-wujianyijin-cn.png" alt="五險一金設定" width="70%">
  <br><sub>五險一金 — 基數上下限同各項比率可按城市調整（圖為北京 2025-2026 默認值）</sub>
</p>

### 假期日曆

內置 2026 年完整資料：🇭🇰 香港 · 🇨🇳 中國大陸 · 🇺🇸 美國 · 🇬🇧 英國 · 🇸🇬 新加坡 · 🇯🇵 日本。

大陸部分按國務院通知，**調休上班日**（如 2026-02-14 星期六）正確計為工作日。匯出嘅 JSON 將正式假日同調休日分開放，桌面工具讀取後都保持一致。

---

## macOS 桌面工具

瀏覽器 tab 係幾好，不過有時你就係想望一眼就知，唔想切窗口。

<table>
<tr>
<td width="50%" align="center">
<img src="./assets/widget-desktop.png" alt="macOS 桌面部件"><br>
<b>桌面部件</b><br>
<sub>磨砂玻璃小卡，停喺 Dock 上面。顯示桌面先見到，全螢幕時自動隱藏。Click 打開完整儀表板，右鍵有選項。</sub>
</td>
<td width="50%" align="center">
<img src="./assets/menubar.png" alt="macOS 選單列"><br>
<b>選單列</b><br>
<sub>數字貼在時鐘旁邊，一直都見到。下拉菜單顯示今日/本月/年度匯總，click 一下開完整頁面。</sub>
</td>
</tr>
</table>

兩個工具都係讀同一份 `paypulse-config.json`，喺網頁版設定頁匯出就得。設定有改動，匯出新 JSON 替換，右鍵點「重新載入設定」。

```bash
cd desktop
bash setup.sh
./install-autostart.command    # 可選，裝 LaunchAgent 開機自啟
```

---

## 私隱

PayPulse 唔發任何網絡請求。你嘅薪金資料全部喺瀏覽器嘅 `localStorage` 入面，唔上傳、唔分析、唔統計、唔使登記，可以完全離線用。

整個 app 就係一個 HTML 檔，代碼隨時睇得到。

詳情見 [`docs/privacy.md`](./docs/privacy.md)。

---

## 技術棧

| | |
|---|---|
| **前端** | 原生 HTML/CSS/JS，無框架，無 build |
| **儲存** | 只用 `localStorage` |
| **圖表** | 手寫 SVG |
| **i18n** | 扁平 `I18N` 字典 + `t()` 函式，翻譯一個對象就能加新語言 |
| **稅 / 強積金** | 可插拔 `TAX_PROVIDERS` / `PENSION_PROVIDERS`，提供 `compute`、`renderConfig`、`readConfig` 鉤子 |
| **桌面部件** | Python + PyObjC（macOS only） |
| **選單列** | Python + rumps（macOS only） |

---

## 文件

| | |
|---|---|
| [`docs/regions.md`](./docs/regions.md) | 點樣新增一個地區，含 HK/CN/US/UK/SG/JP 參考實現 |
| [`docs/tax-providers.md`](./docs/tax-providers.md) | 稅務插件 API 同起始模板 |
| [`docs/privacy.md`](./docs/privacy.md) | 私隱政策 |
| [`docs/FAQ.md`](./docs/FAQ.md) | 常見問題 |
| [`CHANGELOG.md`](./CHANGELOG.md) | 更新日誌 |
| [`CONTRIBUTING.md`](./CONTRIBUTING.md) | 貢獻指引 |

---

## 貢獻

幾個易入手嘅方向：

- **加新語言**：翻譯 `index.html` 入面嘅 `I18N` 對象，兩個鐘搞掂。
- **加你所在地區嘅稅務/公積金**：睇 [`docs/tax-providers.md`](./docs/tax-providers.md) 入面嘅 API 同模板。
- **補假期資料**：往 `HOLIDAYS` 對象加你所在地區，調休日加上 `type: 'workday'`。
- **Bug 反映 / 功能建議**：[開個 issue](../../issues) 就得。

詳細規範見 [CONTRIBUTING.md](./CONTRIBUTING.md)。

---

## 路線圖

- [x] 中國大陸個稅（`cn-iit`）+ 五險一金（`cn-social-insurance`）
- [x] 首次使用嚮導
- [x] macOS 桌面部件 + 選單列
- [x] 調休工作日支持
- [ ] 美國聯邦/州稅
- [ ] 新加坡 CPF + IRAS
- [ ] 英國 PAYE + National Insurance
- [ ] 週薪/雙週薪模式
- [ ] 時薪員工模式
- [ ] PWA 可安裝版本
- [ ] Windows/Linux 桌面部件

喺 [issues](../../issues) 投票或提新需求。

---

## 深色 / 淺色

<table>
<tr>
<td align="center" width="50%"><img src="./assets/home-hero-en.png" alt="深色"><br><sub>深色</sub></td>
<td align="center" width="50%"><img src="./assets/home-hero-light-en.png" alt="淺色"><br><sub>淺色</sub></td>
</tr>
</table>

---

## 授權

[MIT](./LICENSE)。隨你點用。如果俾老細發現你望住個數字數秒，唔係我哋嘅責任。

---

<div align="center">

**覺得有用就 Star 一下，真係好有幫助。⭐**

</div>
