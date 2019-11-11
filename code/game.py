import world, time
#from player import Player
import save as s
import player as p

i = 0
previ = 0
player = None

def make_player():
    return p.Player()

def play(m, l=False):
    previ = 0
    i = 1
    if not l:
        world.load_tiles(m)
    else:
        world.load_tiles('map')
    global player
    global clear
    player = make_player()
    if l:
        global load
        load(m)
    room = world.tile_exists(player.location_x, player.location_y)
    print(room.intro_text())
    while player.is_alive() and not player.victory:
        room = world.tile_exists(player.location_x, player.location_y)
        if previ != i:
            room.modify_player(player)
        # Check again since the room could have changed the player's state
        if player.is_alive() and not player.victory:
            print("\nPlay Turn "+str(i)+", Choose an Action:\n")
            available_actions = room.available_actions()
            for action in available_actions:
                print(action)
            action_input = input('Action: ')
            for action in available_actions:
                if action_input == action.hotkey and action.name == "Rest until healed":
                    if player.hp < player.maxHP:
                        while player.hp < player.maxHP:
                            previ = i
                            i+=1
                            player.heal(0.5)
                            player.do_action(action, **action.kwargs)
                        break
                    else:
                        previ = i
                        i+=1
                        player.heal(0.5)
                        player.do_action(action, **action.kwargs)
                        break
                elif action_input == action.hotkey and action.name == "View inventory":
                    previ = i
                    player.do_action(action, **action.kwargs)
                elif action_input == action.hotkey and action.name == "View stats":
                    previ = i
                    player.do_action(action, **action.kwargs)
                elif action_input == action.hotkey and action.name == "Save/Load/Quit Game":
                    previ = i
                    player.do_action(action, **action.kwargs)
                elif action_input == action.hotkey:
                    player.heal(0.5)
                    previ = i
                    i+=1
                    player.do_action(action, **action.kwargs)
                    break
    if player.victory:
        print("\n\nYou Win!")
        input("Press ENTER key to quit.")
    elif not player.is_alive():
        print("\n\nYou Died!")
        input("Press ENTER key to quit.")

def save(save):
    global i
    global previ
    global player
    if player == None:
        player = make_player()
    s.save(player.save(), save, 'player')
    s.save(world.save(), save, 'world')
    s.save({'turn': i, 'prev. turn': previ}, save, 'game')

def load(save):
    try:
        global i
        global previ
        global player
        if player == None:
            player = make_player()
        player.load(s.load(save, 'player'))
        world.load(s.load(save, 'world'))
        data = s.load(save, 'game')
        i = data['turn']
        pevi = data['prev. turn']
    except Exception as e:
        print(f''' Something went wrong :(
=========================
Error:
{e}''')
        input()

if __name__ == "__main__":
    play()
