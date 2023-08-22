from src.database import db
from src.challenges.rewards import donate_blog, donate_wiki
from src.shop.interface import add_item
from src          import utils

@utils.userTracker("reclamar-recompensas")
async def claimRewards(ctx):
    rewards = db.getUserRewards(ctx.msg.author.uid, ctx.msg.ndcId)
    if len(rewards) == 0: return await ctx.send("No tiene recompensas pendientes por reclamar.")

    ACdonation = False
    objectId   = None
    objectType = None
    for reward in rewards:
        if reward.type == 0: ACdonation = True

    if ACdonation:
        words = ctx.msg.content.split(" ")
        if len(words) < 2: return await ctx.send("Hay una recompensa en AC. Debe colocar un link tras el comando de un blog donde se pueda donar.")
        link = words[1]
        linkInfo    = await ctx.client.get_info_link(link=link)
        objectId    = linkInfo.linkInfo.objectId
        objectType  = linkInfo.linkInfo.objectType

    if objectId is None or objectType is None: return await ctx.send("El link ingresado no es apto para donar.")

    for reward in rewards:
        if   reward.type == 0:
            if   objectType == 1: r = await donate_blog(ctx, None, reward.amount, objectId)
            elif objectType == 2: r = await donate_wiki(ctx, None, reward.amount, objectId)
            else                : return await ctx.send("El link ingresado no es de un blog o wiki.")
            if r is False       : return await ctx.send("El blog o wiki ingresado no es válido para donar.")
            await ctx.send(f"Han sido donados {reward.amount} AC exitosamente.")
        
        elif reward.type == 1:
            db.modifyRecord(44, None, reward.amount, userId=reward.userId)
            await ctx.send(f"Añadidos {reward.amount} puntos de actividad a {ctx.msg.author.nickname}.")

        elif reward.type == 2:
            r = await add_item(objectId=reward.itemId, amount=reward.amount, userId=ctx.msg.author.uid, saveItem=False)
            if r is not True: return await ctx.send("Hay un problema al reclamar un item. Asegure que el inventario no esté lleno.")

        db.removeUserRewards((reward.rewardId, ))

    return


    



        
