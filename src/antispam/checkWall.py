from src import utils
from src import objects
from .detectMessage import findNickname, findContent 

async def get_wall_comments(ctx, user_id=None, sorting="oldest", start=0, size=25):
        if sorting not in ["oldest", "newest"]: return None
        response = await ctx.client.request('GET', f"user-profile/{user_id}/comment?sort={sorting}&start={start}&size={size}")
        return tuple(map(lambda comment : objects.WallComment(**comment), response['commentList'] ))

@utils.userId
async def check_wall(ctx, uid, msg):

        user = await ctx.client.get_user_info(uid)
        print("uid:", uid)
        print("item.count:", user.commentsCount)
        
        sus_users = []
        for a in range( int(user.commentsCount / 100) + 1):
            c = await get_wall_comments(ctx, user_id=uid, sorting="newest", start=(a*100), size=((a+1)*100))
            for b,i in enumerate(c):
                print(a*100+b, i.content, len(i.content))
                
                nickWarnings = await findNickname(i.author.nickname)
                contWarnings = await findContent(i.content, ctx.msg.ndcId)
            
                if nickWarnings or contWarnings: sus_users.append[i.author.uid]

        print(sus_users)
        for i in sus_users:
            u = await ctx.client.get_user_info(i)
            embed = Embed(
                title=u.nickname,
                object_type=0,
                object_id=u.uid,
                content="Usuario malhechor"
                 )
            await ctx.send(f"""
Usuario: {u.nickname}
ID: {i}""", embed=embed)

        print("End")
        await ctx.send(f"""
Posee {user.commentsCount} comentarios
De los cuales hay {len(sus_users)} comentarios sus.
""")
        return


