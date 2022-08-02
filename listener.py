import subprocess
import sys
import os
from edamino import Bot, Context, Client, api
from edamino.api import File
from edamino.objects import UserProfile
import json
import threading
import pathlib
import socket

path = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, f'{path}/src/python')
from commands import commands
import bot_objects as bot_o

time_ct = 300

def main():

    #server = bot_o.Server()
    bot = commands.login()

    @bot.event(message_types=api.MessageType.ALL, media_types=api.MediaType.ALL)
    async def on_message(ctx: Context):
        
        global time_ct
        time_ct = 300
        #try:
        #    if ctx.msg.content.find("Good day. I want") != -1:
        #        await ctx.client.delete_message(
        #            chat_id=ctx.msg.threadId,
        #            message_id=ctx.msg.messageId
        #            )
        #        await ctx.client.kick_from_chat(
        #            ctx.msg.threadId,
        #            ctx.msg.author.uid,
        #            allow_rejoin=False
        #        )
        #        return
        #    if ctx.msg.author.nickname.find("mambll_") != -1:
        #        await ctx.client.kick_from_chat(
        #            ctx.msg.threadId,
        #            ctx.msg.author.uid,
        #            allow_rejoin=False
        #            )
        #        return
        #except Exception:
        #    pass
        reply = await commands.message(ctx);
        return

    #@bot.event()
    #async def on_mention(ctx: Context):
    #    return

    try:
        bot.start();
    except:
        print("Login failed!")

def listen():
    global time_ct
    time_ct -= 1
    if time_ct == 0: sys.ext()

if __name__ == "__main__":
	main()

