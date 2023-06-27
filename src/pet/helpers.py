import math
import random
from src import objects

A = 100
B = 1.0675

def getLevelFromEXP(exp):
    level = math.log( 1 + exp*(-1 + B)/A) / math.log(B)
    return math.floor(level)


def getExpBaseFromLevel(level):
    exp = A * ((1 - B**level) / (1 - B))
    return math.floor(exp)

def getRemainingEXP(exp):
    baseLevel = getLevelFromEXP(exp)
    upperEXP  = getExpBaseFromLevel(baseLevel + 1)
    return (upperExp - exp)

def getEXPGain(item):
    baseEXP = 20
    baseEXP += item.health      / 8000
    baseEXP += item.happiness   / 575
    baseEXP += item.energy      / 350
    baseEXP += item.care        / 400
    baseEXP += item.hunger      / 250
    baseEXP += item.thirst      / 600
    baseEXP += int(random.random() * 10) - 5

    if baseEXP < 5  : baseEXP = 5
    return math.ceil(baseEXP)

class Stickers:
    fine        = 0
    happy       = 1
    energetic   = 2
    love        = 3
    pleased     = 4
    hurt        = 5
    bored       = 6
    sleepy      = 7
    isolated    = 8
    skinny      = 9

def averageStats(pet):
    p = pet.health + pet.happiness + pet.energy + pet.care + pet.hunger + pet.thirst
    return math.floor(p/6)


def getStickerValue(pet):
    if      pet.health         < 4000:                  return Stickers.hurt
    elif    pet.happiness      < 4000:                  return Stickers.bored
    elif    pet.energy         < 4000:                  return Stickers.sleepy
    elif    pet.care           < 4000:                  return Stickers.isolated
    elif    pet.hunger < 4000 or pet.thirst < 4000:     return Stickers.skinny
    
    average = averageStats(pet)
    if      pet.happiness > (average + 1000):           return Stickers.happy
    elif    pet.energy    > (average + 1000):           return Stickers.energetic
    elif    pet.care      > (average + 1000):           return Stickers.love
    elif    pet.hunger    > (average + 1000):           return Stickers.pleased
    elif    pet.thirst    > (average + 1000):           return Stickers.pleased
    return Stickers.fine
