
def calculate_one_small_16_two_large_bottom_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    drawer_count: int,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء وحدة درج صغير 16 سم + 2 درج كبير مجرى سفلية
    (Note: Specifications use 19.6cm for small drawer front)
    
    Args:
        width_cm: عرض الوحدة
        height_cm: ارتفاع الوحدة
        depth_cm: عمق الوحدة
        drawer_count: عدد الأدراج (Total 3)
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
    
    # 5. عرض درج صغير (Small Drawer Width/Box Front-Back) - Bottom Rail Logic
    # العدد: 2 (Front/Back) * 1 drawer = 2.
    # طول: العرض - الجانبين (User specified: 86.4 for 90cm)
    # عرض: 12
    small_drawer_count = 1
    small_drawer_box_length = width_cm - (board_thickness * 2)
    small_drawer_box_width = 12.0
    small_drawer_box_qty = small_drawer_count * 2
    
    parts.append(Part(
        name="small_drawer_width_box",
        width_cm=small_drawer_box_width,
        height_cm=small_drawer_box_length,
        qty=small_drawer_box_qty,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((small_drawer_box_width * small_drawer_box_length * small_drawer_box_qty) / 10000, 4)
    ))
    
    # 6. عمق درج صغير (Small Drawer Depth/Box Sides)
    # العدد: 2 (Sides) * 1 drawer = 2.
    # طول: العمق - 8
    # عرض: 12
    small_drawer_depth_length = depth_cm - 8.0
    small_drawer_depth_width = 12.0
    small_drawer_depth_qty = small_drawer_count * 2
    parts.append(Part(
        name="small_drawer_depth",
        width_cm=small_drawer_depth_width,
        height_cm=small_drawer_depth_length,
        qty=small_drawer_depth_qty,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((small_drawer_depth_width * small_drawer_depth_length * small_drawer_depth_qty) / 10000, 4)
    ))
    
    # 7. عرض درج كبير (Large Drawer Width/Box Front-Back)
    # العدد: 2 (Front/Back) * 2 drawers = 4.
    # طول: العرض - الجانبين
    # عرض: الارتفاع - 46
    large_drawer_count = 2
    large_drawer_box_length = width_cm - (board_thickness * 2)
    large_drawer_box_width = height_cm - 46.0
    large_drawer_box_qty = large_drawer_count * 2
    parts.append(Part(
        name="large_drawer_width_box",
        width_cm=large_drawer_box_width,
        height_cm=large_drawer_box_length,
        qty=large_drawer_box_qty,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((large_drawer_box_width * large_drawer_box_length * large_drawer_box_qty) / 10000, 4)
    ))
    
    # 8. عمق درج كبير (Large Drawer Depth/Box Sides)
    # العدد: 2 (Sides) * 2 drawers = 4.
    # طول: العمق - 8
    # عرض: الارتفاع - 46
    large_drawer_depth_length = depth_cm - 8.0
    large_drawer_depth_width = height_cm - 46.0
    large_drawer_depth_qty = large_drawer_count * 2
    parts.append(Part(
        name="large_drawer_depth",
        width_cm=large_drawer_depth_width,
        height_cm=large_drawer_depth_length,
        qty=large_drawer_depth_qty,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((large_drawer_depth_width * large_drawer_depth_length * large_drawer_depth_qty) / 10000, 4)
    ))
    
    # 9. الظهر 1 (Back Panel)
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
    
    # 10. قاع الدرج (Drawer Bottom)
    # العدد: 3 (All 3 drawers)
    # طول: العمق - 10
    # عرض: عرض الوحدة - 6.4 (User implied 6.4 deduction for bottom rail width adjustment)
    total_drawers = 3
    drawer_bottom_length = depth_cm - 10.0
    drawer_bottom_width = width_cm - 6.4
    parts.append(Part(
        name="drawer_bottom",
        width_cm=drawer_bottom_width,
        height_cm=drawer_bottom_length,
        qty=total_drawers,
        edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
        area_m2=round((drawer_bottom_width * drawer_bottom_length * total_drawers) / 10000, 4)
    ))
    
    # 11. وش الدرج الصغير (Small Drawer Front)
    # العدد: 1
    # طول: 19.6 - ارتفاع قطاع المقبض ان وجد
    # عرض: (العرض-تخصيم عرض الضلفة بدون شريط)
    small_front_height = 19.6 - settings.handle_profile_height
    front_width = width_cm - settings.door_width_deduction_no_edge
    parts.append(Part(
        name="small_drawer_front",
        width_cm=front_width,
        height_cm=small_front_height,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((front_width * small_front_height * 1) / 10000, 4)
    ))
    
    # 12. وش الدرج الكبير (Large Drawer Front)
    # العدد: 2
    # طول: ارتفاع الوحدة - تخصيم ارتفاع الضلفة بدون شريط - 20 - ارتفاع قطاع المقبض ان وجد -.5
    # عرض: العرض-تخصيم عرض الضلفة بدون شريط
    # Interpretation: ((H - 20) / 2) - Handle - 0.5
    large_front_height = ((height_cm - 20.0) / 2) - settings.handle_profile_height - 0.5
    parts.append(Part(
        name="large_drawer_front",
        width_cm=front_width,
        height_cm=large_front_height,
        qty=2,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((front_width * large_front_height * 2) / 10000, 4)
    ))

    return parts
