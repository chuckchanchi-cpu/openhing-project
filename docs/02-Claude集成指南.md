# Claude 集成指南

**更新日期**: 2026-08-27  
**適用**: Claude Max / Claude Pro / Claude API

---

##  你有 Max20 Claude 賬號，點樣加入？

### 方案比較

| 方案 | 適合場景 | 難度 | 成本 |
|------|---------|------|------|
| **方案 1: Claude Code CLI** | 本地開發、腳本 | ⭐⭐ 中等 | 月費已付 |
| **方案 2: OpenClaw + Claude API** | WhatsApp/多平台 | ⭐⭐⭐ 較複雜 | API 按量計費 |
| **方案 3: 手動切換** | 偶爾使用 | ⭐ 簡單 | 月費已付 |

---

##  方案 1: Claude Code CLI (推薦) ⭐

### 什麼是 Claude Code？

Anthropic 官方嘅命令行工具，可以：
- 讀寫文件
- 執行命令
- 搜索代碼
- 自動化任務

### 安裝步驟

```bash
# 1. 安裝 Node.js (如果未裝)
node -v  # 檢查版本

# 2. 安裝 Claude Code
npm install -g @anthropic-ai/claude-code

# 3. 登入
claude login
# → 會打開瀏覽器，用你嘅 Max20 賬號登入

# 4. 測試
claude "你好，測試緊"
```

### 使用方式

```bash
# 對話模式
claude

# 單次命令
claude "幫我分析呢個文件" ./file.txt

# 帶上下文
claude "總結呢個文件夾嘅內容" ./openhing/
```

### 優點
- ✅ 直接用你嘅 Max20 賬號（無額外費用）
- ✅ 官方工具，穩定
- ✅ 可以讀寫文件、執行命令

### 缺點
- ❌ 只能在命令行使用
- ❌ 唔能直接集成到 WhatsApp

---

##  方案 2: OpenClaw + Claude API

### 如果你想讓 OpenClaw (WhatsApp) 都用 Claude

#### 步驟 1: 獲取 API Key

1. 登入 https://console.anthropic.com
2. 用你嘅 Max20 賬號
3. 進入 **API Keys**
4. 點擊 **Create Key**
5. 複製 API Key (開頭係 `sk-ant-...`)

⚠️ **注意**: 
- Claude Pro/Max 賬號**唔一定**包含 API 額度
- API 係**另外計費** ($/token)
- 免費額度可能有限，需綁定信用卡

#### 步驟 2: 配置 OpenClaw

```bash
# 1. 編輯 OpenClaw 配置
nano ~/.openclaw/config.json

# 2. 添加 Claude 模型配置
{
  "models": {
    "claude": {
      "provider": "anthropic",
      "apiKey": "sk-ant-xxxxxxxxxxxxx",
      "model": "claude-opus-4-6-20260518"
    }
  }
}

# 3. 重啟 Gateway
openclaw gateway restart
```

#### 步驟 3: 切換模型

喺 WhatsApp 同我講：
```
/model claude
```

或者用命令：
```bash
openclaw model set claude
```

### 費用參考

| 模型 | 輸入 ($/M tokens) | 輸出 ($/M tokens) |
|------|------------------|------------------|
| **Claude Sonnet 4** | ~$3 | ~$15 |
| **Claude Opus 4.6** | ~$15 | ~$75 |

**例子**: 每日 100 次對話，每次 200 tokens
- 每月約 $30-50 USD (視乎模型)

---

##  方案 3: 手動切換 (最簡單)

### 使用方式

1. **日常用 OpenClaw (WhatsApp)** → Qwen 模型
2. **複雜任務用 Claude Web** → 手動 copy/paste

### 工作流程

```
複雜問題 → 複製去 claude.ai → 獲得答案 → 複製返 WhatsApp
```

### 優點
- ✅ 唔使設定
- ✅ 直接用 Max20 無限額
- ✅ 可以選模型 (Sonnet/Opus)

### 缺點
- ❌ 需要手動切換
- ❌ 無自動化

---

## 🎯 我嘅建議

### 對於 Openhing 項目

**推薦組合**:

| 用途 | 工具 | 原因 |
|------|------|------|
| **日常對話** | OpenClaw (Qwen) | 方便、平 |
| **本地開發** | Claude Code CLI | 用盡 Max20 月費 |
| **複雜分析** | Claude Web | 最高質量 |
| **自動化** | OpenClaw + Qwen | API 便宜 |

### 具體設定

```bash
# 1. 安裝 Claude Code (用你嘅 Max20 賬號)
npm install -g @anthropic-ai/claude-code
claude login

# 2. OpenClaw 繼續用 Qwen (日常)
# 而家已經係 Qwen3.5-Plus，夠用

# 3. 需要時手動切換
/model claude  # 如果設定咗 API
```

---

## 📋 快速檢查清單

- [ ] 確認你嘅 Max20 賬號類型 (Pro? Max? Team?)
- [ ] 檢查 API 額度 (console.anthropic.com)
- [ ] 決定用邊個方案 (CLI / API / 手動)
- [ ] 安裝 Claude Code (如果選方案 1)
- [ ] 測試基本功能

---

## 💡 進階：自動模型路由

如果你想**自動選擇模型**（簡單問題用 Qwen，複雜用 Claude）：

可以設定規則：
```
- 如果消息包含「分析」「研究」「報告」→ 用 Claude
- 其他 → 用 Qwen
```

需要我幫你設定？同我講聲！

---

_有咩問題隨時問！_ 🦀
