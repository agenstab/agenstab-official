"""
AGENSTAB Example: Monitor prices across vendor portals

Demonstrates session state management — login once, save state,
then restore it for subsequent monitoring runs without re-authenticating.
"""

import asyncio
import json
from agens_tab import BrowserAgent


VENDORS = [
    {"name": "Vendor A", "url": "https://vendor-a.example.com/pricing"},
    {"name": "Vendor B", "url": "https://vendor-b.example.com/catalog"},
    {"name": "Vendor C", "url": "https://vendor-c.example.com/products"},
]


async def monitor_prices():
    agent = await BrowserAgent.init(
        api_key="ak_live_...",
        session_config={"headless": True}
    )

    results = []

    try:
        for vendor in VENDORS:
            await agent.navigate(vendor["url"])

            # Extract all elements from the page
            state = await agent.observe()

            # Find price-related elements
            prices = [
                el for el in state["axtree"]
                if any(keyword in el.get("name", "").lower()
                       for keyword in ["price", "$", "cost", "rate"])
            ]

            for price_el in prices:
                results.append({
                    "vendor": vendor["name"],
                    "item": price_el.get("name", "Unknown"),
                    "agent_id": price_el["agent_id"]
                })

            print(f"  {vendor['name']}: found {len(prices)} price elements")

        # Save session state for next run (avoids re-login)
        state_blob = await agent.save_state()
        with open("session_state.json", "w") as f:
            json.dump({"state": state_blob}, f)

        print(f"\nTotal: {len(results)} prices tracked")
        print("Session state saved for next run")

    finally:
        await agent.destroy()

    return results


if __name__ == "__main__":
    prices = asyncio.run(monitor_prices())
    for p in prices:
        print(f"  [{p['vendor']}] {p['item']}")
