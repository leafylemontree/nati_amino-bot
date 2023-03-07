async def fromSticker(ctx):
    if ctx.msg.extensions.replyMessageId is None:
        return ctx.send("Debe usar este comando como respuesta a un sticker")


