from .data  import AS
from src    import utils
from src    import objects
import json
from edamino.api import Embed
import datetime
from src.database import db

@utils.isStaff
async def set_logging(ctx):
    db.setLogConfig(ctx.msg.ndcId, 'threadId', ctx.msg.threadId)
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

async def banUser(ctx, userId, ndcId, reasons):
    log = db.getLogConfig(ndcId)
    if not log.ban: return
    chatId = log.threadId
    try:
        await ctx.client.ban(
                        user_id=userId,
                        reason=f"Baneado automáticamente por razones: {reasons}"
                        )
        user = await ctx.client.get_user_info(user_id=userId)
        await ctx.client.send_message(message=f"""
Se ha baneado a {user.nickname}
Motivo: {reasons}
ID: {userId}
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
    chat = None
    log = db.getLogConfig(ctx.msg.ndcId)
    db.registerReport(ctx.msg.author.uid, ctx.msg.ndcId, ctx.msg.threadId, warnings)
    if log.threadId: chat = log.threadId
    if log.ban:
        try:                await ctx.client.kick_from_chat(ctx.msg.threadId, ctx.msg.uid, allow_rejoin=True)
        except Exception:   pass

    if await register_user(ctx.msg.ndcId, ctx.msg.author.uid) : return
    if log.ban: await banUser(ctx, ctx.msg.author.uid, ctx.msg.ndcId, str(warnings))
    
    base_msg = f"""Posible amenaza detectada:
------------------
Nick: {ctx.msg.author.nickname}
ID: {ctx.msg.author.uid}
Chat: {ctx.msg.threadId}
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
                                    chat_id=log.threadId,
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
        log = db.getLogConfig(int(ctx.client.ndc_id.replace("x", "")))
        await ctx.client.send_message(message=st_str[:2000],
                                    chat_id=log.threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=embed,
                                    link_snippets_list=None,
                                    reply=None )
        print("Message sent")
    return

async def chatAnalyzeLog(ctx, message, warnings):
    log = db.getLogConfig(ctx.msg.ndcId)
    db.registerReport(ctx.msg.author.uid, ctx.msg.ndcId, ctx.msg.threadId, warnings)
    chat = log.threadId if log.threadId else ctx.msg.threadId
    
    if log.ban:
        try:    
                await ctx.client.kick_from_chat(ctx.msg.threadId, ctx.msg.uid, allow_rejoin=True)
                await banUser(ctx, ctx.msg.author.uid, ctx.msg.ndcId, str(warnings))
        except Exception:
                pass
    
    embed = Embed(title="Perfil del usuario", object_type=0, object_id=message.author.uid, content=message.author.nickname)
    base_msg=f"""
Análisis de chat manual
------------------
Nick: {message.author.nickname}
ID: {message.author.uid}
Chat: {ctx.msg.threadId}
Tipo: {message.type}
Mensaje:
{message.content}
-----------------"""
    await ctx.client.send_message(message=base_msg,
                                    chat_id=chat,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=embed,
                                    link_snippets_list=None,
                                    reply=None )
    return

