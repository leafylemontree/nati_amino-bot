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
import ujson
import edamino

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




class FakeMessage:
    def __new__(self):
        self.ndcId = 0
        return self

def main():
    bot = commands.login()

    @bot.event(message_types=api.MessageType.ALL, media_types=api.MediaType.ALL)
    async def on_message(ctx: Context):
        objects.ba.counter = 300
        await commands.message(ctx);
        return


    @bot.ready()
    async def on_ready(ctx: Context):
        print("Start")
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

    #async def parseResponse(data, ws):
    #    s = edamino.objects.SocketAnswer(**data)
    #    if s.t != 1000: return
    #    msg         = s.o.chatMessage
    #    msg.ndcId   = s.o.ndcId
    #    if msg.author.uid == bot.client.uid: return
    #    context     = bot.get_context(bot.client, msg, ws)
    #    bot.loop.create_task(on_message(context))

    #@utils.runSubTask(pollingTime=180)
    #async def ws_reload(ctx):
    #    print("WS reload start")
    #    ws = await ctx.client.ws_connect()
    #    timestamp = time.time()
    #    print("WS reloaded manually")
    #    while True and (time.time() - timestamp) < 180:
    #        try:
    #            data = await ws.receive_json(loads=ujson.loads)
    #            await parseResponse(data, ws)
    #        except Exception as e:
    #            print(e)

    @utils.runSubTask(pollingTime=60*60*12)
    async def re_login(ctx):
        await asyncio.sleep(60*60*12)
        login = await ctx.client.login(self.email, self.password)
        ctx.client.sid = login.sid
        ctx.client.uid = login.auid
        bot.update_cfg()
        try:
            start_context = bot.get_context(bot.client, FakeMessage(), bot.ws)
            bot.loop.create_task(on_reload(start_context))
        except Exception as e:
            pass


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
