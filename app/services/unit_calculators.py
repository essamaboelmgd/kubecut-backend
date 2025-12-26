"""
Unit Calculators - حساب أجزاء الوحدات المختلفة
كل دالة بتحسب الأجزاء المطلوبة لنوع وحدة معين بناءً على الإعدادات
"""
from typing import List, Dict, Any
from app.models.units import Part, EdgeDistribution, DoorType
from app.models.settings import SettingsModel

# سمك اللوح الافتراضي
DEFAULT_BOARD_THICKNESS = 1.8  # cm

def calculate_ground_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    shelf_count: int,
    door_count: int,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء الوحدة الأرضية
    
    Args:
        width_cm: عرض الوحدة
        height_cm: ارتفاع الوحدة
        depth_cm: عمق الوحدة
        shelf_count: عدد الرفوف
        door_count: عدد الضلف
        settings: إعدادات التقطيع
    
    Returns:
        قائمة بالأجزاء المحسوبة
    """
    parts = []
    board_thickness = DEFAULT_BOARD_THICKNESS
    
    # 1. القاعدة (Base)
    # التحقق من طريقة التجميع
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # تجميع بقاعدة كاملة (Ground Base Full)
        # العرض = العمق
        # الطول = العرض الكلي (Full Width)
        base_width = depth_cm
        base_length = width_cm
    else:
        # تجميع بجانبين كاملين (Full Sides) - الافتراضي
        # العرض = العمق
        # الطول = العرض - (سمك الجنبين)
        base_width = depth_cm
        base_length = width_cm - (board_thickness * 2)
        
    parts.append(Part(
        name="base",  # القاعدة
        width_cm=base_width,
        height_cm=base_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((base_width * base_length) / 10000, 4)
    ))
    
    # 2. المرايه الأمامية (Front Mirror)
    mirror_width = settings.mirror_width
    mirror_length = width_cm - (board_thickness * 2)
    parts.append(Part(
        name="front_mirror",  # المرايه الأمامية
        width_cm=mirror_width,
        height_cm=mirror_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((mirror_width * mirror_length) / 10000, 4)
    ))
    
    # 3. المرايه الخلفية (Back Mirror)
    parts.append(Part(
        name="back_mirror",  # المرايه الخلفية
        width_cm=mirror_width,
        height_cm=mirror_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((mirror_width * mirror_length) / 10000, 4)
    ))
    
    # 4. الجانبين (Side Panels)
    # العرض = العمق
    side_width = depth_cm
    
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # تجميع بقاعدة كاملة -> الجناب تقف فوق القاعدة
        # الطول = الارتفاع - سمك القاعدة
        side_height = height_cm - board_thickness
    else:
        # تجميع بجانبين كاملين -> الجناب كاملة للارتفاع
        # الطول = الارتفاع
        side_height = height_cm
        
    parts.append(Part(
        name="side_panel",  # الجانب
        width_cm=side_width,
        height_cm=side_height,
        qty=2,  # قطعتين
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((side_width * side_height * 2) / 10000, 4)
    ))
    
    # 5. الرفوف (Shelves)
    # العرض = العمق - تخصيم الرف من العمق، الطول = العرض - (سمك الجنبين)
    if shelf_count > 0:
        shelf_width = depth_cm - settings.shelf_depth_deduction
        shelf_length = width_cm - (board_thickness * 2)
        parts.append(Part(
            name="shelf",  # الرف
            width_cm=shelf_width,
            height_cm=shelf_length,
            qty=shelf_count,
            edge_distribution=EdgeDistribution(top=True, bottom=False, left=True, right=True),
            area_m2=round((shelf_width * shelf_length * shelf_count) / 10000, 4)
        ))
    
    # 6. الظهر (Back Panel)
    # العرض = العرض - تخصيم الظهر، الطول = الارتفاع - تخصيم الظهر
    # السمك = سمك المفحار من الإعدادات
    back_width = width_cm - settings.back_deduction
    back_height = height_cm - settings.back_deduction
    back_thickness = settings.router_thickness
    parts.append(Part(
        name="back_panel",  # الظهر
        width_cm=back_width,
        height_cm=back_height,
        depth_cm=back_thickness,
        qty=1,
        edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
        area_m2=round((back_width * back_height) / 10000, 4)
    ))
    
    # 7. الضلف (Doors)
    if door_count > 0:
        # العرض = (العرض ÷ عدد الضلف) - تخصيم عرض الضلفة بدون شريط
        door_width = (width_cm / door_count) - settings.door_width_deduction_no_edge
        
        # الطول = الارتفاع - ارتفاع قطاع المقبض - تخصيم ارتفاع الضلفة الأرضي بدون شريط
        door_height = (
            height_cm 
            - settings.handle_profile_height 
            - settings.ground_door_height_deduction_no_edge
        )
        
        parts.append(Part(
            name="door",  # الضلفة
            width_cm=door_width,
            height_cm=door_height,
            qty=door_count,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((door_width * door_height * door_count) / 10000, 4)
        ))
    
    return parts


def calculate_sink_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    shelf_count: int,
    door_count: int,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء وحدة الحوض
    
    الفرق عن الوحدة الأرضية:
    - مرايه أمامية فقط (بدون مرايه خلفية)
    - بدون ظهر (لوجود الحوض)
    
    Args:
        width_cm: عرض الوحدة
        height_cm: ارتفاع الوحدة
        depth_cm: عمق الوحدة
        shelf_count: عدد الرفوف
        door_count: عدد الضلف
        settings: إعدادات التقطيع
    
    Returns:
        قائمة بالأجزاء المحسوبة
    """
    parts = []
    board_thickness = DEFAULT_BOARD_THICKNESS
    
    # 1. القاعدة (Base)
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # تجميع بقاعدة كاملة
        base_width = depth_cm
        base_length = width_cm
    else:
        # تجميع بجانبين كاملين
        base_width = depth_cm
        base_length = width_cm - (board_thickness * 2)
        
    parts.append(Part(
        name="base",  # القاعدة
        width_cm=base_width,
        height_cm=base_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((base_width * base_length) / 10000, 4)
    ))
    
    # 2. مرايه أمامية فقط (Front Mirror Only - 3 pieces)
    mirror_width = settings.mirror_width
    mirror_length = width_cm - (board_thickness * 2)
    parts.append(Part(
        name="front_mirror",  # مرايه أمامية
        width_cm=mirror_width,
        height_cm=mirror_length,
        qty=3,  # 3 قطع للحوض
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((mirror_width * mirror_length * 3) / 10000, 4)
    ))
    
    # 3. الجانبين (Side Panels)
    side_width = depth_cm
    
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # الجناب تقف فوق القاعدة
        side_height = height_cm - board_thickness
    else:
        # الجناب كاملة
        side_height = height_cm
        
    parts.append(Part(
        name="side_panel",  # الجانب
        width_cm=side_width,
        height_cm=side_height,
        qty=2,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((side_width * side_height * 2) / 10000, 4)
    ))
    
    # 4. الرفوف (Shelves)
    if shelf_count > 0:
        shelf_width = depth_cm - settings.shelf_depth_deduction
        shelf_length = width_cm - (board_thickness * 2)
        parts.append(Part(
            name="shelf",  # الرف
            width_cm=shelf_width,
            height_cm=shelf_length,
            qty=shelf_count,
            edge_distribution=EdgeDistribution(top=True, bottom=False, left=True, right=True),
            area_m2=round((shelf_width * shelf_length * shelf_count) / 10000, 4)
        ))
    
    # 5. الضلف (Doors)
    if door_count > 0:
        door_width = (width_cm / door_count) - settings.door_width_deduction_no_edge
        door_height = (
            height_cm 
            - settings.handle_profile_height 
            - settings.ground_door_height_deduction_no_edge
        )
        
        parts.append(Part(
            name="door",  # الضلفة
            width_cm=door_width,
            height_cm=door_height,
            qty=door_count,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((door_width * door_height * door_count) / 10000, 4)
        ))
    
    # ملاحظة: لا يوجد ظهر في وحدة الحوض
    
    return parts


