from src import utils
from src.database import db

@utils.checkFor(m=1, M=1000, notcount=2)
async def register(ctx, args):
    comId  = ctx.msg.ndcId
    userId = ctx.msg.author.uid
    _time  = int(args.pop(0))
    msg    = " ".join(args)
    print(msg)
    print(args)

    db.cursor.execute(f'SELECT * FROM Countdown WHERE userId="{userId}";')
    data = db.cursor.fetchall()
    _id = len(data[0]) if data != [] else 0

    db.cursor.execute(f'INSERT INTO Countdown VALUES ({_id+1}, "{userId}", {comId}, NOW(), {_time}, "{msg}" );')
    return await ctx.send("Temporizador agregado con ID: " + str(_id+1))

@utils.checkFor(m=1, M=1000, notcount=2)
async def remove(ctx, msg):
    db.cursor.execute(f'SELECT * FROM Countdown WHERE userId="{userId}";')
    data = db.cursor.fetchall()
    _id = len(data[0]) if data != [] else 0

    if _id == 0: return await ctx.send("Usted no tiene temporizadores ejecutandose")
    try:
        db.cursor.execute(f'DELETE FROM Countdown WHERE userId="{userId}" AND ID={int(msg[0])};')
        return await ctx.send("Temporizador eliminado")
    except:     
        return await ctx.send("Ha ocurrido un error")
    return

@utils.checkFor(m=0, M=1000, notcount=2)
async def view(ctx, msg):
    userId = ctx.msg.author.uid
    if len(msg) > 0: db.cursor.execute(f'SELECT * FROM Countdown WHERE userId="{userId}" AND ID={int(msg[0])};')
    else: db.cursor.execute(f'SELECT * FROM Countdown WHERE userId="{userId}";')

    data = db.cursor.fetchall()
    if data == []: return await ctx.send("Usted no posee temporizadores ejecutandose, o la ID ingresada no existe")
    
    fmsg = "Temporizadores de " + ctx.msg.author.nickname
    for timer in data:
        fmsg += f"""
---------------------------

ID: {timer[0]}
Creado: {timer[3]}
Tiempo: {timer[4]}
Mensaje: {timer[5][:200]}
"""

    return await ctx.send(fmsg)



@utils.checkFor(m=1, M=1000)
async def main(ctx, msg):
    
    if msg[0].upper() == "-SET":        await register(ctx)
    if msg[0].upper() == "-REMOVE":     await remove(ctx)
    if msg[0].upper() == "-VIEW":       await view(ctx)
    
    return await ctx.send(str(msg))


