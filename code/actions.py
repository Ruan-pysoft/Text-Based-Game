from player import Player # class for creating player character

class Action():
    def __init__(self, method, name, hotkey, **kwargs):
        self.method = method # function/method to be executed
        self.hotkey = hotkey # hotkey to use action
        self.name = name     # display name
        self.kwargs = kwargs # anything else

    def __str__(self):
        return "{}: {}".format(self.hotkey, self.name) # for being printed in the console

class MoveNorth(Action): # used to move north (or 'up')
    def __init__(self):
        super().__init__(method=Player.move_north, name='Move North', hotkey='w')


class MoveSouth(Action): # used to move south (or 'down')
    def __init__(self):
        super().__init__(method=Player.move_south, name='Move South', hotkey='s')


class MoveEast(Action): # used to move East (or 'right')
    def __init__(self):
        super().__init__(method=Player.move_east, name='Move East', hotkey='d')


class MoveWest(Action): # used to move west (or 'left')
    def __init__(self):
        super().__init__(method=Player.move_west, name='Move West', hotkey='a')


class ViewInventory(Action): # Prints the Player's inventory
    def __init__(self):
        super().__init__(method=Player.print_inventory, name='View Inventory', hotkey='e')

class Attack(Action): # used to attack an enemy
    def __init__(self, enemy):
        super().__init__(method=Player.attack, name="Attack", hotkey='q', enemy=enemy)

class Flee(Action): # move to a rendom adjacent room
    def __init__(self, tile):
        super().__init__(method=Player.flee, name="Flee", hotkey='f', tile=tile)

class Rest(Action): # used to do nothing for one turn
    def __init__(self):
        super().__init__(method=Player.rest, name="Rest", hotkey='r')

class ViewStats(Action): # used to check health
    def __init__(self):
        super().__init__(method=Player.stats, name="View stats", hotkey='stats')

class RestFull(Action): # use to rest untill fully healed (or dead)
    def __init__(self):
        super().__init__(method=Player.rr, name="Rest until healed (DANGEROUS IF FIGHTING ENEMY!)", hotkey='R')

class Save(Action): # used to save, load or quit the game
    def __init__(self):
        super().__init__(method=Player.saveGame, name="Save/Load/Quit Game", hotkey='Menu')
