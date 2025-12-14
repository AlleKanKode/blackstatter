import asyncio
import os
import sys
from dotenv import load_dotenv

# Force reload of .env
load_dotenv(override=True)

def print_debug(msg):
    print(f"[DEBUG] {msg}")

async def run_debug():
    print_debug("Starting debug script...")
    
    # 1. Check Environment Variables
    gemini_key = os.getenv("GEMINI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    print_debug(f"GEMINI_API_KEY present: {'Yes' if gemini_key else 'No'}")
    if gemini_key:
        print_debug(f"GEMINI_API_KEY length: {len(gemini_key)}")
        print_debug(f"GEMINI_API_KEY starts with: {gemini_key[:4]}...")
        
    print_debug(f"GOOGLE_API_KEY present: {'Yes' if google_key else 'No'}")
    
    # 2. Setup Keys
    if gemini_key and not google_key:
        print_debug("Setting GOOGLE_API_KEY from GEMINI_API_KEY")
        os.environ["GOOGLE_API_KEY"] = gemini_key
    
    if not os.getenv("GOOGLE_API_KEY"):
        print_debug("ERROR: No API Key found. Please check your .env file.")
        return

    # 3. Import Agent (Import here to ensure env vars are set first)
    try:
        print_debug("Importing agent...")
        from blackstat.controllers.price_agent import find_product_price, agent
        print_debug("Agent imported successfully.")
    except Exception as e:
        print_debug(f"ERROR importing agent: {e}")
        return

    # 4. Test Search Tool directly (optional, but good for debugging)
    print_debug("Testing Search Tool directly...")
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text("test search", max_results=1))
            print_debug(f"Search tool check: {'Success' if results else 'Empty results'}")
    except Exception as e:
        print_debug(f"Search tool ERROR: {e}")

    # 5. Run Agent
    product = "Logitech MX Master 3S"
    print_debug(f"Running agent for product: {product}")
    
    try:
        # We call the function that wraps the agent run
        result = await find_product_price(product)
        
        if result:
            print("\n--- RESULT FOUND ---")
            print(f"Product: {result.product_name}")
            print(f"Price: {result.price} {result.currency}")
            print(f"Source: {result.source_url}")
        else:
            print("\n--- NO RESULT ---")
            print("The agent returned None.")
            
    except Exception as e:
        print_debug(f"ERROR running agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_debug())
