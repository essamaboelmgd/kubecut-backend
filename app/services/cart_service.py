from typing import List, Optional
from datetime import datetime
from uuid import uuid4
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.cart import Cart, CartItem, CartResponse
from app.services.marketplace_service import MarketplaceService, get_marketplace_service
from app.database import get_database
from fastapi import Depends

class CartService:
    def __init__(self, db: AsyncIOMotorDatabase, marketplace_service: MarketplaceService):
        self.db = db
        self.collection = db.carts
        self.marketplace_service = marketplace_service

    async def get_cart(self, user_id: str) -> CartResponse:
        cart_doc = await self.collection.find_one({"user_id": user_id})
        
        items = []
        if cart_doc:
            items = cart_doc.get("items", [])
            
        # Enrich items with product details
        enriched_items = []
        total = 0
        count = 0
        
        # Filter out invalid items and calculate total
        valid_items = []
        
        for item in items:
            product = await self.marketplace_service.get_item_by_id(item["item_id"])
            if product:
                quantity = item["quantity"]
                product_dict = product.model_dump()
                product_dict["item_id"] = product.id  # Ensure item_id is present for frontend
                enriched_items.append({
                    "product": product_dict,
                    "quantity": quantity
                })
                total += product.price * quantity
                count += quantity
                valid_items.append(item)
            # If product not found (deleted), it's removed from enriched view, 
            # and effectively removed from cart on next save logic if we had one.
            # ideally we should clean up.
            
        return CartResponse(items=enriched_items, total=total, count=count)

    async def add_to_cart(self, user_id: str, item_id: str, quantity: int = 1):
        cart = await self.collection.find_one({"user_id": user_id})
        items = []
        if cart:
            items = cart.get("items", [])
            
        # Check if item exists in cart
        found = False
        for item in items:
            if item["item_id"] == item_id:
                item["quantity"] += quantity
                found = True
                break
        
        if not found:
            items.append({"item_id": item_id, "quantity": quantity})
            
        await self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"items": items, "updated_at": datetime.utcnow()}},
            upsert=True
        )

    async def remove_from_cart(self, user_id: str, item_id: str):
        await self.collection.update_one(
            {"user_id": user_id},
            {"$pull": {"items": {"item_id": item_id}}}
        )

    async def update_quantity(self, user_id: str, item_id: str, quantity: int):
        if quantity <= 0:
            await self.remove_from_cart(user_id, item_id)
            return

        await self.collection.update_one(
            {"user_id": user_id, "items.item_id": item_id},
            {"$set": {"items.$.quantity": quantity, "updated_at": datetime.utcnow()}}
        )

    async def clear_cart(self, user_id: str):
        await self.collection.delete_one({"user_id": user_id})

async def get_cart_service(
    market_service: MarketplaceService = Depends(get_marketplace_service)
) -> CartService:
    db = get_database()
    return CartService(db, market_service)
