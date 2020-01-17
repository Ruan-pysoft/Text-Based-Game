from mainclasses import Item
import functions as f

class Gold(Item): # you can't have a game without gold!
    def __init__(self, weight):
        self.weight = weight #In KG
        super().__init__(name="Gold",
                         description="A gold nugget weighing {} grammes.".format(str(self.weight*1000)),
                         value=self.weight*500000)
                         # the values of gold, silver and diamond are based on
                         # the values when I origionally made this game. I can't
                         # remember if it was in USD or ZAR

    @property
    def full_str(self):
        return f'''{repr(self)}:
  Variables:
    weight = {repr(self.weight)}
    name = {repr(self.name)}
    description = {repr(self.description)}
    value = {repr(self.value)}'''

class GoldCoin(Item): # neither can you have a game without coins
    def __init__(self, amt): # (except for Minecraft and Terasology and... actually a lot of games)
        self.amt = round(amt, 2)
        super().__init__(name="Golden Coin",
                         description="A round coin with {} stamped on the front.".format(str(self.amt)),
                         value=self.amt*100)

    @property
    def full_str(self):
        return f'''{repr(self)}:
  Variables:
    amt = {repr(self.amt)}
    name = {repr(self.name)}
    description = {repr(self.description)}
    value = {repr(self.value)}'''

class Silver(Item):
    def __init__(self, weight):
        self.weight = weight #In KG
        super().__init__(name="Silver",
                         description="A piece of silver weighing {} grammes.".format(str(self.weight*1000)),
                         value=self.weight*7000)

    @property
    def full_str(self):
        return f'''{repr(self)}:
  Variables:
    weight = {repr(self.weight)}
    name = {repr(self.name)}
    description = {repr(self.description)}
    value = {repr(self.value)}'''

class SilverCoin(Item):
    def __init__(self, amt):
        self.amt = round(amt, 2)
        super().__init__(name="Silver Coin",
                         description="A round coin with {} stamped on the front.".format(str(self.amt)),
                         value=self.amt)

    @property
    def full_str(self):
        return f'''{repr(self)}:
  Variables:
    amt = {repr(self.amt)}
    name = {repr(self.name)}
    description = {repr(self.description)}
    value = {repr(self.value)}'''

class Copper(Item):
    def __init__(self, weight):
        self.weight = weight #In KG
        super().__init__(name="Gold",
                         description="A gold nugget weighing {} grammes.".format(str(self.weight*1000)),
                         value=self.weight*90)

    @property
    def full_str(self):
        return f'''{repr(self)}:
  Variables:
    weight = {repr(self.weight)}
    name = {repr(self.name)}
    description = {repr(self.description)}
    value = {repr(self.value)}'''

class CopperCoin(Item):
    def __init__(self, amt):
        self.amt = round(amt)
        super().__init__(name="Bronze Coin",
                         description="A round coin with {} stamped on the front.".format(str(self.amt)),
                         value=self.amt*0.01)

    @property
    def full_str(self):
        return f'''{repr(self)}:
  Variables:
    amt = {repr(self.amt)}
    name = {repr(self.name)}
    description = {repr(self.description)}
    value = {repr(self.value)}'''

class Diamond(Item):
    def __init__(self, weight, cut):
        self.weight = weight #In KG
        if cut == True:
            self.cut = "polished"
            self.value = (weight*5000)*7000
        else:
            self.cut = "raw"
            self.value = (weight*5000)*5500
        super().__init__(name="Diamond",
                         description="A {} diamond weighing {} grammes.".format(self.cut, str(self.weight*1000)),
                         value=self.value)

    @property
    def full_str(self):
        return f'''{repr(self)}:
  Variables:
    weight = {repr(self.weight)}
    name = {repr(self.name)}
    description = {repr(self.description)}
    value = {repr(self.value)}'''

class Weapon(Item): # base for all (non-ranged non-magic) weapons
    def __init__(self, name, description, value, damage, sharp, blunt, explotion):
        self.damage = damage # damage the weapon does
        self.sharp_rat = sharp # how much of that damage is sharpness damage
        self.blunt_rat = blunt # how much of that damage is blunt damage
        self.explotion_rat = explotion  # how much of that damage is explotion damage

        super().__init__(name, description, value)

    @property
    def sharp_damage(self):
        return self.damage*self.sharp_rat

    @property
    def blunt_damage(self):
        return self.damage*self.blunt_rat

    @property
    def ex_damage(self):
        return self.damage*self.explotion_rat

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nDamage: {}".format(self.name, self.description, self.value, self.damage)

    @property
    def str(self):
        return "{}, Damage: {}".format(self.name, self.damage)

    @property
    def full_str(self):
        return f'''{repr(self)}:
  Variables:
    damage = {repr(self.damage)}
    sharp_rat = {repr(self.sharp_rat)}
    blunt_rat = {repr(self.blunt_rat)}
    explotion_rat = {repr(self.explotion_rat)}
    name = {repr(self.name)}
    description = {repr(self.description)}
    value = {repr(self.value)}
  Read-only:
    sharp_damage = {repr(self.sharp_damage)}
    blunt_damage = {repr(self.blunt_damage)}
    ex_damage = {repr(self.ex_damage)}'''


class Rock(Weapon):
    def __init__(self):
        self.sharp = f.randomF(0.0,0.2,2)
        super().__init__(name="Rock",
                         description="A fist-sized rock, suitable for bludgeoning.",
                         value=0,
                         damage=f.random(4,6),
                         sharp=self.sharp,
                         blunt=1.0-self.sharp,
                         explotion=0)

class Dagger(Weapon):
    def __init__(self):
        self.sharp = f.randomF(0.6,0.99,2)
        super().__init__(name="Dagger",
                         description="A small dagger with some rust. Somewhat more dangerous than a rock.",
                         value=5,
                         damage=f.random(8,11),
                         sharp=self.sharp,
                         blunt=1.0-self.sharp,
                         explotion=0)

class Sword(Weapon):
    def __init__(self):
        self.sharp = f.randomF(0.9,1.0,2)
        super().__init__(name="Sword",
                         description="A good sword.",
                         value=5,
                         damage=f.random(19,22),
                         sharp=self.sharp,
                         blunt=1.0-self.sharp,
                         explotion=0)

class BlankWeapon(Weapon):
    def __init__(self, name, description, value, damage, sharp, blunt, explotion):
        super().__init__(name=name,
                         description=description,
                         value=value,
                         damage=damage,
                         sharp=sharp,
                         blunt=blunt,
                         explotion=explotion)