def calculate_drawers_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    shelf_count: int,
    door_count: int,
    drawer_count: int,
    drawer_height_cm: float,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء وحدة الأدراج
    
    Args:
        width_cm: عرض الوحدة
        height_cm: ارتفاع الوحدة
        depth_cm: عمق الوحدة
        shelf_count: عدد الرفوف
        door_count: عدد الضلف
        drawer_count: عدد الأدراج
        drawer_height_cm: ارتفاع الدرج
        settings: إعدادات التقطيع
    
    Returns:
        قائمة بالأجزاء المحسوبة
    """
    parts = []
    board_thickness = DEFAULT_BOARD_THICKNESS
    
    # 1. القاعدة (Base)
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # تجميع بقاعدة كاملة
        base_width = depth_cm
        base_length = width_cm
    else:
        # تجميع بجانبين كاملين
        base_width = depth_cm
        base_length = width_cm - (board_thickness * 2)
        
    parts.append(Part(
        name="base",
        width_cm=base_width,
        height_cm=base_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((base_width * base_length) / 10000, 4)
    ))
    
    # 2. مرايه أمامية (Front Mirror)
    mirror_width = settings.mirror_width
    mirror_length = width_cm - (board_thickness * 2)
    parts.append(Part(
        name="front_mirror",
        width_cm=mirror_width,
        height_cm=mirror_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((mirror_width * mirror_length) / 10000, 4)
    ))
    
    # 3. مرايه خلفية (Back Mirror)
    parts.append(Part(
        name="back_mirror",
        width_cm=mirror_width,
        height_cm=mirror_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((mirror_width * mirror_length) / 10000, 4)
    ))
    
    # 4. الجانبين (Side Panels)
    side_width = depth_cm
    
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # الجناب تقف فوق القاعدة
        side_height = height_cm - board_thickness
    else:
        # الجناب كاملة
        side_height = height_cm

    parts.append(Part(
        name="side_panel",
        width_cm=side_width,
        height_cm=side_height,
        qty=2,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((side_width * side_height * 2) / 10000, 4)
    ))
    
    # 5. الرف (Shelf) - لا يوجد رفوف في وحدة الأدراج
    # Drawers units don't have shelves

    # 6. عرض الدرج (Drawer Width)
    # الطول = العرض - (1.8 + 1.8) - (1.8 + 1.8) - 2.6
    # العرض = ارتفاع الدرج
    # العدد = 2 * عدد الأدراج
    if drawer_count > 0:
        drawer_width_length = width_cm - (board_thickness * 2) - (board_thickness * 2) - 2.6
        drawer_width_width = drawer_height_cm
        drawer_width_qty = 2 * drawer_count
        parts.append(Part(
            name="drawer_width",  # عرض الدرج
            width_cm=drawer_width_width,
            height_cm=drawer_width_length,
            qty=drawer_width_qty,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((drawer_width_width * drawer_width_length * drawer_width_qty) / 10000, 4)
        ))
        
        # 7. عمق الدرج (Drawer Depth)
        # العرض = ارتفاع الدرج
        # الطول = العمق - 8
        # العدد = 2 * عدد الأدراج
        drawer_depth_width = drawer_height_cm
        drawer_depth_length = depth_cm - 8
        drawer_depth_qty = 2 * drawer_count
        parts.append(Part(
            name="drawer_depth",  # عمق الدرج
            width_cm=drawer_depth_width,
            height_cm=drawer_depth_length,
            qty=drawer_depth_qty,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((drawer_depth_width * drawer_depth_length * drawer_depth_qty) / 10000, 4)
        ))
        
        # 8. قاع الدرج (Drawer Bottom)
        # الطول = العمق - 8 - تخصيم الظهر
        # العرض = العرض - (1.8 + 1.8) - تخصيم الظهر - 2.6
        # العدد = عدد الأدراج
        drawer_bottom_length = depth_cm - 8 - settings.back_deduction
        drawer_bottom_width = width_cm - (board_thickness * 2) - settings.back_deduction - 2.6
        parts.append(Part(
            name="drawer_bottom",  # قاع الدرج
            width_cm=drawer_bottom_width,
            height_cm=drawer_bottom_length,
            qty=drawer_count,
            edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
            area_m2=round((drawer_bottom_width * drawer_bottom_length * drawer_count) / 10000, 4)
        ))
    
    # 9. الظهر (Back Panel)
    back_width = width_cm - settings.back_deduction
    back_height = height_cm - settings.back_deduction
    back_thickness = settings.router_thickness
    parts.append(Part(
        name="back_panel",
        width_cm=back_width,
        height_cm=back_height,
        depth_cm=back_thickness,
        qty=1,
        edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
        area_m2=round((back_width * back_height) / 10000, 4)
    ))
    
    # 10. الضلف (Doors/Fronts) - لا يوجد ضلف في وحدة الأدراج
    # Drawers units don't have doors
    
    return parts


def calculate_drawers_bottom_rail_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    shelf_count: int,
    door_count: int,
    drawer_count: int,
    drawer_height_cm: float,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء وحدة ادراج مجرة سفلية
    
    الفرق عن الأدراج العادية:
    - عرض الدرج: الطول = العرض - 8.4 (بدل - 7.2 - 2.6)
    - قاع الدرج: العرض = العرض - 6.4 (بدل - 3.6 - تخصيم - 2.6)
    """
    parts = []
    board_thickness = DEFAULT_BOARD_THICKNESS
    
    # 1. القاعدة (Base)
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # تجميع بقاعدة كاملة
        base_width = depth_cm
        base_length = width_cm
    else:
        # تجميع بجانبين كاملين
        base_width = depth_cm
        base_length = width_cm - (board_thickness * 2)
        
    parts.append(Part(
        name="base",
        width_cm=base_width,
        height_cm=base_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((base_width * base_length) / 10000, 4)
    ))
    
    # 2. مرايه أمامية (Front Mirror)
    mirror_width = settings.mirror_width
    mirror_length = width_cm - (board_thickness * 2)
    parts.append(Part(
        name="front_mirror",
        width_cm=mirror_width,
        height_cm=mirror_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((mirror_width * mirror_length) / 10000, 4)
    ))
    
    # 3. مرايه خلفية (Back Mirror)
    parts.append(Part(
        name="back_mirror",
        width_cm=mirror_width,
        height_cm=mirror_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((mirror_width * mirror_length) / 10000, 4)
    ))
    
    # 4. الجانبين (Side Panels)
    side_width = depth_cm
    
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # الجناب تقف فوق القاعدة
        side_height = height_cm - board_thickness
    else:
        # الجناب كاملة
        side_height = height_cm

    parts.append(Part(
        name="side_panel",
        width_cm=side_width,
        height_cm=side_height,
        qty=2,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((side_width * side_height * 2) / 10000, 4)
    ))
    
    # 5. الرف (Shelf) - لا يوجد رفوف في وحدة الأدراج
    # Drawers units don't have shelves

    # 6. عرض الدرج (Drawer Width) - مجرة سفلية
    # الطول = العرض - 8.4
    # العرض = ارتفاع الدرج
    # العدد = 2 * عدد الأدراج
    if drawer_count > 0:
        drawer_width_length = width_cm - 8.4
        drawer_width_width = drawer_height_cm
        drawer_width_qty = 2 * drawer_count
        parts.append(Part(
            name="drawer_width",
            width_cm=drawer_width_width,
            height_cm=drawer_width_length,
            qty=drawer_width_qty,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((drawer_width_width * drawer_width_length * drawer_width_qty) / 10000, 4)
        ))
        
        # 7. عمق الدرج (Drawer Depth)
        # العرض = ارتفاع الدرج
        # الطول = العمق - 8
        # العدد = 2 * عدد الأدراج
        drawer_depth_width = drawer_height_cm
        drawer_depth_length = depth_cm - 8
        drawer_depth_qty = 2 * drawer_count
        parts.append(Part(
            name="drawer_depth",
            width_cm=drawer_depth_width,
            height_cm=drawer_depth_length,
            qty=drawer_depth_qty,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((drawer_depth_width * drawer_depth_length * drawer_depth_qty) / 10000, 4)
        ))
        
        # 8. قاع الدرج (Drawer Bottom) - مجرة سفلية
        # الطول = العمق - 8 - تخصيم الظهر
        # العرض = العرض - 6.4
        # العدد = عدد الأدراج
        drawer_bottom_length = depth_cm - 8 - settings.back_deduction
        drawer_bottom_width = width_cm - 6.4
        parts.append(Part(
            name="drawer_bottom",
            width_cm=drawer_bottom_width,
            height_cm=drawer_bottom_length,
            qty=drawer_count,
            edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
            area_m2=round((drawer_bottom_width * drawer_bottom_length * drawer_count) / 10000, 4)
        ))
    
    # 9. الظهر (Back Panel)
    back_width = width_cm - settings.back_deduction
    back_height = height_cm - settings.back_deduction
    back_thickness = settings.router_thickness
    parts.append(Part(
        name="back_panel",
        width_cm=back_width,
        height_cm=back_height,
        depth_cm=back_thickness,
        qty=1,
        edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
        area_m2=round((back_width * back_height) / 10000, 4)
    ))
    
    # 10. الضلف (Doors/Fronts) - لا يوجد ضلف في وحدة الأدراج مجرة سفلية
    # Drawers bottom rail units don't have doors
    
    return parts


