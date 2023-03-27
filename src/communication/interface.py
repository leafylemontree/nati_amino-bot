from .client            import sc
from .listener          import socketPool
from src.communication  import protocol
from src                import objects
import json
import time
import asyncio

async def get_communities(ctx):

    await ctx.send('Obteniendo información de comunidades. Espere un momento')

    content = {'objectId': 0, 'value': 0}
    nodeId = socketPool.register(data=None, length=3, timeout=10)
    await sc.send(
            dtype=1,
            request=content,
            destinatary=-1,
            nodeId=nodeId
        )

    node = await socketPool.retrieve(nodeId)
    msg = 'Esta es la respuesta que han dado todas las Nati:\n\n'
    for data in node.data:
        instance = data.instance
        comNum   = len((json.loads(data.content.data))['comList'])
        msg     += f'Nati {instance}\n-----------\nComunidades: {comNum}\n\n' 

    await ctx.send(msg)
    return

async def get_wallets(ctx):

    await ctx.send('Obteniendo información de monederos. Espere un momento')

    content = {'objectId': 1, 'value': 0}
    nodeId = socketPool.register(data=None, length=3, timeout=10)
    await sc.send(
            dtype=1,
            request=content,
            destinatary=-1,
            nodeId=nodeId
        )

    node = await socketPool.retrieve(nodeId)
    msg = 'Esta es la respuesta que han dado todas las Nati:\n\n'
    for data in node.data:
        instance = data.instance
        coins    = (json.loads(data.content.data))['coins']
        msg     += f'Nati {instance}\n-----------\nMonedas: {coins}\n\n' 

    await ctx.send(msg)
    return

async def get_activity(ctx):

    await ctx.send('Obteniendo información de actividad de Nati. Espere un momento')

    content = {'objectId': 2, 'value': 0}
    nodeId = socketPool.register(data=None, length=3, timeout=10)
    await sc.send(
            dtype=1,
            request=content,
            destinatary=-1,
            nodeId=nodeId
        )

    node = await socketPool.retrieve(nodeId)
    msg = 'Esta es la respuesta que han dado todas las Nati:\n\n'
    for data in node.data:
        instance = data.instance
        status   = (json.loads(data.content.data))['status']
        msg     += f'Nati {instance}\n-----------\nEstado: {status}\n\n' 

    await ctx.send(msg)
    return
