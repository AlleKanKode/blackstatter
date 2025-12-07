import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

print(f"GEMINI_API_KEY present: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")
print(f"GOOGLE_API_KEY present: {'Yes' if os.getenv('GOOGLE_API_KEY') else 'No'}")

# Ensure GOOGLE_API_KEY is set for pydantic-ai BEFORE importing the agent
if os.getenv("GEMINI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
    print("Set GOOGLE_API_KEY from GEMINI_API_KEY")

from blackstat.agent import find_product_price

async def test_agent():
    print("Testing Price Agent...")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("WARNING: GOOGLE_API_KEY (or GEMINI_API_KEY) not found. Skipping actual API call.")
        # return # Let it fail to see error if we want, or return.
        return

    product_name = "Logitech MX Master 3S"
    print(f"Searching for: {product_name}")
    
    result = await find_product_price(product_name)
    
    if result:
        print("SUCCESS!")
        print(f"Price: {result.price} {result.currency}")
        print(f"Source: {result.source_url}")
        print(f"Product: {result.product_name}")
    else:
        print("FAILED: No result returned.")

if __name__ == "__main__":
    asyncio.run(test_agent())
