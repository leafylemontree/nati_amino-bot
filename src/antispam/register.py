from src.database import db
from src.objects import ba

async def messageRegister(ctx):
    if ctx.msg.author is None: return
    db.redis.hset(db.r_userNickname, f'?{ctx.msg.ndcId}&{ctx.msg.author.uid}', f'{ctx.msg.author.nickname}')
    if not db.redis.hexists(db.r_messageCom, f"?{ctx.msg.ndcId}"):
        db.redis.hset(db.r_messageCom, f"?{ctx.msg.ndcId}", (0).to_bytes(4, 'big'))

    msg = db.redis.hget(db.r_messageCom, f"?{ctx.msg.ndcId}")
    msg = int.from_bytes(msg, 'big')
    msg += 1
    db.redis.hset(db.r_messageCom, f"?{ctx.msg.ndcId}", msg.to_bytes(4, 'big'))

    db.cursor.execute(f'INSERT INTO MessageHistory VALUES (?, NOW(), {ba.instance + 1}, ?);', (ctx.msg.author.uid, ctx.msg.content))
    return
