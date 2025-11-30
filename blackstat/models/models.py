from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: Optional[int] = Field(default=None, description="Unique identifier for the product")
    name: str = Field(..., description="Name of the product")
    url: str = Field(..., description="URL of the product")
    created_at: datetime = Field(default_factory=datetime.now, description="When the product was added")

class PriceTransaction(BaseModel):
    id: Optional[int] = Field(default=None, description="Unique identifier for the transaction")
    product_id: int = Field(..., description="ID of the product this price belongs to")
    price: float = Field(..., description="Price of the product")
    date: datetime = Field(default_factory=datetime.now, description="Date and time of the price check")
    source_url: str = Field(..., description="URL where the price was found")
