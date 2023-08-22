from src import utils
from src.database import db

@utils.userTracker("mensajes-historial")
@utils.userId
async def messageHistory1(ctx, userId, msg):
    ndcId       = ctx.msg.ndcId
    threadId    = ctx.msg.threadId
    user        = await ctx.client.get_user_info(userId)
    messages    = db.getLastMessages(ndcId, threadId, userId)
    msg         = f"Estos son los últimos mensajes de {user.nickname}:\n\n"
    for m in messages: msg += f"{m.content}\n"
    await ctx.send(msg[:1999])
    return


@utils.userTracker("mensajes-borrados")
@utils.userId
async def messageHistory2(ctx, userId, msg):
    ndcId       = ctx.msg.ndcId
    threadId    = ctx.msg.threadId
    user        = await ctx.client.get_user_info(userId)
    messages    = db.getDeletedMessages(ndcId, threadId, userId)
    msg         = f"Estos son los últimos mensajes eliminados de {user.nickname}:\n\n"
    for m in messages: msg += f"{m.content}\n"
    await ctx.send(msg[:1999])
    return

@utils.userTracker("mensajes-borrados-chat")
async def messageHistory3(ctx):
    ndcId       = ctx.msg.ndcId
    threadId    = ctx.msg.threadId
    messages    = db.getDeletedChatMessages(ndcId, threadId)
    msg         = f"Estos son los últimos mensajes eliminados del chat:\n\n"
    for m in messages: msg += f"{m.content}\n"
    await ctx.send(msg[:1999])
    return

