import aiohttp
from aiofile import async_open, AIOFile
import os
import io
import PIL

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


async def getImageBytes(ctx, url):

    response    = await ctx.client.session.request(method='GET', url=url)
    image       = io.BytesIO(await response.read())
    image.seek(0)
    result = io.BytesIO()

    temp        = PIL.Image.open(image)
    temp.save(result, format='PNG')
    result.seek(0)
    return        result
    
