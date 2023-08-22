from src import utils
from src import objects
import time

async def get_notices(ctx, start=0, size=25):
    resp = await ctx.client.request("GET", f"notice?type=usersV2&status=1&start={start}&size={size}")
    return tuple(map(lambda notice: objects.Notice(**notice), resp['noticeList']))


@utils.isStaff
@utils.userTracker("aceptarrol")
async def accept_role(ctx):
    notices = await get_notices(ctx, start=0, size=100)
    noticeType  = None
    noticeId    = None

    try:
        for notice in notices:
            if notice.type not in [1,2,3] : continue
            # 1: Leader. 2: Curator. 3: Agent
            noticeId    = notice.noticeId
            noticeType  = notice.type
        if not noticeId: return await ctx.send("No hay puestos pendientes que aceptar")
        data = {'timestamp': int(time.time() * 1000)}
        request = await ctx.client.request("POST", f"notice/{noticeId}/accept", json=data)
        role    = 'líder' if noticeType == 1 else 'curador' if noticeType == 2 else 'agente'
        await ctx.send(f"Puesto de {role} aceptado.")
    except Exception as e:
        await ctx.send(f"Ha ocurrido un error: {e}")
        print(e)
    
    return


