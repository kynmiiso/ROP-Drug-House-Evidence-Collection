default gcms_step = 1
default gcms_queue_done = {"cocaine": False, "mdma": False, "meth": False}
default gcms_current_drug = None
default gcms_ref_index = 0

init python:
    def get_next_gcms_drug():
        """Return the next prepared sample still awaiting GC-MS analysis, or None."""
        prepared = {
            "cocaine": has_SPE_cocaine,
            "mdma":    has_SPE_mdma,
            "meth":    has_SPE_meth,
        }
        for drug in ("cocaine", "mdma", "meth"):
            if prepared[drug] and not gcms_queue_done[drug]:
                return drug
        return None

    def gcms_autosampler_drop(drags, drop):
        if not drop:
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        dragged_image = drags[0].drag_name
        expected = {
            "cocaine": "inventory-prepared_cocaine",
            "mdma":    "inventory-prepared_mdma",
            "meth":    "inventory-prepared_meth",
        }[store.gcms_current_drug]

        if dragged_image == expected:
            store.gcms_step = 4
            renpy.notify("Sample loaded into the GC autosampler.")
        else:
            renpy.notify("That's not the right prepared sample.")
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        store.selected_tool = None
        renpy.restart_interaction()
        return True

label gcms:
    $ hide_all_lab_screens()
    $ location = "gcms"

    if not analytical_balance_done or choice_SPE != "COMPLETED":
        show nina talk
        n "You'll need to weigh all three presumed samples on the analytical balance and complete Solid Phase Extraction for each before you can begin GC-MS analysis."
        hide nina talk
        jump materials_lab

    scene gcms_background
    show screen gcms_screen
    show screen gcms_checklist
    n normal1 "Welcome to the GC-MS analysis."

    $ gcms_current_drug = get_next_gcms_drug()
    if gcms_current_drug is None:
        show nina talk
        n "All samples have been run through the GC-MS. Great work."
        hide nina talk
        jump materials_lab

    $ gcms_step = 3
    show screen gcms_screen
    show screen gcms_checklist
    show screen inventory
    show screen back_button_screen('materials_lab') onlayer over_screens
    jump gcms_idle

label gcms_idle:
    $ renpy.pause(3600, hard=True)
    jump gcms_idle

label gcms_set_time:
    hide screen gcms_screen
    "Set the GC-MS to run for how many minutes?"
    menu:
        "4 minutes":
            "Wrong."
            jump gcms_set_time
        "6 minutes":
            jump gcms_run
        "8 minutes":
            jump gcms_run
        "10 minutes":
            jump gcms_run
        "12 minutes":
            "Wrong."
            jump gcms_set_time

label gcms_run:
    $ gcms_step = 5
    "Running the sample through the GC-MS..."
    "A chromatogram appears on the monitor, displaying the separated compounds of the sample."

    $ gcms_step = 6
    "You note the relative retention times (RRT) where the major peaks appear."

    $ gcms_step = 7
    "Generating the mass spectrum for the sample..."
    "The mass spectrum for the sample has been generated."

    $ gcms_step = 8
    show screen gcms_screen
    show screen gcms_checklist
    jump gcms_idle

label gcms_compare_interface:
    hide screen gcms_screen
    $ gcms_ref_index = 0
    call screen gcms_compare_screen

label gcms_compare_prev:
    $ gcms_ref_index = (gcms_ref_index - 1) % 3
    call screen gcms_compare_screen

label gcms_compare_next:
    $ gcms_ref_index = (gcms_ref_index + 1) % 3
    call screen gcms_compare_screen

label gcms_identify:
    $ ref_keys = ["cocaine", "mdma", "meth"]
    $ chosen = ref_keys[gcms_ref_index]

    if chosen == gcms_current_drug:
        $ gcms_step = 9
        "The RRT and mass spectrum match the reference standard for [chosen]."
        "You've identified the sample as [chosen]."
        $ gcms_queue_done[gcms_current_drug] = True
        $ evidence.add_to_inventory(evids["Identified " + gcms_current_drug.capitalize() + " Sample"])
        $ gcms_current_drug = None
        jump gcms
    else:
        "That doesn't match. Review the chromatogram and mass spectrum again."
        call screen gcms_compare_screen