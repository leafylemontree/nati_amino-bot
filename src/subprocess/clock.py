from src             import objects
from src.config.data import Config
import datetime, time
import sys
from src.database import db
import asyncio

async def sendTimerMessage(ctx, msg):
    print(msg)
    ctx.client.set_ndc(msg['comId'])
    chat = await ctx.client.start_chat(invitee_ids = [msg['userId']])
    base_msg = f"""
Temporizador
------------------------------
{msg['message']}
"""
    return await ctx.client.send_message(message=base_msg,
                                    chat_id=chat.threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None )

def periodicTasks(ctx, loop):
    time_ct = 300
    stat_ct = 60
    while True:
        time_ct -= 1
        stat_ct -= 1
        if time_ct == 0: sys.exit()
        if stat_ct == 0:
            objects.botStats.write()
            Config.write()

            crdate = datetime.datetime.now()
            db.cursor.execute(f"SELECT * FROM Countdown")
            data = db.cursor.fetchall()
            for timer in data:
                secs =  time.mktime(crdate.timetuple()) - time.mktime(timer[3].timetuple())
                if secs > (timer[4]*60):
                    db.cursor.execute(f'DELETE FROM Countdown WHERE userId="{timer[1]}" AND ID={timer[0]};')
                    msg = {
                                    "message" : timer[5],
                                    "comId"   : timer[2],
                                    "userId"  : timer[1]
                                }
                    f = asyncio.run_coroutine_threadsafe(sendTimerMessage(ctx, msg ), loop=loop)
                    f.result()
            stat_ct = 60
        time.sleep(1)

def clock(loop, ctx):
    periodicTasks(ctx, loop)
