# Python SDK Reference

The AGENSTAB Python SDK is an asynchronous, asyncio-native client for interacting with the JSON-RPC WebSocket API.

## Installation

```bash
pip install agens-tab
```

## Quick Start

```python
import asyncio
from agens_tab import BrowserAgent

async def main():
    agent = await BrowserAgent.init(
        api_key="ak_live_your_api_key",
        session_config={"headless": True}
    )

    await agent.navigate("https://example.com")
    state = await agent.observe()
    print(state["axtree"])
    await agent.destroy()

asyncio.run(main())
```

## Methods

| Method | Description | Returns |
|---|---|---|
| `init(api_key, endpoint?, session_config?)` | Connect and create session | `BrowserAgent` |
| `navigate(url, wait_until?)` | Load a URL | `None` |
| `observe(prompt?, max_elements?)` | Extract AXTree | `{"axtree": list, "dom_hash": str}` |
| `click(agent_id)` | Click element | `None` |
| `type(agent_id, text, clear_first?)` | Type into input | `None` |
| `select(agent_id, option_value)` | Select dropdown option | `None` |
| `scroll(direction, amount?, agent_id?)` | Scroll page/container | `None` |
| `fill_form(fields)` | Fill multiple inputs | `None` |
| `evaluate(script, timeout?)` | Execute JavaScript | `{"result": any}` |
| `wait_for(selector, timeout?)` | Wait for element | `None` |
| `screenshot(format?, quality?)` | Capture viewport | `{"base64": str}` |
| `get_dom(format?)` | Get page HTML | `{"html": str}` |
| `clear_interstitials()` | Dismiss cookie banners | `None` |
| `save_state()` | Export session state | `{"state_blob": str}` |
| `restore_checkpoint(state_blob)` | Restore saved state | `None` |
| `get_audit_log()` | Get action history | `{"log": list}` |
| `pause(reason)` / `resume()` | Human-in-the-loop | `None` |
| `destroy()` | Terminate session | `None` |

## Error Handling

```python
try:
    await agent.click("invalid_id")
except Exception as e:
    print(e)  # [AGENSTAB -32006] ELEMENT_NOT_FOUND
```

The SDK raises standard `Exception` with messages formatted from the RPC error payload.

## Connection Options

| Parameter | Default | Description |
|---|---|---|
| `api_key` | Required | Your API key (`ak_live_...` or `ak_test_...`) |
| `endpoint` | `wss://api.agenstab.com/v1/session` | WebSocket endpoint |
| `session_config.headless` | `True` | Run headless Chromium |
