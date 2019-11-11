import functions as f
from functions import path, save, load, delete
from functions import overWrite as ow
from mainclasses import Enemy
import items

class CreeperCow(Enemy):
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
                'bluntness dmg. resistance': self.blunt_res,
                'explotion dmg. resistance': self.ex_res,
                'inventory': [i.save() for i in self.inventory],
                'has exploded?': self.ex}

    @classmethod
    def load(cls, data):
        from mainclasses import Item
        i = cls()
        i.name = data['name']
        i.hp = data['hp']
        i.damage = data['damage']
        i.sharp_rat = data['sharpness dmg. ratio']
        i.blunt_rat = data['blunt dmg. ratio']
        i.ex_damage = data['explosion damage']
        i.ex_chance = data['explotion chance']
        i.ex_health = data['max health needed to explode']
        i.sharp_res = data['sharpness dmg. resistance']
        i.blunt_res = data['bluntness dmg. resistance']
        i.ex_res = data['explotion dmg. resistance']
        i.inventory = [Item.load(i) for i in data['inventory']]
        i.ex = data['has exploded?']
        return i
 
 
class Brute(Enemy):
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
                'bluntness dmg. resistance': self.blunt_res,
                'explotion dmg. resistance': self.ex_res,
                'inventory': [i.save() for i in self.inventory],
                'has exploded?': self.ex}

    @classmethod
    def load(cls, data):
        from mainclasses import Item
        i = cls([Item.load(i) for i in data['inventory']])
        i.name = data['name']
        i.hp = data['hp']
        i.damage = data['damage']
        i.sharp_rat = data['sharpness dmg. ratio']
        i.blunt_rat = data['blunt dmg. ratio']
        i.ex_damage = data['explosion damage']
        i.ex_chance = data['explotion chance']
        i.ex_health = data['max health needed to explode']
        i.sharp_res = data['sharpness dmg. resistance']
        i.blunt_res = data['bluntness dmg. resistance']
        i.ex_res = data['explotion dmg. resistance']
        i.ex = data['has exploded?']
        return i
