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
    "What would you like to start with?"
    jump materials_lab

# SOLID PHASE EXTRACTION CODE
# there are 5 steps for drugs too, 1. dilute the mixture, 2. condition the cartridge, 
# 3. load it with the sample, 4. wash the cartridge, 5. elution (obtain the extracted compound)
label solid_phase_extraction:
    $ hide_all_lab_screens()
    $ location = "solid_phase_extraction"
    scene lab_counter_bk
    if not analytical_balance_done:
        show nina normal1
        n "You'll need to weigh all three presumed samples on the analytical balance before you can begin extraction."
        hide nina normal1
        jump materials_lab

    if has_SPE_cocaine and has_SPE_mdma and has_SPE_meth:
        show nina normal1
        n "All three samples have already been through Solid Phase Extraction."
        n "Head to the GC-MS to continue the analysis."
        hide nina normal1
        jump materials_lab

    #PRE-TREATMENT
    hide screen back_button_screen onlayer over_screens
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
    menu:
        "37 Celsius":
            scene spe44
            "You've obtained the prepared sample."
            if(has_SPE_cocaine and current_SPE_drug == "cocaine"):
                $ evidence.add_to_inventory(evids["Prepared Cocaine Sample"])
            elif(has_SPE_mdma and current_SPE_drug == "mdma"):
                $ evidence.add_to_inventory(evids["Prepared MDMA Sample"])
            elif(has_SPE_meth and current_SPE_drug == "meth"):
                $ evidence.add_to_inventory(evids["Prepared Meth Sample"])
            if(has_SPE_cocaine and has_SPE_mdma and has_SPE_meth):
                $ gcms_step = 3
                $ choice_SPE = "COMPLETED"
            # reset counter
            hide screen spe_spo
            $ step_num_SPE = 1
            $ current_SPE_drug = ""
            show screen back_button_screen('materials_lab') onlayer over_screens
            jump materials_lab

# toolbox stuffs for SPE
label use5Amm:
    if location == "solid_phase_extraction":
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
    if location == "solid_phase_extraction":
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
    if location == "solid_phase_extraction":
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
    if location == "solid_phase_extraction":
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
    if location == "solid_phase_extraction":
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
    if location == "solid_phase_extraction":
        if(step_num_SPE == 3 and current_SPE_drug == "cocaine"):
            $ has_SPE_cocaine = True
            $ evidence.delete_from_inventory(evids["Cocaine Sample"])
            jump expression step_SPE
        else:
            "Wrong compound!"
            jump expression inv_call_SPE

label useMDMA:
    if location == "solid_phase_extraction":
        if(step_num_SPE == 3 and current_SPE_drug == "mdma"):
            $ has_SPE_mdma = True
            $ evidence.delete_from_inventory(evids["MDMA Sample"])
            jump expression step_SPE
        else:
            "Wrong compound!"
            jump expression inv_call_SPE

label useMeth:
    if location == "solid_phase_extraction":
        if(step_num_SPE == 3 and current_SPE_drug == "meth"):
            $ has_SPE_meth = True
            $ evidence.delete_from_inventory(evids["Meth Sample"])
            jump expression step_SPE
        else:
            "Wrong compound!"
            jump expression inv_call_SPE