from .data  import AS
from src    import utils
from src    import objects
import json
from edamino.api import Embed
import datetime

@utils.isStaff
async def set_logging(ctx):
    AS.logging_chat[str(ctx.msg.ndcId)] = ctx.msg.threadId
    with open("data/com_chatlist.json", "w+") as chatFile:
        json.dump(AS.logging_chat, chatFile, indent=4)
        print(AS.logging_chat)
    return "El chat para el log del bot ha sido cambiado con éxito"

async def register_user(comId, userId):
        
        if comId not in AS.last_user.keys(): AS.last_user[comId] = [
                                                                [None, None],
                                                                [None, None],
                                                                [None, None]
                                                            ]
        
        AS.last_user[comId].pop(0)
        AS.last_user[comId].append([userId,
                                    int(datetime.datetime.now().timestamp())
                                    ])

        print(AS.last_user)


        if AS.last_user[comId][1] == [None, None]: return False
        dif = (AS.last_user[comId][2][1] - AS.last_user[comId][1][1])
        print("Time difference:", dif)

        if (AS.last_user[comId][2][0] != AS.last_user[comId][1][0]): return False
        if (dif > 30):  return False
        return True

async def banUser(ctx, userId, ndcId):
    chatId = None
    if str(ndcId) in AS.ban_no_warn.keys():
        chatId = AS.ban_no_warn[str(ndcId)]
    else: return

    try:
        await ctx.client.ban(
                        user_id=ctx.msg.author.uid,
                        reason=f"Baneado automáticamente por razones: {msg_type}"
                        )
        user = await ctx.client.get_user_info(user_id=uid)
        await ctx.client.send_message(message=f"""
Se ha baneado a {user.nickname}
Motivo: {msg_type}
ID: {uid}
----------
Para desbanear, solo responda este mensaje y ponga --unban
""",
                                    chat_id=chatId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None )
        return True
    except Exception:
        user = await ctx.client.get_user_info(user_id=userId)
        if user.role != 102: await ctx.send("Ha activado el modo de expulsar sin advertencia, sin embargo, el bot no posee del cargo de líder, por lo que no puede expulsar.\n\nPuede desactivar este mensaje desactivando el modo con este comando:\n--log -normal")
    return

async def sendLog(ctx, warnings):
    thread = await ctx.get_chat_info()
    comId  = str(ctx.msg.ndcId)

    try:
        await ctx.client.delete_message(
                chat_id=ctx.msg.threadId,
                message_id=ctx.msg.messageId)
        await ctx.client.kick_from_chat(ctx.msg.threadId, ctx.msg.uid, allow_rejoin=True)
    except Exception:
        pass
            
    chat = None
    if comId in AS.logging_chat.keys(): chat = AS.logging_chat[comId]
    else:                               return
    print(comId, AS.logging_chat[comId])

    if await register_user(ctx.msg.ndcId, ctx.msg.author.uid) : return
    if int(comId) in AS.ban_no_warn: await banUser(ctx, ctx.msg.author.uid. ctx.msg.ndcId)
    
    base_msg = f"""Posible amenaza detectada:
------------------
Nick: {ctx.msg.author.nickname}
ID: {ctx.msg.author.uid}
Chat: {thread.title}
Tipo: {ctx.msg.type}
Mensaje:
{ctx.msg.content}
-----------------"""
    
    for i in warnings:
                base_msg += f"\n- {i}: {objects.AntiSpam.msg_desc[i]}"
                if i in ["1", "2", "3"]: objects.botStats.register(3)
                if i in ["101", "102", "103", "104"]: objects.botStats.register(4)
                if i in ["200"]: objects.botStats.register(5)
                print(f"{i} - {objects.AntiSpam.msg_desc[i]}")
            
    embed = Embed(title="Perfil del usuario", object_type=0, object_id=ctx.msg.author.uid, content=ctx.msg.author.nickname )

    await ctx.client.send_message(message=base_msg,
                                    chat_id=chat,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=embed,
                                    link_snippets_list=None,
                                    reply=None )

    return True

async def wallLog(ctx, user, warnings):
    st_str = f"""
Nati Stalk v0.2
---------------------------
Usuario encontrado potencialmente rompiendo las normas
Usuario analizado: {user.nickname}
ID: {user.uid}
Rzones:"""
    s1, s2, s3, s4 = warnings[0], warnings[1], warnings[2], warnings[3]

    if s1: st_str += f'\n-- Nombre de perfil --\n{s1}: {objects.AntiSpam.msg_desc[str(s1)]}'
    if s2: st_str += f"\n-- Comentarios del muro --\n"
    for key,value in s2.items():
        if key in objects.alreadyChecked: continue
        if key not in objects.alreadyChecked: objects.alreadyChecked.append(key)
        u = await ctx.client.get_user_info(key)
        st_str += f'\nUsuario: {u.nickname}\n{value[0]}: {objects.AntiSpam.msg_desc[str(value[0])]}\ncontenido: {value[1][:500]}\n'

        print(st_str)
        embed = Embed(
            title='Revisar este perfil',
            object_type=0,
            object_id=l.uid,
            content=l.nickname
        )
        await ctx.client.send_message(message=st_str[:2000],
                                    chat_id=AS.logging_chat[str(user.ndcId)],
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=embed,
                                    link_snippets_list=None,
                                    reply=None )
        print("Message sent")
    return
