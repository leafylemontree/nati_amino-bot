from src            import objects
from src            import commands
from src            import subprocess
import asyncio
from edamino import Bot, Context, Client, api

import threading
import time
import sys

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
    #server = objects.Server()
    bot = commands.login()

    @bot.event(message_types=api.MessageType.ALL, media_types=api.MediaType.ALL)
    async def on_message(ctx: Context):
        if objects.ba.loop is False: loop = asyncio.get_event_loop()
        subprocess.run(objects.ba.loop, ctx)
        objects.ba.counter = 300
        await commands.message(ctx);

    try:
        bot.start();
    except Exception as e:
        print("Login failed!")
        print("Exception caught:", e)
        objects.botStats.write()

if __name__ == "__main__":
    objects.ba.instance = int(sys.argv[3])
    keepAlive()
    main()
