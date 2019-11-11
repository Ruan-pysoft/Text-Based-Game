from player import Player
import items, enemies, actions, world, game, save
import functions as f
 
class Action():
    def __init__(self, method, name, hotkey, **kwargs):
        self.method = method
        self.hotkey = hotkey
        self.name = name
        self.kwargs = kwargs
 
    def __str__(self):
        return "{}: {}".format(self.hotkey, self.name)

class MoveNorth(Action):
    def __init__(self):
        super().__init__(method=Player.move_north, name='Move up', hotkey='w')
 
 
class MoveSouth(Action):
    def __init__(self):
        super().__init__(method=Player.move_south, name='Move down', hotkey='s')
 
 
class MoveEast(Action):
    def __init__(self):
        super().__init__(method=Player.move_east, name='Move right', hotkey='d')
 
 
class MoveWest(Action):
    def __init__(self):
        super().__init__(method=Player.move_west, name='Move left', hotkey='a')
 
 
class ViewInventory(Action):
    """Prints the Player's inventory"""
    def __init__(self):
        super().__init__(method=Player.print_inventory, name='View inventory', hotkey='e')

class Attack(Action):
    def __init__(self, enemy):
        super().__init__(method=Player.attack, name="Attack", hotkey='q', enemy=enemy)

class Flee(Action):
    def __init__(self, tile):
        super().__init__(method=Player.flee, name="Flee", hotkey='f', tile=tile)

class Rest(Action):
    def __init__(self):
        super().__init__(method=Player.rest, name="Rest", hotkey='r')

class ViewStats(Action):
    def __init__(self):
        super().__init__(method=Player.stats, name="View stats", hotkey='stats')

class RestFull(Action):
    def __init__(self):
        super().__init__(method=Player.rr, name="Rest until healed", hotkey='R')

class Save(Action):
    def __init__(self):
        super().__init__(method=Player.saveGame, name="Save/Load/Quit Game", hotkey='Save')
