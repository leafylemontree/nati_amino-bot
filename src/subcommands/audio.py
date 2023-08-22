from src import utils
import os
import asyncio
from aiofile import async_open, AIOFile

async def audioSubProcess(ctx, url):
    await utils.downloadAudio(url)
    print("Running")
    proc = await asyncio.create_subprocess_shell('python3 src/utils/audioSP.py')
    r    = await proc.wait()
    async with AIOFile("media/srtext.txt", "r") as textFile:
        text = await textFile.read()
        print(text)
    return await ctx.send(text)

@utils.userTracker("escuchar")
async def audioRecognize(ctx):
    fail_message = "Debe usar este comando respondiendo a un audio"

    if ctx.msg.extensions.replyMessage is None: return await ctx.send(fail_message)
    url = ctx.msg.extensions.replyMessage.mediaValue
    if url is None: return await ctx.send(fail_message)
    
    await ctx.send("Escuchando audio. Esto puede tardar unos momentos")
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(audioSubProcess(ctx, url,), loop=loop)

