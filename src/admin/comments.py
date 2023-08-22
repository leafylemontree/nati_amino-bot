from src.subprocess.test import get_my_communities
from src.antispam import get_wall_comments
import asyncio
from src import utils

async def delete_comment(ctx, commentId, userId):
     resp = await ctx.client.request("DELETE", f"user-profile/{userId}/comment/{commentId}")
     return

@utils.isStaff
@utils.userTracker("eliminarcomentarios")
async def deleteComments(ctx):

    await ctx.send("Eliminando comentarios...")
    ndcId = ctx.msg.ndcId

    #coms = await get_my_communities(ctx, start=0, size=100)
    #comList = list(map(lambda com: com.ndcId, coms))
    comList = [ndcId, 92]

    for i,com in enumerate(comList):
                
        await asyncio.sleep(5)
        ctx.client.set_ndc(com)

        count = 0
        errored = 0
        for j in range(10):
            users = await ctx.client.get_all_users(users_type='recent', start=j * 100, size=100)
            for user in users:

                comments = await get_wall_comments(ctx, user_id=user.uid, sorting='oldest', start=0, size=100)
                for comment in comments:
                    
                    try:
                        if comment.author.uid == ctx.client.uid:
                            await delete_comment(ctx, comment.commentId, user.uid)
                            count += 1
                    except:
                        errored += 1
       
        ctx.client.set_ndc(ndcId)
        await ctx.send(f'Eliminados {count} comentarios de la comunidad {com}\nHan habido: {errored} errores')





