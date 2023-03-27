from src.database import db
from src.objects import ba

async def messageRegister(ctx):
    if ctx.msg.author is None: return
    db.cursor.execute(f'INSERT INTO MessageHistory VALUES (?, NOW(), {ba.instance + 1}, ?);', (ctx.msg.author.uid, ctx.msg.content))
    return
