image house exterior = "images/Scenes/forensics_house_exterior_placeholder.jpg"
image house interior = "images/Scenes/forensics_house_interior_placeholder.jpg"

init python:
    import json

    config.mouse = {
        "default": [("images/cursor.png", 0, 0)],
        "pointer": [("images/cursor.png", 0, 0)],
        "hover":   [("images/hover_cursor.png", 0, 0)]
    }

    evids = load_items("jsons/evidence.json")
    tools = load_items("jsons/toolbox.json")
    for tool in tools.values():
        toolbox.add_to_inventory(tool)

    evidence_found = {
        "firearm":             False,
        "firearm_fingerprint": False,
        "mdma_presumptive":    False,
        "mdma_packaged":       False,
        "mdma_processed":      False,
        "meth_presumptive":    False,
        "meth_packaged":       False,
        "meth_processed":      False,
        "cocaine_presumptive": False,
        "cocaine_packaged":    False,
        "cocaine_processed":   False,   # all the drag and drop steps are done, awaiting collect click
    }

    # valid step definitions 
    # quiz is a marker that triggers the ID question in between steps
    # collect_step is a marker that shows the bagged evidence
    valid_evidence_steps = {
        "cocaine": [
            {"cocaine_idle":            "tube_idle"},
            {"cocaine_tube":            "cobalt_thiocynate_idle"},
            {"cocaine_blue":            "hydrochloric_acid_idle"},
            {"cocaine_pink":            "chloroform_idle"}, 
            {"cocaine_blue_pink":       "evidence_bag_idle"},
            "quiz",
            {"evidence_bag_idle":       "tamper_evident_tape_idle"},
            "collect_step"
        ],
        "mdma": [
            {"mdma_idle":               "marquis_reagent_idle"},
            "quiz",
            {"mdma_purple":             "evidence_bag_idle"},
            {"evidence_bag_idle":       "tamper_evident_tape_idle"},
            "collect_step"
        ],
        "meth": [
            {"meth_idle":               "marquis_reagent_idle"},
            "quiz",
            {"meth_brown":              "evidence_bag_idle"},
            {"evidence_bag_idle":       "tamper_evident_tape_idle"},
            "collect_step"
        ],
    }

    # positions on main screen per item
    evidence_positions = {
        "cocaine": (0.15, 0.70),
        "mdma":    (0.50, 0.65),
        "meth":    (0.30, 0.80),
    }

    # step index for each item (counts drag steps only)
    evidence_step_index = {
        "cocaine": 0,
        "mdma":    0,
        "meth":    0,
    }

    evids = load_items("jsons/evidence.json")

    evids_by_key = {
        "cocaine": evids.get("Cocaine Sample"),
        "mdma": evids.get("MDMA Sample"),
        "meth": evids.get("Meth Sample"),
        "fingerprint": evids.get("Fingerprint"),
    }

    testing_item        = None
    selected_tool       = None
    quiz_pending        = False
    collect_step_flag   = False


default cocaine_id_confirmed = False
default mdma_id_confirmed    = False
default meth_id_confirmed    = False

default collected_evidence_inventory = []
default evidence_inventory = {}

# ---------------------------------------------------------------------------
# Helper: get the current step dict for the active item
# Returns the step dict, or None if all steps done or quiz is next
# ---------------------------------------------------------------------------
init python:
    def _total_drag_steps(item):
        return sum(1 for s in valid_evidence_steps.get(item, []) if isinstance(s, dict))

    def _current_drop_image():
        """Return the drop target image for the current drag step."""
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
        """True if the next thing after the last completed step is a quiz marker."""
        if testing_item is None:
            return False
        steps = valid_evidence_steps.get(testing_item, [])
        idx = evidence_step_index.get(testing_item, 0)
        drag_count = 0
        for i, s in enumerate(steps):
            if s == "quiz":
                continue
            drag_count += 1
            if drag_count == idx:
                if i + 1 < len(steps) and steps[i + 1] == "quiz":
                    return True
                return False
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
                        if steps[j] == "collect_step":
                            return True
                        if isinstance(steps[j], dict):
                            return False
                drag_index += 1
        return False

