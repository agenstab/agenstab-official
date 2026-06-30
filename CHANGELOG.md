# Changelog

All notable changes to the AGENSTAB platform will be documented in this file.

## [2.8.0] — 2026-06-30

### Added
- **Blueprint Engine** — Pre-mapped navigation patterns for SAP Fiori, Salesforce Lightning, Workday, and ServiceNow
- **Redaction Proxy** — Automatic PII detection and masking before data leaves the sandbox
- **Session state persistence** — `save_state()` / `restore_checkpoint()` for multi-run workflows
- **Go SDK** — Native Go client with strongly-typed AXTree structures
- **Chrome Extension** — Run agents on any site you're already logged into

### Improved
- AXTree extraction latency reduced to ~18ms (from ~45ms in 2.7.x)
- Token cost per action reduced to ~450 tokens average
- Stealth engine now includes viewport randomization and typing cadence variation
- `fillForm()` method for batch input filling

### Fixed
- Cookie banner detection now handles shadow DOM elements
- WebSocket reconnection logic improved for unstable networks

---

## [2.7.0] — 2026-05-15

### Added
- **VLM Vision fallback** — Automatic screenshot + vision model when AXTree elements are ambiguous
- **Audit logging** — `get_audit_log()` returns full action history with timestamps and durations
- **Human-in-the-loop** — `pause()` / `resume()` for supervised automation

### Improved
- AXTree pruning algorithm now filters non-interactable decoration elements
- Concurrent session limits enforced at the WebSocket layer

---

## [2.6.0] — 2026-04-01

### Added
- **Python SDK** (`agens-tab`) — Asyncio-native client
- **Node.js SDK** (`@agenstab/sdk`) — EventEmitter-based client
- **`observe()` prompt filtering** — Pass a natural language prompt to focus AXTree extraction
- **`clear_interstitials()`** — Automatic cookie banner dismissal

### Improved
- JSON-RPC error codes now include `data.hint` with actionable guidance
- Rate limit headers added to all responses

---

## [2.5.0] — 2026-02-15

### Added
- Initial public API release
- Core methods: `navigate`, `observe`, `click`, `type`, `select`, `scroll`
- WebSocket JSON-RPC 2.0 protocol
- AES-256-GCM envelope encryption for audit logs
