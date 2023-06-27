from src.database import db
from src.objects import ba
from src.images.expCard import getLevel, getExpLevel, expCardCreate
import math


async def triggerLevelUp(ctx, level):
    from src.challenges.rewards import donateAC
    print(ctx.msg.ndcId, ctx.msg.author.uid, level, ctx.msg.author.nickname)
    await expCardCreate(ctx)
    await donateAC(ctx, ctx.msg.author.uid, (level * 5), silent=True)
    

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

async def messageRegister(ctx):
    if ctx.msg.author is None: return
    
    await nicknameSave(ctx.msg.ndcId, ctx.msg.author.uid, ctx.msg.author.nickname)
    await petMessageRegister(ctx.msg.ndcId)

    c = await userMessageCounter(ctx.msg.ndcId, ctx.msg.author.uid)
    await userExpSave(ctx, ctx.msg.ndcId, ctx.msg.author.uid, c)
    db.cursor.execute(f'INSERT INTO MessageHistory VALUES (?, NOW(), {ba.instance + 1}, ?);', (ctx.msg.author.uid, ctx.msg.content))
    return
