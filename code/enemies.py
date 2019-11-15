import functions as f # my custom module that just has a lot of useful stuff in it
from mainclasses import Enemy # to make enemies
import items # used for drops (when you defeat an enemy you get everything in it's inventory)
             # doesn't efect enemy at all
class CreeperCow(Enemy): # Enemy that can explode if health is lower than 40
    def __init__(self):
        self.sharp=f.randomF(0.25,0.75)
        super().__init__(name="Red Powder Cow", hp=60, damage=5,
                         sharp=self.sharp, blunt=1-self.sharp,
                         ex=f.random(10,20), ex_chance=f.randomF(0.125,0.25,3),
                         ex_health=40, shr=f.randomF(0.005,0.015,3),
                         blr=f.randomF(0.045,0.055,3),
                         exr=f.randomF(-0.5,-1.5,1), inv=[])

    def save(self):
        return {'type': 'CreeperCow', 'name': self.name, 'hp': self.hp,
                'damage': self.damage, 'sharpness dmg. ratio': self.sharp_rat,
                'blunt dmg. ratio': self.blunt_rat,
                'explosion damage': self.ex_damage, 'explotion chance': self.ex_chance,
                'max health needed to explode': self.ex_health,
                'sharpness dmg. resistance': self.sharp_res,
                'blunt dmg. resistance': self.blunt_res,
                'explotion dmg. resistance': self.ex_res,
                'inventory': [i.save() for i in self.inventory],
                'has exploded?': self.ex} # this is saved to a json file when the game is saved

    @classmethod
    def load(cls, data):
        from mainclasses import Item
        i = cls() # make the object
        i.name = data['name'] # assign the name (this is not set to 'Red Powder Cow', so that someone can change the name in the save)
        i.hp = data['hp'] # set the health
        i.damage = data['damage'] # set the damage that it does
        i.sharp_rat = data['sharpness dmg. ratio'] # set how much of the damage is sharpness damage
        i.blunt_rat = data['blunt dmg. ratio'] # set how much of the damage is blunt damage
        i.ex_damage = data['explosion damage'] # set how much damage it does when exploding
        i.ex_chance = data['explotion chance'] # set the chance of exploding if health is under i.ex_health
        i.ex_health = data['max health needed to explode'] # set the max amount of health it can have to explode
        i.sharp_res = data['sharpness dmg. resistance'] # how much of the sharpness damage it recieves is negated
        i.blunt_res = data['blunt dmg. resistance'] # how much of the blunt damage it recieves is negated
        i.ex_res = data['explotion dmg. resistance'] # how much of the explotion damage it recieves is negated
        i.inventory = [Item.load(i) for i in data['inventory']] # load every item in it's inventory
        i.ex = data['has exploded?'] # wether or it has exploded
        return i


class Brute(Enemy): # Enemy with a lot of health that does a lot of damage
    def __init__(self, inv=[items.Sword()]):
        super().__init__(name="Brute", hp=52, damage=f.random(5,11),
                         sharp=0, blunt=1,
                         ex=0, ex_chance=0,
                         ex_health=0, shr=f.randomF(0.01,0.02,3),
                         blr=f.randomF(0.025,0.05,3),
                         exr=f.randomF(-0.55,-0.45,2), inv=inv)

    def save(self):
        return {'type': 'Brute', 'name': self.name, 'hp': self.hp,
                'damage': self.damage, 'sharpness dmg. ratio': self.sharp_rat,
                'blunt dmg. ratio': self.blunt_rat,
                'explosion damage': self.ex_damage, 'explotion chance': self.ex_chance,
                'max health needed to explode': self.ex_health,
                'sharpness dmg. resistance': self.sharp_res,
                'blunt dmg. resistance': self.blunt_res,
                'explotion dmg. resistance': self.ex_res,
                'inventory': [i.save() for i in self.inventory],
                'has exploded?': self.ex} # this is saved to a json file when the game is saved

    @classmethod
    def load(cls, data):
        from mainclasses import Item
        i = cls([Item.load(i) for i in data['inventory']]) # make the object
        i.name = data['name'] # assign the name (this is not set to 'Brute', so that someone can change the name in the save)
        i.hp = data['hp'] # set the health
        i.damage = data['damage'] # set the damage that it does
        i.sharp_rat = data['sharpness dmg. ratio'] # set how much of the damage is sharpness damage
        i.blunt_rat = data['blunt dmg. ratio'] # set how much of the damage is blunt damage
        i.ex_damage = data['explosion damage'] # set how much damage it does when exploding
        i.ex_chance = data['explotion chance'] # set the chance of exploding if health is under i.ex_health
        i.ex_health = data['max health needed to explode'] # set the max amount of health it can have to explode
        i.sharp_res = data['sharpness dmg. resistance'] # how much of the sharpness damage it recieves is negated
        i.blunt_res = data['blunt dmg. resistance'] # how much of the blunt damage it recieves is negated
        i.ex_res = data['explotion dmg. resistance'] # how much of the explotion damage it recieves is negated
        # does NOT load items into it's inventory, as that is done on object ceation
        i.ex = data['has exploded?'] # wether or it has exploded
        return i
