from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: Optional[int] = Field(default=None, description="Unique identifier for the product")
    name: str = Field(..., description="Name of the product")
    url: str = Field(..., description="URL of the product")
    created_at: datetime = Field(default_factory=datetime.now, description="When the product was added")
