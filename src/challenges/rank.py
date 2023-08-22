from src.database import db
from src.images.expCard import getLevel
from src import utils
import asyncio
import traceback

def deleteUser(userId, ndcId):
    db.cursor.execute("DELETE FROM UserEXP WHERE userId=? AND ndcId=?", (userId, ndcId))

async def updateExpTable(ctx, ndcId):
    userExp         = db.getExpRank(ndcId)
    await ctx.send("Forzando actualización de la tabla. Esto puede tardar un minuto.")
    for user in userExp:
        try:
            userData = await ctx.client.get_user_info(user.userId)
            if userData.status == 9: deleteUser(user.userId, ndcId)
        except Exception:
            traceback.print_exc()
            #deleteUser(user.userId, ndcId)
        await asyncio.sleep(3)

@utils.userTracker("tabla-experiencia")
async def getCommunityRank(ctx):
    if ctx.msg.content.upper().find("-ACTUALIZAR") != -1: await updateExpTable(ctx, ctx.msg.ndcId)

    userExp         = db.getExpRank(ctx.msg.ndcId)
    sorted_userExp  = sorted(userExp, key=lambda x: x.exp, reverse=True)
    com             = await utils.get_community_info(ctx, ctx.msg.ndcId)
    msg             = f"[c]Este es el ranking de usuarios de esta comunidad:\n[c]{com.name}\n" 
    for i,user in enumerate(sorted_userExp):
        if i == 20: break
        nickname = await db.getUserNickname(ctx, ctx.msg.ndcId, userId=user.userId)
        msg += f"\n[c]{i + 1}. {nickname}\n[c]Nivel: {getLevel(user.exp) + 1}    - EXP: {user.exp}\n"
    
    await ctx.send(msg[:1999])
    return


@utils.userTracker("tabla-global-experiencia")
async def getGlobalRank(ctx):
    data     = db.getAllUsersExperience()
    rank     = db.getExpRankPosition(ctx.msg.author.uid)

    msg = "[c]Este es el ranking de usuarios global:\n"
    if rank : msg = f"[c]Usted está en el puesto {rank} a nivel global\n\n" + msg
    sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
    for i,user in enumerate(sorted_data):
        if i == 10: break
        nickname = await db.getUserNickname(ctx, ctx.msg.ndcId , userId=user[0])
        msg += f"\n[c]{i + 1}. {nickname}\n[c]Nv: {getLevel(float(user[1])) + 1} - EXP: {user[1]}\n"

    await ctx.send(msg[:1999])
    return

