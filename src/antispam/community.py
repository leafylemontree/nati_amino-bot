import asyncio
from .detectMessage import findNickname, findContent, msgType
from .n_logging import chatAnalyzeLog
import aiofile
import time
from src.subcommands.join import join_chat

CMP1 = '\n'
CMP2 = '\n\t\t'

async def chatReview(ctx, chat):
    response = []
    async for page in ctx.client.get_chat_messages_iter(chat_id=chat.threadId, size=5000):
        await asyncio.sleep(5)
        for message in page:
            t = await msgType(message.type, message.content, message.author)
            c = await findContent(message.content, ctx.msg.ndcId)
            n = await findNickname(message.author.nickname)
            
            warnings = []
            warnings.extend(t)
            warnings.extend(c)
            warnings.extend(n)
            
            try:
                response.append(f"\tid: {message.messageId} - {message.createdTime} - userId: {message.author.uid} - nickname: {message.author.nickname} && {t} : {c} : {n} ----------\n\t\t{message.content.replace(CMP1, CMP2) if message.content else None}\n\t\tResponse to: {message.extensions.replyMessageId if message.extensions.replyMessageId else 'None'}")
            except: pass

    return response


async def communityanalyze(ctx):
    
    msg = ctx.msg.content.split(" ")
    ndcId = ctx.msg.ndcId
    if len(msg) > 1:
        try: ndcId = int(msg[1])
        except: pass

    print("community:", ndcId)
    ctx.client.set_ndc(ndcId)
    
    async with aiofile.AIOFile(f'logs/logresult-{ndcId}-{int(time.time())}.txt', "a+") as f:
        await f.write(f"Log result from {int(time.time())}\nndcId: {ndcId}\n")
        chats = await ctx.client.get_public_chats(start=0, size=100)
        for chat in chats:
            await ctx.send(f"Analizando {chat.title} - {chat.threadId}")
            try:
                await join_chat(ctx, chat.threadId)
            except Exception as e:
                print(e)
                continue
            response = await chatReview(ctx, chat)
            await f.write(f"""
----------------------------------------------
threadId: {chat.threadId}
name    : {chat.title}
last_msg: {chat.latestActivityTime}
----------------------------------------------

""" + "\n\n".join(response))
            await asyncio.sleep(15)

    await ctx.send("Análisis completo")
