# OpenClaw 架構與 Token 計算

**更新日期**: 2026-08-27  
**作者**: Claw 🦀

---

##  我點樣連接 LLM？

### 架構圖

```
WhatsApp → OpenClaw Gateway → Agent → LLM API → 回覆
                                 ↓
                            本地記憶/文件
```

### 連接方式

**我係通過 API 連接 LLM**，具體流程：

1. **用戶發送消息** (WhatsApp/Telegram/ Discord 等)
2. **OpenClaw Gateway 接收** → 路由到對應 Agent
3. **Agent 處理** → 讀取上下文、記憶、文件
4. **調用 LLM API** → 發送 prompt 到模型服務商
5. **接收回覆** → 格式化後發送返給用戶

### 目前使用的模型

| 項目 | 詳情 |
|------|------|
| **當前模型** | Qwen 3.5 Plus (`custom-silra-cn-qwen3.5-plus/qwen3.5-plus`) |
| **服務商** | Silra Cloud (第三方 API 聚合) |
| **連接方式** | HTTP API |
| **認證** | API Key (環境變量) |

### 支持的平台

OpenClaw 可以連接多個 LLM 服務商：

| 服務商 | API 類型 | 費用 |
|--------|---------|------|
| **Silra Cloud** | 聚合 API (Qwen, DeepSeek 等) | 按 Token |
| **Anthropic** | Claude API | 按 Token |
| **OpenAI** | GPT API | 按 Token |
| **本地部署** | Ollama, vLLM 等 | 免費 (硬件成本) |

---

##  Token 如何計算？

### 什麼是 Token？

Token 係 LLM 處理文字嘅基本單位。

**英文**:
- 1 Token ≈ 4 個字符
- 1000 Tokens ≈ 750 單詞

**中文**:
- 1 個中文字 ≈ 1-2 Tokens
- 視乎模型而異

### Token 計算方式

```
總 Token = 輸入 Token + 輸出 Token
```

| 部分 | 說明 | 計費 |
|------|------|------|
| **輸入 Token** | 你發送嘅消息 + 系統提示 + 上下文 | 較便宜 |
| **輸出 Token** | AI 生成嘅回覆 | 較貴 (通常 3-5 倍) |

### 實際例子

**你發送**: 「你好，今日天氣點？」 (10 中文字)
- 輸入 Token: ~15 tokens

**我回覆**: 「你好！今日香港天氣晴朗，氣溫 28-32 度。」 (25 中文字)
- 輸出 Token: ~35 tokens

**總計**: 50 tokens

### 價格參考 (2026 年)

| 模型 | 輸入 ($/M tokens) | 輸出 ($/M tokens) |
|------|------------------|------------------|
| **Qwen3.8-Flash** | ¥1 (~$1.4) | ¥3 (~$4.2) |
| **Qwen3.5-Plus** | ~¥5 | ~¥15 |
| **Claude Opus 4.6** | ~$15 | ~$75 |
| **Claude Max** | 月費制 (無限制) | 月費制 |

### 如何減少 Token 使用？

1. **精簡提示詞** - 唔好太長太複雜
2. **關閉不必要功能** - 例如 reasoning mode
3. **限制回覆長度** - 設定 max_tokens
4. **本地緩存** - 重複問題用本地答案
5. **選擇合適模型** - 簡單任務用 Flash，複雜用 Plus

---

##  成本優化建議

### 對於 Openhing 項目

| 場景 | 推薦模型 | 原因 |
|------|---------|------|
| **日常對話** | Qwen3.8-Flash | 平、快、夠用 |
| **研究分析** | Qwen3.5-Plus | 平衡性價比 |
| **重要文檔** | Claude | 最高質量 |
| **大量實驗** | Qwen3.8-Flash | 成本最低 |

### 預估每月成本

假設每日 100 次對話，每次平均 200 tokens：

```
每日：100 × 200 = 20,000 tokens
每月：20,000 × 30 = 600,000 tokens

Qwen3.8-Flash: 600K × ¥2/1M = ¥1.2 (~$1.7 HKD)
Qwen3.5-Plus:  600K × ¥10/1M = ¥6 (~$8.5 HKD)
Claude Opus:   600K × $50/1M = $30 USD (~$234 HKD)
```

**結論**: Qwen Flash 係探索階段嘅最佳選擇！

---

_待續：Claude 集成指南_
