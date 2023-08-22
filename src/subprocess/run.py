import multiprocessing
import asyncio
import threading

from .stalk     import stalk
from .clock     import clock
from src        import utils

from src.communication import sc

class Process:
    stalk = False
    clock = False
    subTs = False
    socket= False

    def set(at, val):
        if   at == 0: Process.stalk = val
        elif at == 1: Process.clock = val
        elif at == 2: Process.subTs = val
        elif at == 3: Process.socket= val
        return

def st_run(loop, ctx):
    loop.create_task(utils.st.run(ctx))
    return

def socket_run(loop, ctx):
    sc.config(host='localhost', port=31000)
    loop.create_task(sc.run(ctx))
    #coro = asyncio.run_coroutine_threadsafe(sc.run(ctx,), loop=loop)
    #coro.result()

def reloadContext(loop, ctx):
    sc.reloadContext(loop, ctx)
    utils.st.reloadContext(loop, ctx)


def run(loop, ctx):
    if Process.stalk is False:
        Process.set(0, True)
        #p1 = threading.Thread(target=stalk, args=(loop,ctx))
        #p1.start()

    if Process.clock is False:
        Process.set(1, True)
        #try:
        #    p2 = threading.Thread(target=clock, args=(loop,ctx))
        #    p2.start()
        #except Exception:
        #        Process.set(1, False)
        
    if Process.subTs is False:
        Process.set(2, True)
        try:
            p3 = threading.Thread(target=st_run, args=(loop,ctx))
            p3.start()
        except Exception:
            Process.set(2, False)
        
    if Process.socket is False:
        Process.set(3, True)
        try:
            p3 = threading.Thread(target=socket_run, args=(loop,ctx))
            p3.start()
        except Exception:
            Process.set(3, False)
        

    return
