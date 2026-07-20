init python:
    import json

    # FUNCTION FOR DRAG AND DROP
    def put_in_bag(drags, drop):
        if drop:
            return True
        else: 
            return

# CODE BELOW IS FOR THE LAB ------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------
# LAB VARS ---
default in_lab = False
# SPE
default spe_difficulty = 0 # 0 = full checklist, 1 = half checklist, 2 = low checklist
default has_SPE_cocaine = False
default has_SPE_mdma = False
default has_SPE_meth = False
default step_SPE = ""
default step_num_SPE = 1 # see ipad notes for specifics, relates to which step to do, related to the spe_spo
default inv_call_SPE = ""
default choice_SPE = ""
default current_SPE_drug = ""

# LAB LABELS ----------
label lab:
    scene black
    $ in_lab = True

    #removing previous toolbox items
    # $ toolbox.delete_from_inventory(tools["Evidence Markers"])
    # $ toolbox.delete_from_inventory(tools["Marquis Reagent"])
    # $ toolbox.delete_from_inventory(tools["Scott Reagent"])
    # $ toolbox.delete_from_inventory(tools["Tube"])
    # $ toolbox.delete_from_inventory(tools["Evidence Bag"])
    # $ toolbox.delete_from_inventory(tools["Tamper Evident Tape"])

    # adding correct toolbox items
    # $ toolbox.add_to_inventory(tools["100% Methanol"])
    # $ toolbox.add_to_inventory(tools["Distilled Water"])
    # $ toolbox.add_to_inventory(tools["1% Formic acid"])
    # $ toolbox.add_to_inventory(tools["0.1% Formic acid"])
    # $ toolbox.add_to_inventory(tools["Methanol and 5% Ammonium Hydroxide"])

    "What would you like to start with?"
    jump materials_lab

# this is handled by lab_hallway_screen, materials_lab_screen, and data_analysis_lab_screen and called in script.rpy
# label lab_choice: # may add GC-MS and GC-headspace, but these are the minimum requirements to analyse
#     scene black
#     menu:
#         "Solid phase extraction [choice_SPE]":
#             jump solid_phase_extraction
#         "GC-MS":
#             jump lc_ms
#         "Fingerprinting Analysis":
#             jump fingerprint_analysis
#         "Blender":
#             jump blender
#         "Vortex mixer":
#             jump vortexmixer
#         "Centrifuge":
#             jump centrifuge
#     return

# SOLID PHASE EXTRACTION CODE
# there are 5 steps for drugs too, 1. dilute the mixture, 2. condition the cartridge, 
# 3. load it with the sample, 4. wash the cartridge, 5. elution (obtain the extracted compound)
label solid_phase_extraction:
    #PRE-TREATMENT
    $ hide_all_lab_screens()
    $ location = "solid_phase_extraction"
    scene lab_counter_bk
    show beaker_empty:
        xalign 0.5
        yalign 0.5
    show nina talk
    n "Before you do anything, you'll need to pre-treat your sample and dilute it 1:1 with an acidic buffer."
    n "Which drug sample do you want to dilute?"
    hide nina talk
    menu:
        "Cocaine Sample" if not has_SPE_cocaine:
            $ current_SPE_drug = "cocaine"
            show beaker_cocaine:
                xalign 0.5
                yalign 0.5
        "MDMA Sample" if not has_SPE_mdma:
            $ current_SPE_drug = "mdma"
            show beaker_mdma:
                xalign 0.5
                yalign 0.5
        "Methamphetamine Sample" if not has_SPE_meth:
            $ current_SPE_drug = "meth"
            show beaker_meth:
                xalign 0.5
                yalign 0.5
    jump SPE_dilute_question

label SPE_dilute_question:
    $ inv_call_SPE = "SPE_dilute_question"
    $ step_SPE = "SPE_condition"
    "What will you use to dilute the drug sample?"
    call screen inventory
    return

label SPE_condition:
    scene spe11
    show screen spe_spo
    $ inv_call_SPE = "SPE_condition"
    $ step_SPE = "SPE_condition1"
    call screen inventory

label SPE_condition1:
    scene spe12
    $ step_num_SPE = 2 # catridge has been reinsed with methanol waiting for 2
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            jump SPE_condition2
        "1 mL/minute":
            "Wrong."
            jump SPE_condition1

label SPE_condition2:
    $ inv_call_SPE = "SPE_condition2"
    $ step_SPE = "SPE_condition3" #1% formic acid or water
    scene spe13
    call screen inventory

label SPE_condition3:
    scene spe14
    $ step_num_SPE = 3 # catridge has been reinsed with formic or water waiting for loading
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            jump SPE_loading
        "1 mL/minute":
            "Wrong. Try again."
            jump SPE_condition3

label SPE_loading:
    scene spe13
    $ renpy.pause(0.5, hard=True)
    scene spe21
    $ inv_call_SPE = "SPE_loading"
    $ step_SPE = "SPE_loading1"
    call screen inventory

label SPE_loading1:
    scene spe22
    $ step_num_SPE = 4 # drugs in, next wash w/formic
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            "Wrong. Try again."
            jump SPE_loading1
        "1 mL/minute":
            jump SPE_washing

label SPE_washing:
    scene spe23
    $ renpy.pause(0.5, hard=True)
    scene spe31
    $ inv_call_SPE = "SPE_washing"
    $ step_SPE = "SPE_washing1"
    call screen inventory

