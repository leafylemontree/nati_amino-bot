import aiohttp
from aiofile import async_open, AIOFile
import asyncio
import json
import base64
from src import utils

@utils.disabled
@utils.userTracker("craiyon")
async def craiyon(ctx):
    token = ctx.msg.content.split()[1:]
    token = " ".join(token)

    await ctx.send(f"Generando imagen con parámetro '{token}'\nPor favor espere, esto puede tardar hasta dos minutos")

    data = {
        "prompt" : token
        }

    async with aiohttp.ClientSession() as session:
        async with session.post(
                url     = "https://backend.craiyon.com/generate",
                json    = data
                ) as resp:

            response = await resp.json()
            images   = response['images']
            
            rawData = base64.decodebytes(images[0].encode('utf-8'))
            from src.imageSend import send_image
            await send_image(ctx, rawData)
