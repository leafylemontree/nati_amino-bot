import multiprocessing
import asyncio
import threading

from .stalk     import stalk
from .clock     import clock

class Process:
    stalk = False
    clock = False

    def set(at, val):
        if   at == 0: Process.stalk = val
        elif at == 1: Process.clock = val
        return

def run(loop, ctx):
    if Process.stalk is False:
        Process.set(0, True)
        #p1 = threading.Thread(target=stalk, args=(loop,ctx))
        #p1.start()

    if Process.clock is False:
        Process.set(1, True)
        try:
            p2 = threading.Thread(target=clock, args=(loop,ctx))
            p2.start()
        except Exception:
                Process.set(1, False)
    return
