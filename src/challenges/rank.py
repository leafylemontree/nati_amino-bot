from src.database import db
from src.images.expCard import getLevel
from src import utils

async def getCommunityRank(ctx):
    userExp         = db.getExpRank(ctx.msg.ndcId)
    sorted_userExp  = sorted(userExp, key=lambda x: x.exp, reverse=True)
    com             = await utils.get_community_info(ctx, ctx.msg.ndcId)
    msg             = f"[c]Este es el ranking de usuarios de esta comunidad:\n[c]{com.name}\n" 
    for i,user in enumerate(sorted_userExp):
        if i == 20: break
        nickname = await db.getUserNickname(ctx, ctx.msg.ndcId, userId=user.userId)
        msg += f"\n[c]{i + 1}. {nickname}\n[c]Nivel: {getLevel(user.exp) + 1}    - EXP: {user.exp}\n"

    
    await ctx.send(msg)
    return
