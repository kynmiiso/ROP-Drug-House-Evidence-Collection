"""
This file contains the
"""

default current_cursor = ''
default show_case_files = False
default show_toolbox = False
default location = "hallway"

### entries on afis when search
default afis_search = []
default afis_search_coordinates = [{'score_xpos': 0.53, 'xpos':0.61, 'ypos':0.505}]
# default correct_dfo_mixture = {"dfo", "hfe", "acetic acid", "methanol"}
# default player_dfo_mixture = {}
# default player_tool = ""
define s = Character(name=("Nina"), image="nina")

init python:
    
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

    def toolbox_actions(item: str) -> None:
        global tool
        global ready_to_mix
        if ready_to_mix:
            hide_all_inventory()
            if item == "methanol":
                tool = "methanol"
                renpy.hide_screen("full_inventory")
                renpy.jump("pour_methanol")
            elif item == "dfo":
                tool = "dfo"
                renpy.jump("pour_dfo")
            elif item == "acetic_acid":
                tool = "acetic acid"
                renpy.jump("pour_acetic_acid")
            elif item == "hfe":
                tool = "hfe"
                renpy.jump("pour_hfe")
    
    def inventory_actions(item: str) -> None:
        global location
        global gin
        global imported_print
        global pressed

        if item == "gin":
            if location == "fumehood" and not gin.processed:
                hide_all_inventory()
                renpy.jump("fumehood_bottle")
        elif item == "label" or item == "baked_label":
            label_function_alt()
        elif item == "fingerprint":
            if location == "afis" and pressed == "import":
                imported_print = "print_1"
                renpy.jump("import_print")

# Non-inventory related functions -----------------------------------
    config.mouse = {
        "default": [("cursor.png", 0, 0)],
        "dropper": [("dropper.png", 0, 49)],
        "dropper filled": [("dropper filled.png", 0, 49)],
        "hand": [("default_hand.png", 0, 0)]
    }

    default_mouse = "default"

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
        return prints["print_1"].processed and prints["print_4"].processed
    
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
    
    ### declare each piece of evidence
    laptop_fingerprint = Evidence(name = 'laptop_fingerprint',
                                afis_details = {
                                    'image': 'laptop_fingerprint',
                                    'xpos':0.18, 'ypos':0.3,
                                    'score': '70'})
    screwdriver = Evidence(name = 'screwdriver',
                        afis_details = {
                            'image': 'screwdriver_fingerprint',
                            'xpos':0.18, 'ypos':0.3,
                            'score': '70'})
    
    ### declare afis relevant evidence
    afis_evidence = [laptop_fingerprint, screwdriver]

    ### set current_evidence to track which evidence is currently active
    current_evidence = screwdriver

#################################### START #############################################
label start:
    # Dial variables
    $ dial_image = "images/dial.png"
    $ dial_size = (660 / 2, 660 / 2)
    $ t = Transform(child = dial_image, zoom = 0.5)
    $ dial_sprite_manager = SpriteManager(event = dial_events)
    $ dial_sprite = dial_sprite_manager.create(t)
    $ dial_sprite.x = config.screen_width / 2 - dial_size[0] / 2
    $ dial_sprite.y = config.screen_height / 2 - dial_size[1] / 2
    $ dial_rotate = False
    $ dial_sprite.rotate_amount = 0
    $ dial_offset = 68.2
    $ dial_start_rotate = False
    $ dial_number = 0
    $ dial_text = 0
    $ previous_dial_text = 0
    $ dial_changed = False

    # Other variables
    $ old_mousepos = (0.0, 0.0)
    $ degrees = 0
    $ old_degrees = 0
    $ combinations = {"safe_1" : 50, "safe_2" : [23, 5, 75, 44]}
    $ completed_combination_numbers = {}
    $ combination_check = None
    $ current_safe = 1
    $ combination_length = 0
    scene entering_lab_screen
    with Dissolve(1.5)

