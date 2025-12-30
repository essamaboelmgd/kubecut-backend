from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class UnitType(str, Enum):
    """أنواع الوحدات - 42 نوع"""
    # وحدات أرضية
    GROUND = "ground"  # ارضي
    GROUND_SIDE_PANEL = "ground_side_panel"  # ارضي بها جنب عيرة
    GROUND_FIXED = "ground_fixed"  # ارضي ثابت
    GROUND_FIXED_SIDE_PANEL = "ground_fixed_side_panel"  # ارضي ثابت بها جنب عيرة
    
    # وحدات حوض
    SINK = "sink"  # حوض
    SINK_SIDE_PANEL = "sink_side_panel"  # حوض بها جنب عيرة
    SINK_FIXED = "sink_fixed"  # حوض ثابت
    SINK_FIXED_SIDE_PANEL = "sink_fixed_side_panel"  # حوض ثابت بها جنب عيرة
    
    # وحدات أدراج
    DRAWERS = "drawers"  # ادراج
    DRAWERS_SIDE_PANEL = "drawers_side_panel"  # ادراج بها جنب عيرة
    DRAWERS_BOTTOM_RAIL = "drawers_bottom_rail"  # ادراج مجرة سفلية
    DRAWERS_BOTTOM_RAIL_SIDE_PANEL = "drawers_bottom_rail_side_panel"  # ادراج مجرة سفلية بها جنب عيرة
    
    # وحدات ركنة أرضية
    CORNER_90_GROUND = "corner_90_ground"  # ركنة 90 ارضي متساوية الاضلع
    CORNER_45_GROUND = "corner_45_ground"  # ركنة 45 ارضي
    
    # وحدات علوية
    WALL = "wall"  # علوي
    WALL_SIDE_PANEL = "wall_side_panel"  # علوي بها جنب عيرة
    WALL_FIXED = "wall_fixed"  # علوي ثابت
    WALL_FIXED_SIDE_PANEL = "wall_fixed_side_panel"  # علوي ثابت بها جنب عيرة
    WALL_FLIP_TOP_DOORS_BOTTOM = "wall_flip_top_doors_bottom"  # علوي ضلفة قلاب علوية +ضلف سفلية
    
    # وحدات صفاية
    DISH_RACK = "dish_rack"  # صفاية
    DISH_RACK_SIDE_PANEL = "dish_rack_side_panel"  # صفاية بها جنب عيرة
    
    # وحدات ركنة علوية
    CORNER_L_WALL = "corner_l_wall"  # ركنة L علوي متساوية الاضلع
    CORNER_45_WALL = "corner_45_wall"  # ركنة 45 علوي
    
    # وحدات علوية خاصة
    WALL_MICROWAVE = "wall_microwave"  # علوي بها ميكرويف
    
    # دواليب
    TALL_DOORS = "tall_doors"  # دولاب ضلفة سفلي و علوي
    TALL_DOORS_SIDE_PANEL = "tall_doors_side_panel"  # دولاب ضلفة سفلي و علوي جنب عيرة
    TALL_DOORS_APPLIANCES = "tall_doors_appliances"  # دولاب ضلف + أجهزة
    TALL_DOORS_APPLIANCES_SIDE_PANEL = "tall_doors_appliances_side_panel"  # دولاب ضلف + اجهزة جنب عيرة
    
    TALL_DRAWERS_SIDE_DOORS_TOP = "tall_drawers_side_doors_top"  # دولاب ادراج (م)جانبية + ضلف علوية
    TALL_DRAWERS_SIDE_DOORS_TOP_SIDE_PANEL = "tall_drawers_side_doors_top_side_panel"  # دولاب ادراج (م)جانبية + ضلف علوية جنب عيرة
    TALL_DRAWERS_BOTTOM_DOORS_TOP = "tall_drawers_bottom_doors_top"  # دولاب ادراج (م)سفلية + ضلف علوية
    TALL_DRAWERS_BOTTOM_DOORS_TOP_SIDE_PANEL = "tall_drawers_bottom_doors_top_side_panel"  # دولاب ادراج (م)سفلية + ضلف علوية جنب عيرة
    
    TALL_DRAWERS_SIDE_APPLIANCES_DOORS = "tall_drawers_side_appliances_doors"  # دولاب ادراج م جانبية+أجهزة + ضلف
    TALL_DRAWERS_SIDE_APPLIANCES_DOORS_SIDE_PANEL = "tall_drawers_side_appliances_doors_side_panel"  # دولاب ادراج م جانبية + أجهزة + ضلف جنب عيرة
    TALL_DRAWERS_BOTTOM_APPLIANCES_DOORS_TOP = "tall_drawers_bottom_appliances_doors_top"  # دولاب ادراج م سفلية+أجهزة + ضلف علوية
    TALL_DRAWERS_BOTTOM_APPLIANCES_DOORS_TOP_SIDE_PANEL = "tall_drawers_bottom_appliances_doors_top_side_panel"  # دولاب ادراج م سفلية + أجهزة + ضلف علوية جنب عيرة
    
    TALL_WOODEN_BASE = "tall_wooden_base"  # بلاكار قاعدة خشبية
    TALL_DRAWERS_BOTTOM_RAIL_TOP_DOORS = "tall_drawers_bottom_rail_top_doors"  # دولاب ادراج مجرى سفلية + ضلف علوية

    THREE_TURBO = "three_turbo"  # وحدة 3 تربو
    DRAWER_BUILT_IN_OVEN = "drawer_built_in_oven"  # وحدة درج + فرن بيلت ان
    DRAWER_BOTTOM_RAIL_BUILT_IN_OVEN = "drawer_bottom_rail_built_in_oven"  # وحدة درج مجره سفلية+ فرن بيلت    TALL_DRAWERS_BOTTOM_RAIL_TOP_DOORS = "tall_drawers_bottom_rail_top_doors"  # دولاب ادراج مجرى سفلية + ضلف علوية

    # أدراج خاصة
    TWO_SMALL_20_ONE_LARGE_SIDE = "two_small_20_one_large_side"  # 2درج صغير20سم + درج كبير م جانبية
    TWO_SMALL_20_ONE_LARGE_BOTTOM = "two_small_20_one_large_bottom"  # 2درج صغير20سم + درج كبير م سفلية
    ONE_SMALL_16_TWO_LARGE_SIDE = "one_small_16_two_large_side"  # درج صغير 16 سم + 2 درج كبير م جانبية
    ONE_SMALL_16_TWO_LARGE_BOTTOM = "one_small_16_two_large_bottom"  # درج صغير 16 سم + 2 درج كبير م سفلية
    
    # متفرقات
    SIDE_FLUSH = "side_flush"  # جنب لطش
    WALL_MICROWAVE = "wall_microwave"  # علوي بها ميكرويف
    WALL_MICROWAVE_SIDE_PANEL = "wall_microwave_side_panel"  # علوي بها ميكرويف جنب عيرة
    WARDROBE_WOODEN_BASE = "wardrobe_wooden_base"  # بلاكار قاعدة خشبية

