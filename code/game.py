import world
import save as s
import player as p

i = 0 # current turn
previ = 0 # previous turn
# the room only modifies the player if i != previ
# i.e. the player has done something like moving, resting or attacking
# and not something like viewing their inventory
player = None # the player we are using. defined here sothat it's a global var

def make_player():
    return p.Player()

def play(m, l=False): #Set l to True if you're loading a save False not a map
    global i
    global previ
    previ = 0
    i = 1 # game turn 1: the player spawns in
    if not l: # if you're loading a map
        world.load_tiles(m) # load the map
    else: # otherwise
        world.load_tiles('basic world') # temporarily load 'basic world'
    global player
    player = make_player() # make the player
    if l: # if you're loading a save
        global load
        load(m) # run the load function (later in the file)
    room = world.tile_exists(player.location_x, player.location_y) # find the room the player is in
    print(room.intro_text()) # Print the room's "intro text"
    while player.is_alive() and not player.victory:  # the main game loop
        room = world.tile_exists(player.location_x, player.location_y) # the room the player is in
        if previ != i: # if the player has done something like moving, resting or attacking
            room.modify_player(player) # let the room do what it must do
        if player.is_alive() and not player.victory: # check if the player is dead or beat the game since the room could have changed the player's state
            print("\nPlay Turn "+str(i)+", Choose an Action:\n")
            available_actions = room.available_actions() # get all available actions
            for action in available_actions:
                print(action) # print every action you can do
            action_input = input('Action: ') # get input from player
            for action in available_actions:
                if action_input == action.hotkey and action.name == "Rest until healed": # Rest until healed
                    if player.hp < player.maxHP:
                        while player.hp < player.maxHP:
                            previ = i
                            i+=1
                            player.heal(0.5)
                            room.modify_player(player)
                            player.do_action(action, **action.kwargs)
                            if not player.is_alive():
                                break
                        break
                    else:
                        previ = i
                        i+=1
                        player.heal(0.5)
                        player.do_action(action, **action.kwargs)
                        break
                elif action_input == action.hotkey and action.name == "View Inventory": # View inventory
                    previ = i
                    player.do_action(action, **action.kwargs)
                elif action_input == action.hotkey and action.name == "View stats": # View health
                    previ = i
                    player.do_action(action, **action.kwargs)
                elif action_input == action.hotkey and action.name == "Save/Load/Quit Game": # Save, Load or Quit Game
                    previ = i
                    player.do_action(action, **action.kwargs)
                elif action_input == action.hotkey:
                    player.heal(0.5)
                    previ = i
                    i+=1
                    player.do_action(action, **action.kwargs)
                    break
                else:
                    previ = i # if the input was invalid nothing will happen
    if player.victory:
        print("\n\nYou Win!")
        input("Press ENTER key to quit to title.")
    elif not player.is_alive():
        print("\n\nYou Died!")
        input("Press ENTER key to quit to title.")

def save(save): # save the game
    global i
    global previ
    global player
    if player == None:
        player = make_player()
    s.save(player, save, 'player') # save the player
    s.save(world._world, save, 'world') # save the world (no this isn't something the player does :P)
    s.save({'turn': i, 'prev. turn': previ}, save, 'game') # save the current turn

def load(save): # load a game
    import traceback
    try:
        global i
        global previ
        global player
        player = s.load(save, 'player') # load the player
        world.load(s.load(save, 'world')) #load the world
        data = s.load(save, 'game') # retrieve game data
        i = data['turn'] # set current turn
        previ = data['prev. turn'] # set previous turn
    except Exception as e:
        print(f''' Something went wrong :(
=========================
Please report this at https://github.com/TBBYT/Turn-Based-Game/issues
Error:''')
        traceback.print_exc()
        input('Press ENTER to quit to title')
