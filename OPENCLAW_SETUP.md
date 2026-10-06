# OpenClaw Setup Summary

**Date:** 2026-10-05 ~ 2026-10-06  
**Gateway Version:** 2026.9.8 (stable)  
**Host:** DESKTOP-QRV626P (WSL2, Linux 6.18.40.1-microsoft-standard-WSL2)

---

## Models & Providers

| Model | Provider | Context Window | Max Output | Status |
|-------|----------|----------------|------------|--------|
| qwen3.6-plus | qwen3-8-api-silra-cn | 500,000 | 256,000 | ✅ Active |
| MiniMax-M2.5 | minimax-api-silra-cn | 128,000 | 4,096 | ✅ Default |
| qwen3.8-flash | qwen3-8-api-silra-cn / custom-api-silra-cn | 128,000–500,000 | 4,096–128,000 | ✅ Available |
| deepseek-chat | custom-api-silra-cn | 128,000 | 4,096 | ✅ Available |

**Base URL:** `https://api.silra.cn/v1/`  
**Default Model:** MiniMax-M2.5  
**Session Override:** qwen3.6-plus used for this session

### Secrets Stored
- `CHANNELS_DISCORD_TOKEN_80705F3AA17CFECF` — Discord bot token
- `QWEN3_6_PLUS_API_KEY` — qwen3.6-plus API key
- `SILRA_API_KEY` — silra.cn API key

---

## Channels

### Discord ✅
- **Status:** ON, OK, configured
- **Application ID:** 1543790666570534953
- **Guilds:**
  - `1551832067430424597` — requireMention: true
  - `1546402874639126610` — requireMention: true
- **Tools Profile:** full (all tools enabled)
- **Compaction:** disabled (`"compaction": { "enabled": false }`)

### Tailscale ✅
- **Status:** Enabled (mode: on)
- **Devices connected:**
  - desktop-qrv626p-1 (Linux WSL) — 100.111.61.119
  - chuck-s24-ultra (Android) — 100.127.129.16
  - chuckmac-mini (macOS) — 100.102.20.111
  - desktop-qrv626p (Windows) — 100.76.163.66
- **Dashboard accessible via:** `http://127.0.0.1:18789/` (local), Tailscale IP for remote

---

## Plugins Enabled

| Plugin | Status | Purpose |
|--------|--------|---------|
| discord | ✅ enabled | Discord messaging channel |
| browser | ✅ enabled | Web browsing control |
| memory-wiki | ✅ enabled | Persistent memory wiki vault |
| active-memory | ✅ enabled | Session memory recall |
| duckduckgo | ✅ enabled | Web search |
| summarize | ✅ enabled | Content summarization skill |

## Skills Enabled

| Skill | Status |
|-------|--------|
| summarize | ✅ enabled |

All other skills remain disabled in config.

---

## Configuration Changes Made

### Timeout & Token Limits
- `agents.defaults.timeoutSeconds`: 300 (5 minutes) — prevents idle timeout errors
- `qwen3.6-plus.maxTokens`: 256,000 — prevents truncated responses
- `qwen3.6-plus.contextWindow`: 500,000
- `qwen3.8-flash.contextWindow`: 500,000 (qwen3-8-api-silra-cn provider)

### Compaction
- Disabled globally: `"compaction": { "enabled": false }`

### Secrets Fix
- `custom-api-silra-cn.apiKey`: Changed from `source: "env"` to `source: "store"`
- Resolved degraded secret warning (unresolved count: 0)

---

## System Settings (Windows Side)

### Screen Power Management
- Monitor timeout AC: 2 minutes (set via `powercfg /change monitor-timeout-ac 2`)
- Screen turns off after 2 min of inactivity
- Computer continues running (no sleep/hibernate interference)
- Hibernation disabled: `powercfg /hibernate off`

---

## Known Issues / Notes

1. **GitHub not connected** — `gh auth status` shows not logged in. Browser-based login fails in WSL. Requires manual PAT setup or Control UI connection.
2. **Node service** — Not installed yet (`systemd not installed`). Run `openclaw node install` manually if needed.
3. **Update skipped** — User prefers staying on version 2026.9.8. Update warnings in `openclaw status` are informational only.
4. **Plaintext keys in SQLite** — Auth profile API keys stored as plaintext in SQLite database (hashed, not a security issue).

---

## Quick Commands Reference

```bash
# Check status
openclaw status

# Restart gateway
systemctl --user restart openclaw-gateway

# Check secrets
openclaw secrets audit

# Node service (if needed)
openclaw node install

# GitHub auth (manual)
gh auth login
```

---

## Workspace
- **Path:** `/home/fring1117/.openclaw/workspace`
- **Project:** `openedujustan` — AI question generator platform (Python, Google Forms integration)
- **Config:** `/home/fring1117/.openclaw/openclaw.json`
