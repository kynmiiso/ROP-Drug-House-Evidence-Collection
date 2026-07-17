init python:
    def fumehood_drop(drags, drop):
        if not drop:
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        dragged_image = drags[0].drag_name

        if dragged_image == "toolbox-distilled_water" and not store.fumehood_water_added:
            store.fumehood_water_added = True
            renpy.notify("Distilled water added.")
        elif dragged_image == "toolbox-superglue" and not store.fumehood_glue_added:
            store.fumehood_glue_added = True
            renpy.notify("Superglue added.")
        elif dragged_image == "inventory-firearm" and not store.fumehood_firearm_placed:
            store.fumehood_firearm_placed = True
            renpy.notify("Firearm placed in the fumehood chamber.")
        else:
            renpy.notify("That doesn't belong in the fumehood right now.")
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        store.selected_tool = None
        renpy.restart_interaction()
        return True

    def load_fumehood():
        global fumehood_state
        fumehood_state = "loaded"
        renpy.restart_interaction()

    def close_fumehood():
        global fumehood_state
        fumehood_state = "closed"
        renpy.restart_interaction()

screen fumehood_screen():
    if fumehood_state == "empty":
        add "fumehood_empty"
    elif fumehood_state == "loaded":
        add "fumehood_firearm"
    elif fumehood_state == "closed":
        add "fumehood_closed"

    if fumehood_state == "empty" and not fumehood_done:
        draggroup:
            if selected_tool is not None:
                drag:
                    drag_name selected_tool
                    draggable True
                    droppable False
                    dragging item_dragging_package
                    dragged  fumehood_drop
                    xpos 0.75 ypos 0.35
                    child Transform(selected_tool, zoom=1.5)
            drag:
                drag_name "fumehood_dropzone"
                draggable False
                droppable True
                xalign 0.5 yalign 0.5
                child Transform("fumehood_empty", zoom=1.0)

        textbutton "Load Fumehood":
            xpos 0.4 ypos 0.85
            background "#003366"
            hover_background "#0055aa"
            sensitive (fumehood_water_added and fumehood_glue_added and fumehood_firearm_placed)
            action Jump("fumehood_load_dialogue")

    elif fumehood_state == "loaded" and not fumehood_done:
        textbutton "Close Fumehood":
            xpos 0.4 ypos 0.85
            background "#003366"
            hover_background "#0055aa"
            action Function(close_fumehood)
            
label fumehood:
    hide screen materials_lab_screen
    $ hide_all_inventory()
    $ location = "fumehood"
    scene materials_lab
    $ print(renpy.get_screen("materials_lab_screen"))
    show screen fumehood_screen
    show screen inventory
    show screen back_button_screen('materials_lab') onlayer over_screens

label fumehood_load_dialogue:
    $ fumehood_state = "loaded"
    n normal1 "You should set the fumehood to 120 degrees for 15 minutes, with a 5 minute purging period."
    jump fumehood_wait_step

label fumehood_wait_step:
    if fumehood_state == "closed" and not fumehood_done:
        jump fumehood_finish
    $ renpy.pause(0.3)
    jump fumehood_wait_step

label fumehood_finish:
    $ fumehood_done = True
    hide screen fumehood_screen
    hide screen inventory
    hide screen back_button_screen onlayer over_screens
    n normal1 "The superglue fumes have bonded to the amino acids in the print."
    n normal3 "Let's take the firearm out and photograph it."
    "You took a photo of the fingerprints on the fumed firearm."
    $ evidence.add_to_inventory(evids_by_key["firearm_fingerprint"])
    jump materials_lab