from src            import objects
from src            import commands
from src            import subprocess
from src            import utils
import asyncio
from edamino import Bot, Context, Client, api
from src.database import db

import threading
import time
import sys
import traceback

from src.special import LA

def keepAlive():
    def clock():
        objects.ba.counter = 300
        while True:
            objects.ba.counter -= 1
            if objects.ba.counter == 0:
                objects.ba.kill(0)
                sys.exit(0)
            time.sleep(1)
        return
    
    clk_t = threading.Thread(target=clock)
    clk_t.start()

def main():
    bot = commands.login()

    @bot.ready()
    async def on_ready(ctx: Context):
        objects.ba.loop = asyncio.get_event_loop()
        #db.dumpAllChats()
        subprocess.run(objects.ba.loop, ctx)
        await LA.config(ctx)
        await utils.st.set(ctx)
        return

    @bot.reload(message="Bot reloaded")
    async def on_reload(ctx: Context):
        objects.ba.loop = asyncio.get_event_loop()
        objects.ba.context = ctx
        subprocess.reloadContext(objects.ba.loop, ctx)
        return

    @bot.event(message_types=api.MessageType.ALL, media_types=api.MediaType.ALL)
    async def on_message(ctx: Context):
        objects.ba.counter = 300
        await commands.message(ctx);
        return

    try:
        bot.start();
    except Exception as e:
        print("Login failed!")
        print("Exception caught:", e)
        traceback.print_exc()
        objects.ba.kill(0)

if __name__ == "__main__":
    print(sys.argv)
    objects.ba.instance = int(sys.argv[3])
    main()