def calculate_unit_parts(
    unit_type: str,
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    shelf_count: int,
    door_count: int,
    door_type: str,
    flip_door_height: float,
    bottom_door_height: float,
    oven_height: float,
    microwave_height: float,
    vent_height: float,
    drawer_count: int,
    drawer_height_cm: float,
    fixed_part_cm: float,
    width_2_cm: float,
    depth_2_cm: float,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء الوحدة بناءً على نوعها
    
    Args:
        unit_type: نوع الوحدة
        width_cm: العرض
        height_cm: الارتفاع
        depth_cm: العمق
        shelf_count: عدد الرفوف
        door_count: عدد الضلف
        door_type: نوع الضلفة (hinged/flip)
        flip_door_height: ارتفاع ضلفة القلاب
        bottom_door_height: ارتفاع الضلفة السفلية
        oven_height: ارتفاع الفرن
        microwave_height: ارتفاع الميكرويف
        vent_height: ارتفاع الهواية
        drawer_count: عدد الأدراج
        drawer_height_cm: ارتفاع الدرج
        fixed_part_cm: الجزء الثابت
        width_2_cm: العرض 2 (للركنة)
        depth_2_cm: العمق 2 (للركنة)
        settings: الإعدادات
    
    Returns:
        قائمة الأجزاء المحسوبة
    """
    if unit_type == "ground":
        return calculate_ground_unit(
            width_cm, height_cm, depth_cm, shelf_count, door_count, settings
        )
    elif unit_type == "sink":
        return calculate_sink_unit(
            width_cm, height_cm, depth_cm, shelf_count, door_count, settings
        )
    elif unit_type == "wall":
        return calculate_wall_unit(
            width_cm, height_cm, depth_cm, shelf_count, door_count, door_type, settings
        )
    elif unit_type == "drawers":
        return calculate_drawers_unit(
            width_cm, height_cm, depth_cm, shelf_count, door_count,
            drawer_count, drawer_height_cm, settings
        )
    elif unit_type == "drawers_bottom_rail":
        return calculate_drawers_bottom_rail_unit(
            width_cm, height_cm, depth_cm, shelf_count, door_count,
            drawer_count, drawer_height_cm, settings
        )
    elif unit_type == "ground_fixed":
        return calculate_ground_fixed_unit(
            width_cm, height_cm, depth_cm, shelf_count, door_count,
            fixed_part_cm, settings
        )
    elif unit_type == "sink_fixed":
        return calculate_sink_fixed_unit(
            width_cm, height_cm, depth_cm, shelf_count, door_count,
            fixed_part_cm, settings
        )
    elif unit_type == "wall_fixed":
        return calculate_wall_fixed_unit(
            width_cm, height_cm, depth_cm, shelf_count, door_count,
            fixed_part_cm, settings
        )
    elif unit_type == "wall_flip_top_doors_bottom":
        return calculate_wall_flip_top_doors_bottom_unit(
            width_cm, height_cm, depth_cm, shelf_count, door_count,
            flip_door_height, settings
        )
    elif unit_type == "tall_doors":
        return calculate_tall_doors_unit(
            width_cm, height_cm, depth_cm, shelf_count, door_count,
            bottom_door_height, settings
        )
    elif unit_type == "tall_doors_appliances":
        return calculate_tall_doors_appliances_unit(
            width_cm, height_cm, depth_cm, shelf_count, door_count, door_type,
            bottom_door_height, oven_height, microwave_height, vent_height, settings
        )
    elif unit_type == "corner_l_wall":
        return calculate_corner_l_wall_unit(
            width_cm, width_2_cm, height_cm, depth_cm, depth_2_cm,
            shelf_count, settings
        )
    elif unit_type == "tall_drawers_side_doors_top":
        return calculate_tall_drawers_side_doors_top_unit(
            width_cm, height_cm, depth_cm, shelf_count, door_count, door_type,
            drawer_count, drawer_height_cm, bottom_door_height, settings
        )
    
    # TODO: إضافة باقي أنواع الوحدات
    else:
        raise ValueError(f"Unit type '{unit_type}' not implemented yet")


def calculate_total_edge_band(parts: List[Part]) -> float:
    """حساب إجمالي متر الشريط"""
    return sum(part.edge_band_m or 0 for part in parts)


def calculate_total_area(parts: List[Part]) -> float:
    """حساب إجمالي المساحة بالمتر المربع"""
    return sum(part.area_m2 or 0 for part in parts)


def calculate_material_usage(
    total_area_m2: float,
    edge_band_m: float,
    settings: SettingsModel
) -> Dict[str, float]:
    """
    حساب استخدام المواد
    
    Returns:
        Dict with material usage
    """
    return {
        "المساحة الإجمالية": round(total_area_m2, 4),
        "شريط الحافة": round(edge_band_m, 2)
    }

def calculate_ground_fixed_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    shelf_count: int,
    door_count: int,
    fixed_part_cm: float,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء وحدة ارضي ثابت
    
    Args:
        width_cm: عرض الوحدة
        height_cm: ارتفاع الوحدة
        depth_cm: عمق الوحدة
        shelf_count: عدد الرفوف
        door_count: عدد الضلف
        fixed_part_cm: الجزء الثابت بالسنتيمتر
        settings: إعدادات التقطيع
    
    Returns:
        قائمة بالأجزاء المحسوبة
    """
    parts = []
    board_thickness = DEFAULT_BOARD_THICKNESS
    
    # 1. القاعدة (Base)
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # تجميع بقاعدة كاملة
        base_width = depth_cm
        base_length = width_cm
    else:
        # تجميع بجانبين كاملين
        base_width = depth_cm
        base_length = width_cm - (board_thickness * 2)
        
    parts.append(Part(
        name="base",
        width_cm=base_width,
        height_cm=base_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((base_width * base_length) / 10000, 4)
    ))
    
    # 2. مرايا أمامية (Front Mirror)
    mirror_width = settings.mirror_width
    mirror_length = width_cm - (board_thickness * 2)
    parts.append(Part(
        name="front_mirror",
        width_cm=mirror_width,
        height_cm=mirror_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((mirror_width * mirror_length) / 10000, 4)
    ))
    
    # 3. مرايا خلفية (Back Mirror)
    parts.append(Part(
        name="back_mirror",
        width_cm=mirror_width,
        height_cm=mirror_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((mirror_width * mirror_length) / 10000, 4)
    ))
    
    # 4. الجانبين (Side Panels)
    side_width = depth_cm
    
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # الجناب تقف فوق القاعدة
        side_height = height_cm - board_thickness
    else:
        # الجناب كاملة
        side_height = height_cm

    parts.append(Part(
        name="side_panel",
        width_cm=side_width,
        height_cm=side_height,
        qty=2,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((side_width * side_height * 2) / 10000, 4)
    ))
    
    # 5. الرف (Shelf)
    if shelf_count > 0:
        shelf_width = depth_cm - settings.shelf_depth_deduction
        shelf_length = width_cm - (board_thickness * 2)
        parts.append(Part(
            name="shelf",
            width_cm=shelf_width,
            height_cm=shelf_length,
            qty=shelf_count,
            edge_distribution=EdgeDistribution(top=True, bottom=False, left=True, right=True),
            area_m2=round((shelf_width * shelf_length * shelf_count) / 10000, 4)
        ))
    
    # 6. مرايا التركيب المفصلة (Detailed Installation Mirror)
    # الطول = الارتفاع - سمك الجانبين (1.8 + 1.8)
    detailed_mirror_length = height_cm - (board_thickness * 2)
    parts.append(Part(
        name="detailed_installation_mirror",
        width_cm=mirror_width,
        height_cm=detailed_mirror_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((mirror_width * detailed_mirror_length) / 10000, 4)
    ))
    
    # 7. الجزء الثابت (Fixed Part)
    # العرض = الجزء الثابت - 4.5
    fixed_part_width = fixed_part_cm - 4.5
    fixed_part_height = height_cm
    parts.append(Part(
        name="fixed_part",
        width_cm=fixed_part_width,
        height_cm=fixed_part_height,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((fixed_part_width * fixed_part_height) / 10000, 4)
    ))
    
    # 8. الظهر (Back Panel)
    back_width = width_cm - settings.back_deduction
    back_height = height_cm - settings.back_deduction
    back_thickness = settings.router_thickness
    parts.append(Part(
        name="back_panel",
        width_cm=back_width,
        height_cm=back_height,
        depth_cm=back_thickness,
        qty=1,
        edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
        area_m2=round((back_width * back_height) / 10000, 4)
    ))
    
    # 9. الضلف (Doors)
    if door_count > 0:
        # العرض = ((العرض - الجزء الثابت - 3) / عدد الضلف) - تخصيم عرض الضلفة
        door_width = ((width_cm - fixed_part_cm - 3) / door_count) - settings.door_width_deduction_no_edge
        # الطول = الارتفاع - ارتفاع قطاع المقبض
        door_height = height_cm - settings.handle_profile_height
        
        parts.append(Part(
            name="door",
            width_cm=door_width,
            height_cm=door_height,
            qty=door_count,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((door_width * door_height * door_count) / 10000, 4)
        ))
    
    # 10. فيلر (Filler)
    filler_width = mirror_width
    filler_height = height_cm
    parts.append(Part(
        name="filler",
        width_cm=filler_width,
        height_cm=filler_height,
        qty=2,  # قطعتين
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((filler_width * filler_height * 2) / 10000, 4)
    ))
    
    return parts


def calculate_sink_fixed_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    shelf_count: int,
    door_count: int,
    fixed_part_cm: float,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء وحدة حوض ثابت
    
    الفرق عن الأرضي الثابت:
    - مرايا أمامية: 3 قطع (بدل 1)
    - بدون ظهر (لوجود الحوض)
    
    Args:
        width_cm: عرض الوحدة
        height_cm: ارتفاع الوحدة
        depth_cm: عمق الوحدة
        shelf_count: عدد الرفوف
        door_count: عدد الضلف
        fixed_part_cm: الجزء الثابت بالسنتيمتر
        settings: إعدادات التقطيع
    
    Returns:
        قائمة بالأجزاء المحسوبة
    """
    parts = []
    board_thickness = DEFAULT_BOARD_THICKNESS
    
    # 1. القاعدة (Base)
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # تجميع بقاعدة كاملة
        base_width = depth_cm
        base_length = width_cm
    else:
        # تجميع بجانبين كاملين
        base_width = depth_cm
        base_length = width_cm - (board_thickness * 2)
        
    parts.append(Part(
        name="base",
        width_cm=base_width,
        height_cm=base_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((base_width * base_length) / 10000, 4)
    ))
    
    # 2. مرايا أمامية (Front Mirror) - 3 قطع للحوض الثابت
    mirror_width = settings.mirror_width
    mirror_length = width_cm - (board_thickness * 2)
    parts.append(Part(
        name="front_mirror",
        width_cm=mirror_width,
        height_cm=mirror_length,
        qty=3,  # 3 قطع للحوض الثابت
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((mirror_width * mirror_length * 3) / 10000, 4)
    ))
    
    # 3. الجانبين (Side Panels)
    side_width = depth_cm
    
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # الجناب تقف فوق القاعدة
        side_height = height_cm - board_thickness
    else:
        # الجناب كاملة
        side_height = height_cm
    parts.append(Part(
        name="side_panel",
        width_cm=side_width,
        height_cm=side_height,
        qty=2,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((side_width * side_height * 2) / 10000, 4)
    ))
    
    # 4. الرف (Shelf)
    if shelf_count > 0:
        shelf_width = depth_cm - settings.shelf_depth_deduction
        shelf_length = width_cm - (board_thickness * 2)
        parts.append(Part(
            name="shelf",
            width_cm=shelf_width,
            height_cm=shelf_length,
            qty=shelf_count,
            edge_distribution=EdgeDistribution(top=True, bottom=False, left=True, right=True),
            area_m2=round((shelf_width * shelf_length * shelf_count) / 10000, 4)
        ))
    
    # 5. مرايا التركيب المفصلة (Detailed Installation Mirror)
    detailed_mirror_length = height_cm - (board_thickness * 2)
    parts.append(Part(
        name="detailed_installation_mirror",
        width_cm=mirror_width,
        height_cm=detailed_mirror_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((mirror_width * detailed_mirror_length) / 10000, 4)
    ))
    
    # 6. الجزء الثابت (Fixed Part)
    fixed_part_width = fixed_part_cm - 4.5
    fixed_part_height = height_cm
    parts.append(Part(
        name="fixed_part",
        width_cm=fixed_part_width,
        height_cm=fixed_part_height,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((fixed_part_width * fixed_part_height) / 10000, 4)
    ))
    
    # 7. الضلف (Doors)
    if door_count > 0:
        # العرض = ((العرض - الجزء الثابت - 3) / عدد الضلف) - تخصيم عرض الضلفة
        door_width = ((width_cm - fixed_part_cm - 3) / door_count) - settings.door_width_deduction_no_edge
        # الطول = الارتفاع - ارتفاع قطاع المقبض
        door_height = height_cm - settings.handle_profile_height
        
        parts.append(Part(
            name="door",
            width_cm=door_width,
            height_cm=door_height,
            qty=door_count,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((door_width * door_height * door_count) / 10000, 4)
        ))
    
    # 8. فيلر (Filler)
    filler_width = mirror_width
    filler_height = height_cm
    parts.append(Part(
        name="filler",
        width_cm=filler_width,
        height_cm=filler_height,
        qty=2,  # قطعتين
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((filler_width * filler_height * 2) / 10000, 4)
    ))
    
    # ملاحظة: لا يوجد ظهر في وحدة الحوض الثابت
    
    return parts


def calculate_wall_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    shelf_count: int,
    door_count: int,
    door_type: str,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء الوحدة العلوية
    
    Args:
        width_cm: عرض الوحدة
        height_cm: ارتفاع الوحدة
        depth_cm: عمق الوحدة
        shelf_count: عدد الرفوف
        door_count: عدد الضلف
        door_type: نوع الضلفة (hinged/flip)
        settings: إعدادات التقطيع
    
    Returns:
        قائمة بالأجزاء المحسوبة
    """
    parts = []
    board_thickness = DEFAULT_BOARD_THICKNESS
    
    # 1. القاعدة (Base)
    base_width = depth_cm
    base_length = width_cm - (board_thickness * 2)
    parts.append(Part(
        name="base",
        width_cm=base_width,
        height_cm=base_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((base_width * base_length) / 10000, 4)
    ))
    
    # 2. برنيطة / سقف الوحدة (Top/Ceiling)
    # العرض = العمق - مقبض الشاسية
    top_width = depth_cm - settings.chassis_handle_drop
    top_length = width_cm - (board_thickness * 2)
    parts.append(Part(
        name="top_ceiling",  # برنيطة
        width_cm=top_width,
        height_cm=top_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((top_width * top_length) / 10000, 4)
    ))
    
    # 3. الجانبين (Side Panels)
    side_width = depth_cm
    side_height = height_cm
    parts.append(Part(
        name="side_panel",
        width_cm=side_width,
        height_cm=side_height,
        qty=2,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((side_width * side_height * 2) / 10000, 4)
    ))
    
    # 4. الرف (Shelf)
    if shelf_count > 0:
        shelf_width = depth_cm - settings.shelf_depth_deduction
        shelf_length = width_cm - (board_thickness * 2)
        parts.append(Part(
            name="shelf",
            width_cm=shelf_width,
            height_cm=shelf_length,
            qty=shelf_count,
            edge_distribution=EdgeDistribution(top=True, bottom=False, left=True, right=True),
            area_m2=round((shelf_width * shelf_length * shelf_count) / 10000, 4)
        ))
    
    # 5. الظهر (Back Panel)
    back_width = width_cm - settings.back_deduction
    back_height = height_cm - settings.back_deduction
    back_thickness = settings.router_thickness
    parts.append(Part(
        name="back_panel",
        width_cm=back_width,
        height_cm=back_height,
        depth_cm=back_thickness,
        qty=1,
        edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
        area_m2=round((back_width * back_height) / 10000, 4)
    ))
    
    # 6. الضلف (Doors)
    if door_count > 0:
        if door_type == "hinged" or door_type == DoorType.HINGED:
            # ضلف مفصلي
            door_width = (width_cm / door_count) - settings.door_width_deduction_no_edge
            door_height = height_cm - settings.handle_profile_height
            parts.append(Part(
                name="door_hinged",  # ضلفة مفصلي
                width_cm=door_width,
                height_cm=door_height,
                qty=door_count,
                edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
                area_m2=round((door_width * door_height * door_count) / 10000, 4)
            ))
        else:  # flip
            # ضلف قلاب
            door_width = width_cm - settings.door_width_deduction_no_edge
            door_height = (height_cm / door_count) - settings.handle_profile_height - 0.5
            parts.append(Part(
                name="door_flip",  # ضلفة قلاب
                width_cm=door_width,
                height_cm=door_height,
                qty=door_count,
                edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
                area_m2=round((door_width * door_height * door_count) / 10000, 4)
            ))
    
    return parts


def calculate_wall_fixed_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    shelf_count: int,
    door_count: int,
    fixed_part_cm: float,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء وحدة علوي ثابت
    
    Args:
        width_cm: عرض الوحدة
        height_cm: ارتفاع الوحدة
        depth_cm: عمق الوحدة
        shelf_count: عدد الرفوف
        door_count: عدد الضلف
        fixed_part_cm: الجزء الثابت بالسنتيمتر
        settings: إعدادات التقطيع
    
    Returns:
        قائمة بالأجزاء المحسوبة
    """
    parts = []
    board_thickness = DEFAULT_BOARD_THICKNESS
    
    # 1. القاعدة (Base)
    base_width = depth_cm
    base_length = width_cm - (board_thickness * 2)
    parts.append(Part(
        name="base",
        width_cm=base_width,
        height_cm=base_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((base_width * base_length) / 10000, 4)
    ))
    
    # 2. برنيطة / سقف الوحدة (Top/Ceiling)
    # العرض = العمق (بدون تخصيم مقبض الشاسية في الثابت)
    top_width = depth_cm
    top_length = width_cm - (board_thickness * 2)
    parts.append(Part(
        name="top_ceiling",  # برنيطة
        width_cm=top_width,
        height_cm=top_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((top_width * top_length) / 10000, 4)
    ))
    
    # 3. الجانبين (Side Panels)
    side_width = depth_cm
    side_height = height_cm
    parts.append(Part(
        name="side_panel",
        width_cm=side_width,
        height_cm=side_height,
        qty=2,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((side_width * side_height * 2) / 10000, 4)
    ))
    
    # 4. الرف (Shelf)
    if shelf_count > 0:
        shelf_width = depth_cm - settings.shelf_depth_deduction
        shelf_length = width_cm - (board_thickness * 2)
        parts.append(Part(
            name="shelf",
            width_cm=shelf_width,
            height_cm=shelf_length,
            qty=shelf_count,
            edge_distribution=EdgeDistribution(top=True, bottom=False, left=True, right=True),
            area_m2=round((shelf_width * shelf_length * shelf_count) / 10000, 4)
        ))
    
    # 5. مرايا التركيب المفصلة (Detailed Installation Mirror)
    mirror_width = settings.mirror_width
    detailed_mirror_length = height_cm - (board_thickness * 2)
    parts.append(Part(
        name="detailed_installation_mirror",
        width_cm=mirror_width,
        height_cm=detailed_mirror_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((mirror_width * detailed_mirror_length) / 10000, 4)
    ))
    
    # 6. الجزء الثابت (Fixed Part)
    fixed_part_width = fixed_part_cm - 4.5
    fixed_part_height = height_cm
    parts.append(Part(
        name="fixed_part",
        width_cm=fixed_part_width,
        height_cm=fixed_part_height,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((fixed_part_width * fixed_part_height) / 10000, 4)
    ))
    
    # 7. الظهر (Back Panel)
    back_width = width_cm - settings.back_deduction
    back_height = height_cm - settings.back_deduction
    back_thickness = settings.router_thickness
    parts.append(Part(
        name="back_panel",
        width_cm=back_width,
        height_cm=back_height,
        depth_cm=back_thickness,
        qty=1,
        edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
        area_m2=round((back_width * back_height) / 10000, 4)
    ))
    
    # 8. الضلف (Doors)
    if door_count > 0:
        # العرض = ((العرض - الجزء الثابت - 3) / عدد الضلف) - تخصيم عرض الضلفة
        door_width = ((width_cm - fixed_part_cm - 3) / door_count) - settings.door_width_deduction_no_edge
        # الطول = الارتفاع - ارتفاع قطاع المقبض
        door_height = height_cm - settings.handle_profile_height
        
        parts.append(Part(
            name="door",
            width_cm=door_width,
            height_cm=door_height,
            qty=door_count,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((door_width * door_height * door_count) / 10000, 4)
        ))
    
    # 9. فيلر (Filler)
    filler_width = mirror_width
    filler_height = height_cm
    parts.append(Part(
        name="filler",
        width_cm=filler_width,
        height_cm=filler_height,
        qty=2,  # قطعتين
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((filler_width * filler_height * 2) / 10000, 4)
    ))
    
    return parts

def calculate_wall_flip_top_doors_bottom_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    shelf_count: int,
    door_count: int,
    flip_door_height: float,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء وحدة علوية ضلفة قلاب + ضلفة سفلية
    
    Args:
        width_cm: عرض الوحدة
        height_cm: ارتفاع الوحدة
        depth_cm: عمق الوحدة
        shelf_count: عدد الرفوف
        door_count: عدد الضلف السفلية
        flip_door_height: ارتفاع ضلفة القلاب
        settings: إعدادات التقطيع
    
    Returns:
        قائمة بالأجزاء المحسوبة
    """
    parts = []
    board_thickness = DEFAULT_BOARD_THICKNESS
    
    # 1. القاعدة (Base)
    # العرض = العمق، الطول = العرض - (سمك الجنبين)
    base_width = depth_cm
    base_length = width_cm - (board_thickness * 2)
    parts.append(Part(
        name="base",
        width_cm=base_width,
        height_cm=base_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((base_width * base_length) / 10000, 4)
    ))
    
    # 2. برنيطة / سقف الوحدة (Top/Ceiling)
    # العرض = العمق - مقبض الشاسية
    top_width = depth_cm - settings.chassis_handle_drop
    top_length = width_cm - (board_thickness * 2)
    parts.append(Part(
        name="top_ceiling",  # برنيطة
        width_cm=top_width,
        height_cm=top_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((top_width * top_length) / 10000, 4)
    ))
    
    # 3. الجانبين (Side Panels)
    side_width = depth_cm
    side_height = height_cm
    parts.append(Part(
        name="side_panel",
        width_cm=side_width,
        height_cm=side_height,
        qty=2,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((side_width * side_height * 2) / 10000, 4)
    ))
    
    # 4. الرف (Shelf)
    if shelf_count > 0:
        shelf_width = depth_cm - settings.shelf_depth_deduction
        shelf_length = width_cm - (board_thickness * 2)
        parts.append(Part(
            name="shelf",
            width_cm=shelf_width,
            height_cm=shelf_length,
            qty=shelf_count,
            edge_distribution=EdgeDistribution(top=True, bottom=False, left=True, right=True),
            area_m2=round((shelf_width * shelf_length * shelf_count) / 10000, 4)
        ))
    
    # 5. الرف الإضافي (Extra Shelf)
    # العرض = العمق - بعد المفحار - سمك المفحار - 0.2
    # الطول = العرض - سمك الجانبين
    extra_shelf_width = depth_cm - settings.router_distance - settings.router_thickness - 0.2
    extra_shelf_length = width_cm - (board_thickness * 2)
    parts.append(Part(
        name="extra_shelf",  # الرف الإضافي
        width_cm=extra_shelf_width,
        height_cm=extra_shelf_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=False, left=True, right=True),
        area_m2=round((extra_shelf_width * extra_shelf_length) / 10000, 4)
    ))
    
    # 6. الظهر (Back Panel)
    back_width = width_cm - settings.back_deduction
    back_height = height_cm - settings.back_deduction
    back_thickness = settings.router_thickness
    parts.append(Part(
        name="back_panel",
        width_cm=back_width,
        height_cm=back_height,
        depth_cm=back_thickness,
        qty=1,
        edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
        area_m2=round((back_width * back_height) / 10000, 4)
    ))
    
    # 7. الضلف السفلية (Bottom Doors)
    if door_count > 0:
        # العرض = (العرض / عدد الضلف) - تخصيم عرض الضلفة
        door_width = (width_cm / door_count) - settings.door_width_deduction_no_edge
        # الطول = الارتفاع - ارتفاع قطاع المقبض - ارتفاع ضلفة القلاب - 0.5
        door_height = height_cm - settings.handle_profile_height - flip_door_height - 0.5
        
        parts.append(Part(
            name="bottom_door",  # ضلفة سفلية
            width_cm=door_width,
            height_cm=door_height,
            qty=door_count,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((door_width * door_height * door_count) / 10000, 4)
        ))
    
    # 8. الضلفة القلاب (Flip Door)
    # العرض = العرض - تخصيم عرض الضلفة
    flip_door_width = width_cm - settings.door_width_deduction_no_edge
    # الطول = ارتفاع ضلفة القلاب - ارتفاع قطاع المقبض - 2.0
    flip_door_calculated_height = flip_door_height - settings.handle_profile_height - 2.0
    
    parts.append(Part(
        name="flip_door",  # ضلفة قلاب
        width_cm=flip_door_width,
        height_cm=flip_door_calculated_height,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((flip_door_width * flip_door_calculated_height) / 10000, 4)
    ))
    
    return parts

