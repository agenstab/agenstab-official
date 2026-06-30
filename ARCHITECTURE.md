# Architecture Overview

AGENSTAB is a closed-source, cloud-hosted browsing engine. This document describes the **public-facing architecture** — how your agents connect to and interact with the platform.

## System Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     Your Infrastructure                  │
│                                                         │
│  ┌─────────────┐   ┌─────────────┐   ┌──────────────┐ │
│  │ Python Agent │   │ Node Agent  │   │  Go Agent    │ │
│  │ (agens-tab) │   │ (@agenstab/ │   │ (agenstab-go)│ │
│  │             │   │  sdk)       │   │              │ │
│  └──────┬──────┘   └──────┬──────┘   └──────┬───────┘ │
│         │                 │                  │         │
│         └────────────┬────┴──────────────────┘         │
│                      │                                  │
└──────────────────────┼──────────────────────────────────┘
                       │
                WebSocket (wss://)
                JSON-RPC 2.0
                Bearer ak_live_...
                       │
┌──────────────────────┼──────────────────────────────────┐
│                      ▼                                  │
│              AGENSTAB Cloud                             │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │              API Gateway                          │  │
│  │  Authentication · Rate Limiting · Routing         │  │
│  └──────────────────────┬───────────────────────────┘  │
│                         │                               │
│  ┌──────────────────────▼───────────────────────────┐  │
│  │              Session Manager                      │  │
│  │  Session lifecycle · Quota enforcement            │  │
│  └──────────────────────┬───────────────────────────┘  │
│                         │                               │
│  ┌──────────────────────▼───────────────────────────┐  │
│  │              Engine Core                          │  │
│  │                                                   │  │
│  │  ┌────────────┐ ┌────────────┐ ┌──────────────┐  │  │
│  │  │  AXTree    │ │  Stealth   │ │  Blueprint   │  │  │
│  │  │  Extractor │ │  Engine    │ │  Engine      │  │  │
│  │  └────────────┘ └────────────┘ └──────────────┘  │  │
│  │  ┌────────────┐ ┌────────────┐ ┌──────────────┐  │  │
│  │  │  VLM       │ │  Redaction │ │  Observation │  │  │
│  │  │  Grounding │ │  Proxy     │ │  Engine      │  │  │
│  │  └────────────┘ └────────────┘ └──────────────┘  │  │
│  │                                                   │  │
│  │             Sandboxed Chromium Runtime             │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────┐    │
│  │ Encrypted│  │ Audit    │  │ Zero-Retention    │    │
│  │ Storage  │  │ Logging  │  │ Session Cleanup   │    │
│  └──────────┘  └──────────┘  └───────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Connection Flow

1. **Authenticate** — SDK sends API key (`ak_live_...`) in the WebSocket handshake
2. **Create Session** — Engine provisions an isolated Chromium sandbox
3. **Interact** — Agent sends JSON-RPC commands (`navigate`, `observe`, `click`, etc.)
4. **Terminate** — `destroy()` releases all resources; session data is not persisted

## Key Design Principles

### AXTree-First

Every `observe()` call extracts the browser's accessibility tree — the same structure screen readers use. This provides:
- **Semantic stability** — Elements identified by role + name, not CSS selectors
- **Token efficiency** — ~450 tokens per action vs ~14,500 for raw HTML
- **Resilience** — Survives UI redesigns without selector updates

### Zero-Retention

Session data (cookies, localStorage, screenshots) exists only in-memory during the session. After `destroy()`, all session data is purged. Audit logs are encrypted and stored separately.

### Sandboxed Execution

Each session runs in an isolated Chromium instance. Sessions cannot access each other's data, network, or browser state.

## Supported VLM Providers

When AXTree extraction is insufficient (e.g., canvas-heavy apps, image-based UIs), AGENSTAB falls back to vision:

| Provider | Model | Use Case |
|---|---|---|
| OpenAI | GPT-4o | General vision grounding |
| Anthropic | Claude 3.5 Sonnet | Complex reasoning tasks |
| Local | vLLM (self-hosted) | Enterprise / air-gapped deployments |

## Enterprise Deployment

For Enterprise customers, AGENSTAB can be deployed in your own infrastructure:
- Self-hosted engine on your cloud (AWS, GCP, Azure)
- VPC peering for private network access
- Custom VLM provider integration
- BAA for HIPAA-regulated environments

Contact [sales@agenstab.com](mailto:sales@agenstab.com) for enterprise deployment options.
