import os
import nest_asyncio
from typing import Optional
from pydantic_ai import Agent, RunContext
from ddgs import DDGS
from dotenv import load_dotenv
from blackstat.models.price_result import PriceResult

# Allow nested event loops for Textual + Async Agent
nest_asyncio.apply()

load_dotenv()

# Ensure GOOGLE_API_KEY is set for pydantic-ai
if not os.getenv("GOOGLE_API_KEY") and os.getenv("GEMINI_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

if not os.getenv("GOOGLE_API_KEY"):
    print("Warning: GOOGLE_API_KEY not found. Agent features will not work.")

# Try to import Tavily
try:
    from tavily import TavilyClient
    HAS_TAVILY = True
except ImportError:
    HAS_TAVILY = False



# Initialize the agent
# Using gemini-2.5-flash as it is available in the list
agent = Agent(
    'google-gla:gemini-2.5-flash',
    output_type=PriceResult,
    system_prompt=(
        "You are a price finder agent. Your goal is to find the current lowest price for a given product. "
        "You must use the search tool to find real-time pricing information. "
        "Always prefer major retailers. In Denmark"
        "If you find a price, extract the numeric value, currency, and the specific URL. "
        "If you cannot find a price, you should still try your best to give an estimate or find a similar product, "
        "but be accurate with the source URL."
    ),
)

@agent.tool
def search_web(ctx: RunContext, query: str) -> str:
    """Search the web for the given query. Uses Tavily if API key is present, otherwise falls back to DuckDuckGo."""
    print(f"Searching for: {query}")
    
    # 1. Try Tavily
    tavily_key = os.getenv("TAVILY_API_KEY")
    if HAS_TAVILY and tavily_key:
        try:
            client = TavilyClient(api_key=tavily_key)
            # Use 'q' parameter for Tavily and optimize for shopping/news if possible, but standard search is fine.
            logger_print(f"Using Tavily for search: {query}")
            results = client.search(query, search_depth="basic", max_results=5)
            # Tavily returns a dict with 'results' key
            return str(results.get("results", []))
        except Exception as e:
            print(f"Tavily search failed: {e}. Falling back to DuckDuckGo.")
    
    # 2. Fallback to DuckDuckGo
    try:
        logger_print(f"Using DuckDuckGo for search: {query}")
        with DDGS() as ddgs:
            # backend="html" is often more permissive than "api"
            results = list(ddgs.text(query, max_results=5, backend="html"))
            if not results:
                 # Try default backend if html returns nothing (rare but possible)
                 results = list(ddgs.text(query, max_results=5))
            return str(results)
    except Exception as e:
        return f"Search failed: {e}"

def logger_print(msg):
    # Simple helper to print with timestamp or debug prefix if needed
    print(f"[Agent Tool] {msg}")

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
