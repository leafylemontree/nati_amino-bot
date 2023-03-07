import multiprocessing
import asyncio
import threading

from .stalk     import stalk
from .clock     import clock
from src        import utils

class Process:
    stalk = False
    clock = False
    subTs = False

    def set(at, val):
        if   at == 0: Process.stalk = val
        elif at == 1: Process.clock = val
        elif at == 2: Process.subTs = val
        return

def st_run(loop, ctx):
    print("Running SubTs")
    coro = asyncio.run_coroutine_threadsafe(utils.st.run(), loop=loop)
    coro.result()

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
        
    if Process.subTs is False:
        Process.set(2, True)
        try:
            p3 = threading.Thread(target=st_run, args=(loop,ctx))
            p3.start()
        except Exception:
            Process.set(2, False)
        

    return
