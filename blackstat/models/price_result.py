from pydantic import BaseModel, Field

class PriceResult(BaseModel):
    price: float = Field(..., description="The found price of the product")
    currency: str = Field(..., description="The currency of the price (e.g. DKK, USD)")
    source_url: str = Field(..., description="The URL where the price was found")
    product_name: str = Field(..., description="The name of the product found")
