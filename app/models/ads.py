from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class AdLocation(str, Enum):
    """موقع الإعلان"""
    DASHBOARD_BANNER = "dashboard_banner"
    STORE_GRID = "store_grid"
    LANDING_PAGE = "landing_page"

class AdCreate(BaseModel):
    """طلب إنشاء إعلان"""
    title: str = Field(..., description="عنوان الإعلان (للتنظيم)")
    image_url: str = Field(..., description="رابط الصورة")
    link_url: Optional[str] = Field(None, description="الرابط عند الضغط")
    locations: List[AdLocation] = Field(..., description="أماكن العرض")
    is_active: bool = Field(default=True, description="نشط أم لا")
    priority: int = Field(default=1, description="الأولوية في الترتيب (الأعلى يظهر أولاً)")

class AdUpdate(BaseModel):
    """طلب تحديث إعلان"""
    title: Optional[str] = None
    image_url: Optional[str] = None
    link_url: Optional[str] = None
    locations: Optional[List[AdLocation]] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None

class AdResponse(BaseModel):
    """عرض بيانات الإعلان"""
    ad_id: str
    title: str
    image_url: str
    link_url: Optional[str]
    locations: List[AdLocation]
    is_active: bool
    priority: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class AdDocument(BaseModel):
    """نموذج الإعلان في قاعدة البيانات"""
    id: str = Field(alias="_id")
    title: str
    image_url: str
    link_url: Optional[str] = None
    locations: List[AdLocation] = Field(default_factory=list)
    is_active: bool = True
    priority: int = 1
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
        extra = "ignore"
