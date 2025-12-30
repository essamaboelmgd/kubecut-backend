
def calculate_wall_microwave_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    shelf_count: int,
    door_count: int,
    door_type: str,
    microwave_height: float,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء وحدة علوي بها ميكرويف
    
    Args:
        width_cm: عرض الوحدة
        height_cm: ارتفاع الوحدة
        depth_cm: عمق الوحدة
        shelf_count: عدد الارفف
        door_count: عدد الضلف
        door_type: نوع الضلفة (normal/flip)
        microwave_height: ارتفاع الميكرويف
        settings: إعدادات التقطيع
    
    Returns:
        قائمة بالأجزاء المحسوبة
    """
    parts = []
    board_thickness = DEFAULT_BOARD_THICKNESS
    
    # 1. القاعدة (Base)
    # العدد: 1
    # طول: العرض - الجانبين (86.4) -> Width - 2*Thickness
    # عرض: العمق 58
    # Assembly: Inner Base (Between Sides)
    base_length = width_cm - (board_thickness * 2)
    base_width = depth_cm
    
    parts.append(Part(
        name="base",
        width_cm=base_width,
        height_cm=base_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((base_width * base_length) / 10000, 4)
    ))

    # 2. برنيطة (سقف الوحدة) (Top Panel)
    # العدد: 1
    # طول: العرض - الجانبين (86.4) -> Width - 2*Thickness
    # عرض: العمق
    # Assembly: Inner Top (Between Sides)
    top_length = width_cm - (board_thickness * 2)
    top_width = depth_cm
    
    parts.append(Part(
        name="top_panel",
        width_cm=top_width,
        height_cm=top_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((top_width * top_length) / 10000, 4)
    ))

    # 3. جانبين (Side Panels)
    # العدد: 2
    # طول: الارتفاع 80 -> Full Height
    # عرض: العمق 58
    side_height = height_cm
    side_width = depth_cm
    
    parts.append(Part(
        name="side_panel",
        width_cm=side_width,
        height_cm=side_height,
        qty=2,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((side_width * side_height * 2) / 10000, 4)
    ))

    # 4. الرف (Regular Shelf)
    # العدد: عدد الارفف-1
    # طول: العرض - الجانبين (86.4) -> Width - 2*Thickness
    # عرض: العمق - تخصم الرف من العمق
    regular_shelf_count = max(0, shelf_count - 1)
    if regular_shelf_count > 0:
        shelf_length = width_cm - (board_thickness * 2)
        shelf_width = depth_cm - settings.shelf_depth_deduction
        parts.append(Part(
            name="shelf",
            width_cm=shelf_width,
            height_cm=shelf_length,
            qty=regular_shelf_count,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((shelf_width * shelf_length * regular_shelf_count) / 10000, 4)
        ))

    # 5. رف (Microwave Shelf / Fixed Shelf?)
    # العدد: 1
    # طول: العرض - الجانبين 86.4
    # عرض: العمق - بعد المفحار - سمك المفحار - 0.1مم
    # Formula: Depth - router_distance - router_thickness - 0.1
    special_shelf_length = width_cm - (board_thickness * 2)
    special_shelf_width = depth_cm - settings.router_distance - settings.router_thickness - 0.1
    
    parts.append(Part(
        name="microwave_shelf",
        width_cm=special_shelf_width,
        height_cm=special_shelf_length,
        qty=1,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((special_shelf_width * special_shelf_length) / 10000, 4)
    ))

    # 6. الظهر (Back Panel)
    # العدد: 1
    # طول: العرض-تخصيم الظهر (User says: "Width - deduction", "Height - deduction")
    # Usually Back fits into grooves.
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
    
    # 7. الضلف / القلاب (Doors)
    if door_type == "flip":
        # الضلفة القلاب
        # العدد: عدد -> Usually 1 flip door covering the space above/below?
        # Specification says "door_count" splits the width if > 1?
        # Formula: ((الارتفاع - ارتفاع الميكرويف)\ عدد الضلف )- ارتفاع قطاع المقبض-.5
        # This formula divides Height by DoorCount. This implies vertically stacked flip doors?
        # Or did user mean "Width / DoorCount"?
        # "الضلفة القلاب: ... طول: ((الارتفاع - ارتفاع الميكرويف) / عدد الضلف ) ..."
        # Usually flip doors are specialized.
        # Let's assume standard usage: 1 or 2 flip doors stacked vertically?
        # Or maybe User meant Width/DoorCount for width, and Height is calculated differently.
        # "طول: ... عرض: ..." -> In our system Height is length (flow), Width is width.
        # Length (Height in door part): ((H - MicroH)/Count) - ...
        # Width (Width in door part): Width - Deduction.
        # This means the flip door spans the FULL WIDTH, and the HEIGHT is split by count.
        # Valid interpretation: Stacked flip doors.
        
        door_part_height = ((height_cm - microwave_height) / door_count) - settings.handle_profile_height - 0.5
        door_part_width = width_cm - settings.door_width_deduction_no_edge
        
        parts.append(Part(
            name="flip_door",
            width_cm=door_part_width,
            height_cm=door_part_height,
            qty=door_count,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((door_part_width * door_part_height * door_count) / 10000, 4)
        ))
        
    else:
        # الضلف (Normal Doors)
        # العدد: عدد الضلف
        # طول (Height): الارتفاع - ارتفاع قطاع المقبض - ارتفاع الميكرويف - .5
        # عرض (Width): (العرض/ عدد الضلف)-تخصيم عرض الضلفة بدون شريط
        
        door_part_height = height_cm - settings.handle_profile_height - microwave_height - 0.5
        door_part_width = (width_cm / door_count) - settings.door_width_deduction_no_edge
        
        parts.append(Part(
            name="door",
            width_cm=door_part_width,
            height_cm=door_part_height,
            qty=door_count,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((door_part_width * door_part_height * door_count) / 10000, 4)
        ))

    return parts
