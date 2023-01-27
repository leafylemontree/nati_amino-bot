import asyncio
from src.database import db
from src import utils

@utils.isStaff
async def joinChats(ctx):
    text = ctx.msg.content.upper().split(" ")
    msg  = ctx.msg.content.upper()

    try:
        size    = int(text[1]) if len(text) > 1 else 25
        silent  = False if msg.find("-S") != 1 else True
        active  = False if msg.find("-A") != 1 else True
    except ValueError:
        return await ctx.send("El argumento del tamaño no es válido")

    threads = await ctx.client.get_public_chats(start=0, size=size)
    
    success = 0
    failed  = 0

    base_msg = "Bot Nati ha sido añadido a este chat por el staff de la comunidad"
    base_msg += ". Está desactivado por defecto." if active is False else "."

    for chat in threads:
        try:
            print(chat.threadId)
            await ctx.client.join_chat(chat_id=chat.threadId)
            success += 1
            if not silent: await ctx.client.send_message(
                        chat_id      = chat.threadId,
                        message      = base_msg,
                        message_type = 109
                    )
            if not active: db.setChatConfig(chat.threadId, "bot", 1)
        except Exception as e:
            print(e)
            failed  += 1

        await asyncio.sleep(1)

    return await ctx.send(f"""
Tarea completada
--------------------------
Unido a: {success} chats
{failed} han tenido error""")
