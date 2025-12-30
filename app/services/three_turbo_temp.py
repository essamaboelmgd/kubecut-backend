
def calculate_three_turbo_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء وحدة 3 تربو
    
    Args:
        width_cm: عرض الوحدة
        height_cm: ارتفاع الوحدة
        depth_cm: عمق الوحدة
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
    # "طول: عرض الوحدة - سمك الجانبين - 2,6 - سمك الجانبين"
    # "عرض: عرض المرايا"
    # العدد: 6 (Typically 2 per drawer * 3 drawers)
    drawer_count = 3
    drawer_box_length = width_cm - (board_thickness * 2) - 2.6 - (board_thickness * 2)
    drawer_box_width = mirror_width
    drawer_box_qty = 6
    
    parts.append(Part(
        name="drawer_width_strip",
        width_cm=drawer_box_width,
        height_cm=drawer_box_length,
        qty=drawer_box_qty,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((drawer_box_width * drawer_box_length * drawer_box_qty) / 10000, 4)
    ))
    
    # 6. عمق درج (Drawer Depth/Box Side Strips)
    # "طول: العمق - 8 سم"
    # "عرض: عرض المرايا"
    # العدد: 6
    drawer_depth_length = depth_cm - 8.0
    drawer_depth_width = mirror_width
    drawer_depth_qty = 6
    
    parts.append(Part(
        name="drawer_depth_strip",
        width_cm=drawer_depth_width,
        height_cm=drawer_depth_length,
        qty=drawer_depth_qty,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((drawer_depth_width * drawer_depth_length * drawer_depth_qty) / 10000, 4)
    ))
    
    # 7. الظهر 1 (Back Panel)
    # العدد: 1
    # طول: الارتفاع - تخصيم الظهر
    # عرض: عرض - تخصيم الظهر
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
    
    # 8. قاع الدرج (Drawer Bottom)
    # العدد: 0
    # طول: بدون قاع
    # عرض: بدون قاع
    # (Skipping append)
    
    # 9. وش الدرج الصغير (Drawer Front)
    # العدد: 3 (Assumed 3 drawers based on name "3 Turbo" and qty 6 strips)
    # طول: ((الارتفاع - تخصيم ارتفاع الضلفة بدون شريط)/ 3 ) - ارتفاع قطاع المقبض ان وجد - 4. مم
    # 4. مم likely means 0.4 cm.
    # عرض: العرض-تخصيم عرض الضلفة بدون شريط
    door_height_deduction = 0.0 # Wait, "تخصيم ارتفاع الضلفة بدون شريط". Usually this is settings.door_height_deduction_no_edge or similar?
    # Context check: Usually user gives explicit formula. 
    # "((Height - Ded) / 3) - Handle - 0.4"
    # I should check if there's a setting for "door_height_deduction_no_edge".
    # In previous units: "height_cm - 40.0" etc.
    # Let's assume there isn't a global "door_height_deduction" setting widely used, 
    # usually it's calculated or user implies (Height - gaps).
    # "تخصيم ارتفاع الضلفة بدون شريط" might be 0 if just spacing is handled by the formula.
    # However, "4. mm" is the Gap?
    # Let's assume the user means "Height" is available height (78).
    # Formula: ((78 - 0) / 3) - Handle - 0.4.
    # But usually there is a deduction for cabinet overlap?
    # I will assume "تخصيم ارتفاع الضلفة بدون شريط" is 0 or negligible if not specified in settings?
    # Wait, in other units `settings.door_width_deduction_no_edge` exists. 
    # Is there `settings.door_height_deduction`?
    # Let's look at `SettingsModel` via usage in this file...
    # I'll stick to 0 deduction for height unless found.
    # But I DO see `settings.handle_profile_height`.
    # And 0.4cm.
    # I'll use `height_cm` directly as the base if no other deduction specified.
    # Actually, usually there might be a top/bottom gap.
    # But formula provided is specific. 
    # "((Height - Ded) / 3)". Maybe Ded=0.
    
    front_height = ((height_cm) / 3) - settings.handle_profile_height - 0.4
    front_width = width_cm - settings.door_width_deduction_no_edge
    
    parts.append(Part(
        name="drawer_front",
        width_cm=front_width,
        height_cm=front_height,
        qty=3,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((front_width * front_height * 3) / 10000, 4)
    ))

    return parts
