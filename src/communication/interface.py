from .client            import sc
from .listener          import socketPool
from src.communication  import protocol
from src                import objects
import ujson as json
import time
import asyncio
from src import utils

instances = 5

@utils.userTracker("socketcom")
async def get_communities(ctx):

    await ctx.send('Obteniendo información de comunidades. Espere un momento')

    content = {'objectId': 0, 'value': 0}
    nodeId = socketPool.register(data=None, length=instances, timeout=10)
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
        msg     += f'Nati {instance + 1}\n-----------\nComunidades: {comNum}\n\n' 

    await ctx.send(msg)
    return

@utils.userTracker("socketwallet")
async def get_wallets(ctx):

    await ctx.send('Obteniendo información de monederos. Espere un momento')

    content = {'objectId': 1, 'value': 0}
    nodeId = socketPool.register(data=None, length=instances, timeout=10)
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
        msg     += f'Nati {instance + 1}\n-----------\nMonedas: {coins}\n\n' 

    await ctx.send(msg)
    return

@utils.userTracker("socketactivity")
async def get_activity(ctx):

    await ctx.send('Obteniendo información de actividad de Nati. Espere un momento')

    content = {'objectId': 2, 'value': 0}
    nodeId = socketPool.register(data=None, length=instances, timeout=10)
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
        msg     += f'Nati {instance + 1}\n-----------\nEstado: {status}\n\n' 

    await ctx.send(msg)
    return


@utils.userTracker("isinstance")
async def is_instance_in(ctx):
    text = ctx.msg.content.split(" ")
    if len(text) == 1:      return await ctx.send("Debe poner el link de una comunidad")

    link = text[1]
    if link.find("aminoapps") == -1:    return await ctx.send("El link ingresado no es válido")
    linkInfo        = await ctx.client.get_info_link(link=link)

    if hasattr(linkInfo, 'community') and linkInfo.community is not None:
        ndcId = linkInfo.community.ndcId
        name  = linkInfo.community.name
    else:
        await ctx.send("El link ingresado no es de una comunidad")

    await ctx.send('Obteniendo información de comunidades. Espere un momento')

    content = {'objectId': 0, 'value': 0}
    nodeId = socketPool.register(data=None, length=instances, timeout=10)
    await sc.send(
            dtype=1,
            request=content,
            destinatary=-1,
            nodeId=nodeId
        )

    node = await socketPool.retrieve(nodeId)
    msg = f'Se ha encontrado la comunidad {name} (ndcId={ndcId}) en:\n\n'
    for data in node.data:
        instance = data.instance
        coms   = json.loads(data.content.data)['comList']
        if ndcId in coms: msg += f'Nati {instance + 1}\n' 

    await ctx.send(msg)
    return

