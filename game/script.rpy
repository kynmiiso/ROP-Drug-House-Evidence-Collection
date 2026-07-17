image house exterior = "images/Scenes/forensics_house_exterior_placeholder.jpg"
image house interior = "images/Scenes/forensics_house_interior_placeholder.jpg"
image house interior zoom mdma = "images/Scenes/forensics_house_interior_placeholder_zoom_1.jpg"
image house interior zoom meth = "images/Scenes/forensics_house_interior_placeholder_zoom_2.jpg"
image house interior zoom cocaine = "images/Scenes/forensics_house_interior_placeholder_zoom_3.jpg"
image house interior zoom firearm = "images/Scenes/forensics_house_interior_placeholder_zoom_4.jpg"

image lab_hallway_idle = "images/Scenes/lab_hallway_idle.png"

init python:
    import json

    config.mouse = {
        "default":          [("images/cursor.png", 0, 0)],
        "pointer":          [("images/cursor.png", 0, 0)],
        "hover":            [("images/hover_cursor.png", 0, 0)],
        "dropper":          [("dropper.png", 0, 49)],
        "dropper filled":   [("dropper filled.png", 0, 49)],
        "hand":             [("default_hand.png", 0, 0)]
    }

    default_mouse = "default"

    def hide_all_inventory():
        renpy.hide_screen("full_inventory")
        renpy.hide_screen("inventory")
        renpy.hide_screen("toolbox")
        renpy.hide_screen("inv_buttons")
        renpy.hide_screen("close_inv")
        renpy.hide_screen("toolboxpop")
        renpy.hide_screen("inventoryItemMenu")
        renpy.hide_screen("toolboxItemMenu")
        renpy.hide_screen("toolboxPopItemMenu")
        renpy.hide_screen("inspectItem")

    def inventory_actions(item: str) -> None:
        global imported_print, selected_tool

        if item == "firearm":
            if location == "fumehood" and fumehood_state == "empty":
                selected_tool = "firearm"
            elif location == "afis" and pressed == "import":
                imported_print = "firearm_fingerprint"
                renpy.jump("import_print")

    evids = load_items("jsons/evidence.json")
    evids_by_key = {
        "cocaine":            evids.get("Cocaine Sample"),
        "mdma":                evids.get("MDMA Sample"),
        "meth":                evids.get("Meth Sample"),
        "fingerprint":         evids.get("Fingerprint"),
        "firearm":             evids.get("Firearm"),
        "firearm_fingerprint": evids.get("Firearm Fingerprint Photo"),
    }

    tools = load_items("jsons/toolbox.json")

    SCENE_TOOL_NAMES = ["Evidence Markers", "Marquis Reagent", "Scott Reagent",
                        "Tube", "Evidence Bag", "Tamper Evident Tape"]
    LAB_TOOL_NAMES = ["Distilled Water", "Superglue"]

    def load_scene_toolbox():
        toolbox.reset_inventory()
        for name in SCENE_TOOL_NAMES:
            if name in tools:
                toolbox.add_to_inventory(tools[name])

    def load_lab_toolbox():
        toolbox.reset_inventory()
        for name in LAB_TOOL_NAMES:
            if name in tools:
                toolbox.add_to_inventory(tools[name])

    def set_cursor(cursor):
        global default_mouse
        global current_cursor
        if current_cursor == cursor:
            default_mouse = ''
            current_cursor = ''
        else:
            default_mouse = cursor
            current_cursor = cursor

    def analyzed_everything() -> None:
        return prints["print_4"].processed

    def set_timer(item: str):
        item = False

    def disable_timer(item: str):
        item = True

    def calculate_afis(evidence):
        global afis_search
        afis_search = []
        evidence.processed = True

        for e in afis_evidence:
            if e.processed and e!= evidence:
                afis_search.append(e)
    
    def close_menu():
        if renpy.get_screen("casefile_physical"):
            renpy.hide_screen("casefile_physical")
        elif renpy.get_screen("casefile_photos"):
            renpy.hide_screen("casefile_photos")
        elif renpy.get_screen("casefile"):
            renpy.hide_screen("casefile")
        else:
            renpy.show_screen("casefile")

    class Evidence:
        def __init__(self, name, afis_details):
            self.name = name
            self.afis_details = afis_details
            self.processed = False

    # declare each piece of evidence
    firearm_fingerprint = Evidence(name = 'firearm_fingerprint',
                                afis_details = {
                                    'image': 'firearm_fingerprint',
                                    'xpos':0.18, 'ypos':0.3,
                                    'score': '70'})

    # declare afis relevant evidence
    afis_evidence = [firearm_fingerprint]

    # set current_evidence to track which evidence is currently active
    current_evidence = firearm_fingerprint

