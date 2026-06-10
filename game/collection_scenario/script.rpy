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
        "meth_presumptive":    False,
        "meth_packaged":       False,
        "cocaine_presumptive": False,
        "cocaine_packaged":    False,
    }

    # Step definitions 
    # "quiz" is a marker that triggers the identification question in between steps
    valid_evidence_steps = {
        "cocaine": [
            {"cocaine_idle":    "scott_reagent_idle"},
            "quiz",
            {"cocaine_blue":    "evidence_bag_idle"},
            {"evidence_bag_idle":    "tamper_evident_tape_idle"},
        ],
        "mdma": [
            {"mdma_idle":       "marquis_reagent_idle"},
            "quiz",
            {"mdma_purple":     "evidence_bag_idle"},
            {"evidence_bag_idle":    "tamper_evident_tape_idle"},
        ],
        "meth": [
            {"meth_idle":       "marquis_reagent_idle"},
            "quiz",
            {"meth_brown":      "evidence_bag_idle"},
            {"evidence_bag_idle":    "tamper_evident_tape_idle"},
        ],
    }

    # Hotspot positions per item
    evidence_positions = {
        "cocaine": (0.15, 0.70),
        "mdma":    (0.50, 0.65),
        "meth":    (0.30, 0.80),
    }

    # Per-item step index (counts drag steps only, not quiz markers)
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

    testing_item   = None
    selected_tool  = None
    quiz_pending   = False


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
    def _current_drop_image():
        """Return the drop target image for the current drag step."""
        if testing_item is None:
            return None
        steps = valid_evidence_steps.get(testing_item, [])
        idx = evidence_step_index.get(testing_item, 0)
        drag_steps = [s for s in steps if s != "quiz"]
        if idx < len(drag_steps):
            return list(drag_steps[idx].keys())[0]
        return None

    def _quiz_is_next():
        """True if the next thing after the last completed step is a quiz marker."""
        if testing_item is None:
            return False
        steps = valid_evidence_steps.get(testing_item, [])
        idx = evidence_step_index.get(testing_item, 0)
        # Walk through steps counting drag steps; check what follows step idx-1
        drag_count = 0
        for i, s in enumerate(steps):
            if s == "quiz":
                continue
            drag_count += 1
            if drag_count == idx:
                # Check if next entry is quiz
                if i + 1 < len(steps) and steps[i + 1] == "quiz":
                    return True
                return False
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

    if not evidence_found["cocaine_packaged"]:
        imagebutton:
            xpos 0.15  ypos 0.70
            idle  ("cocaine_idle" if not evidence_found["cocaine_presumptive"] else "cocaine_blue")
            hover ("cocaine_hover" if not evidence_found["cocaine_presumptive"] else "cocaine_blue")
            mouse "hover"
            hovered   Notify("Suspected powder")
            unhovered NullAction()
            action [
                SetVariable("testing_item",  "cocaine"),
                SetVariable("selected_tool", None),
                Jump("inspect_evidence"),
            ]
    # elif evidence_found["cocaine_packaged"] and "cocaine" not in collected_evidence_inventory:
    #     imagebutton:
    #         xpos 0.15 ypos 0.70
    #         idle "casefile_evidence_idle"
    #         hover "casefile_evidence_hover"
    #         action [
    #             Function(evidence.add_to_inventory, evids["Cocaine Sample"]),
    #             SetDict(evidence_found, "cocaine_packaged", True),
    #             Show("inventory"),
    #             Notify("Evidence added to inventory"),
    #         ]

    if not evidence_found["mdma_packaged"]:
        imagebutton:
            xpos 0.50  ypos 0.65
            idle  ("mdma_idle" if not evidence_found["mdma_presumptive"] else "mdma_purple")
            hover ("mdma_hover" if not evidence_found["mdma_presumptive"] else "mdma_purple")
            mouse "hover"
            hovered   Notify("Suspected pills")
            unhovered NullAction()
            action [
                SetVariable("testing_item",  "mdma"),
                SetVariable("selected_tool", None),
                Jump("inspect_evidence"),
            ]
    # elif evidence_found["mdma_packaged"] and "mdma" not in collected_evidence_inventory:
    #     imagebutton:
    #         xpos 0.15 ypos 0.70
    #         idle "casefile_evidence_idle"
    #         hover "casefile_evidence_hover"
    #         action [
    #             Function(evidence.add_to_inventory, evids["MDMA Sample"]),
    #             SetDict(evidence_found, "mdma_packaged", True),
    #             Show("inventory"),
    #             Notify("Evidence added to inventory"),
    #         ]

    if not evidence_found["meth_packaged"]:
        imagebutton:
            xpos 0.30  ypos 0.80
            idle  ("meth_idle" if not evidence_found["meth_presumptive"] else "meth_brown")
            hover ("meth_hover" if not evidence_found["meth_presumptive"] else "meth_brown")
            mouse "hover"
            hovered   Notify("Suspected crystals")
            unhovered NullAction()
            action [
                SetVariable("testing_item",  "meth"),
                SetVariable("selected_tool", None),
                Jump("inspect_evidence"),
            ]
    # elif evidence_found["meth_packaged"] and "meth" not in collected_evidence_inventory:
    #     imagebutton:
    #         xpos 0.15 ypos 0.70
    #         idle "casefile_evidence_idle"
    #         hover "casefile_evidence_hover"
    #         action [
    #             Function(evidence.add_to_inventory, evids["Meth Sample"]),
    #             SetDict(evidence_found, "meth_packaged", True),
    #             Show("inventory"),
    #             Notify("Evidence added to inventory"),
    #         ]

    if (evidence_found["cocaine_packaged"]
            and evidence_found["mdma_packaged"]
            and evidence_found["meth_packaged"]):
        textbutton "Finish Investigation":
            xpos 0.02  ypos 0.88
            style "hud_button"
            action Jump("investigation_complete")