class DoorType(str, Enum):
    """نوع الضلفة"""
    HINGED = "hinged"  # مفصلي
    FLIP = "flip"  # قلاب

class EdgeDistribution(BaseModel):
    """توزيع الشريط على الحواف"""
    top: bool = Field(default=True, description="أعلى")
    left: bool = Field(default=True, description="شمال")
    right: bool = Field(default=True, description="يمين")
    bottom: bool = Field(default=True, description="أسفل")

class Part(BaseModel):
    """قطعة من الوحدة"""
    name: str = Field(description="اسم القطعة")
    width_cm: float = Field(description="العرض بالسنتيمتر")
    height_cm: float = Field(description="الارتفاع بالسنتيمتر")
    depth_cm: Optional[float] = Field(default=None, description="العمق بالسنتيمتر (للقطع ثلاثية الأبعاد)")
    qty: int = Field(description="الكمية")
    edge_distribution: Optional[EdgeDistribution] = Field(default=None, description="توزيع الشريط")
    area_m2: Optional[float] = Field(default=None, description="المساحة بالمتر المربع")
    edge_band_m: Optional[float] = Field(default=None, description="متر الشريط المطلوب")

class UnitCalculateRequest(BaseModel):
    """طلب حساب الوحدة"""
    type: UnitType = Field(description="نوع الوحدة")
    width_cm: float = Field(gt=0, description="عرض الوحدة بالسنتيمتر")
    width_2_cm: float = Field(default=0.0, ge=0, description="عرض 2 للوحدات الركنة بالسنتيمتر")
    height_cm: float = Field(gt=0, description="ارتفاع الوحدة بالسنتيمتر")
    depth_cm: float = Field(gt=0, description="عمق الوحدة بالسنتيمتر")
    depth_2_cm: float = Field(default=0.0, ge=0, description="عمق 2 للوحدات الركنة بالسنتيمتر")
    shelf_count: int = Field(default=2, ge=0, description="عدد الرفوف (افتراضي 2)")
    door_count: int = Field(default=2, ge=0, description="عدد الضلف (افتراضي 2)")
    door_type: DoorType = Field(default=DoorType.HINGED, description="نوع الضلفة: hinged (مفصلي) أو flip (قلاب)")
    flip_door_height: float = Field(default=0.0, ge=0, description="ارتفاع ضلفة القلاب (للوحدات التي تحتوي على قلاب)")
    bottom_door_height: float = Field(default=0.0, ge=0, description="ارتفاع الضلفة السفلية (للوحدات الطويلة)")
    oven_height: float = Field(default=60.0, ge=0, description="ارتفاع الفرن بالسنتيمتر")
    microwave_height: float = Field(default=35.0, ge=0, description="ارتفاع الميكرويف بالسنتيمتر")
    vent_height: float = Field(default=10.0, ge=0, description="ارتفاع الهواية بالسنتيمتر")
    drawer_count: int = Field(default=0, ge=0, description="عدد الأدراج (افتراضي 0)")
    drawer_height_cm: float = Field(default=20.0, gt=0, description="ارتفاع الدرج بالسنتيمتر (افتراضي 20)")
    fixed_part_cm: float = Field(default=0.0, ge=0, description="الجزء الثابت بالسنتيمتر (للوحدات الثابتة)")
    options: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="خيارات إضافية"
    )