default evidence_found = {
        "firearm_processed":            False,
        "firearm_packaged":             False,
        "mdma_presumptive":             False,
        "mdma_packaged":                False,
        "mdma_processed":               False,
        "meth_presumptive":             False,
        "meth_packaged":                False,
        "meth_processed":               False,
        "cocaine_presumptive":          False,
        "cocaine_packaged":             False,
        "cocaine_processed":            False
    }

default valid_evidence_steps = {
        "cocaine": [
            {"drop_target_idle":        "marker_dynamic"},
            {"cocaine_idle":            "tube_idle"},
            {"cocaine_tube":            "scott_reagent_idle"},
            "quiz",
            {"cocaine_idle":            "evidence_bag_idle"},
            {"evidence_bag_idle":       "tamper_evident_tape_idle"},
            "collect_step"
        ],
        "mdma": [
            {"drop_target_idle":        "marker_dynamic"},
            {"mdma_idle":               "tube_idle"},
            {"mdma_tube":               "marquis_reagent_idle"},
            "quiz",
            {"mdma_idle":               "tube_idle"},
            {"mdma_tube":               "evidence_bag_idle"},
            {"evidence_bag_idle":       "tamper_evident_tape_idle"},
            "collect_step"
        ],
        "meth": [
            {"drop_target_idle":        "marker_dynamic"},
            {"meth_idle":               "tube_idle"},
            {"meth_tube":               "marquis_reagent_idle"},
            "quiz",
            {"meth_idle":               "tube_idle"},
            {"meth_tube":               "evidence_bag_idle"},
            {"evidence_bag_idle":       "tamper_evident_tape_idle"},
            "collect_step"
        ],
        "firearm": [
            {"drop_target_idle":                    "marker_dynamic"},
            # {"firearm_idle":                        "uv_light_idle"},
            # {"firearm_light_idle":                  "magnetic_powder_idle"},
            # {"firearm_fingerprint_idle":            "scalebar_idle"},
            # {"fingerprint_scalebar_idle":           "tape_idle"},
            # {"lifted_fingerprint_idle":             "backing_card_idle"},
            # {"fingerprint_backing_idle":            "pen_idle"},
            # {"fingerprint_backing_initial_idle":    "evidence_bag_idle"},
            # {"evidence_bag_idle":                   "tamper_evident_tape_idle"},
            # "fingerprint_collect",
            {"firearm_idle":                        "evidence_bag_idle"},
            {"evidence_bag_idle":                   "tamper_evident_tape_idle"},
            "collect_step"
        ]
    }

default evidence_positions = {
        "cocaine": (0.15, 0.70),
        "mdma":    (0.50, 0.65),
        "meth":    (0.30, 0.80),
        "firearm": (0.40, 0.30),
    }

default marker_drop_positions = {
        "cocaine": (0.35, 0.62),
        "mdma":    (0.40, 0.57),
        "meth":    (0.22, 0.72),
        "firearm": (0.32, 0.22),
    }

default evidence_step_index = {
        "cocaine": 0,
        "mdma":    0,
        "meth":    0,
        "firearm": 0,
    }

default evidence_marker_placed = {
        "cocaine": False,
        "mdma":    False,
        "meth":    False,
        "firearm": False,
    }

default evidence_visited_order = []
default testing_item        = None
default selected_tool       = None
default quiz_pending        = False
default collect_step_flag   = False

default cocaine_id_confirmed = False
default mdma_id_confirmed    = False
default meth_id_confirmed    = False

default collected_evidence_inventory = []
default evidence_inventory = {}

default fingerprint_collect_ready   = False
default collect_step_ready          = False

default current_cursor = ''
default show_case_files = False
default show_toolbox = False
default location = "hallway"

# entries on afis when searching
default afis_search = []
default afis_search_coordinates = [{'score_xpos': 0.53, 'xpos':0.61, 'ypos':0.505}]

