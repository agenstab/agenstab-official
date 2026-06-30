# Node.js SDK Reference

The AGENSTAB Node.js SDK provides a high-level wrapper around the JSON-RPC WebSocket protocol.

## Installation

```bash
npm install @agenstab/sdk
```

## Quick Start

```javascript
const { BrowserAgent } = require('@agenstab/sdk');

async function main() {
    const agent = await BrowserAgent.init({
        apiKey: 'ak_live_your_api_key',
        sessionConfig: { headless: true }
    });

    await agent.navigate('https://example.com');
    const state = await agent.observe();
    console.log(state.axtree);
    await agent.destroy();
}

main();
```

## Events

`BrowserAgent` extends `EventEmitter`:

| Event | Description |
|---|---|
| `disconnected` | WebSocket connection lost |
| `expired` | Session timed out or terminated |
| `error` | Network or protocol error |

## Methods

| Method | Description | Returns |
|---|---|---|
| `init(config)` | Connect and create session | `BrowserAgent` |
| `navigate(url, waitUntil?)` | Load a URL | `void` |
| `observe(prompt?, maxElements?)` | Extract AXTree | `{ axtree, domHash }` |
| `click(agentId)` | Click element | `void` |
| `type(agentId, text, clearFirst?)` | Type into input | `void` |
| `select(agentId, optionValue)` | Select dropdown | `void` |
| `scroll(direction, amount?, agentId?)` | Scroll | `void` |
| `fillForm(fields)` | Fill multiple inputs | `void` |
| `evaluate(script, timeout?)` | Execute JavaScript | `{ result }` |
| `waitFor(selector, timeout?)` | Wait for element | `void` |
| `screenshot(format?, quality?)` | Capture viewport | `{ base64 }` |
| `get_dom(format?)` | Get page HTML | `{ html }` |
| `clear_interstitials()` | Dismiss cookie banners | `void` |
| `save_state()` | Export session state | `{ stateBlob }` |
| `restore_checkpoint(stateBlob)` | Restore saved state | `void` |
| `get_audit_log()` | Get action history | `{ log }` |
| `pause(reason)` / `resume()` | Human-in-the-loop | `void` |
| `destroy()` | Terminate session | `void` |

## Error Handling

```javascript
try {
    await agent.click('invalid_id');
} catch (err) {
    console.error(err.message); // [AGENSTAB -32006] ELEMENT_NOT_FOUND
}
```
