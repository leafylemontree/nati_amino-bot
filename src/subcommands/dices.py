from random import random
from src import objects

def dices(msg):
        if len(msg.split(" ")) == 1:
            return objects.Reply("Debe ingresar un número después del comando, por ejemplo\n\n--dados 6", False)
        else :
            num = msg[8:]
            num = int(num)
            return objects.Reply(str(int(random() * (num - 1)) + 1), False)

def rand():
    return objects.Reply(random()*1_000_000_000, False)
