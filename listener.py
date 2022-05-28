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

# Function definitions

# Running app

def main():
    # os.system(f"cd {path}")
    # print("************************\nexecuting nodejs\n********************\n\n")
    # print("Session logged in!")
    # server = bot_o.Server()

    with open("src/json/login.json", "r") as loginFile:
        loginData = json.load(loginFile)
        bot = Bot(email=loginData['username'], password=loginData['password'], prefix=loginData['prefix'])

    @bot.event()
    async def on_mention(ctx: Context):
        reply = await commands.mention(ctx, msg_text)
        if reply['msg'] is not None: await ctx.send(reply['msg'])

    @bot.event(message_types=api.MessageType.ALL, media_types=api.MediaType.ALL)
    async def on_message(ctx: Context):
        # server.send(ctx)
        # curr_msg['nick'] = ctx.msg.author.nickname
        # curr_msg['msg'] = ctx.msg.content
        # cl.send(bytes(json.dumps(curr_msg),encoding='utf-8'))
        reply = await commands.message(ctx);

        # if ((reply is None) | (reply is False)) : return
        # if (reply['audio'] is not False) :
        #     with open(reply['audio'], "rb") as file:
        #         audio = file.read()
        #         await ctx.send_audio(audio)

        return

    try:
        bot.start();
    except:
        print("Login failed!")


if __name__ == "__main__":
    main()
