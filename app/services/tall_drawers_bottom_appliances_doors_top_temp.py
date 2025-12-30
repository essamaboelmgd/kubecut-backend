
def calculate_tall_drawers_bottom_appliances_doors_top_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    shelf_count: int,
    door_count: int,
    door_type: str,
    drawer_count: int,
    drawer_height_cm: float,
    bottom_door_height: float,
    oven_height: float,
    microwave_height: float,
    vent_height: float,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء دولاب ادراج مجرة سفلية + أجهزة + ضلف علوية
    
    Args:
        width_cm: عرض الوحدة
        height_cm: ارتفاع الوحدة
        depth_cm: عمق الوحدة
        shelf_count: عدد الرفوف
        door_count: عدد الضلف العلوية (ووشوش الأدراج)
        door_type: نوع الضلفة العلوية (hinged/flip)
        drawer_count: عدد الأدراج
        drawer_height_cm: ارتفاع الدرج
        bottom_door_height: ارتفاع الضلف السفلية (الجزء السفلي)
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
    
    # 2. برنيطة / سقف الوحدة (Top/Ceiling)
    # العدد: 1
    # طول: عرض - سمك الجنبين (Default)
    # عرض: العمق
    top_width = depth_cm
    
    if settings.assembly_method == "base_full_top_sides_back_routed":
        # سقف كامل
        top_length = width_cm
    else:
        # سقف بين الجنبين
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
    # جنب 1 وجنب 2
    # العدد: 2
    # طول: ارتفاع (Default)
    # عرض: العمق
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
    
    # 4. الرف (Regular Shelf)
    # العدد: عدد السمي - 3
    # طول: العرض - الجانبين (86.4 for 90cm -> 1.8*2 = 3.6 deduction)
    # عرض: العمق - تخصم الرف من العمق
    regular_shelf_count = max(0, shelf_count - 3)
    if regular_shelf_count > 0:
        shelf_width = depth_cm - settings.shelf_depth_deduction
        shelf_length = width_cm - (board_thickness * 2)
        parts.append(Part(
            name="shelf",
            width_cm=shelf_width,
            height_cm=shelf_length,
            qty=regular_shelf_count,
            edge_distribution=EdgeDistribution(top=True, bottom=False, left=True, right=True),
            area_m2=round((shelf_width * shelf_length * regular_shelf_count) / 10000, 4)
        ))
        
    # 5. رف (Extra/Appliance Shelf)
    # العدد: 3
    # طول: العرض - الجانبين
    # عرض: العمق - بعد المفحار - سمك الظهر
    extra_shelf_count = 3
    extra_shelf_width = depth_cm - settings.router_distance - settings.router_thickness
    extra_shelf_length = width_cm - (board_thickness * 2)
    parts.append(Part(
        name="appliance_shelf",
        width_cm=extra_shelf_width,
        height_cm=extra_shelf_length,
        qty=extra_shelf_count,
        edge_distribution=EdgeDistribution(top=True, bottom=False, left=True, right=True),
        area_m2=round((extra_shelf_width * extra_shelf_length * extra_shelf_count) / 10000, 4)
    ))
    
    # 6. عرض الدرج (Drawer Width - actually front/back of box for bottom rail)
    # العدد: عدد الادراج * 2
    # طول: عرض الوحدة - 8.4 سم (Same as user request)
    # عرض: ارتفاع الدرج
    if drawer_count > 0:
        drawer_width_length = width_cm - 8.4
        drawer_width_width = drawer_height_cm
        drawer_width_qty = drawer_count * 2
        parts.append(Part(
            name="drawer_width",
            width_cm=drawer_width_width,
            height_cm=drawer_width_length,
            qty=drawer_width_qty,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((drawer_width_width * drawer_width_length * drawer_width_qty) / 10000, 4)
        ))
        
        # 7. عمق الدرج (Drawer Depth - sides of box)
        # العدد: عدد الادراج * 2
        # طول: العمق - 8 سم
        # عرض: ارتفاع الدرج
        drawer_depth_length = depth_cm - 8.0
        drawer_depth_width = drawer_height_cm
        drawer_depth_qty = drawer_count * 2
        parts.append(Part(
            name="drawer_depth",
            width_cm=drawer_depth_width,
            height_cm=drawer_depth_length,
            qty=drawer_depth_qty,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((drawer_depth_width * drawer_depth_length * drawer_depth_qty) / 10000, 4)
        ))
        
        # 8. قاع الدرج (Drawer Bottom)
        # العدد: عدد الادراج
        # طول: العمق - 10 (2+8)
        # عرض: عرض الوحدة - 6.4 (User wrote 6,4 cm, likely full width minus 6.4)
        drawer_bottom_length = depth_cm - 10.0
        drawer_bottom_width = width_cm - 6.4
        parts.append(Part(
            name="drawer_bottom",
            width_cm=drawer_bottom_width,
            height_cm=drawer_bottom_length,
            qty=drawer_count,
            edge_distribution=EdgeDistribution(top=False, bottom=False, left=False, right=False),
            area_m2=round((drawer_bottom_width * drawer_bottom_length * drawer_count) / 10000, 4)
        ))
        
        # 9. وش الدرج (Drawer Front)
        # العدد: عدد الضلف (Should be drawer count)
        # طول: (ارتفاع الضلفة السفلية / عدد الادراج ) -ارتفاع قطاع المقبض ان وجد - 0.5 سم
        # عرض: العرض-تخصيم عرض الضلفة بدون شريط
        one_drawer_front_height = (bottom_door_height / drawer_count) - settings.handle_profile_height - 0.5
        drawer_front_width = width_cm - settings.door_width_deduction_no_edge
        parts.append(Part(
            name="drawer_front",
            width_cm=drawer_front_width,
            height_cm=one_drawer_front_height,
            qty=drawer_count,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((drawer_front_width * one_drawer_front_height * drawer_count) / 10000, 4)
        ))

    # 10. الظهر 1 (Back Panel)
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

    # 11. الهواية (Vent)
    # العدد: 1
    # طول: ارتفاع الهواية - 0.2
    # عرض: العرض - تخصيم عرض الضلف بدون شريط
    vent_part_height = vent_height - 0.2
    vent_part_width = width_cm - settings.door_width_deduction_no_edge
    parts.append(Part(
        name="vent_panel",
        width_cm=vent_part_width,
        height_cm=vent_part_height,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((vent_part_width * vent_part_height) / 10000, 4)
    ))

    # 12. الضلفة العلوية (Top Door)
    if door_count > 0:
        door_width = (width_cm / door_count) - settings.door_width_deduction_no_edge
        
        # Common Height Calculation:
        # H - BottomH - H.Prof? - (Oven+2) - Microwave
        # User formula (Hinged): الارتفاع - ارتفاع الضلفة السفلية - ارتفاع قطاع المقبض ان وجد - (ارتفاع الفرن+2) - ارتفاع الميكرويف
        # User formula (Flip): ((الارتفاع - ارتفاع الضلفة السفلية - (ارتفاع الفرن+2) - ارتفاع الميكرويف) /عدد الضلف ) - ارتفاع قطاع المقبض ان وجد-.4مم
        
        available_height = height_cm - bottom_door_height - (oven_height + 2.0) - microwave_height
        
        if door_type == "hinged" or door_type == DoorType.HINGED:
            # المفصلي:
            top_door_height = available_height - settings.handle_profile_height
            
            parts.append(Part(
                name="top_door_hinged",
                width_cm=door_width,
                height_cm=top_door_height,
                qty=door_count,
                edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
                area_m2=round((door_width * top_door_height * door_count) / 10000, 4)
            ))
        else:
            # القلاب:
            # طول: (Available / عدد الضلف) - مقبض - 0.4
            # عرض: العرض كامل - تخصيم
            flip_door_width = width_cm - settings.door_width_deduction_no_edge
            top_door_height = (available_height / door_count) - settings.handle_profile_height - 0.4
            
            parts.append(Part(
                name="top_door_flip",
                width_cm=flip_door_width,
                height_cm=top_door_height,
                qty=door_count,
                edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
                area_m2=round((flip_door_width * top_door_height * door_count) / 10000, 4)
            ))

    return parts
