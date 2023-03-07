import time
import asyncio
from src import utils

async def join_community(ctx, ndcId: int, invitationId: str = None):
    data = {"timestamp" : int(time.time() * 1000)}     
    response = await ctx.client.request(
            "POST",
            f"https://service.narvii.com/api/v1/x{ndcId}/s/community/join",
            full_url=True,
            json=data
            )
    return 


async def leave_community(ctx, ndcId: int, invitationId: str = None):
    data = {"timestamp" : int(time.time() * 1000)}     
    response = await ctx.client.request(
            "POST",
            f"https://service.narvii.com/api/v1/x{ndcId}/s/community/leave",
            full_url=True,
            json=data
            )
    return 


@utils.isStaff
async def newCommunity(ctx):
    text = ctx.msg.content.split(" ")
    if len(text) == 1:      return await ctx.send("Debe poner el link de una comunidad")

    link = text[1]
    if link.find("aminoapps") == -1:    return await ctx.send("El link ingresado no es válido")
    linkInfo        = await ctx.client.get_info_link(link=link)

    if hasattr(linkInfo, 'community') and linkInfo.community is not None:
        ndcId = linkInfo.community.ndcId
        await ctx.send(f"El ndcId del link ingresado es: {str(ndcId)}")

        try:
            await join_community(ctx, ndcId=ndcId)
            await ctx.send(f"Unido a la comunidad {linkInfo.community.name}")
        except Exception as e:
            await ctx.send("Error al unir a la comunidad")
            return
        
        baseNdc = ctx.msg.ndcId
        ctx.client.set_ndc(ndcId)
        baseLink = await ctx.client.get_from_id(object_id=ctx.client.uid, object_type=0)
        ctx.client.set_ndc(baseNdc)
        await ctx.send(str(baseLink.shareURLShortCode))
        
    else:
        await ctx.send("El link ingresado no es de una comunidad")


@utils.isStaff
async def removeCommunity(ctx):
    text = ctx.msg.content.split(" ")
    if len(text) == 1:      return await ctx.send("Debe poner el link de una comunidad")

    link = text[1]
    if link.find("aminoapps") == -1:    return await ctx.send("El link ingresado no es válido")
    linkInfo        = await ctx.client.get_info_link(link=link)

    if hasattr(linkInfo, 'community') and linkInfo.community is not None:
        ndcId = linkInfo.community.ndcId
        await ctx.send(f"El ndcId del link ingresado es: {str(ndcId)}")

        try:
            await leave_community(ctx, ndcId=ndcId)
            await ctx.send(f"Removido de la comunidad {linkInfo.community.name}")
        except Exception as e:
            await ctx.send("Error al salir a la comunidad")
            return
    else:
        await ctx.send("El link ingresado no es de una comunidad")
