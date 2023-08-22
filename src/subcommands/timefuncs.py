from src import utils
import time
import datetime
import asyncio

async def stopTime(ctx, aw):
    initTime = aw.data
    delta = datetime.datetime.now() - aw.data
    await ctx.send(f"¡Cronómetro detenido!\nHan pasado {int(delta.total_seconds())} segundos")


@utils.waitForMessage("-detener", callback=stopTime)
@utils.userTracker("cronometro")
async def stopwatch(ctx):
    date = datetime.datetime.now()
    await ctx.send(f"Temporizador puesto por {ctx.msg.author.nickname}:\n{date}")
    return date


@utils.userTracker("temporizador")
async def timer(ctx):
    com = ctx.msg.content.upper().split()

    waitTime = None
    if len(com) > 1:
        try     :   waitTime = int(com[1])
        except  :   pass

    message = ""
    if (len(com) > 1) and (waitTime is None):
        message = ctx.msg.content.split(" ")[1:]
        message = " ".join(message)
    elif (len(com) > 2) and waitTime:
        message = ctx.msg.content.split(" ")[2:]
        message = " ".join(message)

    if waitTime is None  : waitTime = 60
    w = "[c]---------------------------"

    await ctx.send(f"Se ha programado un mensaje para dentro de {waitTime} segundos")
    await asyncio.sleep(waitTime)
    await ctx.send(f"{w}\n[c]{message}\n{w}")

    return

