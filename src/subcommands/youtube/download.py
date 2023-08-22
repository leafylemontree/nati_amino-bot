from __future__ import unicode_literals
import asyncio
from aiofile import async_open, AIOFile
from src import utils

loop = False

@utils.userTracker("download")
async def videoDownload(ctx):
    global loop

    msg = ctx.msg.content
    if msg.find("youtu") == -1: return await ctx.send("Debe ingresar el link a un video")

    url = msg.split(" ")[1]
    await ctx.send("Descargando video")
    
    proc = await asyncio.create_subprocess_shell(f'python3 src/subcommands/youtube/subp.py {url}')
    await proc.wait()

    async with AIOFile("media/youtube/list.bin", "r") as file:
        videos = await file.read()
        print(videos, type(videos))


    for i in range(int(videos) + 1):
        filename = f'media/youtube/download{i:03d}.wav'
        print(filename)
        async with AIOFile(filename, "rb") as file:
            audio = await file.read()
            await ctx.send_audio(audio)
