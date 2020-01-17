import items, enemies, actions, world, game
import functions as f
import mainclasses as mc

def init_class(X, *y, **z):
    x = X(*y, **z)
    x.__init__(*y, **z)
    print(type(x))
    return x

class MapTile:
    def __init__(self, x, y, start=False):
        self.x = x # x position in world
        self.y = y # y position in world
        self.start = start # is this where the player should start the game

    def intro_text(self):
        import re
        print(f'''[PLACEHOLDER]
If you see this you are in a room without intro text!
Room: {re.sub(r"'>", '', re.sub(r"<class '__main__.", '', str(self.__class__)))}
Please report this at https://github.com/TBBYT/Turn-Based-Game/issues''')

    def modify_player(self, player):
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves

    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
        moves.append(actions.Rest())
        moves.append(actions.RestFull())
        moves.append(actions.ViewStats())
        moves.append(actions.Save())

        return moves

    @property
    def str(self):
        return f'''{repr(self)[1:-1]} in RAM:
  Variables:
    x = {repr(self.x)}
    y = {repr(self.y)}
    start = {repr(self.start)}
  Read-only:
    available_actions() = {repr(self.available_actions())}
    adjacent_moves() = {repr(self.adjacent_moves())}
    intro_text() = {self.intro_text()}'''

    @property
    def full_str(self):
        return f'''{repr(self)[1:-1]} in RAM:
  Variables:
    x = {repr(self.x)}
    y = {repr(self.y)}
    start = {repr(self.start)}
  Read-only:
    available_actions() = {repr(self.available_actions())}
    adjacent_moves() = {repr(self.adjacent_moves())}
    intro_text() = {self.intro_text()}'''

class LootRoom(MapTile): # a room with one item in
    def __init__(self, x, y, item, looted = False):
        self.item = item[0](*item[1], **item[2])
        self.looted = looted
        super().__init__(x, y)

    def add_loot(self, player): # add item to player's inventory
        player.inventory.append(self.item)
        self.item = None
        self.looted = True

    def new_loot(self, item):
        self.item = item
        self.looted = False

    def modify_player(self, player):
        if self.item != None:
            self.add_loot(player)
        else:
            pass

    @property
    def str(self):
        return f'''{repr(self)[1:-1]} in RAM:
  Variables:
    item = {None if self.item is None else self.item.name}
    looted = {repr(self.looted)}
    x = {repr(self.x)}
    y = {repr(self.y)}
    start = {repr(self.start)}
  Read-only:
    available_actions() = {repr(self.available_actions())}
    adjacent_moves() = {repr(self.adjacent_moves())}
    intro_text() = {self.intro_text()}
  Functions:
    new_loot(item) # Changes the rooms loot to 'item', and sets 'looted' to False'''

    @property
    def full_str(self):
        return f'''{repr(self)[1:-1]} in RAM:
  Variables:
    ===
    item =
    {None if self.item is None else self.item.full_str}
    ===
    looted = {repr(self.looted)}
    x = {repr(self.x)}
    y = {repr(self.y)}
    start = {repr(self.start)}
  Read-only:
    available_actions() = {repr(self.available_actions())}
    adjacent_moves() = {repr(self.adjacent_moves())}
    intro_text() = {self.intro_text()}
  Functions:
    new_loot(item) # Changes the rooms loot to 'item', and sets 'looted' to False'''

class TresureRoom(MapTile): # like LootRoom, but with multiple items
    def __init__(self, x, y, items, looted = False):
        self.items = [item[0](*item[1], **item[2]) for item in items]
        self.looted = looted
        super().__init__(x, y)

    def add_loot(self, player):
        for item in self.items:
            player.inventory.append(item)
        self.items = []
        self.looted = True

    def new_loot(self, items):
        self.looted = False
        self.items = items

    def modify_player(self, player):
        if len(self.items) > 0:
            self.add_loot(player)
        else:
            pass

    @property
    def str(self):
        return f'''{repr(self)[1:-1]} in RAM:
  Variables:
    items = [
{str([None if item is None else item.name for item in self.items])[1:-1]}
    ]
    looted = {repr(self.looted)}
    x = {repr(self.x)}
    y = {repr(self.y)}
    start = {repr(self.start)}
  Read-only:
    available_actions() = {repr(self.available_actions())}
    adjacent_moves() = {repr(self.adjacent_moves())}
    intro_text() = {self.intro_text()}
  Functions:
    new_loot(item) # Changes the rooms loot to 'item', and sets 'looted' to False'''

    @property
    def full_str(self):
        def full_inv():
            full_inv = ['None' if item is None else item.full_str for item in self.items]
            full_inv_str = ''
            for i in full_inv:
                full_inv_str += i + ',\n'
            return full_inv_str[:-2]
        return f'''{repr(self)[1:-1]} in RAM:
  Variables:

    items = [ # start inv
{full_inv()}
    ] # end inv

    looted = {repr(self.looted)}
    x = {repr(self.x)}
    y = {repr(self.y)}
    start = {repr(self.start)}
  Read-only:
    available_actions() = {repr(self.available_actions())}
    adjacent_moves() = {repr(self.adjacent_moves())}
    intro_text() = {self.intro_text()}
  Functions:
    new_loot(items) # Changes the rooms loot to 'items', and sets 'looted' to False'''

class SpawnPoint(TresureRoom): # starting room
    def __init__(self, x, y, items=[[items.SilverCoin, (f.random(10,20),), {}], [items.Rock, (), {}]]):
        super().__init__(x, y, items)
        self.start=True

