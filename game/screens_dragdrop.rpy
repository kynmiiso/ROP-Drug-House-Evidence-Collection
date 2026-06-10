# Replaces the per-drug screens in screens.rpy.
# Rule: drug/evidence is ALWAYS the stationary droppable target (draggable False).
#       Tool is ALWAYS the draggable (shown only when the player picks it from inventory).

# ---------------------------------------------------------------------------
# COCAINE
# ---------------------------------------------------------------------------

# Step 1 — drag Scott reagent onto cocaine
screen cocaine_reagent_screen():
    draggroup:
        drag:
            drag_name "scott"
            draggable True
            droppable False
            dragging item_dragging_package
            dragged  cocaine_reagent_drop
            xpos 0.60  ypos 0.45
            child "scott_reagent_idle"
        drag:
            drag_name "target"
            draggable False
            droppable True
            xpos 0.15  ypos 0.70
            child "cocaine_idle"

# Step 2 — drag evidence bag onto cocaine (coloured)
screen cocaine_bag_screen():
    draggroup:
        drag:
            drag_name "cocaine"
            draggable True
            droppable False
            dragging item_dragging_package
            dragged  cocaine_bag_drop
            xpos 0.60  ypos 0.45
            child "evidence_bag_idle"
        drag:
            drag_name "bag_target"
            draggable False
            droppable True
            xpos 0.15  ypos 0.70
            child "cocaine_blue"

# Step 3 — drag tamper tape onto bagged cocaine
screen cocaine_seal_screen():
    draggroup:
        drag:
            drag_name "tamper_tape"
            draggable True
            droppable False
            dragging item_dragging_package
            dragged  cocaine_seal_drop
            xpos 0.60  ypos 0.45
            child "tamper_evident_tape_idle"
        drag:
            drag_name "seal_target"
            draggable False
            droppable True
            xpos 0.15  ypos 0.70
            child "evidence_bag_with_cocaine"


# ---------------------------------------------------------------------------
# MDMA
# ---------------------------------------------------------------------------

screen mdma_reagent_screen():
    draggroup:
        drag:
            drag_name "marquis"
            draggable True
            droppable False
            dragging item_dragging_package
            dragged  mdma_reagent_drop
            xpos 0.60  ypos 0.45
            child "marquis_reagent_idle"
        drag:
            drag_name "target"
            draggable False
            droppable True
            xpos 0.50  ypos 0.65
            child "mdma_idle"

screen mdma_bag_screen():
    draggroup:
        drag:
            drag_name "mdma"
            draggable True
            droppable False
            dragging item_dragging_package
            dragged  mdma_bag_drop
            xpos 0.60  ypos 0.45
            child "evidence_bag_idle"
        drag:
            drag_name "bag_target"
            draggable False
            droppable True
            xpos 0.50  ypos 0.65
            child "mdma_purple"

screen mdma_seal_screen():
    draggroup:
        drag:
            drag_name "tamper_tape"
            draggable True
            droppable False
            dragging item_dragging_package
            dragged  mdma_seal_drop
            xpos 0.60  ypos 0.45
            child "tamper_evident_tape_idle"
        drag:
            drag_name "seal_target"
            draggable False
            droppable True
            xpos 0.50  ypos 0.65
            child "evidence_bag_with_mdma"


# ---------------------------------------------------------------------------
# METH
# ---------------------------------------------------------------------------

screen meth_reagent_screen():
    draggroup:
        drag:
            drag_name "marquis"
            draggable True
            droppable False
            dragging item_dragging_package
            dragged  meth_reagent_drop
            xpos 0.60  ypos 0.45
            child "marquis_reagent_idle"
        drag:
            drag_name "target"
            draggable False
            droppable True
            xpos 0.30  ypos 0.80
            child "meth_idle"

screen meth_bag_screen():
    draggroup:
        drag:
            drag_name "meth"
            draggable True
            droppable False
            dragging item_dragging_package
            dragged  meth_bag_drop
            xpos 0.60  ypos 0.45
            child "evidence_bag_idle"
        drag:
            drag_name "bag_target"
            draggable False
            droppable True
            xpos 0.30  ypos 0.80
            child "meth_brown"

screen meth_seal_screen():
    draggroup:
        drag:
            drag_name "tamper_tape"
            draggable True
            droppable False
            dragging item_dragging_package
            dragged  meth_seal_drop
            xpos 0.60  ypos 0.45
            child "tamper_evident_tape_idle"
        drag:
            drag_name "seal_target"
            draggable False
            droppable True
            xpos 0.30  ypos 0.80
            child "evidence_bag_with_meth"
