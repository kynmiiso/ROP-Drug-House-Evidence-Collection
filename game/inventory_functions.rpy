init -5 python:

    def item_dragging_package(drags):
        global default_mouse
        default_mouse = "hand_grab"

    _IMAGE_TO_DRAG_NAME = {
        "marker_1": "marker_1",
        "marker_2": "marker_2",
        "marker_3": "marker_3",
        "marker_4": "marker_4",
        "marquis_reagent_idle":      "marquis_reagent_idle",
        "scott_reagent_idle":        "scott_reagent_idle",
        "tube_idle":                 "tube_idle",
        "evidence_bag_idle":         "evidence_bag_idle",
        "tamper_evident_tape_idle":  "tamper_evident_tape_idle",
        "backing_card_idle":         "backing_card_idle",
        "tape_idle":                 "tape_idle",
        "uv_light_idle":             "uv_light_idle",
        "magnetic_powder_idle":      "magnetic_powder_idle",
        "scalebar_idle":             "scalebar_idle",
        "pen_idle":                  "pen_idle"
    }

    _TOOL_NAME_TO_IMAGE = {
        "Evidence Markers":     "marker_dynamic",
        "Marquis Reagent":      "marquis_reagent_idle",
        "Scott Reagent":        "scott_reagent_idle",
        "Tube":                 "tube_idle",
        "Evidence Bag":         "evidence_bag_idle",
        "Tamper Evident Tape":  "tamper_evident_tape_idle",
        "Backing Card":         "backing_card_idle",
        "Tape":                 "tape_idle",
        "UV Light":             "uv_light_idle",
        "Magnetic Powder":      "magnetic_powder_idle",
        "Scalebar":             "scalebar_idle",
        "Pen":                  "pen_idle"
    }

    def _get_current_step():
        if testing_item is None:
            return None
        steps = valid_evidence_steps.get(testing_item, [])
        idx = store.evidence_step_index.get(testing_item, 0)
        drag_step = 0
        for s in steps:
            if isinstance(s, dict):
                if drag_step == idx:
                    return s
                drag_step += 1
        return None

    def _total_drag_steps(item):
        return sum(1 for s in valid_evidence_steps.get(item, []) if isinstance(s, dict))

    def _current_drop_image():
        if testing_item is None:
            return None
        steps = valid_evidence_steps.get(testing_item, [])
        idx = store.evidence_step_index.get(testing_item, 0)
        drag_index = 0
        for s in steps:
            if isinstance(s, dict):
                if drag_index == idx:
                    return list(s.keys())[0]
                drag_index += 1
        return None

    def _marker_after_index(item, idx):
        """
        Return the string marker immediately following dict step at position idx,
        or None if the next entry is another dict or end of list.
        """
        steps = valid_evidence_steps.get(item, [])
        drag_count = 0
        for i, s in enumerate(steps):
            if isinstance(s, dict):
                if drag_count == idx:
                    if i + 1 < len(steps) and isinstance(steps[i + 1], str):
                        return steps[i + 1]
                    return None
                drag_count += 1
        return None

    def _quiz_is_next():
        if testing_item is None:
            return False
        idx = store.evidence_step_index.get(testing_item, 0)
        return _marker_after_index(testing_item, idx) == "quiz"

    def _fingerprint_collect_is_next():
        """
        True only when the COMPLETED step (idx - 1) has fingerprint_collect
        immediately after it — meaning we just finished the tamper tape step
        that precedes the fingerprint_collect marker.
        """
        if testing_item is None:
            return False
        idx = store.evidence_step_index.get(testing_item, 0)
        if idx == 0:
            return False
        # Check marker after the step we just completed (idx - 1)
        return _marker_after_index(testing_item, idx - 1) == "fingerprint_collect"

    def _collect_step_is_next():
        if testing_item is None:
            return False
        idx = store.evidence_step_index.get(testing_item, 0)
        if idx == 0:
            return False
        return _marker_after_index(testing_item, idx - 1) == "collect_step"

    def _advance_step():
        idx = store.evidence_step_index.get(testing_item, 0)
        store.evidence_step_index[testing_item] = idx + 1

    def generic_drop(drags, drop):
        if not drop:
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        dragged_image = drags[0].drag_name
        step = _get_current_step()

        if step is None:
            store.selected_tool = None
            renpy.restart_interaction()
            return False

        correct_tool_image = list(step.values())[0]

        if correct_tool_image == "marker_dynamic":
            order = store.evidence_visited_order
            expected = "marker_" + str(order.index(store.testing_item) + 1)
            if dragged_image != expected:
                renpy.notify("That's not the right tool for this step.")
                store.selected_tool = None
                renpy.hide_screen("drug_processing_screen")
                renpy.restart_interaction()
                return False
            store.evidence_marker_placed[store.testing_item] = True
        elif dragged_image != correct_tool_image:
            renpy.notify("That's not the right tool for this step.")
            store.selected_tool = None
            renpy.hide_screen("drug_processing_screen")
            renpy.restart_interaction()
            return False

        _advance_step()

        new_idx = store.evidence_step_index.get(store.testing_item, 0)
        marker = _marker_after_index(store.testing_item, new_idx - 1)

        if marker == "quiz":
            store.evidence_found[store.testing_item + "_presumptive"] = True
            store.quiz_pending = True
        elif marker == "fingerprint_collect":
            store.fingerprint_collect_ready = True
        elif marker == "collect_step":
            store.collect_step_ready = True

        store.selected_tool = None
        renpy.restart_interaction()
        return True

    def _use_tool(tool_name):
        if testing_item is None:
            renpy.notify("Select an evidence item first.")
            return
        image_name = _TOOL_NAME_TO_IMAGE.get(tool_name)
        if image_name is None:
            renpy.notify("This tool can't be used here.")
            return
        store.selected_tool = image_name
        renpy.restart_interaction()

    def use_evidence_markers():
        if testing_item is None:
            renpy.notify("Select an evidence item first.")
            return
        order = store.evidence_visited_order
        if testing_item not in order:
            renpy.notify("This evidence hasn't been logged yet.")
            return
        num = order.index(testing_item) + 1
        image_name = "marker_" + str(num)
        store.selected_tool = image_name
        renpy.restart_interaction()

    def use_marquis_reagent():      _use_tool("Marquis Reagent")
    def use_scott_reagent():        _use_tool("Scott Reagent")
    def use_tube():                 _use_tool("Tube")
    def use_evidence_bag():         _use_tool("Evidence Bag")
    def use_tamper_evident_tape():  _use_tool("Tamper Evident Tape")
    def use_backing_card():         _use_tool("Backing Card")
    def use_tape():                 _use_tool("Tape")
    def use_uv_light():             _use_tool("UV Light")
    def use_magnetic_powder():      _use_tool("Magnetic Powder")
    def use_scalebar():             _use_tool("Scalebar")
    def use_pen():                  _use_tool("Pen")

    def import_firearm_fingerprint():
        global imported_print
        if location == "afis":
            if not ca_chamber_done:
                renpy.notify("Process the firearm in the CA chamber before importing a print.")
                return
            imported_print = "firearm_fingerprint"
            renpy.jump("import_print")
        else:
            renpy.notify("Bring this to AFIS to import it.")

    def use_distilled_water():
        if location != "ca_chamber" and location != "solid_phase_extraction":
            renpy.notify("Bring this to the CA chamber or Solid Phase Extraction to use it.")
            return
        if location == "solid_phase_extraction":
            renpy.jump("useWater")
        store.selected_tool = "toolbox-distilled_water"
        renpy.restart_interaction()

    def use_superglue():
        if location != "ca_chamber":
            renpy.notify("Bring this to the CA chamber to use it.")
            return
        store.selected_tool = "toolbox-superglue"
        renpy.restart_interaction()

    def use_firearm():
        if location != "ca_chamber":
            renpy.notify("Bring this to the CA chamber to use it.")
            return
        if ca_chamber_state != "empty":
            renpy.notify("The CA chamber isn't ready for the firearm right now.")
            return
        store.selected_tool = "inventory-firearm"
        renpy.restart_interaction()

    def use_methanol():
        renpy.jump("useMethanol")

    def use_step3():
        renpy.jump("useStep3")

    def use_01formic():
        renpy.jump("use01Formic")

    def use_5amm():
        renpy.jump("use5Amm")
        
    def use_cocaine_sample():
        if location == "analytical_balance":
            analytical_balance_use_sample("cocaine")
        elif location == "solid_phase_extraction":
            renpy.jump("useCocaine")
        else:
            renpy.notify("Bring this to the balance or SPE to use it.")

    def use_mdma_sample():
        if location == "analytical_balance":
            analytical_balance_use_sample("mdma")
        elif location == "solid_phase_extraction":
            renpy.jump("useMDMA")
        else:
            renpy.notify("Bring this to the balance or SPE to use it.")

    def use_meth_sample():
        if location == "analytical_balance":
            analytical_balance_use_sample("meth")
        elif location == "solid_phase_extraction":
            renpy.jump("useMeth")
        else:
            renpy.notify("Bring this to the balance or SPE to use it.")

    def analytical_balance_use_sample(drug):
        if store.balance_state != "zero":
            renpy.notify("Remove the current sample before weighing another.")
            return
        store.balance_state = drug
        weigh_sample(drug)
        renpy.restart_interaction()

    def use_prepared_cocaine():
        gcms_use_prepared_sample("cocaine")

    def use_prepared_mdma():
        gcms_use_prepared_sample("mdma")

    def use_prepared_meth():
        gcms_use_prepared_sample("meth")

    def gcms_use_prepared_sample(drug):
        if location != "gcms":
            renpy.notify("Bring this to the GC-MS to analyze it.")
            return
        if gcms_step != 3:
            renpy.notify("The GC-MS isn't ready for a sample right now.")
            return
        if drug != gcms_current_drug:
            renpy.notify("That's not the sample queued for analysis.")
            return
        store.gcms_step = 4
        renpy.notify("Sample loaded into the GC autosampler.")
        renpy.restart_interaction()
    
    def view_lab_notebook():
        renpy.show_screen("lab_notebook")