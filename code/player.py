import items, world, save, game
import mainclasses as mc
import functions as f
import _pickle
from pathlib import Path
import os, sys
 
class Player():
    def __init__(self):
        self.intelligence = 10
        self.strength = 10
        self.toughness = 10
        self.base_damage = 0.1*self.strength
        self.inventory = [items.SilverCoin(f.random(10,20)), items.Rock()]
        self.maxHP = 5*self.toughness
        self.hp = 5*self.toughness
        self.location_x, self.location_y = world.starting_position
        self.victory = False

        self.blunt_res = f.randomF(0.025,0.25,3)
        self.sharp_res = f.randomF(0,0.1,2)
        self.ex_res = f.randomF(-0.5,-0.25,2)

    def save(self):
        return {'intelligence': self.intelligence, 'strength': self.strength,
                'toughness': self.toughness, 'base_damage': self.base_damage,
                'inventory': [x.save() for x in self.inventory], 'maxHP': self.maxHP,
                'hp': self.hp, 'location': [self.location_x, self.location_y],
                'victory': self.victory, 'blunt_res': self.blunt_res,
                'sharp_res': self.sharp_res, 'ex_res': self.ex_res}

    def load(self, data):
        self.intelligence = data['intelligence']
        self.strength = data['strength']
        self.toughness = data['toughness']
        self.base_damage = data['base_damage']
        #print(data)
        #print(data['inventory'])
        #[print('giving '+str(x)+' to Item class') for x in data['inventory']]
        self.inventory = [mc.Item.load(x) for x in data['inventory']]
        self.maxHP = data['maxHP']
        self.hp = data['hp']
        self.location_x = data['location'][0]
        self.location_y = data['location'][1]
        self.victory = data['victory']
        self.blunt_res = data['blunt_res']
        self.sharp_res = data['sharp_res']
        self.ex_res = data['ex_res']
 
    def is_alive(self):
        return self.hp > 0

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.maxHP:
            self.hp = self.maxHP
        else:
            self.hp = self.hp
 
    def print_inventory(self):
        print("\n==========\nInventory:\n")
        for item in self.inventory:
            print(item, '\n')

    def rest(self):
        self.heal(1.5)
        print("\n==========\nHealth:\n"+str(round(self.hp,2))+"/"+str(self.maxHP)+"HP\n==========")

    def stats(self):
        print("\n==========\nHealth:\n"+str(round(self.hp,2))+"/"+str(self.maxHP)+"HP\n==========")
        print("Damage:\n"+str(round(self.base_damage,2))+"\n==========")
        print("Damage Resistance:\nBlunt: "+str(round(self.blunt_res*100,2))+"%\nSharp: "+str(round(self.sharp_res*100,2))+"%\nExplotion: "+str(round(self.ex_res*100,2))+"%\n==========")
    
    def rr(self):
        if self.hp < self.maxHP-2:
            self.heal(1.5)
        else:
            self.rest()

    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        print(world.tile_exists(self.location_x, self.location_y).intro_text())
    
    def move_north(self):
        self.move(dx=0, dy=-1)
     
    def move_south(self):
        self.move(dx=0, dy=1)
     
    def move_east(self):
        self.move(dx=1, dy=0)
     
    def move_west(self):
        self.move(dx=-1, dy=0)

    def attack(self, enemy):
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
        if o == '1':
            savegame()
        elif o == '2':
            print('Saves:')
            print(save.list_saves())
            o = input("Wich save do you want to load? ")
            if Path(f.path()+"/saves/"+str(o)+"/game.json").is_file():
                game.load(o)
            else:
                print("That save does not exsist!")
        elif o == '3':
            import menus
            yn = input("Do you want to save first?\n(Y/N) ")
            if yn.lower() == "y":
                if savegame():
                    menus.TitleScreen()
            else:
                menus.TitleScreen()
