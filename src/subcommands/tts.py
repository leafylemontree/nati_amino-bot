import aiohttp
import asyncio
import base64
import aiofile

async def tts(ctx):
    text = ctx.msg.content.split(" ")[1:]
    text = " ".join(text)

    data = {
        "text"  : text,
        "voice" : "es_mx_002"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
                'https://tiktok-tts.weilnet.workers.dev/api/generation',
                json=data
                ) as resp:

            response = await resp.json()
            audio = base64.decodebytes(response['data'].encode('utf-8'))
            
            async with aiofile.AIOFile('media/tts/audio.mp3', 'wb+') as f:
                await f.write(audio)
            
            proc = await asyncio.create_subprocess_shell('rm media/tts/audio.wav')
            await proc.wait()
            
            proc = await asyncio.create_subprocess_shell('ffmpeg -i media/tts/audio.mp3 media/tts/audio.wav')
            await proc.wait()

            async with aiofile.AIOFile('media/tts/audio.wav', 'rb+') as f:
                a = await f.read()
                await ctx.send_audio(a)
    return





