from src             import objects
from src.config.data import Config
import time
import sys

def periodicTasks():
    time_ct = 300
    stat_ct = 60
    while True:
        time_ct -= 1
        stat_ct -= 1
        if time_ct == 0: sys.exit()
        if stat_ct == 0:
            objects.botStats.write()
            Config.write()
            stat_ct = 60
        time.sleep(1)


def clock(loop, ctx):
    periodicTasks()
