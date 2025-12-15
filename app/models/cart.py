from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class CartItem(BaseModel):
    item_id: str
    quantity: int = 1

class Cart(BaseModel):
    user_id: str
    items: List[CartItem] = []
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CartDocument(Cart):
    id: str = Field(alias="_id")

class CartResponse(BaseModel):
    items: List[dict] # We will enrich items with product details
    total: float
    count: int
