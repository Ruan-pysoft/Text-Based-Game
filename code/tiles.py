import items, enemies, actions, world, game
import functions as f
import mainclasses as mc

class MapTile:
    def __init__(self, x, y, start=False):
        self.x = x # x position in world
        self.y = y # y position in world
        self.start = start # is this where the player should start the game

    def intro_text(self):
        print(f'''[PLACEHOLDER]
If you see this you are in a room without intro text!
Room: {repr(self)}
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

    def __repr__(self):
        return 'MapTile({}, {}, {})'.format(repr(self.x), repr(self.y), repr(self.start))

    def save(self):
        return {'type': 'MapTile', 'pos': [self.x, self.y], 'start': self.start}

    @classmethod
    def load(cls, data):
        if data == None:
            return None
        elif data['type'] == 'MapTile':
            return cls(data['pos'][0], data['pos'][1], start=data['start'])
        elif data['type'] == 'StartingRoom':
            return StartingRoom.load(data)
        elif data['type'] == 'TestStart':
            return TestStart.load(data)
        elif data['type'] == 'LootRoom':
            return LootRoom.load(data)
        elif data['type'] == 'TresureRoom':
            return TresureRoom.load(data)
        elif data['type'] == 'EnemyRoom':
            return EnemyRoom.load(data)
        elif data['type'] == 'EmptyCavePath':
            return EmptyCavePath.load(data)
        elif data['type'] == 'ExplodingCowRoom':
            return ExplodingCowRoom.load(data)
        elif data['type'] == 'BruteRoom':
            return BruteRoom.load(data)
        elif data['type'] == 'StashRoom':
            return StashRoom.load(data)
        elif data['type'] == 'CoinsRoom':
            return CoinsRoom.load(data)
        elif data['type'] == 'LeaveCaveRoom':
            return LeaveCaveRoom.load(data)
        elif data['type'] == 'otherMap':
            return otherMap.load(data)
        elif data['type'] == 'pitToSmallCave':
            return pitToSmallCave.load(data)
        elif data['type'] == 'caveLabrinth':
            return caveLabrinth.load(data)
        elif data['type'] == 'testPortal':
            return testPortal.load(data)

class StartingRoom(MapTile): # starting room
    def __init__(self, x, y):
        super().__init__(x, y, start=True)

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

    def modify_player(self, player):
        pass # does nothing to player

    def __repr__(self):
        #to return the code that was used to create it, so that I can save the
        #object in a file or string.
        return 'StartingRoom({}, {})'.format(repr(self.x), repr(self.y))

    def save(self):
        return {'type': 'StartingRoom', 'pos': [self.x, self.y]}

    @classmethod
    def load(cls, data):
        return cls(data['pos'][0], data['pos'][1])

class LootRoom(MapTile): # a room with one item in
    def __init__(self, x, y, item, looted = False):
        self.item = item
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

    def __repr__(self):
        return 'LootRoom({}, {}, {}, {})'.format(repr(self.x), repr(self.y), repr(self.item), repr(self.item))

    def save(self):
        if item is not None:
            return {'type': 'LootRoom', 'pos': [self.x, self.y], 'item': self.item.save(), 'looted': self.looted}
        else:
            return {'type': 'LootRoom', 'pos': [self.x, self.y], 'item': None, 'looted': self.looted}

    @classmethod
    def load(cls, data):
        return cls(data['pos'][0], data['pos'][1], data['item'], data['looted'])

class TresureRoom(MapTile): # like LootRoom, but with multiple items
    def __init__(self, x, y, items, looted = False):
        self.items = items
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

    def __repr__(self):
        return 'LootRoom({}, {}, {}, {})'.format(repr(self.x), repr(self.y), repr(self.items), repr(self.looted))

    def save(self):
        return {'type': 'TresureRoom', 'pos': [self.x, self.y], 'items': [i.save() for i in self.items], 'looted': self.looted}

    @classmethod
    def load(cls, data):
        return cls(data['pos'][0], data['pos'][1], data['items'], data['looted'])

class EnemyRoom(MapTile): # a room with an enemy in it
    def __init__(self, x, y, enemy, defeat = False):
        self.enemy = enemy
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

    def __repr__(self):
        return 'EnemyRoom({}, {}, {}, {})'.format(repr(self.x), repr(self.y), repr(self.enemy), repr(self.defeat))

    def save(self):
        return {'type': 'EnemyRoom', 'pos': [self.x, self.y], 'enemy': self.enemy.save(), 'defeated': self.defeat}

    @classmethod
    def load(cls, data):
        return cls(data['pos'][0], data['pos'][1], data['enemy'], data['defeated'])

class EmptyCavePath(MapTile): # empty room
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """

    def modify_player(self, player):
        #Room has no action on player
        pass

    def __repr__(self):
        return 'EmptyCavePath({}, {}, {})'.format(repr(self.x), repr(self.y), repr(self.start))

    def save(self):
        return {'type': 'EmptyCavePath', 'pos': [self.x, self.y]}

    @classmethod
    def load(cls, data):
        return cls(data['pos'][0], data['pos'][1])

class ExplodingCowRoom(EnemyRoom): # I think the room's name explains it all
    def __init__(self, x, y, enemy = enemies.CreeperCow(), defeat = False):
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

    def __repr__(self):
        return 'ExplodingCowRoom({}, {}, {}, {})'.format(repr(self.x), repr(self.y), repr(self.enemy), repr(self.defeat))

    def save(self):
        return {'type': 'ExplodingCowRoom', 'pos': [self.x, self.y], 'enemy': self.enemy.save(), 'defeated': self.defeat}

    @classmethod
    def load(cls, data):
        return cls(data['pos'][0], data['pos'][1], data['enemy'], data['defeated'])

class BruteRoom(EnemyRoom): # a room with a Brute enemy in
    def __init__(self, x, y, enemy = enemies.Brute(), defeat = False):
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

    def __repr__(self):
        return 'BruteRoom({}, {}, {}, {})'.format(repr(self.x), repr(self.y), repr(self.enemy), repr(self.defeat))

    def save(self):
        return {'type': 'BruteRoom', 'pos': [self.x, self.y], 'enemy': self.enemy.save(), 'defeated': self.defeat}

    @classmethod
    def load(cls, data):
        return cls(data['pos'][0], data['pos'][1], data['enemy'], data['defeated'])

class StashRoom(TresureRoom):
    def w():
        w = f.randomWeight([0,5,2.5,1.5,1])
        minw = 0.005/4
        maxw = 0.025/4
        return f.randomF(minw, maxw) * w

    def __init__(self, x, y, items=[items.Dagger(), items.Diamond(round(w(), 3), False), items.SilverCoin(f.random(25,75)), items.GoldCoin(f.randomF(0.5, 2.0))], looted = False):
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

    def __repr__(self):
        return 'StashRoom({}, {}, {}, {})'.format(repr(self.x), repr(self.y), repr(self.items), repr(self.looted))

    def save(self):
        return {'type': 'StashRoom', 'pos': [self.x, self.y], 'items': [i.save() for i in self.items], 'looted': self.looted}

    @classmethod
    def load(cls, data):
        return cls(data['pos'][0], data['pos'][1], data['items'], data['looted'])

class CoinsRoom(LootRoom):
    def __init__(self, x, y, item=items.CopperCoin(f.random(10,200)), looted = False):
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

    def __repr__(self):
        return 'CoinsRoom({}, {}, {}, {})'.format(repr(self.x), repr(self.y), repr(self.item), repr(self.looted))

    def save(self):
        if self.item is not None:
            return {'type': 'CoinsRoom', 'pos': [self.x, self.y], 'item': self.item.save(), 'looted': self.looted}
        else:
            return {'type': 'CoinsRoom', 'pos': [self.x, self.y], 'item': None, 'looted': self.looted}

    @classmethod
    def load(cls, data):
        return cls(data['pos'][0], data['pos'][1], data['item'], data['looted'])

class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!


        Victory is yours!
        """

    def modify_player(self, player):
        player.victory = True

    def __repr__(self):
        #to return the code that was used to create it, so that I can save the
        #object in a file or string.
        return 'LeaveCaveRoom({}, {}, {})'.format(repr(self.x), repr(self.y), repr(self.start))

    def save(self):
        return {'type': 'LeaveCaveRoom', 'pos': [self.x, self.y], 'start': self.start}

    @classmethod
    def load(cls, data):
        return cls(data['pos'][0], data['pos'][1], data['start'])
