# This is a file of usefull functions I use in my programs and is not exclusively
# used for this game
import os
import sys
from random import randint, uniform
import random as ra
import pickle
import math
import time
import secrets

global TAU
TAU =  math.pi * 2 # Easier to say 'C=TAU*r' than 'C=2*math.pi*r'

global C
C = 299792458 # Speed of light in E=mc^2 (I know it's ** in python)

def factorial(n):
  if n == 0:
    return 1 # 0! = 1
  elif n < 0:
    raise ValueError('factorial can only take numbers of zero or more! {} is too small'.format(n)) # Can't do -n!
  elif n%1 != 0:
    raise ValueError('factorial can only take intigers!'.format(n)) # n.x! is technically possible, but it uses a LOT of comlicated maths I don't understand
  else:
    return n * factorial(n-1) # n! = n*n-1*n-2*...*1

def nChooseK(n,k): # This is some maths thing I put in because I thought it would be fun
  return factorial(n)/(factorial(k)*factorial(n-k))

def kgToJ(kg): # E=mc^2
  return kg*(C**2)

def JToKg(J): # E=mc^2 thus E/c^2=mc^2/c^2 thus E/c^2=m or m=E/c^2
  return J/(C**2)

def change_char(s, p, r): # string, position of char to be replaced, char to be replaced with
    l = list(s) # make the string a list
    l[p] = r # replace the char at p with char r
    return "".join(l) # stich the list back into a string and return it

def path(): # get the path to the current file
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def txtfile(file, mode="r", data=None): # method to read from, append to or overwrite a file
    file = path()+file
    try:
        if mode=="w":
            if data != None:
                try:
                    with open(file, 'a') as f:
                        pickle.dump(data, f)
                    return "Data saved"
                except:
                    os.mkdir(file)
                    with open(file, 'w') as f:
                        pickle.dump(data, f)
                    return "Data saved in new file"
            else:
                return "No data to save"
        if mode =="r":
            try:
                with open(file) as f:
                        _data = pickle.load(f)
                return _data
            except:
                return None
        if mode=="ow":
            if data != None:
                try:
                    with open(file, 'w') as f:
                        pickle.dump(data, f)
                    return "Data overwritten"
                except:
                    #os.mkdir(file)
                    with open(file, 'w') as f:
                        pickle.dump(data, f)
                    return "Data saved in new file"
            else:
                return "No data to save"
    except Exception as e:
        print("Error! \n" + str(e))
        return "Error!"

def save(name, data=None): # I don't really use this anywhere... maybe I should delete it.
    _save=txtfile("\\saves\\"+str(name)+".sav", mode="w", data=data)
    return _save
def load(name): # I don't really use this anywhere... maybe I should delete it.
    _data=txtfile("\\saves\\"+str(name)+".sav", mode="r")
    return _data
def overWrite(name, data=None): # I don't really use this anywhere... maybe I should delete it.
    _save=txtfile("\\saves\\"+str(name)+".sav", mode="ow", data=data)
    return _save

def delete(name): # I don't really use this anywhere... maybe I should delete it.
    try:
        os.remove(path()+"\\saves\\"+str(name)+".sav")
    except Exception as e:
        print("Error! \n" + str(e))
        return "Error!"

def random(a,b): # easier to type than randint
    return randint(a,b)

def randomI(a,b): # randint like range
    return randint(a,b-1)

def randomF(a,b,d=None): # uniform, but with a option to round the answer
    if d==None:
        return uniform(a,b)
    else:
        return round(uniform(a,b), d) # round the answer to d numbers after the .

def randomWeight(weights): # return a weighted random int (input as list)
    wt = 0
    for w in weights:
        wt += w
    r = uniform(0,wt)
    i = 0
    for w in weights:
        if r < w:
            return i
        else:
            i += 1
            r -= w

def randomWeights(*weights): # return a weighted random int (multiple inputs)
    wt = 0
    for w in weights:
        wt += w
    r = uniform(0,wt)
    i = 0
    for w in weights:
        if r < w:
            return i
        else:
            i += 1
            r -= w

def LCGRand(seed='0',mult=1664525,inc=1013904223,mod=math.pow(2,32)): # a certain type of random
    if seed == '0':
        seed=time.time()/secrets.randbelow(math.floor(time.time()))
    seed = (mult*seed+inc)%mod
    return seed

def LCGFloat(seed='0',mult=1664525,inc=1013904223,mod=math.pow(2,32)): # a certain type of random (for floats)
    if seed == '0':
        seed=time.time()/secrets.randbelow(math.floor(time.time()))
    seed = ((mult*seed+inc)%mod)/mod
    return seed

