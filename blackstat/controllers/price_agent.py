import os
from typing import Optional
from pydantic_ai import Agent, RunContext
from ddgs import DDGS
from dotenv import load_dotenv
from blackstat.models.price_result import PriceResult
from blackstat.utils.logger import setup_logger

# Setup logging to file (logs/price_agent.log) and console
logger = setup_logger()

# Load environment variables from .env file
load_dotenv()

# --- Configuration & API Keys ---

# Ensure GOOGLE_API_KEY is available for the Gemini agent.
# If only GEMINI_API_KEY is set, copy it to GOOGLE_API_KEY.
if not os.getenv("GOOGLE_API_KEY") and os.getenv("GEMINI_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

if not os.getenv("GOOGLE_API_KEY"):
    logger.warning("GOOGLE_API_KEY not found. Agent features will not work.")

# Try to import Tavily client (preferred search tool)
# We handle the ImportError so the app works even if 'tavily-python' is missing.
try:
    from tavily import TavilyClient
    HAS_TAVILY = True
except ImportError:
    HAS_TAVILY = False

# --- Agent Initialization ---

# Initialize the PydanticAI agent.
# We use 'google-gla:gemini-2.5-flash' because it's fast and cost-effective.
# The 'output_type=PriceResult' ensures the agent returns a structured object, not just text.
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

# --- Tools ---

@agent.tool
def search_web(ctx: RunContext, query: str) -> str:
    """
    Search the web for the given query.
    
    Strategy:
    1. Try Tavily Search API (High quality, meant for LLMs) if key is present.
    2. Fallback to DuckDuckGo (Free, but sometimes timed out/blocked) if Tavily fails or is missing.
    """
    logger.info(f"Searching for: {query}")
    
    # 1. Try Tavily (Preferred)
    tavily_key = os.getenv("TAVILY_API_KEY")
    if HAS_TAVILY and tavily_key:
        try:
            client = TavilyClient(api_key=tavily_key)
            logger.info(f"Using <green>Tavily</green> for search: {query}")
            
            # search_depth="basic" is faster and usually sufficient for specific product prices
            results = client.search(query, search_depth="basic", max_results=5)
            
            # Log raw results for debugging purposes
            logger.debug(f"Tavily Results: {results}")
            
            # Tavily returns a dict with a "results" list
            return str(results.get("results", []))
        except Exception as e:
            logger.error(f"Tavily search failed: {e}. Falling back to DuckDuckGo.")
    
    # 2. Fallback to DuckDuckGo
    try:
        logger.info(f"Using <yellow>DuckDuckGo</yellow> for search: {query}")
        with DDGS() as ddgs:
            # We first try the 'html' backend as it is often more permissive/robust than the API backend
            results = list(ddgs.text(query, max_results=5, backend="html"))
            
            if not results:
                 logger.debug("DuckDuckGo HTML backend empty, trying default backend.")
                 results = list(ddgs.text(query, max_results=5))
            
            logger.debug(f"DuckDuckGo Results: {results}")
            return str(results)
    except Exception as e:
        logger.error(f"DuckDuckGo search failed: {e}")
        return f"Search failed: {e}"

# --- Main Logic ---

async def find_product_price(product_name: str) -> Optional[PriceResult]:
    """
    Finds the price for a product using the AI agent.
    
    Returns:
        PriceResult: Object containing price, currency, url if found.
        None: If search fails, API key is missing, or invalid data is returned.
    """
    try:
        if not os.getenv("GEMINI_API_KEY"):
            logger.error("GEMINI_API_KEY not found.")
            return None

        logger.info(f"Starting price check for: {product_name}")
        
        # Run the agent with a prompt constructed from the product name
        result = await agent.run(
            f"Find the current price for: {product_name}. "
            f"Return the price in DKK if possible, otherwise convert or state original."
        )
        
        # The result object has an .output property because we defined output_type=PriceResult
        data = result.output
        
        # Validation: Filter out bad results like negative prices or missing URLs
        if data.price <= 0 or not data.source_url or data.source_url.lower() in ["n/a", "none"]:
            logger.warning(f"Agent returned invalid data: {data}")
            return None
            
        logger.info(f"Price found: {data.price} {data.currency} at {data.source_url}")
        return data
        
    except Exception as e:
        logger.exception(f"Error running agent: {e}")
        return None
