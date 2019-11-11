import os
import sys
from random import randint, uniform
import random as ra
import pickle
import math
import time
import secrets
import datetime as dt

global TAU
TAU =  math.pi * 2

global C
C = 299792458

def factorial(n):
  if n == 0:
    return 1
  elif n < 0:
    raise ValueError('factorial can only take numbers of zero or more! {} is too small'.format(n))
  elif n%1 != 0:
    raise ValueError('factorial can only take intigers!'.format(n))
  else:
    return n * factorial(n-1)

def nChooseK(n,k):
  return factorial(n)/(factorial(k)*factorial(n-k))

def kgToJ(kg):
  return kg*(C**2)

def JToKg(J):
  return J/(C**2)

def change_char(s, p, r):
    l = list(s)
    l[p] = r
    return "".join(l)

def path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def txtfile(file, mode="r", data=None):
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

def save(name, data=None):
    _save=txtfile("\\saves\\"+str(name)+".sav", mode="w", data=data)
    return _save
def load(name):
    _data=txtfile("\\saves\\"+str(name)+".sav", mode="r")
    return _data
def overWrite(name, data=None):
    _save=txtfile("\\saves\\"+str(name)+".sav", mode="ow", data=data)
    return _save

def delete(name):
    try:
        os.remove(path()+"\\saves\\"+str(name)+".sav")
    except Exception as e:
        print("Error! \n" + str(e))
        return "Error!"

def random(a,b):
    return randint(a,b)

def randomI(a,b):
    return randint(a,b-1)

def randomF(a,b,d=None):
    if d==None:
        return uniform(a,b)
    else:
        return round(uniform(a,b), d)

def randomWeight(weights):
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

def randomWeights(*weights):
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

def LCGRand(seed='0',mult=1664525,inc=1013904223,mod=math.pow(2,32)):
    if seed == '0':
        seed=time.time()/secrets.randbelow(math.floor(time.time()))
    seed = (mult*seed+inc)%mod
    return seed

def LCGFloat(seed='0',mult=1664525,inc=1013904223,mod=math.pow(2,32)):
    if seed == '0':
        seed=time.time()/secrets.randbelow(math.floor(time.time()))
    seed = ((mult*seed+inc)%mod)/mod
    return seed

def norm(val, mini, maxi):
    return (val - mini) / (maxi - mini)

def mapp(val, min0, max0, min1, max1):
    mult = max1 - min1
    return (norm(val, min0, max0) * mult) + min1

def lerp(val, mini, maxi):
    mult = maxi - mini
    return (val * mult) + mini

def clamp(val, mini, maxi):
    if val < maxi and val > mini:
        return val
    elif val > maxi:
        return maxi
    else:
        return mini

def sqrt(val):
    return val**0.5

def ditance(x0, y0, x1, y1):
    dx = x1-x0
    dy = y1-y0
    y = dy*dy
    x = dx*dx
    return sqrt(x+y)

def radToDeg(rad):
    return mapp(rad, 0, TAU, 0, 360)

def degToRad(deg):
    return mapp(deg, 0, 360, 0, TAU)

def roundF(val, dec):
    dec = 1/(10**dec)
    val0 = val - (val%dec)
    if val-val0 < (val0+dec)-val:
        return val
    else:
        return val + dec

def roundI(val, num):
    val0 = val - (val%num)
    if val-val0 < (val0+num)-val:
        return val0
    else:
        return val0 + num

def floorF(val, dec):
    dec = 1/(10**dec)
    val0 = val - (val%dec)
    return val0

def floorI(val, num):
    val0 = val - (val%num)
    return val0

def ceilF(val, dec):
    dec = 1/(10**dec)
    val0 = val - (val%dec)
    if val0 == val:
        return val0
    else:
        return val0+dec

def ceilI(val, num):
    val0 = val - (val%num)
    if val0 == val:
        return val0
    else:
        return val0+num

def randomBellCurve(minR, maxR, i = 2):
    total = 0
    for j in range(0,i+1):
        total += randomF(minR,maxR)
    return roundF(total/i, 0)

def rand2():
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

def bin2bool(b): return b == 1

def bool2bin(b):
    if b: return 1
    return 0

def AND(b0, b1): return bool2bin(bin2bool(b0) and bin2bool(b1))

def OR(b0, b1): return bool2bin(bin2bool(b0) or bin2bool(b1))

def NOT(b): return bool2bin(not bin2bool(b))

def NAND(b0, b1): return NOT(AND(b0, b1))

def NOR(b0, b1): return NOT(OR(b0, b1))

def XOR(b0, b1): return AND(OR(b0, b1), NAND(b0, b1))#OR(AND(NOT(b0), b1), AND(b0, NOT(b1)))#bool2bin(b0 != b1)#return NAND(NAND(b0, NAND(b0, b1)), NAND(b1, NAND(b0, b1)))