label lab_hallway_intro:  
    scene lab_hallway_idle
    show nina normal1 
    s "Officer, good to see you again."
    show nina normal3 
    s "Great job processing the scene! I knew I could count on you!"
    # s "While you’ve been busy, I talked to the other officers who were on the scene that day. They collected this."
    s "Welcome to the lab! Here, you can analyze all the evidence you collected from the crime scene."
    show nina thinknote1 
    s "I need you to perform a pattern analysis on the fingerprint you found on the door and on the gin bottle you collected."
    s "For the gin bottle, you'll have to remove the label and use DFO to actually get a print to load into the fingerprint pattern analysis application."
    show nina normal3 
    s "You can go wherever you want - but I suggest beginning with the oven first so we won't have to waste time waiting for it to heat up."

    # REQUIRED FOR INVENTORY:
    $config.rollback_enabled = False # disables rollback
    $quick_menu = False # removes quick menu (at bottom of screen) - might put this back since inventory bar moved to right side
    
    # environment:
    $environment_SM = SpriteManager(event = environmentEvents) # sprite manager that manages environment items; triggers function environmentEvents() when event happens with sprites (e.g. button click)
    $environment_sprites = [] # holds all environment sprite objects
    $environment_items = [] # holds environment items
    $environment_item_names = [] # holds environment item names
    
    # inventory
    $inventory_SM = SpriteManager(update = inventoryUpdate, event = inventoryEvents) # sprite manager that manages evidence items; triggers function inventoryUpdate 
    $inventory_sprites = [] # holds all evidence sprite objects
    $inventory_items = [] # holds evidence items
    $inventory_item_names = ["Tape on acetate", "Tapeglo in bag", "Tape photo", "Duct tape tapeglo", "Distilled water", "Tape in tweezers", "Duct tape", "Tapeglo", 
    "Fingerprint on card", "Backing card","Scalebar", "Lifting tape", "Jar photo", "Lid in tweezers", "Camel brush", "Lid with soot", "Lid", "Camphor smoke", "Lighter", 
    "Tweezers", "Gloves box", "Evidence bag", "Jar in bag", "Tape in bag", "Pvs in bag"] # holds names for inspect pop-up text 
    $inventory_db_enabled = False # determines whether up arrow on evidence hotbar is enabled or not
    $inventory_ub_enabled = False # determines whether down arrow on evidence hotbar is enabled or not
    $inventory_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for evidence bar
    $inventory_slot_padding = 120 / 2 # sets padding size between evidence slots
    $inventory_first_slot_x = 110 # sets x coordinate for first evidence slot
    $inventory_first_slot_y = 175 # sets y coordinate for first evidence slot
    $inventory_drag = False # by default, item isn't draggable

    # toolbox:
    $toolbox_SM = SpriteManager(update = toolboxUpdate, event = toolboxEvents) # sprite manager that manages toolbox items; triggers function toolboxUpdate 
    $toolbox_sprites = [] # holds all toolbox sprite objects
    $toolbox_items = [] # holds toolbox items
    # $toolbox_item_names = ["Tape", "Ziploc bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag"] # holds names for inspect pop-up text 
    $toolbox_db_enabled = False # determines whether up arrow on toolbox hotbar is enabled or not
    $toolbox_ub_enabled = False # determines whether down arrow on toolbox hotbar is enabled or not
    # $toolbox_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for toolbox bar
    $toolbox_slot_size = (100, 100)
    # $toolbox_slot_padding = 125 / 2 # sets padding size between toolbox slots
    $toolbox_slot_padding = 69
    $toolbox_first_slot_x = 110 # sets x coordinate for first toolbox slot
    $toolbox_first_slot_y = 175 # sets y coordinate for first toolbox slot
    $toolbox_drag = False # by default, item isn't draggable

    # toolbox popup:
    $toolboxpop_SM = SpriteManager(update = toolboxPopUpdate, event = toolboxPopupEvents) # sprite manager that manages toolbox pop-up items; triggers function toolboxPopUpdate
    $toolboxpop_sprites = [] # holds all toolbox pop-up sprite objects
    $toolboxpop_items = [] # holds toolbox pop-up items
    # $toolboxpop_item_names = ["Tape", "Ziploc bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag"] # holds names for inspect pop-up text 
    $toolboxpop_db_enabled = False # determines whether up arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_ub_enabled = False # determines whether down arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_slot_size = (100, 100) # sets slot size for toolbox pop-up bar
    $toolboxpop_slot_padding = 69 # sets padding size between toolbox pop-up slots
    $toolboxpop_first_slot_x = 406 # sets x coordinate for first toolbox pop-up slot
    $toolboxpop_first_slot_y = 445 # sets y coordinate for first toolbox pop-up slot
    $toolboxpop_drag = False # by default, item isn't draggable

    $current_scene = "scene1" # keeps track of current scene
    
    $dialogue = {} # set that holds name of character saying dialogue and dialogue message
    $item_dragged = "" # keeps track of current item being dragged
    $mousepos = (0.0, 0.0) # keeps track of current mouse position
    $i_overlap = False # checks if 2 inventory items are overlapping/combined
    $ie_overlap = False # checks if an inventory item is overlapping with an environment item

    $all_pieces = 0

    # python code block
    python:
        addToToolbox(["methanol", "acetic_acid", "dfo", "hfe"])
        addToInventory(["gin", "fingerprint"])


    # scene scene-1-bg at half_size - sets background image, don't need rn

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

label wet_lab:
    $ location = ""
    show screen full_inventory
    python:
        if analyzed_everything():
            renpy.hide_screen("full_inventory")
            renpy.jump("end")
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen wet_lab_screen

label analytical_instruments:
    show screen full_inventory
    python:
        if analyzed_everything():
            renpy.hide_screen("full_inventory")
            renpy.jump("end")
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen analytical_instruments_screen

label end:
    hide screen back_button_screen onlayer over_screens
    show nina normal1 
    s "It looks like you've analyzed all the evidence. Great work!"
    s "I hope you took note of the results. Tomorrow, you'll be testifying in court about your findings."
    show nina normal3 
    s "But for now, give yourself a pat on the back and go get some rest!"
    return