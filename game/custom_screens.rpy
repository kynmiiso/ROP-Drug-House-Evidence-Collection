
################################################################################
## In-game screens
################################################################################

# Drag and drop screen
screen drag_and_drop(drag_name, drag_image, drop_name, drop_image):
    draggroup:
        drag:
            drag_name drag_name
            draggable True
            droppable False

            dragged item_dragged_package
            dragging item_dragging_package

            xpos 400
            ypos 250

            add drag_image
        drag:
            drag_name drop_name
            draggable False
            droppable True

            xpos 900
            ypos 250

            add drop_image

# ---------------------------------------------------------------------------
# Generic drug processing screen
# Drop target image and position come from the current step dict.
# Tool draggable only appears after player clicks Use (selected_tool set).
# ---------------------------------------------------------------------------

screen drug_processing_screen(drop_image, drop_xpos, drop_ypos):
    draggroup:
        if selected_tool is not None:
            drag:
                drag_name selected_tool
                draggable True
                droppable False
                dragging item_dragging_package
                dragged  generic_drop
                xpos 0.75 ypos 0.35
                child Transform(selected_tool, zoom=1.5)
        drag:
            drag_name drop_image
            draggable False
            droppable True
            xalign 0.5 yalign 0.5
            child Transform(drop_image, zoom=2)

screen drug_collection_screen():
    modal True
    imagebutton:
        idle "casefile_evidence_idle"
        hover "casefile_evidence_hover"
        at Transform(zoom=2)
        xalign 0.5
        yalign 0.5
        action [
            SetVariable("collect_step_flag", True),
            Return()
        ]
        
screen placed_marker_display(marker_image):
    add marker_image at Transform(xpos=0.2, ypos=0.1)

screen investigation_buttons():
    # get the order of the evidence markers
    $ _order = evidence_visited_order
    $ cocaine_num  = (_order.index("cocaine")  + 1) if "cocaine"  in _order else None
    $ mdma_num     = (_order.index("mdma")     + 1) if "mdma"     in _order else None
    $ meth_num     = (_order.index("meth")     + 1) if "meth"     in _order else None
    $ firearm_num  = (_order.index("firearm")  + 1) if "firearm"  in _order else None

    if not evidence_found["cocaine_processed"] and not evidence_found["cocaine_packaged"]:
        imagebutton:
            xpos 0.43 ypos 0.32
            idle  ("cocaine_idle" if not evidence_found["cocaine_presumptive"] else "cocaine_blue")
            hover ("cocaine_hover" if not evidence_found["cocaine_presumptive"] else "cocaine_blue")
            mouse "hover"
            hovered   Notify("Suspected drugs")
            unhovered NullAction()
            action [
                SetVariable("testing_item",  "cocaine"),
                SetVariable("selected_tool", None),
                Jump("inspect_evidence"),
            ]
        if cocaine_num is not None:
            add ("marker_" + str(cocaine_num)) at Transform(xpos=0.43, ypos=0.32)
    elif evidence_found["cocaine_packaged"]:
        if cocaine_num is not None:
            add ("marker_" + str(cocaine_num)) at Transform(xpos=0.43, ypos=0.32)
    
    if not evidence_found["mdma_processed"] and not evidence_found["mdma_packaged"]:
        imagebutton:
            xpos 0.46 ypos 0.75
            idle  ("drawer_idle" if not evidence_found["mdma_presumptive"] else "mdma_purple")
            hover ("drawer_hover" if not evidence_found["mdma_presumptive"] else "mdma_purple")
            mouse "hover"
            hovered   Notify("Drawer")
            unhovered NullAction()
            action [
                SetVariable("testing_item",  "mdma"),
                SetVariable("selected_tool", None),
                Jump("inspect_evidence"),
            ]
        if mdma_num is not None:
            add ("marker_" + str(mdma_num)) at Transform(xpos=0.46, ypos=0.75)
    elif evidence_found["mdma_packaged"]:
        add ("marker_" + str(mdma_num)) at Transform(xpos=0.46, ypos=0.75)

    if not evidence_found["meth_processed"] and not evidence_found["meth_packaged"]:
        imagebutton:
            xpos 0.30 ypos 0.80
            idle  ("meth_idle" if not evidence_found["meth_presumptive"] else "meth_brown")
            hover ("meth_hover" if not evidence_found["meth_presumptive"] else "meth_brown")
            mouse "hover"
            hovered   Notify("Suspected drugs")
            unhovered NullAction()
            action [
                SetVariable("testing_item",  "meth"),
                SetVariable("selected_tool", None),
                Jump("inspect_evidence"),
            ]
        if meth_num is not None:
            add ("marker_" + str(meth_num)) at Transform(xpos=0.30, ypos=0.80)
    elif evidence_found["meth_packaged"]:
        add ("marker_" + str(meth_num)) at Transform(xpos=0.30, ypos=0.80)
    
    if not evidence_found["firearm_processed"] and not evidence_found["firearm_packaged"]:
        imagebutton:
            xpos 0.67 ypos 0.5
            idle  "firearm_idle"
            hover "firearm_idle"
            mouse "hover"
            hovered   Notify("Firearm")
            unhovered NullAction()
            action [
                SetVariable("testing_item",  "firearm"),
                SetVariable("selected_tool", None),
                Jump("inspect_evidence"),
            ]
        if firearm_num is not None:
            add ("marker_" + str(firearm_num)) at Transform(xpos=0.67, ypos=0.5)
    elif evidence_found["firearm_packaged"]:
        add ("marker_" + str(firearm_num)) at Transform(xpos=0.67, ypos=0.5)

    if (evidence_found["cocaine_packaged"]
        and evidence_found["mdma_packaged"]
        and evidence_found["meth_packaged"]
        and evidence_found["firearm_packaged"]):
        textbutton "Finish Investigation":
            xpos 0.75 ypos 0.9
            style "hud_button"
            background "#006"
            hover_background "#00a"
            action Jump("investigation_complete")

