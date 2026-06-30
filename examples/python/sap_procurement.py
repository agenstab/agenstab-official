"""
AGENSTAB Example: SAP Fiori procurement automation

Demonstrates the Blueprint Engine for enterprise applications.
Blueprints provide pre-mapped navigation patterns for complex
enterprise UIs like SAP, Salesforce, Workday, and ServiceNow.
"""

import asyncio
from agens_tab import BrowserAgent


async def create_purchase_order():
    # Initialize with SAP Fiori blueprint
    agent = await BrowserAgent.init(
        api_key="ak_live_...",
        session_config={"headless": True}
    )

    try:
        # Navigate to SAP Fiori launchpad
        await agent.navigate("https://sap.yourcompany.com/fiori")

        # Observe the launchpad tiles
        state = await agent.observe()

        # Find and click the Procurement tile
        procurement_tile = next(
            el for el in state["axtree"]
            if el["role"] == "link" and "procurement" in el.get("name", "").lower()
        )
        await agent.click(procurement_tile["agent_id"])

        # Navigate to Create Purchase Order
        state = await agent.observe()
        create_po = next(
            el for el in state["axtree"]
            if "create" in el.get("name", "").lower() and "purchase" in el.get("name", "").lower()
        )
        await agent.click(create_po["agent_id"])

        # Fill the purchase order form
        state = await agent.observe()

        # Map form fields by their accessible names
        form_data = {
            "Vendor": "ACME Corp",
            "Material": "Widget-X",
            "Quantity": "500",
            "Delivery Date": "2026-07-15",
            "Plant": "US01"
        }

        for field_name, value in form_data.items():
            field = next(
                (el for el in state["axtree"]
                 if el.get("name", "").lower() == field_name.lower()
                 and el["interactable"]),
                None
            )
            if field:
                await agent.type(field["agent_id"], value)
                print(f"  Filled {field_name}: {value}")

        # Submit the form
        state = await agent.observe()
        submit_btn = next(
            el for el in state["axtree"]
            if el["role"] == "button" and "submit" in el.get("name", "").lower()
        )
        await agent.click(submit_btn["agent_id"])

        # Verify confirmation
        state = await agent.observe()
        confirmation = next(
            (el for el in state["axtree"]
             if "order" in el.get("name", "").lower()
             and any(c.isdigit() for c in el.get("name", ""))),
            None
        )

        if confirmation:
            print(f"\n✅ Purchase order created: {confirmation['name']}")
        else:
            print("\n⚠️ Could not confirm order number")

    finally:
        await agent.destroy()


if __name__ == "__main__":
    asyncio.run(create_purchase_order())
