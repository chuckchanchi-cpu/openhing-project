# 20 — 數據源與核實

## 原則
- 席位**只准用 brief 入面核實數據**，唔可以亂編數字
- 所有數字標明出處；口徑差異要註明（例：-20.3% vs -21.8%）

## Nvidia/Jensen 議題數據源（2026-11-12 核實）

### 股價
- Yahoo Finance chart API（NVDA 日線）：$217.94 (10/27) → $173.73 (11/11)
- 口徑勘誤（Claude 捉到）：間段跌幅 **-20.3%**；傳媒「一個月 -21.8%」係另一個窗口 → 兩個都啱，要標明

### 信貸
- CDS：ICE Data Services / Benzinga / Yahoo — NVDA 5yr 39bp(2025底)→82bp(7/27)→84bp(10/10)→127bp(10月底)→139bp(11月, +76%)
- CoreWeave：債券 79.5¢、孳息 16-17%、CDS 1,240bp(+50%/月)、債務 $2B→$29.8B（CNBC、Bloomberg、MLQ.ai）
- 對比：ORCL 298bp、AVGO +49%、AMZN +44%（qz.com / BigGo Finance）

### 基本面
- Nvidia IR / Bloomberg / FourWeekMBA：Q2 收入 $96.2B(+106%)、DC $89B、Q3 指引 $108B±2%、FY26 $215.9B、存貨 $31.6B(+22%)

### 晶片貶值
- HashrateIndex / ClusterBid / GPUnex / Introl / Forbes / TechFlow：二手 H100 $18-22k、EOL 殘值 $3-5k(10-16%)、轉售回收 60-80%、年更節奏 Hopper'22→Blackwell'24→Rubin'26→Rubin Ultra'27、GPU 貸款 ~3 年 vs 貶值 5-6 年、晶片成本係數據中心 2-4 倍

### 技術指標
- Investing.com / Yahoo / Blockchain.News / StoneX / Gokhshtein：RSI 21.67、%B 0.02、ADX 34.7、成交 306M、put-call skew 年度極值、Nov 11 +5% 至 $177

## 事件時間線
11/08 Jensen 承認婚外情+董事會調查 → 11/09 「間諜」指控+FBI+股價 -4.3% → 11/10 NYT 第二宗緋聞 → 11/11 董事會討論去留+CoreWeave 業績紓緩 → 11/12 WSJ 稱準備炒人+董事會開會 → **11/17 Q3 業績**（分水嶺）

## All-In Podcast 11/14 補充（2026-11-16 Claude/ai1 整合，原文 raw/intel/）
- **新數字**：The Information — 關係「幫助促成」2023 起 ~$7.5B 晶片賣去中國公司（未核實口徑）；Chamath — AI 經濟增長 -50~150bp；「Bank of Nvidia」擔保「幾千億」（Friedberg [00:31:22]）
- **⚠️ 唔引用**：Friedberg「46% 收入來自中國」[00:56:14] — 同財報唔夾，Calacanis 即場質疑，要用就對 10-Q
- **市值口徑**：Chamath 前後不一致（$1T vs $1.5T）；Wikipedia 口徑係由 10/6 高位計 ~$1.5T（11/9）
- **成集冇提 CDS/信貸/債券** — 144.5bp 仍係最新核實讀數（11/12 ICE），11/16-17 要重攞
- **錄影後新事實（Wikipedia 二手，未核原文）**：11/13 Malaysia 查 SpeedMatrix 再出口；11/14 WSJ 新加坡官員疑 Alice 被招募；11/15 FT Jensen 考慮回朝+war room；11/15 Bessent 要「大改組」外來領導、唔使新立法
- **FT 11/15 回朝報道未對原文** — 引用前要核實
