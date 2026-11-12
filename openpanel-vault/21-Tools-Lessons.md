# 21 — 工具與教訓（踩過嘅坑）

## MRC（VNC）驅動 ai1 — vncdotool 教訓
- **key 名必須細階**：`key return` ✅ / `key Return` ❌（大寫 → `ord() expected a character` 爆炸）
- `click` 前要 `move X Y`，組合命令要 `pause`
- 打字淨係穩打 **ASCII**（中文打唔到）；長文用 `typefile` 分 chunk（~220 字符）
- **Enter 喺 chat 輸入框 = 發送**：typefile 檔案千祈唔好有換行
- taskbar icon 位置會因新視窗而移位 → click 前要重新對位（Round 3 brief 曾打咗去 PowerShell）
- PowerShell 一招：`Invoke-Expression ((Get-History -Count 1).CommandLine -replace '--local','')` 改寫重跑上一條命令
- ai1 OpenClaw 有 Gateway 跑緊時 `--local` 會拒絕 → 去掉先用到
- Ctrl+Home 會跳到成個對話最頂（要逐頁搵）；Ctrl+End 落尾

## 傳檔去 ai1
- 正路：GitHub repo push → ai1 PowerShell `Invoke-WebRequest` download zip → `Expand-Archive`（中文檔名 OK，Windows tar 會跳過中文名）
- VNC typefile 打唔到中文 → 中文內容必須經文件傳遞

## 圖表 / PDF
- matplotlib：中文字體用 **Arial Unicode MS**；emoji 會 missing glyph → 用文字代替
- 文字入面 `$` 會被當 mathtext → 用 `\$` escape
- 報告風格（Chuck 要求）：**圖多字少**，結論卡 + 儀表板 + 對比圖

## Model 路由
- Claude Code 直連 api.anthropic.com = 403（香港區）→ 要經 ai1 機（Claude.Ai2-HK relay）
- Claude desktop「Opus 5.5 High」= Seat A；ai1 OpenClaw qwen3.8-flash = Seat C

## Session 規則（Johnson 指定）
唔同 project 唔同 session/label（`openpanel-*`），續談 reuse session key 記得立場
