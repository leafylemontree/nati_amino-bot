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

def main():
    # server = bot_o.Server()
    bot = commands.login()

    @bot.event(message_types=api.MessageType.ALL, media_types=api.MediaType.ALL)
    async def on_message(ctx: Context):
        # server.send(ctx)
        reply = await commands.message(ctx);
        return

    try:
        bot.start();
    except:
        print("Login failed!")

if __name__ == "__main__":
	main()

