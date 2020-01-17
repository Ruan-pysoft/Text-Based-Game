import items, world, save, game
import mainclasses as mc
import functions as f
import os

class Player: # player object
    def __init__(self):
        self.intelligence = 10 # currently not used
        self.strength = 10 # used to determine how much damage the player should deal
        self.toughness = 10 # used to determine how much health the player should have
        self.inventory = [] # inventory
        self.hp = 5*self.toughness # current amount of health player has
        self.location_x, self.location_y = world.starting_position # player's position
        self.victory = False

        self.blunt_res = f.randomF(0.025,0.25,3) # how much blunt damage the player can absorb
        self.sharp_res = f.randomF(0,0.1,2) # how much sharpess damage the player can absorb
        self.ex_res = f.randomF(-0.5,-0.25,2)  # how much explotion damage the player can absorb
        # negative means that source of damage does MORE damage

    @property
    def maxHP(self):
        return 5*self.toughness # max amount of health player can have

    @property
    def base_damage(self):
        return 0.1*self.strength # damage player deals

    @property
    def str(self):
        return f'''{repr(self)[1:-1]} in RAM:
  Variables:
    intelligence = {repr(self.intelligence)}
    strength = {repr(self.strength)}
    toughness = {repr(self.toughness)}

    inventory = [
{str([i.name for i in self.inventory])[1:-1]}
    ]

    hp = {repr(self.hp)}
    location_x, location_y = {repr(self.location_x)}, {repr(self.location_y)}
    victory = {repr(self.victory)}
    blunt_res = {repr(self.blunt_res)}
    sharp_res = {repr(self.sharp_res)}
    ex_res = {repr(self.ex_res)}
  Read-only:
    is_alive() = {repr(self.is_alive())}
    maxHP = {repr(self.maxHP)}
    base_damage = {repr(self.base_damage)}'''

    @property
    def full_str(self):
        def full_inv():
            full_inv = [i.full_str for i in self.inventory]
            full_inv_str = ''
            for i in full_inv:
                full_inv_str += i + ',\n'
            return full_inv_str[:-2]
        return f'''{repr(self)[1:-1]} in RAM:
  Variables:
    intelligence = {repr(self.intelligence)}
    strength = {repr(self.strength)}
    toughness = {repr(self.toughness)}

    inventory = [ # start inv
{full_inv()}
    ] # end inv

    hp = {repr(self.hp)}
    location_x, location_y = {repr(self.location_x)}, {repr(self.location_y)}
    victory = {repr(self.victory)}
    blunt_res = {repr(self.blunt_res)}
    sharp_res = {repr(self.sharp_res)}
    ex_res = {repr(self.ex_res)}
  Read-only:
    is_alive() = {repr(self.is_alive())}
    maxHP = {repr(self.maxHP)}
    base_damage = {repr(self.base_damage)}'''

    def is_alive(self):
        return self.hp > 0

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.maxHP:
            self.hp = self.maxHP
        else:
            self.hp = self.hp

    def print_inventory(self): # print the player's inventory
        print("\n==========\nInventory:\n")
        for item in self.inventory:
            print(item, '\n')

    def rest(self):
        self.heal(1.5) # resting heals 1.5 damage more than, for example, walking around does
        print("\n==========\nHealth:\n"+str(round(self.hp,2))+"/"+str(self.maxHP)+"HP\n==========")

    def stats(self): # print player's health, damage player deals and player's damage resistance
        print("\n==========\nHealth:\n"+str(round(self.hp,2))+"/"+str(self.maxHP)+"HP\n==========")
        print("Damage:\n"+str(round(self.base_damage,2))+"\n==========")
        print("Damage Resistance:\nBlunt: "+str(round(self.blunt_res*100,2))+"%\nSharp: "+str(round(self.sharp_res*100,2))+"%\nExplotion: "+str(round(self.ex_res*100,2))+"%\n==========")

    def rr(self): # rest until healed
        if self.hp < self.maxHP-2:
            self.heal(1.5)
        else:
            self.rest()

    def move(self, dx, dy): # move somewhere
        self.location_x += dx
        self.location_y += dy
        print(world.tile_exists(self.location_x, self.location_y).intro_text())

    def move_north(self): # move 'up'
        self.move(dx=0, dy=-1)

    def move_south(self): # move 'down'
        self.move(dx=0, dy=1)

    def move_east(self): # move 'right'
        self.move(dx=1, dy=0)

    def move_west(self): # move 'left'
        self.move(dx=-1, dy=0)

    def attack(self, enemy): # attack something
        weapon = None
        weapons = []
        max_dmg = 0
        for i in self.inventory:
            if isinstance(i, items.Weapon):
                weapons.append(i)
        if len(weapons) > 0:
            print(f'\nWeapons:\n-------\n\n0: Fists, Damage: {self.base_damage}')
            for i, w in enumerate(weapons):
                print(str(i+1) + ': ' + w.str)
        def get_weapon():
            if len(weapons) == 0: return None
            try:
                i = int(input('What weapon do you want to use? '))
                if i == 0: return None
                if i < 0: return get_weapon()
                return weapons[int(i)-1]
            except: return get_weapon()
        weapon = get_weapon()
        if weapon != None:
            print("\nYou use {} against {}!".format(weapon.name, enemy.name))
            blunt = weapon.blunt_damage - (enemy.blunt_res*weapon.blunt_damage)
            sharp = weapon.sharp_damage - (enemy.sharp_res*weapon.sharp_damage)
            ex = weapon.ex_damage - (enemy.ex_res*weapon.ex_damage)
            enemy.hp -= (blunt + sharp + ex)
        else:
            print("\nYou punch {}!".format(enemy.name))
            blunt = self.base_damage - (enemy.blunt_res*self.base_damage)
            enemy.hp -= blunt
        if not enemy.is_alive():
            print("You killed {}!".format(enemy.name))
        else:
            print("{} HP is {}.".format(enemy.name, round(enemy.hp,2)))

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def flee(self, tile):
        """Moves the player randomly to an adjacent tile"""
        available_moves = tile.adjacent_moves()
        r = f.random(0, len(available_moves) - 1)
        self.do_action(available_moves[r])

    def saveGame(self):
        from inspect import currentframe, getframeinfo
        from pathlib import Path
        def savegame():
            o = input("Give the save a name: ")
            path = str(Path(getframeinfo(currentframe()).filename).resolve().parent) + str(Path(f'/saves/{o}/'))
            if os.path.exists(path):
                yn = input("The save \""+o+"\" already exists, do you want to overwrite it?\n(Y/N): ")
                if yn.lower() == "y":
                    game.save(o)
                    print("Done Saving!")
                    return True
                else:
                    print('Aborting save!')
                    return False
            else:
                game.save(o)
                print("Done Saving!")
                return True
        o = input("Do you want to:\n1) Save the game\n2) Load another game\n3) Quit game\n")
        if o == '1': # save the game
            savegame()
        elif o == '2': # load a game
            print('Saves:')
            for i, a in enumerate(save.list_saves(), 1):
                print(f'{i}) {a}') # list all the saves
            o = input("Which save do you want to load? ")
            try:
                o = int(o)
                if int(o) > len(save.list_saves()) or int(o) < 1:
                    print("That isn't a valid save!")
                else:
                    game.load(save.list_saves()[o - 1])
            except:
                print("That isn't a valid number!")
        elif o == '3': # quit game
            import menus
            yn = input("Do you want to save first?\n(Y/N) ")
            if yn.lower() == "y":
                if savegame():
                    menus.TitleScreen()
            else:
                menus.TitleScreen()
