image house exterior = "images/Scenes/forensics_house_exterior_placeholder.jpg"
image house interior = "images/Scenes/forensics_house_interior_placeholder.jpg"
image house interior zoom1 = "images/Scenes/forensics_house_interior_placeholder_zoom_1.jpg"
image house interior zoom2 = "images/Scenes/forensics_house_interior_placeholder_zoom_2.jpg"
image house interior zoom3 = "images/Scenes/forensics_house_interior_placeholder_zoom_3.jpg"
image house interior zoom4 = "images/Scenes/forensics_house_interior_placeholder_zoom_4.jpg"

init python:
    import json

    config.mouse = {
        "default": [("images/cursor.png", 0, 0)],
        "pointer": [("images/cursor.png", 0, 0)],
        "hover":   [("images/hover_cursor.png", 0, 0)]
    }

    evids = load_items("jsons/evidence.json")
    evids_by_key = {
        "cocaine":     evids.get("Cocaine Sample"),
        "mdma":        evids.get("MDMA Sample"),
        "meth":        evids.get("Meth Sample"),
        "fingerprint": evids.get("Fingerprint"),
        "firearm":     evids.get("Firearm")
    }

    tools = load_items("jsons/toolbox.json")
    for tool in tools.values():
        toolbox.add_to_inventory(tool)

default evidence_found = {
        "firearm_processed":            False,
        "firearm_packaged":             False,
        "fingerprint_processed":        False,
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

label inspect_evidence:
    hide screen investigation_buttons
    show screen inventory

    if testing_item not in evidence_visited_order:
        $ evidence_visited_order.append(testing_item)

    if "mdma" in testing_item:
        scene house interior zoom1
    elif "meth" in testing_item:
        scene house interior zoom2
    elif "cocaine" in testing_item:
        scene house interior zoom3
    elif "firearm" in testing_item:
        scene house interior zoom4

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

label scene_room:
    scene house interior
    "You take photos of the scene and suspicious looking powder scattered about."
    show nina normal1
    n "Here we are. Take a good look around before we start."
    n "Some suspected drugs are scattered around the room."
    n "We'll need to process them with presumptive field tests."
    n "Fingerprints must also be dusted and collected for identification purposes. All evidence must be packed."
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

    $ testing_item = None
    $ selected_tool = None
    $ collect_step_flag = False
    $ quiz_pending = False

    $ evidence_found = {
        "firearm_processed":     False,
        "firearm_packaged":      False,
        "fingerprint_processed": False,
        "fingerprint_packaged":  False,
        "mdma_presumptive":      False,
        "mdma_packaged":         False,
        "mdma_processed":        False,
        "meth_presumptive":      False,
        "meth_packaged":         False,
        "meth_processed":        False,
        "cocaine_presumptive":   False,
        "cocaine_packaged":      False,
        "cocaine_processed":     False,
    }

    $ evidence_step_index = {"cocaine": 0, "mdma": 0, "meth": 0, "firearm": 0}
    $ evidence_marker_placed = {"cocaine": False, "mdma": False, "meth": False, "firearm": False}
    $ evidence_visited_order = []

    $ cocaine_id_confirmed = False
    $ mdma_id_confirmed    = False
    $ meth_id_confirmed    = False

    $ evidence.reset_inventory()
    $ collected_evidence_inventory = []
    $ evidence_inventory = {}

    return