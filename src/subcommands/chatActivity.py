from src.database import db
import edamino
from src import utils
from src import objects
from src.text import text

async def enter(ctx):
        user = await ctx.get_user_info()
        if user.nickname in objects.AntiSpam.banned_nicks :
            objects.botStats.register(0)
            return None

        chatWelcome = db.getWelcomeMessage(ctx.msg.ndcId, 'CHAT')
        if chatWelcome is None: chatWelcome = "-DEFAULT"

        if chatWelcome.find("-DEFAULT") != -1:
            thread   = await ctx.get_chat_info()
            message = f"{text['enter'][0]}{thread.membersCount}{text['enter'][1]}<$@{ctx.msg.author.nickname}$>"
        else:
            message = await utils.formatter(ctx, chatWelcome)

        embed = edamino.api.Embed(
                title="Bella personita",
                object_type=0,
                object_id=ctx.msg.author.uid,
                content="se ha unido, uwu."
            )

        return await ctx.client.send_message(
                                    message=message,
                                    chat_id=ctx.msg.threadId,
                                    mentions=[ctx.msg.author.uid],
                                    embed=embed
                                    )

async def leave(ctx):
        user = await ctx.get_user_info()    
        if user.nickname in objects.AntiSpam.banned_nicks : return None
        name = user.nickname
        return await ctx.send(f"[ci]¡Adios {name}! Esperamos verte pronto.")
