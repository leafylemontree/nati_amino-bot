import math

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

