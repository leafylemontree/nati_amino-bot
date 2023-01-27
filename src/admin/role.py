import json
from src import utils

@utils.isStaff
async def accept_role(ctx):

    request     = await ctx.client.request("GET", "notice?type=usersV2&status=1&start=0&size=100")
    noticeType  = None
    noticeId    = None

    for notice in request['noticeList']:
        if notice['type'] not in [1,2,3] : continue
        # 1: Leader. 2: Curator. 3: Agent
        noticeId    = notice['noticeId']
        noticeType  = notice['type']
    if not noticeId: return await ctx.send("No hay puestos pendientes que aceptar")

    request = await ctx.client.request("POST", f"notice/{noticeId}/accept")
    role    = 'líder' if noticeType == 1 else 'curador' if noticeType == 2 else 'agente'
    await ctx.send(f"Puesto de {role} aceptado.")
    return
