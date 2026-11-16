# 30 — 待辦與追蹤

## 🔔 追蹤節點（Nvidia 議題）
- [x] **11/12**：Nvidia 董事會決定 Jensen 去留 → ✅ 已發生：Jensen 辭任（即時生效），Kress 臨時 CEO，Harvey Jones 首位董事長；Openhing group 已獲 Round 4 報告
- [x] **Round 4 final verdict**？→ ✅ 已做（2026-11-12）：三席一致「觀望 WAIT」（Claude 65% / ai1 60% / Claw 65%）；見底分數 Claude 3/6、ai1 2.3/6、Claw 3/6；報告 `OpenPanel_Trial3_Round4_FinalVerdict_2026-11-12.pdf`
- [ ] **11/17**：Nvidia Q3 業績（$108B 指引過關 =「生意冇事」實證）— **確認見底單一事件 = 業績過關 + 股價同 NVDA 5y CDS 同日改善** → Round 5 = 見底確認審判
  - 追蹤埋：電話會議管治問答（律師封口風險）｜Q4 指引口吻（收緊/附加條件？）｜當日 CDS 方向
  - （11/16 podcast 補）Kress 主持電話會議加追蹤：①客戶擔保/投資承諾有冇收緊 ②合規整改（遙測、kill switch、渠道審查）③中國指引
- [ ] **11/16-17 重新攞 NVDA 5y CDS**（144.5bp 係 11/12 讀數）
- [ ] **FT 11/15「Jensen 考慮回朝」原文核實**（現時只係經 Wikipedia 見到）；跟進 war room 游說 / 員工請願 / 董事會回應
- [ ] **11/9 集體訴訟進展**（預警線「證券欺詐訴訟入稟」已部分觸發）
- [ ] $7.5B（The Information）原文同口徑核實
- [ ] FBI / 獨立調查初步結論（Claude 估 90 日內公開結果機會 ~15%；注意「個人失當 vs 公司共謀」分支）
- [ ] 10-Q 腳注（採購承諾/存貨減值/兜底或有負債/法律程序披露）
- [ ] 臨時 CFO 委任（Claude 建議 2027/1 前）＋ 正式 CEO 招聘進度

## 🚨 預警升級線（Round 4 更新，實戰化未批；11/16 podcast 輸入後修訂）
- NVDA 5y CDS > 150bp（ai1 決定數字：過咗就唔算見底）
- 出口管制正式行動（Megaspeed 線）｜證券欺詐訴訟入稟（**已部分觸發：11/9 集體訴訟**）
- **新增（11/16）：董事會公開回應回朝游說 / Jensen 正式提出回歸**（雙向事件：短期股價可能升、信貸未必跟；「事件落地/管治清晰度」唔加分甚至要扣）
- 風險框架：「個人失當 vs 公司共謀」二分 → **三分**（①個人失當 code of conduct ②公司披露失效 Section 16/證券法 ③公司出口管制失效 BIS/DOJ）
- 舊線繼續：H100 二手價 < $15k｜CoreWeave CDS > 1,500bp｜GPU mortgage spread 每周 >50bp｜ING 拍賣折讓｜存貨週轉 >30 天｜covenant waiver｜德州立法

## ⏸️ HUMAN STOP 未答事項（等 Chuck/Johnson）
1. 預警清單**實戰化**？（指標自動監察 + 異動通知）
2. 三席組合 keep 定加席位？
3. Round 5 幾時開？（建議：11/17 業績後）— **已建議議題：回朝情景（A 外聘 CEO ~50% / B 非執行回歸 ~25% / C 12 個月內返 CEO ~15% / D 法律升級冇可能 ~10%，Claude 粗估）+ 責任三分法**

## 🔧 技術待辦
- [ ] Claude Code 經 relay 直連（選項 B：配 ANTHROPIC_BASE_URL）→ Trial #4 全自動
- [ ] openpanel vault 每 round 自動同步到 ai1 Obsidian（今 round 已手動做）
- [ ] 預警清單自動監察腳本（cron：H100 價 / CoreWeave CDS / 新聞）

## 📁 報告檔案索引
- `OpenPanel_Trial1_Nvidia_Jensen_2026-11-12.pdf`（charts 1-8）
- `OpenPanel_Trial2_3AI_Panel_Nvidia_2026-11-12.pdf`（charts 9-10）
- `OpenPanel_Trial3_Round2_StockBondCascade_2026-11-12.pdf`（charts 11-15）
- `OpenPanel_Trial3_Round3_BottomChecklist_2026-11-12.pdf`（charts 16-18）
- `OpenPanel_Trial3_Round4_FinalVerdict_2026-11-12.pdf`（charts 19-22）
- 位置：mini `~/Desktop/openpanel/nvidia-trial/`

相關：[[03-Logic-Flow]] ｜ [[14-Round4]]
