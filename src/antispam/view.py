from src import utils

@utils.userTracker("view")
async def view(ctx):
        msg = await ctx.client.get_chat_messages(chat_id=ctx.msg.threadId, size=10)
        out = ""
        for n,m in enumerate(msg.messageList):
            out +=  f"""
Item    : {n}
Mensaje : {m.content}
Tipo    : {m.type}
Autor   : {m.author.nickname}
Id      : {m.messageId}
"""
        return out[:2000]

