from src.database import db
from src.objects import ba
from src.images.expCard import getLevel, getExpLevel, expCardCreate
import math


async def triggerLevelUp(ctx, level):
    from src.challenges.rewards import donateAC
    await expCardCreate(ctx)
    if level < 21:
        await donateAC(ctx, ctx.msg.author.uid, (level * 5), silent=True)
    elif level > 20 and (level % 5) == 0:
        await donateAC(ctx, ctx.msg.author.uid, 100, silent=True)
    return

async def petMessageRegister(ndcId):
    if not db.redis.hexists(db.r_messageCom, f"?{ndcId}"):
        db.redis.hset(db.r_messageCom, f"?{ndcId}", (0).to_bytes(4, 'big'))
    msg  = db.redis.hget(db.r_messageCom, f"?{ndcId}")
    msg  = int.from_bytes(msg, 'big')
    msg += 1
    db.redis.hset(db.r_messageCom, f"?{ndcId}", msg.to_bytes(4, 'big'))
    return

async def nicknameSave(ndcId, userId, nickname):
    db.redis.hset(db.r_userNickname, f'?{ndcId}&{userId}', f'{nickname}')
    return

async def userMessageCounter(ndcId, userId):
    label = f"?{ndcId}&{userId}"
    if not db.redis.hexists(db.r_userMsgCounter, label):
        db.redis.hset(db.r_userMsgCounter, label, (0).to_bytes(4, 'big'))

    raw      = db.redis.hget(db.r_userMsgCounter, label)
    counter  = int.from_bytes(raw, 'big')
    counter += 1
    db.redis.hset(db.r_userMsgCounter, label, counter.to_bytes(4, 'big'))
    return counter

async def userExpSave(ctx, ndcId, userId, counter):
    label = f"?{ndcId}&{userId}"

    if not db.redis.hexists(db.r_userExp, label):
        exp = db.getUserExp(ndcId, userId)
        db.redis.hset(db.r_userExp, label, (exp).to_bytes(4, 'big'))

    raw      = db.redis.hget(db.r_userExp, label)
    oldExp   = int.from_bytes(raw, "big")
    newExp   = int.from_bytes(raw, 'big') + counter

    oldLevel = getLevel(oldExp)
    newLevel = getLevel(newExp)
    
    if newLevel > oldLevel:
        db.getUserExp(ndcId, userId)
        await triggerLevelUp(ctx, newLevel)
    return


async def messageCopy(ctx):
    ndcId       = ctx.msg.ndcId
    threadId    = ctx.msg.threadId
    userId      = ctx.msg.author.uid
    messageId   = ctx.msg.messageId

    message     = db.getChatMessage(ndcId, threadId, userId, messageId)
    if message is None: return
    db.cursor.execute("INSERT INTO DeletedMessageHistory VALUES (?, ?, ?, ?, ?, NOW(), ?)", (ndcId, threadId, userId, messageId, message.instance, message.content))
    db.cursor.execute("DELETE FROM MessageHistory WHERE ndcId=? AND threadId=? AND userId=? AND messageId=?", (ndcId, threadId, userId, messageId))
    return

async def messageRegister(ctx):
    if ctx.msg.author is None: return
    
    await nicknameSave(ctx.msg.ndcId, ctx.msg.author.uid, ctx.msg.author.nickname)
    await petMessageRegister(ctx.msg.ndcId)

    c = await userMessageCounter(ctx.msg.ndcId, ctx.msg.author.uid)
    await userExpSave(ctx, ctx.msg.ndcId, ctx.msg.author.uid, c)
    if ctx.msg.type == 100: return await messageCopy(ctx)

    db.cursor.execute(f'INSERT INTO MessageHistory VALUES (?, ?, ?, ?, {ba.instance + 1}, NOW(), ?);', (ctx.msg.ndcId, ctx.msg.threadId, ctx.msg.author.uid, ctx.msg.messageId, ctx.msg.content))
    return