init python:
    def _total_drag_steps(item):
        return sum(1 for s in valid_evidence_steps.get(item, []) if isinstance(s, dict))

    def _current_drop_image():
        if testing_item is None:
            return None
        steps = valid_evidence_steps.get(testing_item, [])
        idx = evidence_step_index.get(testing_item, 0)
        drag_index = 0
        for s in steps:
            if isinstance(s, dict):
                if drag_index == idx:
                    return list(s.keys())[0]
                drag_index += 1
        return None

    def _quiz_is_next():
        if testing_item is None:
            return False
        steps = valid_evidence_steps.get(testing_item, [])
        idx = evidence_step_index.get(testing_item, 0)
        drag_index = 0
        for i, s in enumerate(steps):
            if isinstance(s, dict):
                if drag_index == idx:
                    if i + 1 < len(steps) and steps[i + 1] == "quiz":
                        return True
                    return False
                drag_index += 1
        return False

    def _collect_step_is_next():
        if testing_item is None:
            return False
        steps = valid_evidence_steps.get(testing_item, [])
        idx = evidence_step_index.get(testing_item, 0)
        drag_index = 0
        for i, s in enumerate(steps):
            if isinstance(s, dict):
                if drag_index == idx:
                    for j in range(i+1, len(steps)):
                        if steps[j] in ("collect_step", "fingerprint_collect"):
                            return True
                        if isinstance(steps[j], dict):
                            return False
                drag_index += 1
        return False

    def _fingerprint_collect_is_next():
        """Checks if a fingerprint_collect marker directly follows our current drag index."""
        if testing_item is None:
            return False
        steps = valid_evidence_steps.get(testing_item, [])
        idx = evidence_step_index.get(testing_item, 0)
        drag_index = 0
        for i, s in enumerate(steps):
            if isinstance(s, dict):
                if drag_index == idx:
                    for j in range(i+1, len(steps)):
                        if steps[j] == "fingerprint_collect":
                            return True
                        if isinstance(steps[j], dict):
                            return False
                drag_index += 1
        return False

    def _is_marker_step():
        step = _get_current_step()
        if step is None:
            return False
        return list(step.values())[0] == "marker_dynamic"

init python:
    _QUIZ = {
        "cocaine": {
            "chart":   "scott_chart",
            "correct": "Cocaine",
            "correct_msg": "Correct! The pink on top and blue at the bottom with the Scott test indicates cocaine.",
            "wrong": {
                "MDMA":           "Incorrect. The Marquis test is used for MDMA.",
                "Methamphetamine":"Incorrect. The Marquis test is used for methamphetamine.",
            }
        },
        "mdma": {
            "chart":   "marquis_chart",
            "correct": "MDMA",
            "correct_msg": "Correct! The purple colour indicates MDMA.",
            "wrong": {
                "Methamphetamine":"Incorrect. Look at the colour chart again.",
                "Cocaine":        "Incorrect. The Scott test is used for cocaine.",
            }
        },
        "meth": {
            "chart":   "marquis_chart",
            "correct": "Methamphetamine",
            "correct_msg": "Correct! The orange-brown colour indicates methamphetamine.",
            "wrong": {
                "MDMA":   "Incorrect. Look at the colour chart again.",
                "Cocaine":"Incorrect. The Scott test is used for cocaine.",
            }
        },
    }