class EnemyRoom(MapTile): # a room with an enemy in it
    def __init__(self, x, y, enemy, defeat = False):
        self.enemy = enemy[0](*enemy[1], **enemy[2])
        super().__init__(x, y)
        self.defeat = defeat

    def add_loot(self, player):
        for item in self.enemy.inventory:
            player.inventory.append(item)
        self.enemy.inventory = []

    def modify_player(self, the_player):
        self.enemy.explode()
        if self.enemy.is_alive():
            if not self.enemy.ex:
                blunt_dam = self.enemy.damage*self.enemy.blunt_rat
                sharp_dam = self.enemy.damage*self.enemy.sharp_rat
                blunt = blunt_dam - (the_player.blunt_res*blunt_dam)
                sharp = sharp_dam - (the_player.sharp_res*sharp_dam)
                the_player.hp -= (blunt+sharp)
                print("Enemy does {} damage. You have {} HP remaining.".format(round(blunt+sharp,2), round(the_player.hp,2)))
            else:
                self.enemy.hp = 0
                the_player.hp -= ( self.enemy.ex_damage - (the_player.ex_res*self.enemy.ex_damage) )
                print("Enemy explodes and does {} damage! You have {} HP remaining.".format(round(self.enemy.ex_damage - (the_player.ex_res*self.enemy.ex_damage),2), round(the_player.hp,2)))
        elif not self.defeat:
            self.defeat = True
            if len(self.enemy.inventory) > 0:
                self.add_loot(the_player)
            else:
                pass

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy), actions.Rest(), actions.Save()]
        else:
            moves = self.adjacent_moves()
            moves.append(actions.ViewInventory())
            moves.append(actions.Rest())
            moves.append(actions.RestFull())
            moves.append(actions.ViewStats())
            moves.append(actions.Save())
            return moves

    @property
    def str(self):
        return f'''{repr(self)[1:-1]} in RAM:
  Variables:

    #=====#
    enemy = {self.enemy.str}
    #=====#

    x = {repr(self.x)}
    y = {repr(self.y)}
    start = {repr(self.start)}
    defeat = {repr(self.defeat)}
  Read-only:
    available_actions() = {repr(self.available_actions())}
    adjacent_moves() = {repr(self.adjacent_moves())}
    intro_text() = {self.intro_text()}
  Functions:
    new_loot(item) # Changes the rooms loot to 'item', and sets 'looted' to False'''

    @property
    def full_str(self):
        return f'''{repr(self)[1:-1]} in RAM:
  Variables:

    #=====#
    enemy = {self.enemy.full_str}
    #=====#

    x = {repr(self.x)}
    y = {repr(self.y)}
    start = {repr(self.start)}
    defeat = {repr(self.defeat)}
  Read-only:
    available_actions() = {repr(self.available_actions())}
    adjacent_moves() = {repr(self.adjacent_moves())}
    intro_text() = {self.intro_text()}'''

class StartingRoom(SpawnPoint): # starting room
    def __init__(self, x, y):
        super().__init__(x, y, [[items.SilverCoin, (f.random(10,20),), {}], [items.Rock, (), {}]])

    def intro_text(self):
        if game.i == 1:
            return """
        You find yourself in a cave with a flickering torch on the wall.
        You can make out four paths, each equally as dark and foreboding.
        """
        else:
            return """
        Another unremarkable part of the cave. You must forge onwards.
        """

class EmptyCavePath(MapTile): # empty room
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """

    def modify_player(self, player):
        #Room has no action on player
        pass

class CaveMouth(MapTile): # empty room
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!

        As you walk towards the light, you can see that it is the mouth of a cave.
        """

    def modify_player(self, player):
        #Room has no action on player
        pass

class Forest(MapTile): # empty room
    def intro_text(self):
        return """
        You find yourself surrounded with dense trees.
        You should stay on the path.
        """

    def modify_player(self, player):
        #Room has no action on player
        pass

class Clearing(MapTile): # empty room
    def intro_text(self):
        return """
        You find a clearing full of grass.
        """

    def modify_player(self, player):
        #Room has no action on player
        pass

class ExplodingCowRoom(EnemyRoom): # I think the room's name explains it all
    def __init__(self, x, y, enemy = [enemies.CreeperCow, (), {}], defeat = False):
        super().__init__(x, y, enemy, defeat)

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A big cow charges you!
            """
        else:
            return """
            The corpse of a dead (and very hot) cow rots on the ground.
            """

class BruteRoom(EnemyRoom): # a room with a Brute enemy in
    def __init__(self, x, y, enemy = [enemies.Brute, (), {}], defeat = False):
        super().__init__(x, y, enemy, defeat)

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A bandit attacks you!
            """
        else:
            return """
            The corpse of the big man lies on the ground.
            """

class StashRoom(TresureRoom):
    def w():
        w = f.randomWeight([0,5,2.5,1.5,1])
        minw = 0.005/4
        maxw = 0.025/4
        return f.randomF(minw, maxw) * w

    def __init__(self, x, y, items=[[items.Dagger, (), {}], [items.Diamond, (round(w(), 3), False), {}], [items.SilverCoin, (f.random(25,75),), {}], [items.GoldCoin, (f.randomF(0.5, 2.0),), {}]], looted = False):
        super().__init__(x, y, items, looted)

    def intro_text(self):
        if not self.looted:
            return """
            You notice something in the corner.
            It's a chest! You open it up.
            """
        else:
            return """
            You notice an empty chest in the corner.
            Either you've already been here or...
            """

class CoinsRoom(LootRoom):
    def __init__(self, x, y, item=[items.CopperCoin, (f.random(10,200),), {}], looted = False):
        super().__init__(x, y, item, looted)

    def intro_text(self):
        if not self.looted:
            return """
            Your notice something shiny in the corner.
            It's a coin. You pick it up.
            """
        else:
            return """
            Another unremarkable part of the cave. You must forge onwards.
            """

class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!


        Victory is yours!
        """

    def modify_player(self, player):
        player.victory = True
