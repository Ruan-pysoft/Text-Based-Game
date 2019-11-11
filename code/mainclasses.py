import functions as f
from random import randint, uniform

class Item():
    """The base class for all items"""
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value
 
    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\n".format(self.name, self.description, self.value)

    def __iter__(self):
        return iter([self.name, self.description, self.value])

    def save(self):
        return {'type': 'Item', 'name': self.name,
                'description': self.description, 'value': self.value}

    @classmethod
    def load(cls, data):
        import items as it
        i = Item(data['name'], data['description'], data['value'])
        if data['type'] == 'Item':
            i = Item(data['name'], data['description'], data['value'])
        elif data['type'] == 'Gold':
            i = it.Gold(data['weight'])
            i.name = data['name']
            i.description = data['description']
            i.value = data['value']
        elif data['type'] == 'GoldCoin':
            i = it.GoldCoin(data['amt'])
            i.name = data['name']
            i.description = data['description']
            i.value = data['value']
        elif data['type'] == 'Silver':
            i = it.Silver(data['weight'])
            i.name = data['name']
            i.description = data['description']
            i.value = data['value']
        elif data['type'] == 'SilverCoin':
            i = it.SilverCoin(data['amt'])
            i.name = data['name']
            i.description = data['description']
            i.value = data['value']
        elif data['type'] == 'Copper':
            i = it.Copper(data['weight'])
            i.name = data['name']
            i.description = data['description']
            i.value = data['value']
        elif data['type'] == 'CopperCoin':
            i = it.CopperCoin(data['amt'])
            i.name = data['name']
            i.description = data['description']
            i.value = data['value']
        elif data['type'] == 'Diamond':
            i = it.Diamond(data['weight'], False)
            i.name = data['name']
            i.description = data['description']
            i.value = data['value']
            i.cut = data['cut']
        elif data['type'] == 'Weapon':
            i = it.Weapon(data['name'], data['description'], data['value'],
                          data['damage'], data['sharp_rat'], data['blunt_rat'],
                          data['explotion_rat'])
            i.sharp_damage = data['sharp_damage']
            i.blunt_damage = data['blunt_damage']
            i.ex_damage = data['ex_damage']
        elif data['type'] == 'Rock':
            i = it.Rock()
            i.name = data['name']
            i.description = data['description']
            i.value = data['value']
            i.damage = data['damage']
            i.sharp_rat = data['sharp_rat']
            i.blunt_rat = data['blunt_rat']
            i.explotion_rat = data['explotion_rat']
            i.sharp_damage = data['sharp_damage']
            i.blunt_damage = data['blunt_damage']
            i.ex_damage = data['ex_damage']
            i.sharp = data['sharp']
        elif data['type'] == 'Dagger':
            i = it.Dagger()
            i.name = data['name']
            i.description = data['description']
            i.value = data['value']
            i.damage = data['damage']
            i.sharp_rat = data['sharp_rat']
            i.blunt_rat = data['blunt_rat']
            i.explotion_rat = data['explotion_rat']
            i.sharp_damage = data['sharp_damage']
            i.blunt_damage = data['blunt_damage']
            i.ex_damage = data['ex_damage']
            i.sharp = data['sharp']
        elif data['type'] == 'Sword':
            i = it.Sword()
            i.name = data['name']
            i.description = data['description']
            i.value = data['value']
            i.damage = data['damage']
            i.sharp_rat = data['sharp_rat']
            i.blunt_rat = data['blunt_rat']
            i.explotion_rat = data['explotion_rat']
            i.sharp_damage = data['sharp_damage']
            i.blunt_damage = data['blunt_damage']
            i.ex_damage = data['ex_damage']
            i.sharp = data['sharp']
        elif data['type'] == 'BlankWeapon':
            i = it.BlankWeapon(data['name'], data['description'], data['value'],
                               data['damage'], data['sharp_rat'], data['blunt_rat'],
                               data['explotion_rat'], data['sharp_damage'],
                               data['blunt_damage'], data['ex_damage'],
                               data['sharp'])
        return i

class Enemy():
    def __init__(self, name, hp, damage, sharp, blunt, ex, ex_chance, ex_health,
                 shr, blr, exr, inv):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.sharp_rat = sharp
        self.blunt_rat = blunt
        self.ex_damage = ex
        self.ex_chance = ex_chance
        self.ex_health = ex_health
        self.blunt_res = blr
        self.sharp_res = shr
        self.ex_res = exr
        self.ex = False
        self.inventory = inv

    def explode(self):
        if self.hp < self.ex_health and uniform(0.0000,1.0000) < self.ex_chance:
            self.ex = True
 
    def is_alive(self):
        return self.hp > 0

    def save(self):
        return {'type': 'Enemy', 'name': self.name, 'hp': self.hp,
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
        import enemies as en
        if data['type'] == 'Enemy':
            e = cls(data['name'], data['hp'], data['damage'], data['sharpness dmg. ratio'],
                    data['blunt dmg. ratio'], data['explosion damage'],
                    data['explotion chance'], data['max health needed to explode'],
                    data['sharpness dmg. resistance'], data['bluntness dmg. resistance'],
                    data['explotion dmg. resistance'], [Item.load(i) for i in data['inventory']])
            i.ex = data['has exploded?']
            return i
        elif data['type'] == 'CreeperCow':
            return en.CreeperCow.load(data)
        elif data['type'] == 'Brute':
            return en.Brute.load(data)