label inspect_evidence:
    hide screen investigation_buttons
    show screen inventory

    if testing_item not in evidence_visited_order:
        $ evidence_visited_order.append(testing_item)

    if "mdma" in testing_item:
        scene house interior zoom mdma
    elif "meth" in testing_item:
        scene house interior zoom meth
    elif "cocaine" in testing_item:
        scene house interior zoom cocaine
    elif "firearm" in testing_item:
        scene house interior zoom firearm

    $ _marker_num = evidence_visited_order.index(testing_item) + 1
    $ _marker_img = "marker_" + str(_marker_num)

    if evidence_marker_placed[testing_item]:
        show screen placed_marker_display(_marker_img)

    label evidence_wait_step:
        if evidence_found[testing_item + "_processed"]:
            jump evidence_done

        if quiz_pending:
            jump evidence_quiz

        if fingerprint_collect_ready:
            jump fingerprint_collect_step

        if collect_step_ready:
            jump collect_step

        if evidence_step_index[testing_item] > 0:
            show screen placed_marker_display(_marker_img)
        else:
            hide screen placed_marker_display

        $ drop_img = _current_drop_image()
        $ xp, yp = marker_drop_positions[testing_item] if _is_marker_step() else evidence_positions[testing_item]

        if _is_marker_step() and not evidence_marker_placed[testing_item]:
            if not renpy.get_screen("notify"):
                $ renpy.notify("Place an evidence marker here")

        show screen drug_processing_screen(drop_img, xp, yp)
        $ renpy.pause(0.3)
        jump evidence_wait_step

    label fingerprint_collect_step:
        $ fingerprint_collect_ready = False
        hide screen drug_processing_screen
        show screen drug_collection_screen
        "Click to collect and package the lifted fingerprint."
        $ evidence_found["fingerprint_processed"] = True
        $ evidence_found["fingerprint_packaged"]  = True
        $ evidence.add_to_inventory(evids_by_key["fingerprint"])
        $ fingerprint_collected = True
        $ renpy.restart_interaction()
        hide screen drug_collection_screen
        jump evidence_wait_step

    label collect_step:
        $ collect_step_ready = False
        hide screen drug_processing_screen
        show screen drug_collection_screen
        "Click to collect and package the evidence."
        $ evidence_found[testing_item + "_processed"] = True
        $ evidence_found[testing_item + "_packaged"]  = True
        $ evidence.add_to_inventory(evids_by_key[testing_item])
        $ renpy.restart_interaction()
        jump evidence_done

    label evidence_quiz:
        hide screen drug_processing_screen
        $ _q = _QUIZ[testing_item]
        show screen colour_chart(_q["chart"])
        show screen reagent_result(testing_item)
        "What drug is this based on the colour reaction?"

        menu:
            "[_q['correct']]":
                $ quiz_pending = False
                hide screen colour_chart
                hide screen reagent_result
                "[_q['correct_msg']]"

            "[list(_q['wrong'].keys())[0]]":
                hide screen colour_chart
                hide screen reagent_result
                "[_q['wrong'][list(_q['wrong'].keys())[0]]]"
                show screen inventory
                show screen colour_chart(_q["chart"])
                jump evidence_quiz

            "[list(_q['wrong'].keys())[1]]":
                hide screen colour_chart
                hide screen reagent_result
                "[_q['wrong'][list(_q['wrong'].keys())[1]]]"
                show screen inventory
                show screen colour_chart(_q["chart"])
                jump evidence_quiz

        jump evidence_wait_step

    label evidence_done:
        hide screen drug_collection_screen
        hide screen drug_processing_screen
        hide screen placed_marker_display
        hide screen colour_chart
        hide screen reagent_result
        hide screen inventory
        scene house interior

        $ testing_item              = None
        $ selected_tool             = None
        $ collect_step_flag         = False
        $ quiz_pending              = False
        $ fingerprint_collected     = False
        $ fingerprint_collect_ready = False
        $ collect_step_ready        = False

        $ renpy.restart_interaction()

        show screen investigation_buttons
        jump scene_room_loop

label scene_room_loop:
    show screen investigation_buttons
    pause
    jump scene_room_loop

define n = Character(name=("Nina"), image="nina")

label start:
    scene lab_hallway_dim
    show nina talk
    
    n "Hello Officer, welcome to the drug house! I'm Nina, your supervisor." 
    n "You can either collect evidence on the scene or skip to the lab analysis portion."

    menu:
        "Start Investigation (Full playthrough)":
            jump house_intro

        "Skip to Lab Analysis":
            jump skip_to_lab

label house_intro:
    scene house exterior
    show nina normal1
    n "Last night, police officers obtained and executed a search warrant for a room within this residence suspected of being used for drug trafficking activity."
    show nina talk
    n "Are you the forensic identification officer who has been put in charge of this case? Great!"
    show nina normal1
    n "I'm Nina, I'm here to supervise you for the day"
    show nina thinknote1
    n "You must collect evidence on this case to later be further analyzed in the lab."
    n "Before we enter, remember that everything must be documented and photographed before it is touched."
    n "Go ahead, let's head inside."
    jump scene_room

label skip_to_lab:
    # Mark all scene evidence as processed/packaged and pre-load the evidence
    # inventory so the lab flow has everything it expects, without playing
    # through the house scene.
    python:
        for key in evidence_found:
            evidence_found[key] = True
        collected_evidence_inventory = ["cocaine", "mdma", "meth", "firearm", "fingerprint"]
        for key in ["cocaine", "mdma", "meth", "firearm", "fingerprint"]:
            evidence.add_to_inventory(evids_by_key[key])
    jump lab_hallway_intro