# ---------------------------------------------------------------------------
# Quiz data per item
# ---------------------------------------------------------------------------
init python:
    _QUIZ = {
        "cocaine": {
            "chart":   "scott_chart",
            "correct": "Cocaine",
            "correct_msg": "Correct! The blue colour with the Scott test indicates cocaine.",
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

# ---------------------------------------------------------------------------
# Room hotspot screen
# ---------------------------------------------------------------------------
screen investigation_buttons():
    if not evidence_found["cocaine_processed"] and not evidence_found["cocaine_packaged"]:
        imagebutton:
            xpos 0.15  ypos 0.70
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
    elif evidence_found["cocaine_packaged"]:
        add "marker_1" at Transform(zoom=0.5, xpos=0.15, ypos=0.70)
    
    if not evidence_found["mdma_processed"] and not evidence_found["mdma_packaged"]:
        imagebutton:
            xpos 0.50  ypos 0.65
            idle  ("mdma_idle" if not evidence_found["mdma_presumptive"] else "mdma_purple")
            hover ("mdma_hover" if not evidence_found["mdma_presumptive"] else "mdma_purple")
            mouse "hover"
            hovered   Notify("Suspected drugs")
            unhovered NullAction()
            action [
                SetVariable("testing_item",  "mdma"),
                SetVariable("selected_tool", None),
                Jump("inspect_evidence"),
            ]
    elif evidence_found["mdma_packaged"]:
        add "marker_3" at Transform(zoom=0.5, xpos=0.50, ypos=0.65)

    if not evidence_found["meth_processed"] and not evidence_found["meth_packaged"]:
        imagebutton:
            xpos 0.30  ypos 0.80
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
    elif evidence_found["meth_packaged"]:
        add "marker_2" at Transform(zoom=0.5, xpos=0.30, ypos=0.80)

    if (evidence_found["cocaine_packaged"]
        and evidence_found["mdma_packaged"]
        and evidence_found["meth_packaged"]):
        textbutton "Finish Investigation":
            xpos 0.75  ypos 0.9
            style "hud_button"
            background "#006"
            hover_background "#00a"
            action Jump("investigation_complete")

# ---------------------------------------------------------------------------
# Colour chart screen for quiz
# ---------------------------------------------------------------------------
screen colour_chart(chart_image):
    modal False
    add chart_image at Transform(zoom=1.2, xalign=0.5, yalign=0.2)

# ---------------------------------------------------------------------------
# Reagent color change result screen
# ---------------------------------------------------------------------------
screen reagent_result(item):
    modal False

    if item == "cocaine":
        add "cocaine_blue" at Transform(zoom=1.5, xalign=0.75, yalign=0.3)
    elif item == "mdma":
        add "mdma_purple" at Transform(zoom=1.5, xalign=0.75, yalign=0.3)
    elif item == "meth":
        add "meth_brown" at Transform(zoom=1.5, xalign=0.75, yalign=0.3)

label inspect_evidence:
    hide screen investigation_buttons
    show screen inventory

    label evidence_wait_step:
        if evidence_found[testing_item + "_processed"]:
            jump evidence_done

        if quiz_pending:
            jump evidence_quiz

        if evidence_step_index[testing_item] >= _total_drag_steps(testing_item):
            jump collect_step

        $ drop_img = _current_drop_image()
        $ xp, yp  = evidence_positions[testing_item]
        show screen drug_processing_screen(drop_img, xp, yp)
        $ renpy.pause(0.3)
        jump evidence_wait_step
        
    label collect_step:
        hide screen drug_processing_screen
        show screen drug_collection_screen
        "Click to collect and package the evidence."
        $ evidence_found[testing_item + "_processed"] = True
        $ evidence_found[testing_item + "_packaged"] = True
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
        hide screen colour_chart
        hide screen reagent_result
        hide screen Inventory
        
        $ testing_item = None
        $ selected_tool = None
        $ collect_step_flag = False
        $ quiz_pending = False

        $ renpy.restart_interaction()

        show screen investigation_buttons
        jump scene_room_loop

# ---------------------------------------------------------------------------
# scene_room_loop
# ---------------------------------------------------------------------------
label scene_room_loop:
    show screen investigation_buttons
    pause
    jump scene_room_loop

# ---------------------------------------------------------------------------
# Main script
# ---------------------------------------------------------------------------
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
    hide screen investigation_buttons
    hide screen inventory
    show nina normal1
    n "Great job! Looks like you've collected all of the evidence at the scene."
    show nina talk
    n "We will send this over to the lab for further analysis, in order to fully determine whether your presumptive field tests were correct."
    show nina thinknote1
    n "For now, give yourself a pat on the back!"

    # reset the backend so the scene can be played again when player clicks start game for a second time (or more)
    $ testing_item = None
    $ selected_tool = None
    $ collect_step_flag = False
    $ quiz_pending = False

    $ evidence_found = {
        "firearm":             False,
        "firearm_fingerprint": False,
        "mdma_presumptive":    False,
        "mdma_packaged":       False,
        "mdma_processed":      False,
        "meth_presumptive":    False,
        "meth_packaged":       False,
        "meth_processed":      False,
        "cocaine_presumptive": False,
        "cocaine_packaged":    False,
        "cocaine_processed":   False,
    }

    $ evidence_step_index = {"cocaine": 0, "mdma": 0, "meth": 0}

    $ cocaine_id_confirmed = False
    $ mdma_id_confirmed    = False
    $ meth_id_confirmed    = False

    $ evidence.reset_inventory()
    $ collected_evidence_inventory = []
    $ evidence_inventory = {}

    return
