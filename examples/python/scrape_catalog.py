"""
AGENSTAB Example: Scrape a product catalog

Demonstrates the observe → act loop for extracting
structured data from an e-commerce site.
"""

import asyncio
from agens_tab import BrowserAgent


async def main():
    agent = await BrowserAgent.init(
        api_key="ak_live_...",
        session_config={"headless": True}
    )

    try:
        await agent.navigate("https://shop.example.com/catalog")

        # Extract all interactive elements
        state = await agent.observe()

        # Filter for product links
        products = [
            el for el in state["axtree"]
            if el["role"] == "link" and "product" in el.get("name", "").lower()
        ]

        print(f"Found {len(products)} products")

        for product in products:
            # Click into the product detail page
            await agent.click(product["agent_id"])

            # Extract detail page elements
            detail = await agent.observe()

            # Find the price element
            price_el = next(
                (el for el in detail["axtree"] if "price" in el.get("name", "").lower()),
                None
            )

            if price_el:
                print(f"  {product['name']}: {price_el['name']}")

            # Navigate back to catalog
            await agent.navigate("https://shop.example.com/catalog")

    finally:
        await agent.destroy()


if __name__ == "__main__":
    asyncio.run(main())