screen colour_chart(chart_image):
    modal False
    add chart_image xalign 0.5 yalign 0.5


# ---------------------------------------------------------------------------
# Single generic inspect label — handles all three drugs
# ---------------------------------------------------------------------------
screen reagent_result(item):
    modal False

    if item == "cocaine":
        add "cocaine_blue" xalign 0.75 yalign 0.5
    elif item == "mdma":
        add "mdma_purple" xalign 0.75 yalign 0.5
    elif item == "meth":
        add "meth_brown" xalign 0.75 yalign 0.5

label inspect_evidence:
    hide screen investigation_buttons
    show screen inventory

    label evidence_wait_step:
        # All drag steps done for this item?
        if evidence_found[testing_item + "_packaged"]:
            jump evidence_done

        # Check if a quiz is pending before the next drag step
        if quiz_pending:
            jump evidence_quiz

        # Show the drag screen for the current step
        $ drop_img = _current_drop_image()
        $ xp, yp  = evidence_positions[testing_item]
        show screen drug_processing_screen(drop_img, xp, yp)
        $ renpy.pause(0.3)
        jump evidence_wait_step

    label evidence_quiz:
        hide screen drug_processing_screen
        $ _q = _QUIZ[testing_item]
        show screen colour_chart(_q["chart"])
        show screen reagent_result(testing_item)
        "What drug is this based on the colour reaction?"
        menu:
            "[_q['correct']]":
                $ store.quiz_pending = False
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
        hide screen drug_processing_screen
        hide screen colour_chart
        hide screen reagent_result
        hide screen Inventory
        $ evidence.add_to_inventory(testing_item)
        $ evidence_found[testing_item + "_packaged"] = True
        $ testing_item = None
        $ selected_tool = None
        show screen investigation_buttons
        jump scene_room_loop

# ---------------------------------------------------------------------------
# scene_room_loop
# ---------------------------------------------------------------------------
label scene_room_loop:
    show screen investigation_buttons
    pause 0.3
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
    n ""
    show nina thinknote1
    n "Once the player has finished collecting all their evidence, we should move on to the lab level for analysis."
    n "This won't be covered until later on though. For now, give yourselves a pat on the back!"
    return