screen colour_chart(chart_image):
    modal False
    add chart_image at Transform(zoom=1.2, xalign=0.3, yalign=0.2)

screen reagent_result(item):
    modal False
    if item == "cocaine":
        add "cocaine_blue_pink" at Transform(zoom=1.5, xalign=0.75, yalign=0.3)
    elif item == "mdma":
        add "mdma_purple" at Transform(zoom=1.5, xalign=0.75, yalign=0.3)
    elif item == "meth":
        add "meth_brown" at Transform(zoom=1.5, xalign=0.75, yalign=0.3)

# initial screen
screen lab_hallway_screen:
    image "lab_hallway_dim"
    hbox:
        xpos 0.20 yalign 0.5
        imagebutton:
            idle "data_analysis_lab_idle"
            hover "data_analysis_lab_hover"
            # hovered Notify("Data Analysis Lab")
            # unhovered Notify('')
            action Jump('data_analysis_lab')
    hbox:
        xpos 0.55 yalign 0.48
        imagebutton:
            idle "materials_lab_idle"
            hover "materials_lab_hover"
            # hovered Notify("Materials Lab")
            # unhovered Notify('')
            action Jump('materials_lab')

############################## DATA ANALYSIS ##############################
screen data_analysis_lab_screen:
    image "afis_interface"
    hbox:
        xpos 0.25 yalign 0.25
        imagebutton:
            idle "afis_software_idle"
            hover "afis_software_hover"
            action Jump("computer")

screen afis_screen:
    default afis_bg = "software_interface"
    default interface_import = False
    default interface_imported = False
    default interface_search = False
    image afis_bg

    hbox:
        xpos 0.35 ypos 0.145
        textbutton('Import'):
            style "afis_button"
            action [
                ToggleLocalVariable('interface_import'),
                ToggleVariable('show_case_files'),
                SetLocalVariable('interface_imported', False),
                SetLocalVariable('interface_search', False),
                SetLocalVariable('afis_bg', 'software_interface'),
                Function(set_cursor, '')]
    
    hbox:
        xpos 0.55 ypos 0.145
        textbutton('Search'):
            sensitive not interface_search
            style "afis_button"
            action [
                ToggleLocalVariable('interface_search'),
                SetLocalVariable('afis_bg', 'software_search'),
                Function(calculate_afis, current_evidence),
                Function(set_cursor, '')]
    
    showif interface_import:
        imagemap:
            idle "software_interface"
            hover "software_import_hover"
            hotspot (282,241,680,756) action [
                SetLocalVariable('interface_import', False), 
                SetLocalVariable('interface_imported', True),
                Function(set_cursor, '')]

    showif interface_imported:
        hbox:
            xpos current_evidence.afis_details['xpos'] ypos current_evidence.afis_details['ypos']
            image current_evidence.afis_details['image']
    
    showif interface_search:
        if afis_search:
            for i in range(len(afis_search)):
                hbox:
                    xpos afis_search_coordinates[i]['xpos'] ypos afis_search_coordinates[i]['ypos']
                    hbox:
                        text("{color=#000000}"+afis_search[i].name+"{/color}")
                hbox:
                    xpos afis_search_coordinates[i]['score_xpos'] ypos afis_search_coordinates[i]['ypos']
                    hbox:
                        text("{color=#000000}"+afis_search[i].afis_details['score']+"{/color}")
            
        else:
            hbox:
                xpos 0.57 yalign 0.85
                hbox:
                    text("{color=#000000}No match found in records.{/color}")

    

    
#################################### MATERIALS ####################################
screen materials_lab_screen:
    image "materials_lab"

    # hbox:
    #     xpos 0.15 yalign 0.5
    #     imagebutton:
    #         idle "wet_lab_idle"
    #         hover "wet_lab_hover"
    #         hovered Notify("Wet Lab")
    #         unhovered Notify('')
    #         action Jump('wet_lab')
    hbox:
        xpos 0.26 yalign 0.5
        imagebutton:
            auto "oven_%s" at Transform(zoom=0.7)
            # hovered Notify("Dry Oven")
            # unhovered Notify('')
            action [SetVariable("location", "gcms"), Jump("gcms")]
    text "Dry Oven" xpos 0.31 ypos 0.66
    
    hbox:
        xpos 0.52 yalign 0.5
        imagebutton:
            auto "fumehood_%s" at Transform(zoom=0.95)
            # hovered Notify("Fumehood")
            # unhovered Notify('')
            action [SetVariable("location", "fumehood"), Jump("fumehood")]
    text "Fumehood" xpos 0.59 ypos 0.67

screen wet_lab_screen:
    image "fumehood"

screen analytical_instruments_screen:
    image "lab_bench"
