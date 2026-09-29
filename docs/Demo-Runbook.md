# 🎯 Sep 7 Live Demo Runbook（後備計劃）

> 準備：Openclaw · 2026-09-04 · 目的：確保會議 demo 萬無一失

## 一、Demo 前檢查清單（會議前一日 + 當日早上）

- [ ] Web UI 運行中（`ss -tlnp | grep 5000`）
- [ ] tunnel 有效（撳一次網址確認 200）
- [ ] `api.silra.cn` 網絡通（curl 測試）
- [ ] Serper key 已入 .env（如果 Chuck 有俾）
- [ ] GitHub Pages 正常（永久網址，唔使 check 都得）
- [ ] 瀏覽器預先開定：Pages 入口、可讀版報告、圖表
- [ ] 準備後備主題 2-3 個（見下面）

## 二、後備主題（萬一主 Demo 主題失敗）

| 優先 | 主題 | 點解好 |
|------|------|--------|
| 1 | 2026 香港企業 AI 採用趨勢 | 本地相關、search 結果豐富 |
| 2 | AI Agent 喺教育領域嘅應用 | 已測試過（9/3 跑過），快 |
| 3 | 年青人 AI 時代技能發展 | 已跑過完整版，穩陣 |

**⚠️ 每個主題預期成本：~10 分鐘 + 少量 API 費用**

## 三、主 Demo 流程（10 分鐘版）

1. **0:00-0:02** — 開場：Bill Gates 警告 → 我哋嘅答案（AI 增強人）
2. **0:02-0:08** — Web UI 輸入主題 → 展示：
   - 研究員真實搜索（畫面會見到搜索進行）
   - Agent 分工（3 個 agent 角色）
   - 文章生成 + 自動儲存
3. **0:08-0:10** — 同時開 GitHub Pages 展示過往成果（報告、圖表、框架比較）

## 四、Live Search 失敗嘅 Fallback

| 情況 | 應對 |
|------|------|
| api.silra.cn timeout | 轉用備用主題（已 cache 嘅文章） |
| DuckDuckGo 被 ban | 等 Serper key / 用預先準備嘅搜索結果截圖 |
| Web UI 死機 | 直接命令行跑 `research_assistant.py`（已驗證可行） |
| 完全斷網 | 展示 GitHub Pages 靜態材料（永久網址唔受影響） |

## 五、預先準備嘅展示材料（已存在）

- ✅ 入口頁：https://chuckchanchi-cpu.github.io/openhing-project/
- ✅ 可讀版報告（連圖）：`notes/03-完整報告_未來20年年青人努力方向_可讀版.html`
- ✅ 4 張圖表：`charts/*.png`
- ✅ 會議材料：`docs/Sep7-會議材料.md`
- ✅ 框架比較：`docs/技術框架比較.md`
- ✅ 道德設計原則：`docs/道德設計原則.md`

## 六、Demo 後嘅跟進（會議即場）

- [ ] 收集與會者意見（應用場景投票）
- [ ] 確認下一步 commitment（人手/資源/時間線）
- [ ] 決定 POC 場景（建議：文書/研究自動化）
- [ ] 記錄會議決定 → 更新項目文件

---
_呢份 runbook 會隨項目更新_
