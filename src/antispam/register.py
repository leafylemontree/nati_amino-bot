from src.database import db
from src.objects import ba

async def messageRegister(ctx):
    content = str(ctx.msg.content).replace('"', '')
    db.cursor.execute(f'INSERT INTO MessageHistory VALUES ("{ctx.msg.author.uid}", NOW(), {ba.instance + 1}, "{content}");')
    return
