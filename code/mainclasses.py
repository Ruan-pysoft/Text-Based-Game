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

    @property
    def full_str(self):
        return f'''{repr(self)}:
  Variables:
    name = {repr(self.name)}
    description = {repr(self.description)}
    value = {repr(self.value)}'''

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
        self.inventory = [item[0](*item[1], **item[2]) for item in inv]

    @property
    def str(self):
        return f'''{repr(self)[1:-1]} in RAM:
  Variables:
    name = {repr(self.name)}
    hp = {repr(self.hp)}
    damage = {repr(self.damage)}
    sharp_rat = {repr(self.sharp_rat)}
    blunt_rat = {repr(self.blunt_rat)}
    ex_damage = {repr(self.ex_damage)}
    ex_chance = {repr(self.ex_chance)}
    ex_health = {repr(self.ex_health)}
    blunt_res = {repr(self.blunt_res)}
    sharp_res = {repr(self.sharp_res)}
    ex_res = {repr(self.ex_res)}
    ex = {repr(self.ex)}

    #===#
    inventory = [
{str([i.name for i in self.inventory])[1:-1]}
    ]
    #===#

  Read-only:
    is_alive() = {repr(self.is_alive())}'''

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
    name = {repr(self.name)}
    hp = {repr(self.hp)}
    damage = {repr(self.damage)}
    sharp_rat = {repr(self.sharp_rat)}
    blunt_rat = {repr(self.blunt_rat)}
    ex_damage = {repr(self.ex_damage)}
    ex_chance = {repr(self.ex_chance)}
    ex_health = {repr(self.ex_health)}
    blunt_res = {repr(self.blunt_res)}
    sharp_res = {repr(self.sharp_res)}
    ex_res = {repr(self.ex_res)}
    ex = {repr(self.ex)}

    #===#
    inventory = [
{full_inv()}
    ]
    #===#

  Read-only:
    is_alive() = {repr(self.is_alive())}'''

    def explode(self):
        if self.hp < self.ex_health and uniform(0.0000,1.0000) < self.ex_chance:
            self.ex = True

    def is_alive(self):
        return self.hp > 0