label scene_room:
    $ load_scene_toolbox()
    scene house interior
    "You take photos of the scene and suspicious looking powder scattered about."
    show nina normal1
    n "Here we are. Take a good look around before we start."
    n "Some suspected drugs are scattered around the room."
    n "We'll need to process them with presumptive field tests."
    n "All evidence must be packed in an evidence bag and sealed with tamper evident tape."
    show nina normal3
    n "Remember, you can check your toolbox and collected evidence on the lefthand side."
    n "Good luck, Officer. We're counting on you to help us solve this case."
    hide nina normal1
    show screen inventory
    show screen investigation_buttons
    jump scene_room_loop

label investigation_complete:
    scene house interior
    hide screen investigation_buttons
    hide screen inventory
    show nina normal1
    n "Great job! Looks like you've collected all of the evidence at the scene."
    show nina talk
    n "We will send this over to the lab for further analysis, in order to fully determine whether your presumptive field tests were correct."
    show nina thinknote1
    n "For now, give yourself a pat on the back!"

label lab_hallway_intro:
    $ load_lab_toolbox()
    scene lab_hallway_idle
    show nina normal1
    n "Officer, good to see you again."
    show nina normal3
    n "Great job processing the scene! I knew I could count on you!"
    n "Welcome to the lab! Here, you can analyze all the evidence you collected from the crime scene."
    show nina thinknote1
    n "I need you to perform a pattern analysis on potential fingerprints on the firearm and do a serial number restoration."
    n "You will also have to conduct a GC-MS test to identify the chemical compounds of the presumed drugs collected on the field."
    n "For the firearm, you'll have to use the superglue fumehood to vaporise the super glue that will bind to the fingerprint amino acids."
    n "Then, you will have to use AFIS to compare your fingerprint to the existing dataset of fingerprints to figure out the suspect's identity."
    show nina normal3
    n "You can go wherever you want - but I suggest beginning with the fumehood first so we won't have to waste time waiting for it to heat up."

    $config.rollback_enabled = False # disables rollback
    $quick_menu = False # removes quick menu (at bottom of screen)

    # toolbox is already populated at game start (see the `tools = load_items(...)`
    # loop near the top of script.rpy), and evidence is populated as it's
    # collected/skipped-to, so no extra setup is needed here beyond showing it.
    show screen inventory

    $ inventory_item_names = ["Cocaine sample vial", "MDMA sample vial", "Methamphetamine sample vial", "Analytical balance photo", "Weighed sample bag", "GC-MS printout",
    "Firearm photo", "Firearm with developed print", "Superglue capsule", "Fumehood photo", "Serial number restoration reagent", "Restored serial number photo",
    "Fingerprint on card", "Fingerprint lift - digital scale", "Fingerprint lift - drug packaging", "Fingerprint lift - cell phone", "Backing card", "Scalebar", "Lifting tape",
    "AFIS comparison printout", "Distilled water", "Tweezers", "Gloves box", "Evidence bag", "Jar in bag", "Tape in bag"]
    
    jump hallway

label hallway:
    $ location = ""
    $ hide_all_inventory()
    scene lab_hallway_idle
    python:
        if analyzed_everything():
            renpy.hide_screen("full_inventory")
            renpy.jump("end")
    hide screen back_button_screen onlayer over_screens
    call screen lab_hallway_screen

label data_analysis_lab:
    $ location = ""
    hide screen full_inventory
    python:
        if analyzed_everything():
            renpy.hide_screen("full_inventory")
            renpy.jump("end")
    show screen back_button_screen('hallway') onlayer over_screens
    call screen data_analysis_lab_screen

label afis:
    hide screen back_button_screen onlayer over_screens
    hide screen full_inventory
    show screen back_button_screen('data_analysis_lab') onlayer over_screens
    call screen afis_screen

label materials_lab:
    $ location = ""
    $ hide_all_inventory()
    python:
        if analyzed_everything():
            renpy.hide_screen("full_inventory")
            renpy.jump("end")
    hide screen back_button_screen onlayer over_screens
    show screen back_button_screen('hallway') onlayer over_screens
    call screen materials_lab_screen

label end:
    hide screen back_button_screen onlayer over_screens
    show nina normal1 
    s "It looks like you've analyzed all the evidence. Great work!"
    s "I hope you took note of the results. Tomorrow, you'll be testifying in court about your findings."
    show nina normal3 
    s "But for now, give yourself a pat on the back and go get some rest!"
    return