def calculate_tall_doors_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    shelf_count: int,
    door_count: int,
    bottom_door_height: float,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء وحدة دولاب ضلفة سفلية وعلوي ضلفة
    
    Args:
        width_cm: عرض الوحدة
        height_cm: ارتفاع الوحدة
        depth_cm: عمق الوحدة
        shelf_count: عدد الرفوف
        door_count: عدد الضلف
        bottom_door_height: ارتفاع الضلفة السفلية
        settings: إعدادات التقطيع
    
    Returns:
        قائمة بالأجزاء المحسوبة
    """
    parts = []
    board_thickness = DEFAULT_BOARD_THICKNESS
    
    # 1. القاعدة (Base)
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # تجميع بقاعدة كاملة وسقف كامل
        base_width = depth_cm
        base_length = width_cm
    else:
        # تجميع بجانبين كاملين
        base_width = depth_cm
        base_length = width_cm - (board_thickness * 2)
        
    parts.append(Part(
        name="base",
        width_cm=base_width,
        height_cm=base_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((base_width * base_length) / 10000, 4)
    ))
    
    # 2. برنيطة / سقف الوحدة (Top/Ceiling)
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # سقف كامل
        top_width = depth_cm
        top_length = width_cm
    else:
        # سقف بين الجنبين
        top_width = depth_cm
        top_length = width_cm - (board_thickness * 2)
        
    parts.append(Part(
        name="top_ceiling",
        width_cm=top_width,
        height_cm=top_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((top_width * top_length) / 10000, 4)
    ))
    
    # 3. الجانبين (Side Panels)
    side_width = depth_cm
    
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # الجناب بين القاعدة والسقف
        side_height = height_cm - (board_thickness * 2)
    else:
        # الجناب كاملة
        side_height = height_cm

    parts.append(Part(
        name="side_panel",
        width_cm=side_width,
        height_cm=side_height,
        qty=2,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((side_width * side_height * 2) / 10000, 4)
    ))
    
    # 4. الرفوف (Shelves)
    if shelf_count > 0:
        shelf_width = depth_cm - settings.shelf_depth_deduction
        shelf_length = width_cm - (board_thickness * 2)
        parts.append(Part(
            name="shelf",
            width_cm=shelf_width,
            height_cm=shelf_length,
            qty=shelf_count,
            edge_distribution=EdgeDistribution(top=True, bottom=False, left=True, right=True),
            area_m2=round((shelf_width * shelf_length * shelf_count) / 10000, 4)
        ))
    
    # 5. الرف الإضافي (Extra Shelf)
    # العرض = العمق - بعد المفحار - سمك المفحار - 0.2
    # الطول = العرض - سمك الجانبين
    extra_shelf_width = depth_cm - settings.router_distance - settings.router_thickness - 0.2
    extra_shelf_length = width_cm - (board_thickness * 2)
    parts.append(Part(
        name="extra_shelf",
        width_cm=extra_shelf_width,
        height_cm=extra_shelf_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=False, left=True, right=True),
        area_m2=round((extra_shelf_width * extra_shelf_length) / 10000, 4)
    ))
    
    # 6. الظهر (Back Panel)
    back_width = width_cm - settings.back_deduction
    back_height = height_cm - settings.back_deduction
    back_thickness = settings.router_thickness
    parts.append(Part(
        name="back_panel",
        width_cm=back_width,
        height_cm=back_height,
        depth_cm=back_thickness,
        qty=1,
        edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
        area_m2=round((back_width * back_height) / 10000, 4)
    ))
    
    # 7. الأبواب
    if door_count > 0:
        door_width = (width_cm / door_count) - settings.door_width_deduction_no_edge
        
        # الضلفة السفلية (Bottom Door)
        # الطول = ارتفاع السفلية - تخصيم السفلية - ارتفاع المقبض
        bottom_door_calc_height = (
            bottom_door_height
            - settings.ground_door_height_deduction_no_edge
            - settings.handle_profile_height
        )
        parts.append(Part(
            name="bottom_door",
            width_cm=door_width,
            height_cm=bottom_door_calc_height,
            qty=door_count,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((door_width * bottom_door_calc_height * door_count) / 10000, 4)
        ))
        
        # الضلفة العلوية (Top Door)
        # الطول = الارتفاع الكلي - ارتفاع السفلية - ارتفاع المقبض - 0.5 (استخدمت 0.5 بدلاً من 5 للمنطقية، لو 5 سم اكتبها 5.0)
        # المستخدم كتب "5" -> هفترض 0.5 سم فواصل، لو 5 سم يبقى large gap
        # المعادلة المكتوبة: الارتفاع - ارتفاع الضلفة العلوية (المقصود السفلية هنا لتكملة الباقي) - مقبض - 0.5
        top_door_calc_height = (
            height_cm
            - bottom_door_height
            - settings.handle_profile_height
        )
        parts.append(Part(
            name="top_door",
            width_cm=door_width,
            height_cm=top_door_calc_height,
            qty=door_count,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((door_width * top_door_calc_height * door_count) / 10000, 4)
        ))
    
    return parts

def calculate_corner_l_wall_unit(
    width_cm: float,
    width_2_cm: float,
    height_cm: float,
    depth_cm: float,
    depth_2_cm: float,
    shelf_count: int,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء وحدة ركنة حرف L (علوي)
    
    Args:
        width_cm: عرض 1
        width_2_cm: عرض 2
        height_cm: الارتفاع
        depth_cm: عمق 1
        depth_2_cm: عمق 2
        shelf_count: عدد الرفوف
        settings: إعدادات التقطيع
    
    Returns:
        قائمة بالأجزاء المحسوبة
    """
    parts = []
    board_thickness = DEFAULT_BOARD_THICKNESS
    
    # التحقق من القيم الافتراضية
    w1 = width_cm
    w2 = width_2_cm if width_2_cm > 0 else width_cm
    d1 = depth_cm
    d2 = depth_2_cm if depth_2_cm > 0 else depth_cm
    
    # 1. القاعدة (Base)
    # العرض = عرض 1 - سمك الجنب
    # الطول = عرض 2 - سمك الجنب
    base_width = w1 - board_thickness
    base_length = w2 - board_thickness
    parts.append(Part(
        name="base",
        width_cm=base_width,
        height_cm=base_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((base_width * base_length) / 10000, 4)
    ))
    
    # 2. برنيطة / سقف الوحدة (Top/Ceiling)
    # العرض = عرض 1 - سمك الجنب
    # الطول = عرض 2 - سمك الجنب
    top_width = w1 - board_thickness
    top_length = w2 - board_thickness
    parts.append(Part(
        name="top_ceiling",
        width_cm=top_width,
        height_cm=top_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((top_width * top_length) / 10000, 4)
    ))
    
    # 3. جنب 1 (Side 1)
    # العرض = عمق 1
    # الطول = الارتفاع
    side1_width = d1
    side1_height = height_cm
    parts.append(Part(
        name="side_1",
        width_cm=side1_width,
        height_cm=side1_height,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((side1_width * side1_height) / 10000, 4)
    ))
    
    # 4. جنب 2 (Side 2)
    # العرض = عمق 2
    # الطول = الارتفاع
    side2_width = d2
    side2_height = height_cm
    parts.append(Part(
        name="side_2",
        width_cm=side2_width,
        height_cm=side2_height,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((side2_width * side2_height) / 10000, 4)
    ))
    
    # 5. الرف (Shelf)
    if shelf_count > 0:
        # العرض = عرض 1 - سمك الجنب - بعد المفحار - سمك المفحار
        shelf_width = w1 - board_thickness - settings.router_distance - settings.router_thickness
        # الطول = عرض 2 - سمك الجنب - بعد المفحار - سمك المفحار
        shelf_length = w2 - board_thickness - settings.router_distance - settings.router_thickness
        
        parts.append(Part(
            name="shelf",
            width_cm=shelf_width,
            height_cm=shelf_length,
            qty=shelf_count,
            edge_distribution=EdgeDistribution(top=True, bottom=False, left=True, right=True),
            area_m2=round((shelf_width * shelf_length * shelf_count) / 10000, 4)
        ))
    
    # 6. ظهر 1 (Back 1)
    # العرض = عرض 1 - تخصيم الظهر
    # الطول = الارتفاع - تخصيم الظهر
    back1_width = w1 - settings.back_deduction
    back1_height = height_cm - settings.back_deduction
    back_thickness = settings.router_thickness
    
    parts.append(Part(
        name="back_1",
        width_cm=back1_width,
        height_cm=back1_height,
        depth_cm=back_thickness,
        qty=1,
        edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
        area_m2=round((back1_width * back1_height) / 10000, 4)
    ))
    
    # 7. ظهر 2 (Back 2)
    # العرض = عرض 2 - بعد المفحار - سمك المفحار - 5
    # الطول = الارتفاع - تخصيم الظهر
    back2_width = w2 - settings.router_distance - settings.router_thickness - 5
    back2_height = height_cm - settings.back_deduction
    
    parts.append(Part(
        name="back_2",
        width_cm=back2_width,
        height_cm=back2_height,
        depth_cm=back_thickness,
        qty=1,
        edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
        area_m2=round((back2_width * back2_height) / 10000, 4)
    ))
    
    # 8. ضلفة 1 (Door 1)
    # العرض = عرض 1 - عمق 1 - 2.3
    # الطول = الارتفاع - ارتفاع قطاع المقبض
    door1_width = w1 - d1 - 2.3
    door1_height = height_cm - settings.handle_profile_height
    
    parts.append(Part(
        name="door_1",
        width_cm=door1_width,
        height_cm=door1_height,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((door1_width * door1_height) / 10000, 4)
    ))
    
    # 9. ضلفة قلاب (Flip Door)
    # العرض = عرض 2 - عمق 2 - 1.2
    # الطول = الارتفاع - ارتفاع قطاع المقبض
    flip_width = w2 - d2 - 1.2
    flip_height = height_cm - settings.handle_profile_height
    
    parts.append(Part(
        name="flip_door",
        width_cm=flip_width,
        height_cm=flip_height,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((flip_width * flip_height) / 10000, 4)
    ))
    
    return parts