class UnitCalculateResponse(BaseModel):
    """نتيجة حساب الوحدة"""
    unit_id: Optional[str] = Field(default=None, description="معرف الوحدة إذا تم الحفظ")
    type: UnitType
    width_cm: float
    height_cm: float
    depth_cm: float
    shelf_count: int
    parts: List[Part] = Field(description="قائمة القطع المحسوبة")
    total_edge_band_m: float = Field(description="إجمالي متر الشريط")
    total_area_m2: float = Field(description="إجمالي المساحة بالمتر المربع")
    material_usage: Dict[str, float] = Field(
        default_factory=dict,
        description="استخدام المواد (ألواح الخشب, شريط الحافة, etc.)"
    )
    cost_breakdown: Dict[str, float] = Field(
        default_factory=dict,
        description="تفاصيل التكلفة لكل مادة"
    )
    total_cost: float = Field(default=0.0, description="التكلفة الإجمالية")

class UnitEstimateRequest(BaseModel):
    """طلب تقدير تكلفة الوحدة"""
    type: UnitType = Field(description="نوع الوحدة")
    width_cm: float = Field(gt=0)
    width_2_cm: float = Field(default=0.0, ge=0)
    height_cm: float = Field(gt=0)
    depth_cm: float = Field(gt=0)
    depth_2_cm: float = Field(default=0.0, ge=0)
    shelf_count: int = Field(default=2, ge=0)
    door_count: int = Field(default=2, ge=0)
    door_type: DoorType = Field(default=DoorType.HINGED)
    flip_door_height: float = Field(default=0.0, ge=0)
    bottom_door_height: float = Field(default=0.0, ge=0)
    oven_height: float = Field(default=60.0, ge=0)
    microwave_height: float = Field(default=35.0, ge=0)
    vent_height: float = Field(default=10.0, ge=0)
    drawer_count: int = Field(default=0, ge=0)
    drawer_height_cm: float = Field(default=20.0, gt=0)
    fixed_part_cm: float = Field(default=0.0, ge=0)
    options: Optional[Dict[str, Any]] = Field(default_factory=dict)

class UnitEstimateResponse(BaseModel):
    """نتيجة تقدير التكلفة"""
    unit_id: Optional[str] = None
    type: UnitType
    width_cm: float
    height_cm: float
    depth_cm: float
    shelf_count: int
    parts: List[Part]
    total_edge_band_m: float
    total_area_m2: float
    material_usage: Dict[str, float]
    cost_breakdown: Dict[str, float] = Field(
        description="تفاصيل التكلفة لكل مادة"
    )
    total_cost: float = Field(description="التكلفة الإجمالية")

class UnitDocument(BaseModel):
    """نموذج الوحدة المحفوظة في MongoDB"""
    id: Optional[str] = None
    type: UnitType
    width_cm: float
    height_cm: float
    depth_cm: float
    shelf_count: int
    parts_calculated: List[Dict]
    edge_band_m: float
    total_area_m2: float
    material_usage: Dict[str, float]
    price_estimate: Optional[float] = None
    project_id: Optional[str] = None
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
