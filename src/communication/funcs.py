from .client import sc

async def send(ctx):
    msg = ctx.msg.content.split(" ")
    if len(msg) < 2: return await ctx.send("Debe añadir un mensaje tras el comando")
    msg = " ".join(msg[1:])
    
    await ctx.send(f'Enviando {msg}')
    await sc.send(msg)
