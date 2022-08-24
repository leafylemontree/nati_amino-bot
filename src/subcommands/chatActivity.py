from src import objects
from src.text import text
from edamino.api import Embed

async def enter(ctx):
        user = await ctx.get_user_info()    
        if user.nickname in objects.AntiSpam.banned_nicks : return None
        objects.botStats.register(0)

        thread = await ctx.get_chat_info()
        msg = f"{text['enter'][0]}{thread.membersCount}{text['enter'][1]}<$@{ctx.msg.author.nickname}$>"
        embed = Embed(
                title="Bella personita",
                object_type=0,
                object_id=ctx.msg.author.uid,
                content="se ha unido, uwu."
            )

        return await ctx.client.send_message(  message=msg,
                                    chat_id=ctx.msg.threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=[ctx.msg.author.uid],
                                    embed=embed,
                                    link_snippets_list=None,
                                    reply=None )
        return

async def leave(ctx):
        user = await ctx.get_user_info()    
        if user.nickname in objects.AntiSpam.banned_nicks : return None
        name = user.nickname
        return await ctx.send(f"[ci]¡Adios {name}! Esperamos verte pronto.")
