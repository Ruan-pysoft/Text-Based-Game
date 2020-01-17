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


class Brute(Enemy): # Enemy with a lot of health that does a lot of damage
    def __init__(self, inv=[[items.Sword, (), {}]]):
        super().__init__(name="Brute", hp=52, damage=f.random(5,11),
                         sharp=0, blunt=1,
                         ex=0, ex_chance=0,
                         ex_health=0, shr=f.randomF(0.01,0.02,3),
                         blr=f.randomF(0.025,0.05,3),
                         exr=f.randomF(-0.55,-0.45,2), inv=inv)
