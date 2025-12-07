import os
import nest_asyncio
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from duckduckgo_search import DDGS
from dotenv import load_dotenv

# Allow nested event loops for Textual + Async Agent
nest_asyncio.apply()

load_dotenv()

# Ensure GOOGLE_API_KEY is set for pydantic-ai
if not os.getenv("GOOGLE_API_KEY") and os.getenv("GEMINI_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

if not os.getenv("GOOGLE_API_KEY"):
    print("Warning: GOOGLE_API_KEY not found. Agent features will not work.")

class PriceResult(BaseModel):
    price: float = Field(..., description="The found price of the product")
    currency: str = Field(..., description="The currency of the price (e.g. DKK, USD)")
    source_url: str = Field(..., description="The URL where the price was found")
    product_name: str = Field(..., description="The name of the product found")

# Initialize the agent
# We use 'google-gla:gemini-2.0-flash' as a good default for speed/cost
agent = Agent(
    'google-gla:gemini-2.0-flash',
    output_type=PriceResult,
    system_prompt=(
        "You are a price finder agent. Your goal is to find the current lowest price for a given product. "
        "You must use the search tool to find real-time pricing information. "
        "Always prefer major retailers. "
        "If you find a price, extract the numeric value, currency, and the specific URL. "
        "If you cannot find a price, you should still try your best to give an estimate or find a similar product, "
        "but be accurate with the source URL."
    ),
)

@agent.tool
def search_web(ctx: RunContext, query: str) -> str:
    """Search the web for the given query using DuckDuckGo."""
    print(f"Searching for: {query}")
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
        return str(results)

async def find_product_price(product_name: str) -> Optional[PriceResult]:
    """
    Finds the price for a product using the AI agent.
    """
    try:
        # Check for API Key
        if not os.getenv("GEMINI_API_KEY"):
            print("Error: GEMINI_API_KEY not found in environment variables.")
            return None

        result = await agent.run(f"Find the current price for: {product_name}. Return the price in DKK if possible, otherwise convert or state original.")
        return result.data
    except Exception as e:
        print(f"Error running agent: {e}")
        return None
