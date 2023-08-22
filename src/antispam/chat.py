from .detectMessage import findNickname, findContent, msgType
from .n_logging import chatAnalyzeLog
from asyncio import sleep
from src.database import db
from src import objects
from src.subcommands._math.rate import rt
import math
from src import utils

@utils.userTracker("chatanalyze")
async def chatAnalyze(ctx):
    m = 0
    userList = []
    strange = 0
    msg = ctx.msg.content.upper().split(" ")
    
    l = msg[1] if len(msg)>1 else '2500'
    try                 : l = int(l)
    except ValueError   : l = 2500

    await ctx.send(f"Analizando el chat, espere un momento.\nAnalizando {l} mensajes.") 
    async for page in ctx.client.get_chat_messages_iter(chat_id=ctx.msg.threadId, size=l):
        await sleep(3)
        for message in page:
            t = await msgType(message.type, message.content, message.author)
            c = await findContent(message.content, ctx.msg.ndcId)
            n = await findNickname(message.author.nickname)
            
            warnings = []
            warnings.extend(t)
            warnings.extend(c)
            warnings.extend(n)

            m += 1
            if (t or c or n):
                strange += 1
                if message.author.uid not in userList:
                    await chatAnalyzeLog(ctx, message, warnings)
                    userList.append(message.author.uid)
                
    await ctx.send(f"""
¡Analisis completado!
------------------------
Analizados: {l} mensajes
Encontradas: {strange} incidencias
Usuarios: {len(userList)}
""")
    return

async def checkIfNewChat(ctx):
    threadId    = ctx.msg.threadId
    ndcId       = ctx.msg.ndcId
   
    data = db.getChatConfig(threadId, ndcId, exists=True)
    if data is not None: return
    data = db.getChatConfig(threadId, ndcId)

    message_amount  = 0
    message_bad     = 0
    message_value   = 0

    await sleep(5)

    userList = []
    async for page in ctx.client.get_chat_messages_iter(threadId, size=100):
        for message in page:
            message_amount += 1
            warning_type    = await msgType(message.type, message.content, message.author)
            warning_content = await findContent(message.content, ctx.msg.ndcId)
            warning_nick    = await findNickname(message.author.nickname)
            
            warnings = []
            warnings.extend(warning_type)
            warnings.extend(warning_content)
            warnings.extend(warning_nick)

            if message.content is not None:
                value = rt.rate(message.content, len(message.content))
                score = math.sin(value)
                score = (2/((math.e ** score) + (math.e ** -score)))**2
                message_value += score

            if warnings:
                message_bad += 1
                if message.author.uid not in userList:
                    await chatAnalyzeLog(ctx, message, warnings, auto=True)
                    userList.append(message.author.uid)
                
    if message_amount == 0: message_amount = 1
    rate    = message_bad/message_amount
    status  = None
    if   rate > 0.75 : status = "Muy malo.\nHay demasiadas incidencias dentro del chat para hacerlo adecuado"
    elif rate > 0.5  : status = "Malo.\nHay un gran número de incidencias"
    elif rate > 0.25 : status = "Regular.\nBastantes malhechores todavía"
    elif rate > 0.1  : status = "Aceptable.\nBaja cantidad de incidencias, aunque todavía bastantes"
    elif rate > 0.05 : status = "Bueno.\nNati ha encontrado pocas incidencias en este chat"
    elif rate > 0    : status = "Muy bueno.\nHay uno o dos mensajes problemáticos solamente"
    elif rate == 0   : status = "Excelente.\nNada que reportar"
    else             : status = f"Desconodido - {rate}"

    try: await ctx.send(f"""
Nati ha analizado este chat
------------------------
Analizados: {message_amount} mensajes
Encontradas: {message_bad} incidencias
Usuarios : {len(userList)}
Puntuación de la conversación: {(message_value * 10/message_amount):.2}/10

Este chat está valorado como: {status}""")
    except Exception as e:
        pass

    print('New chat created')
    

