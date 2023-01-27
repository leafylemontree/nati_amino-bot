import time

async def send_image(ctx, image):
    """
    ctx is Context
    image is a bytes object
    """

    media = await ctx.client.upload_media(image, "image/jpg")
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
    return await ctx.client.request("POST", f"chat/thread/{ctx.msg.threadId}/message", json=data)

async def send_gif(ctx, image):
    """
    ctx is Context
    image is a bytes object
    """

    media = await ctx.client.upload_media(image, "image/gif")
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
    return await ctx.client.request("POST", f"chat/thread/{ctx.msg.threadId}/message", json=data)

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
