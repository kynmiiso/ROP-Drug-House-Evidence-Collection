default weighed_cocaine = False
default weighed_mdma    = False
default weighed_meth    = False
default drug_weights = {"cocaine": None, "mdma": None, "meth": None}
default balance_state = "zero"   # zero / cocaine / mdma / meth

init python:
    _CORRECT_WEIGHTS = {"cocaine": 2.6703, "mdma": 1.8415, "meth": 3.1296}

    def weigh_sample(drug):
        global weighed_cocaine, weighed_mdma, weighed_meth
        drug_weights[drug] = _CORRECT_WEIGHTS[drug]
        if drug == "cocaine":
            weighed_cocaine = True
        elif drug == "mdma":
            weighed_mdma = True
        elif drug == "meth":
            weighed_meth = True
        renpy.notify(f"Recorded weight: {_CORRECT_WEIGHTS[drug]} g")

    def analytical_balance_drop(drags, drop):
        if not drop:
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        dragged_image = drags[0].drag_name

        if dragged_image == "inventory-cocaine" and store.balance_state == "zero":
            store.balance_state = "cocaine"
            weigh_sample("cocaine")
        elif dragged_image == "inventory-mdma" and store.balance_state == "zero":
            store.balance_state = "mdma"
            weigh_sample("mdma")
        elif dragged_image == "inventory-meth" and store.balance_state == "zero":
            store.balance_state = "meth"
            weigh_sample("meth")
        else:
            renpy.notify("Remove the current sample before weighing another.")
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        store.selected_tool = None
        renpy.restart_interaction()
        return True

label analytical_balance:
    $ hide_all_lab_screens()
    $ hide_all_inventory()
    $ location = "analytical_balance"
    scene materials_lab
    show screen analytical_balance_screen
    show screen inventory
    show screen back_button_screen('materials_lab') onlayer over_screens
