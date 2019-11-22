import items, world, save, game
import mainclasses as mc
import functions as f
import os

class Player: # player object
    def __init__(self):
        self.intelligence = 10 # currently not used
        self.strength = 10 # used to determine how much damage the player should deal
        self.toughness = 10 # used to determine how much health the player should have
        self.base_damage = 0.1*self.strength # damage player deals
        self.inventory = [items.SilverCoin(f.random(10,20)), items.Rock()] # inventory
        self.maxHP = 5*self.toughness # max amount of health player can have
        self.hp = 5*self.toughness # current amount of health player has
        self.location_x, self.location_y = world.starting_position # player's position
        self.victory = False

        self.blunt_res = f.randomF(0.025,0.25,3) # how much blunt damage the player can absorb
        self.sharp_res = f.randomF(0,0.1,2) # how much sharpess damage the player can absorb
        self.ex_res = f.randomF(-0.5,-0.25,2)  # how much explotion damage the player can absorb
        # negative means that source of damage does MORE damage

    def save(self):
        return {'intelligence': self.intelligence, 'strength': self.strength,
                'toughness': self.toughness, 'base_damage': self.base_damage,
                'inventory': [x.save() for x in self.inventory], 'maxHP': self.maxHP,
                'hp': self.hp, 'location': [self.location_x, self.location_y],
                'victory': self.victory, 'blunt_res': self.blunt_res,
                'sharp_res': self.sharp_res, 'ex_res': self.ex_res}

    def load(self, data):
        self.intelligence = data['intelligence'] # set intelligence
        self.strength = data['strength'] # set strength
        self.toughness = data['toughness'] # set toughness
        self.base_damage = data['base_damage'] # set damage player deals
        self.inventory = [mc.Item.load(x) for x in data['inventory']] # load inventory
        self.maxHP = data['maxHP'] # set max health player can have
        self.hp = data['hp'] # set health player has
        self.location_x = data['location'][0] # set x location
        self.location_y = data['location'][1] # set y location
        self.victory = data['victory'] # has the player beaten the game?
        self.blunt_res = data['blunt_res'] # set blunt resistance
        self.sharp_res = data['sharp_res'] # set sharpness resistance
        self.ex_res = data['ex_res'] # set explotion resistance

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
        #TODO: let player choose weapon
        best_weapon = None
        max_dmg = 0
        for i in self.inventory:
            if isinstance(i, items.Weapon):
                if i.damage > max_dmg:
                    max_dmg = i.damage
                    best_weapon = i
        if best_weapon != None:
            print("\nYou use {} against {}!".format(best_weapon.name, enemy.name))
            blunt = best_weapon.blunt_damage - (enemy.blunt_res*best_weapon.blunt_damage)
            sharp = best_weapon.sharp_damage - (enemy.sharp_res*best_weapon.sharp_damage)
            ex = best_weapon.ex_damage - (enemy.ex_res*best_weapon.ex_damage)
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
