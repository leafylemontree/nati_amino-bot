import aiohttp
from aiofile import async_open, AIOFile
import os

async def downloadImage(url):
        async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    async with AIOFile("media/dl.jpg", "wb+") as img:
                        await img.write(await resp.read())
        return

async def downloadAudio(url):
        async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    async with AIOFile("media/audio.aac", "wb+") as audio:
                        await audio.write(await resp.read())
        return

async def getPfp(user):
        async with aiohttp.ClientSession() as session:
                async with session.get(user.icon) as resp:
                    async with AIOFile("media/pfp.jpg", "wb+") as img:
                        await img.write(await resp.read())
        os.system("magick media/pfp.jpg media/pfp.png")
        return

