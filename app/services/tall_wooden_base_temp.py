
def calculate_tall_wooden_base_unit(
    width_cm: float,
    height_cm: float,
    depth_cm: float,
    shelf_count: int,
    door_count: int,
    settings: SettingsModel
) -> List[Part]:
    """
    حساب أجزاء بلاكار قاعدة خشبية
    
    Args:
        width_cm: عرض الوحدة
        height_cm: ارتفاع الوحدة
        depth_cm: عمق الوحدة
        shelf_count: عدد الارفف
        door_count: عدد الضلف
        settings: إعدادات التقطيع
    
    Returns:
        قائمة بالأجزاء المحسوبة
    """
    parts = []
    board_thickness = DEFAULT_BOARD_THICKNESS
    
    # 1. القاعدة (Base)
    # العدد: 1
    # طول: العرض - سمك الشريط اللي هو 0.2 مم (User says 2. مم but context suggests 0.2mm edge band or minor tolerance, usually we use Width unless deduction is huge)
    # Let's interpret "سمك الشريط" as negligible or strict deduction. 
    # If board thickness isn't factored, it means FULL WIDTH.
    # Logic: Base length = Width (approx, or minus edge band).
    # Since we are cutting boards, usually we simply output dimensions.
    # If user wants strict Width - 0.02cm, we can do that.
    # But usually Edge Band is applied AFTER.
    # However, user explicitly wrote "طول: العرض - سمك الشريط اللي هو 2. مم". 
    # 2. مم could be 2 mm = 0.2 cm.
    # I will deduce 0.2 cm.
    base_length = width_cm - 0.2
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
    # طول: العرض - الجانبين (86.4 for 90 width) -> Width - 2*Thickness
    # عرض: العمق
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
    # طول: الارتفاع - سمك الجنب (!!! High Priority Logic)
    # Usually sides are Full Height, but here User specifies `Height - Thickness`.
    # This confirms Sides sit ON TOP of Base.
    side_height = height_cm - board_thickness
    side_width = depth_cm
    
    parts.append(Part(
        name="side_panel",
        width_cm=side_width,
        height_cm=side_height,
        qty=2,
        edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
        area_m2=round((side_width * side_height * 2) / 10000, 4)
    ))

    # 4. الرف (Shelf)
    # العدد: عدد الارفف
    # طول: العرض - الجانبين (86.4) -> Width - 2*Thickness
    # عرض: العمق - تخصم الرف من العمق
    if shelf_count > 0:
        shelf_length = width_cm - (board_thickness * 2)
        shelf_width = depth_cm - settings.shelf_depth_deduction
        parts.append(Part(
            name="shelf",
            width_cm=shelf_width,
            height_cm=shelf_length,
            qty=shelf_count,
            edge_distribution=EdgeDistribution(top=True, bottom=True, left=True, right=True),
            area_m2=round((shelf_width * shelf_length * shelf_count) / 10000, 4)
        ))

    # 5. الظهر (Back Panel)
    # العدد: 1
    # طول: العرض-تخصيم الظهر (Usually Height)
    # عرض: العرض-تخصيم الظهر (Usually Width)
    # Context check: User wrote "Length: Width-deduction", "Width: Width-deduction".
    # This is strongly suggestive of copy-paste.
    # Logic for Back Panel typically covers the opening.
    # Opening Height = Height approx (maybe minus legs).
    # Since it's a "Tall wooden base", maybe it has no legs?
    # I will use Height - Deduction and Width - Deduction to be safe and standard.
    # Unless "Width-deduction" meant Side-deduction? No.
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
    # العدد: عدد الضلف
    # طول: الارتفاع - ارتفاع قطاع المقبض ان وجد - 0.5
    # عرض: العرض - تخصيم عرض الضلفة بدون شريط
    # Note: If multiple doors, "Width" is divided by count usually, OR total width provided.
    # User formula: "عرض: العرض-تخصيم عرض الضلفة بدون شريط".
    # It does NOT say "/ count".
    # But for "Door Count", normally we distribute width.
    # I will apply standard logic: (Width / Count) - Deduction.
    # Or should I follow text literally? "Width - Deduction".
    # If door_count = 2, and I output Width-Deduction, I get 2 giant doors overlapping.
    # Standard logic applies: Width/Count. User likely described 'per door' logic simply or meant 'Total Width available'.
    # I will use (Width / DoorCount) - Deduction.
    
    door_part_height = height_cm - settings.handle_profile_height - 0.5
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
