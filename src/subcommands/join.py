import time
from src import utils

async def join_chat(ctx, threadId: str):
        data = {"timestamp": int(time.time() * 1000)}
        return await ctx.client.request(
                'POST',
                f'chat/thread/{threadId}/member/{ctx.client.uid}',
                json=data
                )

@utils.userTracker("join")
async def joinChat(ctx):
        link = ctx.msg.content.split(" ")
        if len(link) == 1: return "Debe poner el link del chat al cual quiere que el bot se una"

        try:
            chatId = await ctx.client.get_info_link(link=link[1])
            print(chatId.linkInfo.objectId)
            if chatId.linkInfo.objectType == 12:
               await join_chat(ctx, threadId=chatId.linkInfo.objectId)
            #else if chatId.linkInfo.objectType == 12:
            #   await ctx.client.join_chat(chat_id=chatId.linkInfo.objectId)
        except:
            return "Se ha producido un error :c"
        
        return "Listo, ya me he unido c:"

@utils.userTracker("unirvc")
async def joinVC(ctx):
    data = {
        "o": {
            "ndcId": ctx.msg.ndcId,
            "threadId": ctx.msg.threadId,
            "joinRole": 1,
            "id": "2154531"
        },
        "t": 112
    }
    await ctx.ws.send_json(data)
    await ctx.send("Unido al chat de voz.")
    return

@utils.userTracker("unirsala")
async def joinSR(ctx):
    data = {
        "o": {
            "ndcId": ctx.msg.ndcId,
            "threadId": ctx.msg.threadId,
            "joinRole": 2,
            "id": "72446"
        },
        "t": 112
    }
    await ctx.ws.send_json(data)
    await ctx.send("Unido a la sala de proyección.")
    return
