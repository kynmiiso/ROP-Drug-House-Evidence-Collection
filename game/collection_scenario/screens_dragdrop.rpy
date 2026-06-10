# ---------------------------------------------------------------------------
# Replaces the generic drag_and_drop screen for evidence items.
# The drug/evidence image IS the drop target — positioned at the same
# xpos/ypos as its hotspot button so it never moves.
# The tool draggable appears near centre-left for the player to grab.
# ---------------------------------------------------------------------------
screen evidence_drag(drag_name, drag_image, drop_name, drop_image, item_xpos, item_ypos):
    # Prompt
    frame:
        background "#000000bb"
        xalign 0.5
        yalign 0.08
        padding (20, 10)
        text "Drag the tool onto the evidence." color "#ffffff" size 22

    draggroup:
        # Tool — draggable, positioned centre-left
        drag:
            drag_name drag_name
            draggable True
            droppable False
            dragging item_dragging_package
            dragged  item_dragged_package
            xpos 0.35 ypos 0.45
            add drag_image

        # Evidence — drop target at exact hotspot position, not draggable
        drag:
            drag_name drop_name
            draggable False
            droppable True
            xpos item_xpos ypos item_ypos
            add drop_image
