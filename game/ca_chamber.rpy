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
        if store.ca_chamber_state != "empty":
            return
        if not (store.ca_chamber_water_added and store.ca_chamber_glue_added and store.ca_chamber_firearm_placed):
            renpy.notify("Add the distilled water, superglue, and firearm first.")
            return
        store.ca_chamber_state = "closed"
        renpy.restart_interaction()

label ca_chamber:
    $ hide_all_lab_screens()
    $ hide_all_inventory()
    $ location = "ca_chamber"
    scene materials_lab
    show screen ca_chamber_screen
    show screen inventory
    show screen back_button_screen('materials_lab') onlayer over_screens

label ca_chamber_load_dialogue:
    if ca_chamber_done or ca_chamber_state != "closed":
        jump ca_chamber_wait_step

    hide screen ca_chamber_screen
    n normal1 "Set the CA chamber to between 120-150 degrees celsius and 12-15 minutes."

    $ reset_ca_chamber_entry()
    $ ca_correct_temp_start = "120"
    $ ca_correct_temp_end   = "151"
    $ ca_correct_time_start = "12"
    $ ca_correct_time_end   = "16"
    $ ca_correct_label      = "ca_chamber_settings_confirmed"
    $ ca_incorrect_label    = "ca_chamber_settings_incorrect"

    call screen ca_chamber_main_interface

label ca_chamber_settings_incorrect:
    n normal1 "That's not quite right. Remember: 120-150 degrees, 12-15 minutes."
    call screen ca_chamber_main_interface

label ca_chamber_settings_confirmed:
    hide screen ca_chamber_keyboard
    hide screen ca_chamber_temperature_screen
    hide screen ca_chamber_cooking_time_screen
    $ ca_chamber_state = "loaded"
    n normal1 "You've correctly set the CA chamber between 120-150 degrees for 12-15 minutes!"
    show screen ca_chamber_screen
    n normal1 "Now wait an additional 5 minute purging period..."
    $ renpy.pause(3.0)
    n normal1 "Purging complete."
    jump ca_chamber_wait_step

label ca_chamber_wait_step:
    if ca_chamber_state == "loaded" and not ca_chamber_done:
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