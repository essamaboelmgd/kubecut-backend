
def calculate_drawer_bottom_rail_built_in_oven_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    oven_height: float,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء وحدة درج مجره سفلية+ فرن بيلت
    
    Args:
        width_cm: عرض الوحدة
        height_cm: ارتفاع الوحدة
        depth_cm: عمق الوحدة
        oven_height: ارتفاع الفرن (User specifies 60 usually)
        settings: إعدادات التقطيع
    
    Returns:
        قائمة بالأجزاء المحسوبة
    """
    parts = []
    board_thickness = DEFAULT_BOARD_THICKNESS
    
    # 1. القاعدة (Base)
    # العدد: 1
    # طول: عرض - سمك الجنبين (Default)
    # عرض: العمق
    base_width = depth_cm
    
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # تجميع بقاعدة كاملة
        base_length = width_cm
    else:
        # تجميع بجانبين كاملين
        base_length = width_cm - (board_thickness * 2)

    parts.append(Part(
        name="base",
        width_cm=base_width,
        height_cm=base_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((base_width * base_length) / 10000, 4)
    ))
    
    # 2. المرايا الامامية (Front Rail/Mirror)
    # العدد: 1
    # طول: عرض - سمك الجنبين
    # عرض: عرض المرايا
    rail_length = width_cm - (board_thickness * 2)
    mirror_width = getattr(settings, 'mirror_width', 10.0)
    
    parts.append(Part(
        name="front_rail_mirror",
        width_cm=mirror_width,
        height_cm=rail_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((mirror_width * rail_length) / 10000, 4)
    ))
    
    # 3. المرايا الخلفية (Back Rail/Mirror)
    # العدد: 1
    # طول: عرض - سمك الجنبين
    # عرض: عرض المرايا
    parts.append(Part(
        name="back_rail_mirror",
        width_cm=mirror_width,
        height_cm=rail_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((mirror_width * rail_length) / 10000, 4)
    ))

    # 4. الجانبين (Side Panels)
    # العدد: 2
    # طول: الارتفاع
    # عرض: العمق
    side_width = depth_cm
    
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # الجناب فوق القاعدة
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
    
    # 5. عرض درج (Drawer Width/Box Front-Back Strips)
    # العدد: 2 (Strips for 1 drawer)
    # طول: عرض الوحدة - 8.4 سم
    # عرض: عرض المرايا
    drawer_box_length = width_cm - 8.4
    drawer_box_width = mirror_width
    drawer_box_qty = 2
    
    parts.append(Part(
        name="drawer_width_strip",
        width_cm=drawer_box_width,
        height_cm=drawer_box_length,
        qty=drawer_box_qty,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((drawer_box_width * drawer_box_length * drawer_box_qty) / 10000, 4)
    ))
    
    # 6. عمق درج (Drawer Depth/Box Side Strips)
    # العدد: 2
    # طول: 40 (Fixed)
    # عرض: عرض المرايا
    drawer_depth_length = 40.0
    drawer_depth_width = mirror_width
    drawer_depth_qty = 2
    
    parts.append(Part(
        name="drawer_depth_strip",
        width_cm=drawer_depth_width,
        height_cm=drawer_depth_length,
        qty=drawer_depth_qty,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((drawer_depth_width * drawer_depth_length * drawer_depth_qty) / 10000, 4)
    ))
    
    # 7. الظهر 1 (Back Panel)
    # العدد: 0
    # (Skipping append)
    
    # 8. قاع الدرج (Drawer Bottom)
    # العدد: 1
    # طول: تخصيم الظهر - 40 (Interpreted as "40 - Deduction" again)
    # عرض: عرض الوحدة - 6.4 سم
    
    drawer_bottom_length = 40.0 - settings.back_deduction 
    drawer_bottom_width = width_cm - 6.4
    
    parts.append(Part(
        name="drawer_bottom",
        width_cm=drawer_bottom_width,
        height_cm=drawer_bottom_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
        area_m2=round((drawer_bottom_width * drawer_bottom_length) / 10000, 4)
    ))
    
    # 9. وش الدرج (Drawer Front)
    # العدد: 1
    # طول: الارتفاع - تخصيم ارتفاع الضلفة بدون شريط - ارتفاع الفرن- ارتفاع قطاع المقبض ان وجد - 0.5
    # عرض: العرض-تخصيم عرض الضلفة بدون شريط
    
    front_height = height_cm - oven_height - settings.handle_profile_height - 0.5
    front_width = width_cm - settings.door_width_deduction_no_edge
    
    parts.append(Part(
        name="drawer_front",
        width_cm=front_width,
        height_cm=front_height,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((front_width * front_height) / 10000, 4)
    ))

    return parts
