init python:
    def ca_chamber_drop(drags, drop):
        if not drop:
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        dragged_image = drags[0].drag_name

        if dragged_image == "toolbox-distilled_water" and not store.ca_chamber_water_added:
            store.ca_chamber_water_added = True
            renpy.notify("Distilled water added.")
        elif dragged_image == "toolbox-superglue" and not store.ca_chamber_glue_added:
            store.ca_chamber_glue_added = True
            renpy.notify("Superglue added.")
        elif dragged_image == "inventory-firearm" and not store.ca_chamber_firearm_placed:
            store.ca_chamber_firearm_placed = True
            renpy.notify("Firearm placed in the CA chamber.")
        else:
            renpy.notify("That doesn't belong in the CA chamber right now.")
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        store.selected_tool = None
        renpy.restart_interaction()
        return True

    def close_ca_chamber():
        global ca_chamber_state
        ca_chamber_state = "closed"
        renpy.restart_interaction()

screen ca_chamber_screen():
    $ bg_image = (
        "ca_chamber_closed" if (ca_chamber_done or ca_chamber_state == "closed")
        else "ca_chamber_firearm" if ca_chamber_firearm_placed
        else "ca_chamber_empty"
    )
    add bg_image at Transform(xalign=0.5, yalign=0.5, rotate=90)

    if not ca_chamber_done:
        if ca_chamber_state == "empty":
            draggroup:
                if selected_tool is not None:
                    drag:
                        drag_name selected_tool
                        draggable True
                        droppable False
                        dragging item_dragging_package
                        dragged  ca_chamber_drop
                        xpos 0.75 ypos 0.35
                        child Transform(selected_tool, zoom=1.5)
                drag:
                    drag_name "ca_chamber_dropzone"
                    draggable False
                    droppable True
                    xalign 0.5 yalign 0.5
                    child Transform(Solid("#00000000"), size=(300, 300))

            textbutton "Load CA Chamber":
                xpos 0.4 ypos 0.85
                background "#003366"
                hover_background "#0055aa"
                sensitive (ca_chamber_water_added and ca_chamber_glue_added and ca_chamber_firearm_placed)
                action Jump("ca_chamber_load_dialogue")

        elif ca_chamber_state == "loaded":
            textbutton "Close CA Chamber":
                xpos 0.4 ypos 0.85
                background "#003366"
                hover_background "#0055aa"
                action Function(close_ca_chamber)

label ca_chamber:
    hide screen materials_lab_screen
    $ hide_all_inventory()
    $ location = "ca_chamber"
    scene materials_lab
    show screen ca_chamber_screen
    show screen inventory
    show screen back_button_screen('materials_lab') onlayer over_screens

label ca_chamber_load_dialogue:
    if ca_chamber_done or not (ca_chamber_water_added and ca_chamber_glue_added and ca_chamber_firearm_placed):
        jump ca_chamber_wait_step

    hide screen ca_chamber_screen
    n normal1 "Set the CA chamber to the correct temperature and time."

    $ reset_ca_chamber_entry()
    $ ca_correct_temp_start = "120"   # 120 degrees celsius
    $ ca_correct_temp_end   = "151"   # it's an exclusive end, so 150 counts
    $ ca_correct_time_start = "012"   # 12 minutes
    $ ca_correct_time_end   = "016"   # it's an exclusive end, so 15 counts
    $ ca_correct_label      = "ca_chamber_settings_confirmed"
    $ ca_incorrect_label    = "ca_chamber_settings_incorrect"

    call screen ca_chamber_main_interface

label ca_chamber_settings_incorrect:
    n normal1 "That's not quite right. Remember set it to 120-150 degrees for 12-15 minutes."
    call screen ca_chamber_main_interface

label ca_chamber_settings_confirmed:
    hide screen ca_chamber_keyboard
    hide screen ca_chamber_temperature_screen
    hide screen ca_chamber_cooking_time_screen
    $ ca_chamber_state = "loaded"
    n normal1 "Correct! You've set the CA chamber between 120-150 degrees for 12-15 minutes."
    show screen ca_chamber_screen
    n normal1 "Now waiting an additional 5 minute purging period..."
    $ renpy.pause(3.0)
    n normal1 "Purging complete."
    jump ca_chamber_wait_step

label ca_chamber_wait_step:
    if ca_chamber_state == "closed" and not ca_chamber_done:
        jump ca_chamber_finish
    $ renpy.pause(3)
    jump ca_chamber_wait_step

label ca_chamber_finish:
    $ ca_chamber_done = True
    hide screen ca_chamber_screen
    hide screen inventory
    hide screen back_button_screen onlayer over_screens
    show firearm_fumed at Transform(xalign=0.5, yalign=0.1)
    n normal1 "The superglue fumes have bonded to the fingerprint."
    n normal3 "Let's take the firearm out and photograph it."
    "You took a photo of the fingerprints on the fumed firearm."
    hide firearm_fumed
    $ evidence.add_to_inventory(evids_by_key["firearm_fingerprint"])
    jump materials_lab