def calculate_tall_doors_appliances_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    shelf_count: int,
    door_count: int,
    door_type: str,
    bottom_door_height: float,
    oven_height: float,
    microwave_height: float,
    vent_height: float,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء وحدة دولاب ضلف + أجهزة
    
    Args:
        width_cm: عرض الوحدة
        height_cm: ارتفاع الوحدة
        depth_cm: عمق الوحدة
        shelf_count: عدد الرفوف (العادية)
        door_count: عدد الضلف
        door_type: نوع الضلفة العلوية (hinged/flip)
        bottom_door_height: ارتفاع الضلفة السفلية
        oven_height: ارتفاع الفرن
        microwave_height: ارتفاع الميكرويف
        vent_height: ارتفاع الهواية
        settings: إعدادات التقطيع
    
    Returns:
        قائمة بالأجزاء المحسوبة
    """
    parts = []
    board_thickness = DEFAULT_BOARD_THICKNESS
    
    # 1. القاعدة (Base)
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # تجميع بقاعدة كاملة وسقف كامل
        base_width = depth_cm
        base_length = width_cm
    else:
        # تجميع بجانبين كاملين
        base_width = depth_cm
        base_length = width_cm - (board_thickness * 2)
        
    parts.append(Part(
        name="base",
        width_cm=base_width,
        height_cm=base_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((base_width * base_length) / 10000, 4)
    ))
    
    # 2. برنيطة / سقف الوحدة (Top/Ceiling)
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # سقف كامل
        top_width = depth_cm
        top_length = width_cm
    else:
        # سقف بين الجنبين
        top_width = depth_cm
        top_length = width_cm - (board_thickness * 2)
        
    parts.append(Part(
        name="top_ceiling",
        width_cm=top_width,
        height_cm=top_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((top_width * top_length) / 10000, 4)
    ))
    
    # 3. جنب 1 (Side 1)
    side_width = depth_cm
    
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # الجناب بين القاعدة والسقف
        side_height = height_cm - (board_thickness * 2)
    else:
        # الجناب كاملة
        side_height = height_cm

    parts.append(Part(
        name="side_1",
        width_cm=side_width,
        height_cm=side_height,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((side_width * side_height) / 10000, 4)
    ))
    
    # 4. جنب 2 (Side 2)
    parts.append(Part(
        name="side_2",
        width_cm=side_width,
        height_cm=side_height,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((side_width * side_height) / 10000, 4)
    ))
    
    # 5. الرفوف العادية (Regular Shelves)
    if shelf_count > 0:
        shelf_width = depth_cm - settings.shelf_depth_deduction
        shelf_length = width_cm - (board_thickness * 2)
        parts.append(Part(
            name="shelf",
            width_cm=shelf_width,
            height_cm=shelf_length,
            qty=shelf_count,
            edge_distribution=EdgeDistribution(top=True, bottom=False, left=True, right=True),
            area_m2=round((shelf_width * shelf_length * shelf_count) / 10000, 4)
        ))
    
    # 6. أرفف الأجهزة (Appliance Shelves) - العدد 3
    appliance_shelf_count = 3
    app_shelf_width = depth_cm - settings.router_distance - settings.router_thickness
    app_shelf_length = width_cm - (board_thickness * 2)
    parts.append(Part(
        name="appliance_shelf",
        width_cm=app_shelf_width,
        height_cm=app_shelf_length,
        qty=appliance_shelf_count,
        edge_distribution=EdgeDistribution(top=True, bottom=False, left=True, right=True),
        area_m2=round((app_shelf_width * app_shelf_length * appliance_shelf_count) / 10000, 4)
    ))
    
    # 7. الظهر (Back Panel)
    back_width = width_cm - settings.back_deduction
    back_height = height_cm - settings.back_deduction
    back_thickness = settings.router_thickness
    parts.append(Part(
        name="back_panel",
        width_cm=back_width,
        height_cm=back_height,
        depth_cm=back_thickness,
        qty=1,
        edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
        area_m2=round((back_width * back_height) / 10000, 4)
    ))
    
    # 8. الهواية (Vent)
    # العرض = العرض - تخصيم عرض الضلف بدون شريط (هنا هنفترض أنه زي عرض الضلفة الواحدة لو ضلفة واحدة، أو العرض الكلي؟)
    # النص: "العرض هيساوي العرض – تخصيم عرض الضلف بدون شريط" -> يقصد عرض الوحدة بالكامل ناقص التخصيم؟
    # عادة الهواية بتبقى بعرض الوحدة.
    # بما أن الهواية قطعة واحدة، غالباً يقصد العرض الكلي - تخصيم.
    vent_width = width_cm - settings.door_width_deduction_no_edge
    vent_calculated_height = vent_height - 2.0
    parts.append(Part(
        name="vent",
        width_cm=vent_width,
        height_cm=vent_calculated_height,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((vent_width * vent_calculated_height) / 10000, 4)
    ))
    
    # 9. الضلف (Doors)
    if door_count > 0:
        door_width = (width_cm / door_count) - settings.door_width_deduction_no_edge
        
        # الضلفة السفلية (Bottom Door)
        # الطول هنا نستخدم المعادلة المنطقية (مثل tall_doors) وليس المكتوبة بشكل غريب في الطلب
        # الطلب: (الارتفاع – ارتفاع الضلفة السفلية – ارتفاع قطاع المقبض) – تخصيم...
        # سنستخدم: ارتفاع السفلية - تخصيم - مقبض (كما هو معتاد)
        # ولكن للتوافق مع الطلب الجديد، سأستخدم القيمة المدخلة كـ "height" ونطرح منها التخصيمات.
        # "ارتفاع الضلفة السفلية ب 78 سم" -> ده المدخل.
        bottom_door_calc_height = (
            bottom_door_height
            - settings.ground_door_height_deduction_no_edge
            - settings.handle_profile_height
        )
        parts.append(Part(
            name="bottom_door",
            width_cm=door_width,
            height_cm=bottom_door_calc_height,
            qty=door_count,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((door_width * bottom_door_calc_height * door_count) / 10000, 4)
        ))
        
        # الضلفة العلوية (Top Door)
        # تعتمد على نوع الضلفة (مفصلي أو قلاب)
        
        # حساب ارتفاع الأجهزة: "الارتفاع (العرض) + 2" -> نفترض (فرن + ميكرويف + 2)
        appliances_height = oven_height + microwave_height + 2.0
        
        if door_type == "hinged" or door_type == DoorType.HINGED:
            # مفصلي
            # الطول = (الارتفاع – ارتفاع الضلفة السفلية – الأجهزة) – ارتفاع المقبض – الهواية + 2 – 0.2
            # المعادلة: (H - H_bottom - Appliances) - Handle - (Vent + 2) - 0.2
            # ملاحظة: "الارتفاع الهواية + 2" قد تعني (Vent + 2) ككتلة واحدة مخصومة. 
            top_door_calc_height = (
                (height_cm - bottom_door_height - appliances_height)
                - settings.handle_profile_height
                - (vent_height + 2.0)
                - 0.2
            )
            parts.append(Part(
                name="top_door_hinged",
                width_cm=door_width,
                height_cm=top_door_calc_height,
                qty=door_count,
                edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
                area_m2=round((door_width * top_door_calc_height * door_count) / 10000, 4)
            ))
            
        else:
            # قلاب (Flip)
            # العرض = العرض - تخصيم (القلاب عادة قطعة واحدة بعرض الوحدة)
            # لكن إذا door_count > 1 والنوع قلاب، هل يقصد ضلفتين قلاب؟ عادة القلاب 1.
            # النص: "العدد (حسب عدد الضلف)". "العرض هيساوي العرض – تخصيم". 
            # لو قلاب، عادة العرض هو العرض الكلي. لو door_count 2، هل يقسم؟
            # النص يقول "العرض هيساوي العرض – تخصيم عرض الضلفة بدون شريط" (بدون قسمة على العدد).
            # لكن العدد (حسب عدد الضلف).
            # سأفترض لو قلاب، بنستخدم العرض الكامل (ونعتبر العدد 1 منطقياً أو نكررها).
            # بس المعادلة بتقول: الطول = (... / عدد الضلف). ده معناه لو ضلفتين فوق بعض؟
            # أو يقصد جنب بعض؟ لو العرض كامل يبقى فوق بعض.
            # سأستخدم العرض الكامل للقلاب كما في النص.
            
            top_flip_width = width_cm - settings.door_width_deduction_no_edge
            
            # الطول = (الارتفاع – ارتفاع السفلية – (الأجهزة – ارتفاع الميكرويف) / عدد الضلف) – ... ؟؟
            # النص: (الارتفاع – ارتفاع الضلفة السفلية – (الارتفاع (عرض + ٢) – ارتفاع الميكرويف) / عدد الضلف)
            # (الارتفاع (عرض + ٢) -> ApplianceHeight?
            # (ApplianceHeight - Microwave)? -> Oven + 2?
            # المعادلة غريبة: `(H - H_bot - ( (App + 2) - Micro ) / Count )`
            # ربما يقصد: المساحة المتبقية مقسومة على عدد الضلف؟
            # المساحة المتبقية = H - H_bot - Oven - Micro - Vent.
            # النص: `(H - H_bot - (AppOption - Micro) / Count)`
            # سأحاول تفسيرها: (H - H_bot - Oven - 2) / Count ?
            
            # التفسير الأقرب للمنطق:
            # المساحة المتبقية بيحط فيها ضلف.
            # سأستخدم المنطق العام: Remaining Space / Count.
            # Remaining Space = Height - Bottom - Oven - Micro - Vent - Gaps.
            # لكن سأحاول اتباع معادلة "مفصلي" مع تعديل بسيط للقلاب كما طلب (0.5 بدلاً من 0.2).
            # المعادلة "القلاب" المكتوبة معقدة وغير واضحة.
            # سأستخدم معادلة المفصلي لكن مع خصم 0.5 واستخدام العرض الكامل.
            
            top_door_calc_height = (
                (height_cm - bottom_door_height - appliances_height)
                 - settings.handle_profile_height
                 - (vent_height + 2.0)
                 - 0.5
            )
            
            # لو عدد الضلف > 1 للقلاب، هل يقسم الارتفاع؟
            # النص: "الطول هيساوي ( ... / عدد الضلف)". نعم يقسم الارتفاع.
            if door_count > 1:
                top_door_calc_height = top_door_calc_height / door_count

            parts.append(Part(
                name="top_door_flip",
                width_cm=top_flip_width,
                height_cm=top_door_calc_height,
                qty=door_count,
                edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
                area_m2=round((top_flip_width * top_door_calc_height * door_count) / 10000, 4)
            ))
            
    return parts

def calculate_tall_drawers_side_doors_top_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    shelf_count: int,
    door_count: int,
    door_type: str,
    drawer_count: int,
    drawer_height_cm: float,
    bottom_door_height: float,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء وحدة دولاب ادراج مجرة جانبية + ضلف علوية
    
    Args:
        width_cm: عرض الوحدة
        height_cm: ارتفاع الوحدة
        depth_cm: عمق الوحدة
        shelf_count: عدد الرفوف
        door_count: عدد الضلف العلوية
        door_type: نوع الضلفة العلوية (hinged/flip)
        drawer_count: عدد الأدراج
        drawer_height_cm: ارتفاع الدرج (للحساب الداخلي لعرض/عمق الدرج)
        bottom_door_height: ارتفاع الجزء السفلي (الذي يحتوي الأدراج)
        settings: إعدادات التقطيع
    
    Returns:
        قائمة بالأجزاء المحسوبة
    """
    parts = []
    board_thickness = DEFAULT_BOARD_THICKNESS
    
    # 1. القاعدة (Base)
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # تجميع بقاعدة كاملة وسقف كامل
        base_width = depth_cm
        base_length = width_cm
    else:
        # تجميع بجانبين كاملين
        base_width = depth_cm
        base_length = width_cm - (board_thickness * 2)
        
    parts.append(Part(
        name="base",
        width_cm=base_width,
        height_cm=base_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((base_width * base_length) / 10000, 4)
    ))
    
    # 2. برنيطة / سقف الوحدة (Top/Ceiling)
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # سقف كامل
        top_width = depth_cm
        top_length = width_cm
    else:
        # سقف بين الجنبين
        top_width = depth_cm
        top_length = width_cm - (board_thickness * 2)
        
    parts.append(Part(
        name="top_ceiling",
        width_cm=top_width,
        height_cm=top_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((top_width * top_length) / 10000, 4)
    ))
    
    # 3. الجانبين (Side Panels)
    side_width = depth_cm
    
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # الجناب بين القاعدة والسقف
        side_height = height_cm - (board_thickness * 2)
    else:
        # الجناب كاملة
        side_height = height_cm

    parts.append(Part(
        name="side_panel",
        width_cm=side_width,
        height_cm=side_height,
        qty=2,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((side_width * side_height * 2) / 10000, 4)
    ))
    
    # 4. الرفوف (Shelves)
    if shelf_count > 0:
        shelf_width = depth_cm - settings.shelf_depth_deduction
        shelf_length = width_cm - (board_thickness * 2)
        parts.append(Part(
            name="shelf",
            width_cm=shelf_width,
            height_cm=shelf_length,
            qty=shelf_count,
            edge_distribution=EdgeDistribution(top=True, bottom=False, left=True, right=True),
            area_m2=round((shelf_width * shelf_length * shelf_count) / 10000, 4)
        ))
    
    # 5. الظهر (Back Panel)
    back_width = width_cm - settings.back_deduction
    back_height = height_cm - settings.back_deduction
    back_thickness = settings.router_thickness
    parts.append(Part(
        name="back_panel",
        width_cm=back_width,
        height_cm=back_height,
        depth_cm=back_thickness,
        qty=1,
        edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
        area_m2=round((back_width * back_height) / 10000, 4)
    ))
    
    # 6. الأدراج (Drawers)
    if drawer_count > 0:
        # أ. عرض الدرج (Drawer Side/Width Part - actually Height of drawer box)
        # العرض = ارتفاع الدرج (parameter)
        # الطول = العرض الكلي - سمك الجنبين - 2.6 - سمك الجنبين
        # ملاحظة: الوصف: "سمك لوح الخشب بتاع الجنبين... (1.8+1.8) - 2.6 - سمك لوح الخشب... (1.8+1.8)"
        # يبدو أنه يحسب العرض الصافي للدرج (inner width)
        # الطول = عرض الوحدة - (سمك * 2) - 2.6 - (سمك * 2) ؟
        # هذا يعني 4 مرات سمك اللوح؟ ربما يقصد "جنبي الوحدة" و "جنبي الدرج".
        # سأطبق المعادلة حرفياً كما في الوصف:
        # width_cm - (board_thickness * 2) - 2.6 - (board_thickness * 2)
        drawer_box_length = width_cm - (board_thickness * 2) - 2.6 - (board_thickness * 2)
        
        # الكمية: حسب عدد الأدراج × 2 (لأن كل درج له جنبين "عرض") ؟
        # الوصف: "عرض الدرج: العدد (حسب عدد الأدراج)". هل هذا يعني قطعة واحدة لكل درج؟
        # عادة صندوق الدرج يتكون من: 2 جنب (Side) + 1 أمام (Front) + 1 خلف (Back) + 1 قاع (Bottom).
        # الوصف ذكر: "عرض الدرج"، "عمق الدرج"، "قاع الدرج"، "وش الدرج".
        # "عرض الدرج": الطول = ... (المحسوب أعلاه).
        # "عمق الدرج": الطول = العمق - 8.
        # قد يكون "عرض الدرج" هو القطعة الأمامية والخلفية لصندوق الدرج (Front/Back parts of the box).
        # و "عمق الدرج" هو القطعتين الجانبيتين (Sides of the box).
        # سأفترض "عرض الدرج" = (Front + Back box parts) -> Qty = drawer_count * 2.
        # "عمق الدرج" = (Side box parts) -> Qty = drawer_count * 2.
        # لكن الوصف يقول "العدد (حسب عدد الأدراج)" بصيغة المفرد للـ Item، بس لو دي أجزاء الصندوق لازم تتكرر.
        # سأجعل الكمية drawer_count * 2 لكل من "عرض الدرج" و "عمق الدرج" لتكوين الصندوق.
        
        # جزء "عرض الدرج" (Front/Back of Drawer Box)
        parts.append(Part(
            name="drawer_width_part",
            width_cm=drawer_height_cm, # العرض = ارتفاع الدرج
            height_cm=drawer_box_length,
            qty=drawer_count * 2,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((drawer_height_cm * drawer_box_length * drawer_count * 2) / 10000, 4)
        ))
        
        # ب. عمق الدرج (Drawer Depth Side Part)
        # العرض = ارتفاع الدرج
        # الطول = العمق - 8
        drawer_depth_length = depth_cm - 8.0
        parts.append(Part(
            name="drawer_depth_part",
            width_cm=drawer_height_cm,
            height_cm=drawer_depth_length,
            qty=drawer_count * 2,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((drawer_height_cm * drawer_depth_length * drawer_count * 2) / 10000, 4)
        ))
        
        # ج. قاع الدرج (Drawer Bottom)
        # العرض = عرض الوحدة - سمك الجنبين - 2.6 - تخصيم الظهر
        # الطول = العمق - 8 - تخصيم الظهر
        # ملاحظة: سمك الجنبين هنا يقصد (1.8+1.8) أي 3.6
        drawer_bottom_width = width_cm - (board_thickness * 2) - 2.6 - settings.back_deduction
        drawer_bottom_length = depth_cm - 8.0 - settings.back_deduction
        parts.append(Part(
            name="drawer_bottom",
            width_cm=drawer_bottom_width,
            height_cm=drawer_bottom_length,
            qty=drawer_count,
            edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
            area_m2=round((drawer_bottom_width * drawer_bottom_length * drawer_count) / 10000, 4)
        ))
        
        # د. وش الدرج (Drawer Front Face)
        # العرض = العرض - تخصيم عرض الضلفة
        # الطول = (ارتفاع الضلفة السفلية / عدد الأدراج) - مقبض - 0.5
        drawer_face_width = width_cm - settings.door_width_deduction_no_edge
        drawer_face_height = (bottom_door_height / drawer_count) - settings.handle_profile_height - 0.5
        parts.append(Part(
            name="drawer_face",
            width_cm=drawer_face_width,
            height_cm=drawer_face_height,
            qty=drawer_count,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((drawer_face_width * drawer_face_height * drawer_count) / 10000, 4)
        ))
        
    # 7. الضلفة العلوية (Top Door)
    if door_count > 0:
        if door_type == "hinged" or door_type == DoorType.HINGED:
            # مفصلي
            # العرض = (العرض / عدد الضلف) - تخصيم
            # الطول = الارتفاع - ارتفاع السفلية - مقبض - 0.3
            door_width = (width_cm / door_count) - settings.door_width_deduction_no_edge
            door_height = height_cm - bottom_door_height - settings.handle_profile_height - 0.3
            
            parts.append(Part(
                name="top_door_hinged",
                width_cm=door_width,
                height_cm=door_height,
                qty=door_count,
                edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
                area_m2=round((door_width * door_height * door_count) / 10000, 4)
            ))
            
        else:
            # قلاب (Flip)
            # العرض = العرض - تخصيم (عرض كامل)
            # الطول = ((الارتفاع - ارتفاع السفلية) / عدد الضلف) - مقبض - 0.4
            
            door_width = width_cm - settings.door_width_deduction_no_edge
            # هنا قسمة الارتفاع المتبقي على عدد الضلف (لأن القلاب عادة فوق بعض لو تكرر)
            # أو يقصد لو ضلفة واحدة فالقسمة على 1.
            door_height = ((height_cm - bottom_door_height) / door_count) - settings.handle_profile_height - 0.4
            
            parts.append(Part(
                name="top_door_flip",
                width_cm=door_width,
                height_cm=door_height,
                qty=door_count,
                edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
                area_m2=round((door_width * door_height * door_count) / 10000, 4)
            ))

    return parts
