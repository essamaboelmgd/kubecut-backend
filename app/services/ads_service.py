from typing import List, Optional
from datetime import datetime
from uuid import uuid4
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.ads import AdCreate, AdUpdate, AdDocument, AdLocation
from app.database import get_database

class AdsService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.ads

    async def create_ad(self, ad_data: AdCreate) -> AdDocument:
        ad_dict = ad_data.model_dump()
        ad_doc = AdDocument(
            _id=str(uuid4()),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            **ad_dict
        )
        
        await self.collection.insert_one(ad_doc.model_dump(by_alias=True))
        return ad_doc

    async def update_ad(self, ad_id: str, update_data: AdUpdate) -> Optional[AdDocument]:
        ad = await self.collection.find_one({"_id": ad_id})
        if not ad:
            return None
            
        update_dict = update_data.model_dump(exclude_unset=True)
        if not update_dict:
            return AdDocument(**ad)
            
        update_dict["updated_at"] = datetime.utcnow()
        
        await self.collection.update_one(
            {"_id": ad_id},
            {"$set": update_dict}
        )
        
        updated_doc = await self.collection.find_one({"_id": ad_id})
        return AdDocument(**updated_doc)

    async def get_ads(self, location: Optional[AdLocation] = None, active_only: bool = True) -> List[AdDocument]:
        query = {}
        if location:
            # MongoDB finds documents where 'locations' array contains the specific 'location' value
            query["locations"] = location
        if active_only:
            query["is_active"] = True
            
        # Sort by priority (desc) then created_at (desc)
        cursor = self.collection.find(query).sort([("priority", -1), ("created_at", -1)])
        
        ads = []
        async for doc in cursor:
            # Handle migration/compatibility if needed: if 'locations' missing, try 'location'
            if "locations" not in doc and "location" in doc:
                doc["locations"] = [doc["location"]]
            elif "locations" not in doc:
                doc["locations"] = []
                
            ads.append(AdDocument(**doc))
        return ads

    async def get_all_ads(self) -> List[AdDocument]:
        """Get all ads for admin (including inactive)"""
        cursor = self.collection.find({}).sort("created_at", -1)
        ads = []
        async for doc in cursor:
            # Migration/Compat
            if "locations" not in doc and "location" in doc:
                doc["locations"] = [doc["location"]]
            elif "locations" not in doc:
                doc["locations"] = []
                
            ads.append(AdDocument(**doc))
        return ads

    async def delete_ad(self, ad_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ad_id})
        return result.deleted_count > 0

    async def toggle_ad_status(self, ad_id: str) -> Optional[AdDocument]:
        ad = await self.collection.find_one({"_id": ad_id})
        if not ad:
            return None
            
        new_status = not ad.get("is_active", True)
        await self.collection.update_one(
            {"_id": ad_id},
            {"$set": {"is_active": new_status, "updated_at": datetime.utcnow()}}
        )
        
        updated_doc = await self.collection.find_one({"_id": ad_id})
        # Migration/Compat
        if "locations" not in updated_doc and "location" in updated_doc:
            updated_doc["locations"] = [updated_doc["location"]]
            
        return AdDocument(**updated_doc)

# Helper
async def get_ads_service() -> AdsService:
    db = get_database()
    return AdsService(db)
