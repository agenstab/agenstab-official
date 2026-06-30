# Go SDK Reference

The AGENSTAB Go SDK provides a strongly-typed client for the JSON-RPC WebSocket API.

## Installation

```bash
go get github.com/agenstab/agenstab-go
```

## Quick Start

```go
package main

import (
    "context"
    "fmt"
    "log"

    agenstab "github.com/agenstab/agenstab-go"
)

func main() {
    ctx := context.Background()

    client, err := agenstab.NewClient(ctx, agenstab.Config{
        APIKey: "ak_live_...",
    })
    if err != nil {
        log.Fatal(err)
    }
    defer client.Destroy()

    // Navigate
    if err := client.Navigate("https://example.com"); err != nil {
        log.Fatal(err)
    }

    // Observe the page
    state, err := client.Observe(nil)
    if err != nil {
        log.Fatal(err)
    }

    for _, el := range state.AXTree {
        fmt.Printf("[%s] %s: %s\n", el.AgentID, el.Role, el.Name)
    }

    // Interact
    if err := client.Click("a_42"); err != nil {
        log.Fatal(err)
    }
}
```

## Types

```go
type Config struct {
    APIKey   string
    Endpoint string // Default: "wss://api.agenstab.com/v1/session"
    Headless bool   // Default: true
}

type AXTreeElement struct {
    AgentID      string    `json:"agent_id"`
    Role         string    `json:"role"`
    Name         string    `json:"name"`
    Value        string    `json:"value,omitempty"`
    Bounds       [4]int    `json:"bounds"`
    Interactable bool      `json:"interactable"`
}

type ObserveResult struct {
    AXTree  []AXTreeElement `json:"axtree"`
    DOMHash string          `json:"dom_hash"`
    URL     string          `json:"url"`
    Title   string          `json:"title"`
}
```

## Methods

| Method | Signature | Description |
|---|---|---|
| `NewClient` | `(ctx, Config) (*Client, error)` | Connect and create session |
| `Navigate` | `(url string) error` | Load a URL |
| `Observe` | `(opts *ObserveOpts) (*ObserveResult, error)` | Extract AXTree |
| `Click` | `(agentID string) error` | Click element |
| `Type` | `(agentID, text string) error` | Type into input |
| `Select` | `(agentID, value string) error` | Select dropdown option |
| `Scroll` | `(dir string, amount int) error` | Scroll page |
| `FillForm` | `(fields map[string]string) error` | Fill multiple inputs |
| `Screenshot` | `(format string) ([]byte, error)` | Capture viewport |
| `Evaluate` | `(script string) (interface{}, error)` | Execute JavaScript |
| `SaveState` | `() (string, error)` | Export session state |
| `RestoreCheckpoint` | `(blob string) error` | Restore state |
| `Destroy` | `() error` | Terminate session |

## Error Handling

```go
err := client.Click("invalid_id")
if err != nil {
    var rpcErr *agenstab.RPCError
    if errors.As(err, &rpcErr) {
        fmt.Printf("Code: %d, Message: %s\n", rpcErr.Code, rpcErr.Message)
    }
}
```
