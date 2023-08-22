from .data import ga
from src import utils

@utils.userTracker("sala")
async def main(ctx):
    msg = ctx.msg.content.split(" ")
    if len(msg) < 2: return await ctx.send("Comando para activar la sala de juegos. Revise --help juegos para obetener ayuda.")

    com = msg[1].upper()
    if   com == "NUEVO":    await ga.createRoom(ctx)
    elif com == "UNIRSE":   await ga.joinRoom(ctx)
    elif com == "SALIR":    await ga.leaveRoom(ctx)
    elif com == "CERRAR":   await ga.closeRoom(ctx)
    elif com == "INICIAR":  await ga.start(ctx)
    return


@utils.userTracker("j")
async def turn(ctx):
    await ga.run(ctx)
