from asyncio import sleep
from src import utils

@utils.isStaff
async def del_(ctx):
    msg = ctx.msg.content.upper().split(" ")
    l = msg[1] if len(msg)>1 else 10
    try:    l = int(l)
    except: l = 10
    success= 0
    failed = 0
    async for page in ctx.client.get_chat_messages_iter(chat_id=ctx.msg.threadId, size=l):
        await sleep(3)
        for message in page:
            try:
                await ctx.client.delete_message(
                        chat_id=ctx.msg.threadId,
                        message_id=message.messageId,
                        as_staff=False
                    )
                success += 1
            except:
                failed += 1
            await sleep(1)

    await ctx.send(f"""Se han intentado eliminar {l} mensajes
--------------
Borrados: {success}
Fallidos: {failed}""")
    return
