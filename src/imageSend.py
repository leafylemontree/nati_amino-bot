import time

async def send_image(ctx, image=None, media=None, itype='jpg', threadId=None):
    """
    ctx is Context
    image is a bytes object
    """

    if media is None:   media = await ctx.client.upload_media(image, f"image/{itype}")
    if threadId is None: threadId = ctx.msg.threadId
    data = {
            "content": None,
            "clientRefId": int(time.time() / 10 % 1000000000),
            "timestamp": int(time.time() * 1000),
            "mediaType": 100,
            "sendFailed": False,
            "type": 0,
            "uploadId": 0,
            "mediaValue": media
            }
    return await ctx.client.request("POST", f"chat/thread/{threadId}/message", json=data)

async def send_gif(ctx, image=None, media=None):
    """
    ctx is Context
    image is a bytes object
    """
    
    if media is None:   media = await ctx.client.upload_media(image, "image/gif")
    data = {
            "content": None,
            "clientRefId": int(time.time() / 10 % 1000000000),
            "timestamp": int(time.time() * 1000),
            "mediaType": 100,
            "sendFailed": False,
            "type": 0,
            "uploadId": 0,
            "mediaValue": media
        }
    await ctx.client.request("POST", f"chat/thread/{ctx.msg.threadId}/message", json=data)
    return media

async def send_audio(ctx, audio):
    """
    ctx is Context
    audio is a bytes object
    """

    media = await ctx.client.upload_media(audio, "audio/wav")
    data = {
            "content": None,
            "clientRefId": int(time.time() / 10 % 1000000000),
            "timestamp": int(time.time() * 1000),
            "mediaType": 110,
            "sendFailed": False,
            "type": 2,
            "uploadId": 0,
            "mediaValue": media
            }
    return await ctx.client.request("POST", f"chat/thread/{ctx.msg.threadId}/message", json=data)
