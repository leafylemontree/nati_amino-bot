import asyncio
from src.database import db
from src import utils
import traceback

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
            if not active: db.setChatConfig(chat.threadId, "bot", 1, ctx.msg.ndcId)
        except Exception as e:
            print(e)
            failed  += 1

        await asyncio.sleep(1)

    return await ctx.send(f"""
Tarea completada
--------------------------
Unido a: {success} chats
{failed} han tenido error""")


@utils.isStaff
async def inviteEveryone(ctx):
        link = ctx.msg.content.split(" ")
        if len(link) == 1: return "Debe poner el link del chat al cual quiere que el bot se una"
        try:
            chatId = await ctx.client.get_info_link(link=link[1])
            if chatId.linkInfo.objectType != 12: return await ctx.send("El link ingresado no corresponde a un chat.")
        except:
            return "Se ha producido un error :c"

        users = []
        for i in range(100):
            us = await ctx.client.get_all_users(users_type='recent', start=i*100, size=100)
            u = list(map(lambda user: user.uid, us))
            if len(u) == 0: break
            users.extend(u)
            print(f"Inviting {len(u)} recent users to {chatId.linkInfo.objectId} / {ctx.msg.ndcId} : step {i*100}")
            await asyncio.sleep(5)

        for i in range(10):
            us = await ctx.client.get_online_users(start=i*100, size=100)
            u = list(map(lambda user: user.uid, us))
            if len(u) == 0: break
            users.extend(u)
            print(f"Inviting {len(u)} recent users to {chatId.linkInfo.objectId} / {ctx.msg.ndcId} : step {i*100}")
            await asyncio.sleep(5)

        try:
            print(f"Inviting {len(u)} users to {chatId.linkInfo.objectId} / {ctx.msg.ndcId}")
            await asyncio.sleep(5)
            await ctx.client.invite_to_chat(uids=users, chat_id=chatId.linkInfo.objectId)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return await ctx.send("Ocurrio un error al invitarlos.")

        
        return await ctx.send(f"Listo, he invitado a {len(users)} al chat.")


