from .detectMessage import findNickname, findContent, msgType
from .n_logging import chatAnalyzeLog
from asyncio import sleep

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