label SPE_washing1:
    scene spe32
    $ step_num_SPE = 5 # washg fromic, next wash w/methanol
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            "Wrong. Try again."
            jump SPE_washing1
        "1 mL/minute":
            jump SPE_washing2

label SPE_washing2:
    scene spe33
    $ inv_call_SPE = "SPE_washing2"
    $ step_SPE = "SPE_washing3" #methanol
    call screen inventory

label SPE_washing3:
    scene spe34
    $ step_num_SPE = 6 # 5% ammonium hydroxide ELUTION
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            "Wrong."
            jump SPE_washing3
        "1 mL/minute":
            jump SPE_elution

label SPE_elution:
    scene spe33
    $ renpy.pause(0.5, hard=True)
    scene spe41
    $ inv_call_SPE = "SPE_elution"
    $ step_SPE = "SPE_elution1"
    call screen inventory

label SPE_elution1:
    $ step_num_SPE = 7
    scene spe42
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            "Wrong."
            jump SPE_elution1
        "1 mL/minute":
            jump SPE_elution2

label SPE_elution2:
    scene spe43
    "What temperature should the mixture be dried at?"
    # can add the timer, so like, do fingerprinting analysis while the mixture dries
    menu:
        "37 Celsius": # this is the correct temperature, ummmm may change this
            scene spe44
            "You've obtained the prepared sample."
            if(has_SPE_cocaine):
                $ evidence.add_to_inventory(evids["Prepared Cocaine Sample"])
            elif(has_SPE_mdma):
                $ evidence.add_to_inventory(evids["Prepared MDMA Sample"])
            elif(has_SPE_meth):
                $ evidence.add_to_inventory(evids["Prepared Meth Sample"])
            if(has_SPE_cocaine and has_SPE_mdma and has_SPE_meth):
                $ choice_SPE = "COMPLETED"
            # reset counter
            hide screen spe_spo
            $ step_num_SPE = 1
            jump materials_lab
        # can add other choices here

# toolbox stuffs for SPE
label use5Amm:
    if(inv_call_SPE == "SPE_dilute_question"):
        "Wrong!"
        jump expression inv_call_SPE
    else:
        if(step_num_SPE != 6):
            "Wrong compound!"
            jump expression inv_call_SPE

        "How much will you add?"
        menu:
            "1 mL":
                jump expression step_SPE
            "2 mL":
                "Wrong amount."
                jump expression inv_call_SPE
            "5 mL":
                "Wrong amount."
                jump expression inv_call_SPE

label use01Formic:
    if(inv_call_SPE == "SPE_dilute_question"):
        "Wrong!"
        jump expression inv_call_SPE
    else:
        if(step_num_SPE != 4):
            "Wrong compound!"
            jump expression inv_call_SPE

        "How much will you add?"
        menu:
            "1 mL":
                jump expression step_SPE
            "2 mL":
                "Wrong amount."
                jump expression inv_call_SPE
            "5 mL":
                "Wrong amount."
                jump expression inv_call_SPE

label useMethanol:
    if(inv_call_SPE == "SPE_dilute_question"):
        "Wrong!"
        jump expression inv_call_SPE
    else:
        if(step_num_SPE != 1 and step_num_SPE != 5):
            "Wrong compound!"
            jump expression inv_call_SPE

        "How much will you add?"
        menu:
            "1 mL":
                jump expression step_SPE
            "2 mL":
                "Wrong amount."
                jump expression inv_call_SPE
            "5 mL":
                "Wrong amount."
                jump expression inv_call_SPE
            # can add other options here

label useStep3: # 1% formic acid 
    if(inv_call_SPE == "SPE_dilute_question"):
        show nina normal1
        "Good! Now we'll start."
        hide nina normal1
        jump expression step_SPE
    else:
        if(step_num_SPE != 2):
            "Wrong compound!"
            jump expression inv_call_SPE

        "How much will you add?"
        menu:
            "1 mL":
                jump expression step_SPE
            "2 mL":
                "Wrong amount."
                jump expression inv_call_SPE
            "5 mL":
                "Wrong amount."
                jump expression inv_call_SPE

label useWater: # use water
    if(inv_call_SPE == "SPE_dilute_question"):
        "Wrong!"
        jump expression inv_call_SPE
    else:
        if(step_num_SPE != 2):
            "Wrong compound!"
            jump expression inv_call_SPE

        "How much will you add?"
        menu:
            "1 mL":
                jump expression step_SPE
            "2 mL":
                "Wrong amount."
                jump expression inv_call_SPE
            "5 mL":
                "Wrong amount."
                jump expression inv_call_SPE

label useCocaine:
    $ has_SPE_cocaine = True
    if(step_num_SPE == 3 and current_SPE_drug == "cocaine"):
        $ evidence.delete_from_inventory(evids["Cocaine Sample"])
        jump expression step_SPE
    else:
        "Wrong compound!"
        jump expression inv_call_SPE

label useMDMA:
    $ has_SPE_mdma = True
    if(step_num_SPE == 3 and current_SPE_drug == "mdma"):
        $ evidence.delete_from_inventory(evids["MDMA Sample"])
        jump expression step_SPE
    else:
        "Wrong compound!"
        jump expression inv_call_SPE

label useMeth:
    $ has_SPE_meth = True
    if(step_num_SPE == 3 and current_SPE_drug == "meth"):
        $ evidence.delete_from_inventory(evids["Meth Sample"])
        jump expression step_SPE
    else:
        "Wrong compound!"
        jump expression inv_call_SPE