def norm(val, mini, maxi): # ?? I can't remember what this does (I know it "normalises" a number)
    return (val - mini) / (maxi - mini)

def mapp(val, min0, max0, min1, max1): # ?? I can't remember what this does
    mult = max1 - min1
    return (norm(val, min0, max0) * mult) + min1

def lerp(val, mini, maxi): # ?? I can't remember what this does
    mult = maxi - mini
    return (val * mult) + mini

def clamp(val, mini, maxi):
    if val < maxi and val > mini: # if the number is within min & max
        return val # return the number
    elif val > maxi: # otherwise, if the number is more than max
        return maxi # return max
    else: # otherwise (number is less than min)
        return mini # return min

def sqrt(val):
    return val**0.5 # return the square root of the number

def ditance(x0, y0, x1, y1): # uses the pythagorean theorem to find the distance between 2 points
    dx = x1-x0
    dy = y1-y0
    y = dy*dy
    x = dx*dx
    return sqrt(x+y)

def radToDeg(rad): # converts radians to degrees
    return mapp(rad, 0, TAU, 0, 360) # so this is what mapp does...

def degToRad(deg): # converts degrees to radians
    return mapp(deg, 0, 360, 0, TAU) # I think I got this "mapp" off of wikipedia (as a maths equation)

def roundF(val, dec): # rounds to the nearest dec (ex: 0.5)
    dec = 1/(10**dec)
    val0 = val - (val%dec)
    if val-val0 < (val0+dec)-val:
        return val
    else:
        return val + dec

def roundI(val, num): # rounds to the nearest num (ex: 7)
    val0 = val - (val%num)
    if val-val0 < (val0+num)-val:
        return val0
    else:
        return val0 + num

def floorF(val, dec): # rounds down to the nearest dec (ex: 0.5)
    dec = 1/(10**dec)
    val0 = val - (val%dec)
    return val0

def floorI(val, num): # rounds down to the nearest num (ex: 7)
    val0 = val - (val%num)
    return val0

def ceilF(val, dec): # rounds up to the nearest dec (ex: 0.5)
    dec = 1/(10**dec)
    val0 = val - (val%dec)
    if val0 == val:
        return val0
    else:
        return val0+dec

def ceilI(val, num): # rounds up to the nearest num (ex: 7)
    val0 = val - (val%num)
    if val0 == val:
        return val0
    else:
        return val0+num

def randomBellCurve(minR, maxR, i = 2): # bell curve random ( (minR+maxR)/2 is more likely than minR or maxR)
    total = 0
    for j in range(0,i+1):
        total += randomF(minR,maxR)
    return roundF(total/i, 0)

def rand2(): # my own wierd random, because why not
    r = random(0,4)
    if r == 0:
        r = randomWeight([2,2,1,1,1,1,1,1,1,1])+1
    elif r == 1:
        r = randomWeight([1,1,2,2,1,1,1,1,1,1])+1
    elif r == 2:
        r = randomWeight([1,1,1,1,2,2,1,1,1,1])+1
    elif r == 3:
        r = randomWeight([1,1,1,1,1,1,2,2,1,1])+1
    elif r == 4:
        r = randomWeight([1,1,1,1,1,1,1,1,2,2])+1
    return (ra.random() * r) / 10

def bin2bool(b): return b == 1 # convert binary to boolean

def bool2bin(b): # convert boolean to binary
    if b: return 1
    return 0

def AND(b0, b1): return bool2bin(bin2bool(b0) and bin2bool(b1)) # binary AND
# the ONLY place (in my opinion) that Java beats Python is that this ^ can be binary AND boolean
# at the same time without a lot of if statements (operator overloading)
def OR(b0, b1): return bool2bin(bin2bool(b0) or bin2bool(b1)) # binary OR

def NOT(b): return bool2bin(not bin2bool(b)) # binary NOT

def NAND(b0, b1): return NOT(AND(b0, b1)) # binary NAND ( NOT (A AND B) )

def NOR(b0, b1): return NOT(OR(b0, b1)) # binary NOR ( NOT (A OR B) )

def XOR(b0, b1): return AND(OR(b0, b1), NAND(b0, b1)) # binary XOR/EOR (A OR B) AND NOT (A AND B)
'''
Other ways to make XOR/EOR:

OR(AND(NOT(b0), b1), AND(b0, NOT(b1)))
bool2bin(b0 != b1)
NAND(NAND(b0, NAND(b0, b1)), NAND(b1, NAND(b0, b1)))

(The last one I got somewhere on the internet. It works,
but the other three makes more sense)
'''
