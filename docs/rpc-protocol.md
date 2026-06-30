# WebSocket RPC Protocol Reference

AGENSTAB uses **JSON-RPC 2.0** over WebSocket for all browser communication.

## Connection

```
Endpoint: wss://api.agenstab.com/v1/session
Authorization: Bearer ak_live_...
```

### Handshake

```json
// Client sends after WebSocket opens:
{
  "jsonrpc": "2.0",
  "method": "createSession",
  "params": {
    "config": {
      "headless": true,
      "viewport": { "width": 1920, "height": 1080 },
      "userAgent": "custom-agent-string"
    }
  },
  "id": 1
}

// Server responds:
{
  "jsonrpc": "2.0",
  "result": {
    "session_id": "ses_a1b2c3d4e5f6",
    "expires_at": "2026-06-30T14:00:00Z"
  },
  "id": 1
}
```

## Methods

### Navigation

#### `navigate`

Load a URL in the browser.

```json
{
  "method": "navigate",
  "params": {
    "url": "https://example.com",
    "waitUntil": "networkidle"  // "load" | "domcontentloaded" | "networkidle"
  }
}
```

**Response:**
```json
{
  "result": {
    "url": "https://example.com",
    "title": "Example Domain",
    "status": 200
  }
}
```

---

### Observation

#### `observe`

Extract the Accessibility Tree from the current page.

```json
{
  "method": "observe",
  "params": {
    "prompt": "Find the login form",  // Optional: filter by prompt
    "maxElements": 50                  // Optional: limit results
  }
}
```

**Response:**
```json
{
  "result": {
    "axtree": [
      {
        "agent_id": "a_1",
        "role": "textbox",
        "name": "Email Address",
        "value": "",
        "bounds": [100, 200, 300, 40],
        "interactable": true,
        "focused": false
      },
      {
        "agent_id": "a_2",
        "role": "textbox",
        "name": "Password",
        "value": "",
        "bounds": [100, 260, 300, 40],
        "interactable": true,
        "focused": false
      },
      {
        "agent_id": "a_3",
        "role": "button",
        "name": "Sign In",
        "bounds": [100, 320, 300, 48],
        "interactable": true
      }
    ],
    "dom_hash": "d4e5f6a7b8c9",
    "url": "https://example.com/login",
    "title": "Sign In"
  }
}
```

---

### Actions

#### `click`

Click an element by its `agent_id`.

```json
{
  "method": "click",
  "params": {
    "agentId": "a_3"
  }
}
```

#### `type`

Type text into an input field.

```json
{
  "method": "type",
  "params": {
    "agentId": "a_1",
    "text": "user@example.com",
    "clearFirst": true
  }
}
```

#### `select`

Choose an option from a `<select>` dropdown.

```json
{
  "method": "select",
  "params": {
    "agentId": "a_5",
    "optionValue": "option_2"
  }
}
```

#### `scroll`

Scroll the page or a specific container.

```json
{
  "method": "scroll",
  "params": {
    "direction": "down",   // "up" | "down" | "left" | "right"
    "amount": 500,         // pixels (optional)
    "agentId": "a_10"      // specific container (optional)
  }
}
```

#### `fillForm`

Fill multiple fields in a single call.

```json
{
  "method": "fillForm",
  "params": {
    "fields": {
      "a_1": "user@example.com",
      "a_2": "secure_password",
      "a_4": "John Smith"
    }
  }
}
```

---

### Page Inspection

#### `screenshot`

Capture the current viewport.

```json
{
  "method": "screenshot",
  "params": {
    "format": "png",   // "png" | "jpeg"
    "quality": 80       // 0-100 (jpeg only)
  }
}
```

**Response:**
```json
{
  "result": {
    "base64": "iVBORw0KGgoAAAANSUhEUg..."
  }
}
```

#### `get_dom`

Get the page HTML.

```json
{
  "method": "get_dom",
  "params": {
    "format": "clean"  // "clean" (stripped) | "raw" (full)
  }
}
```

#### `evaluate`

Execute JavaScript in the browser context.

```json
{
  "method": "evaluate",
  "params": {
    "script": "document.title",
    "timeout": 5000
  }
}
```

**Response:**
```json
{
  "result": {
    "result": "Example Domain"
  }
}
```

#### `waitFor`

Wait for a CSS selector to appear in the DOM.

```json
{
  "method": "waitFor",
  "params": {
    "selector": "#success-message",
    "timeout": 10000
  }
}
```

---

### Session Management

#### `clear_interstitials`

Automatically close cookie consent banners and popups.

```json
{ "method": "clear_interstitials" }
```

#### `save_state`

Export the current session state (cookies + localStorage).

```json
{ "method": "save_state" }
```

**Response:**
```json
{
  "result": {
    "state_blob": "eyJjb29raWVzIjpb..."
  }
}
```

#### `restore_checkpoint`

Restore a previously saved session state.

```json
{
  "method": "restore_checkpoint",
  "params": {
    "stateBlob": "eyJjb29raWVzIjpb..."
  }
}
```

#### `get_audit_log`

Get the complete action history for the current session.

```json
{ "method": "get_audit_log" }
```

**Response:**
```json
{
  "result": {
    "log": [
      { "ts": "2026-06-30T12:00:01Z", "method": "navigate", "params": {"url": "..."}, "duration_ms": 1200 },
      { "ts": "2026-06-30T12:00:03Z", "method": "observe", "result_count": 12, "duration_ms": 18 },
      { "ts": "2026-06-30T12:00:04Z", "method": "click", "params": {"agentId": "a_3"}, "duration_ms": 45 }
    ]
  }
}
```

#### `pause` / `resume`

Human-in-the-loop control.

```json
{ "method": "pause", "params": { "reason": "Awaiting human verification" } }
```

```json
{ "method": "resume" }
```

#### `destroy`

Terminate the session and release all resources.

```json
{ "method": "destroy" }
```

---

## Error Codes

| Code | Name | Description |
|---|---|---|
| -32600 | `INVALID_REQUEST` | Malformed JSON-RPC |
| -32601 | `METHOD_NOT_FOUND` | Unknown method name |
| -32602 | `INVALID_PARAMS` | Missing or invalid parameters |
| -32603 | `INTERNAL_ERROR` | Server-side error |
| -32001 | `SESSION_NOT_FOUND` | Invalid session ID |
| -32002 | `SESSION_EXPIRED` | Session timed out |
| -32003 | `ELEMENT_NOT_FOUND` | `agent_id` not in current AXTree |
| -32004 | `NAVIGATION_FAILED` | URL failed to load |
| -32005 | `TIMEOUT` | Operation exceeded timeout |
| -32006 | `RATE_LIMIT_EXCEEDED` | Too many requests |
| -32007 | `QUOTA_EXCEEDED` | Plan session-minutes exhausted |
| -32008 | `UNAUTHORIZED` | Invalid or expired API key |

**Error response format:**
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32003,
    "message": "ELEMENT_NOT_FOUND",
    "data": { "agentId": "a_999", "hint": "Element may have been removed after a page navigation." }
  },
  "id": 5
}
```

---

## Rate Limits

| Tier | Requests/sec | Concurrent Sessions |
|---|---|---|
| Free | 5 | 1 |
| Developer | 20 | 5 |
| Builder | 50 | 10 |
| Team | 100 | 20 |
| Enterprise | Custom | Custom |

Rate limit headers are returned on every response:
```
X-RateLimit-Limit: 20
X-RateLimit-Remaining: 18
X-RateLimit-Reset: 1719748800
```
