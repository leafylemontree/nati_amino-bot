import time

async def join_chat(ctx, threadId: str):
        data = {"timestamp": int(time.time() * 1000)}
        return await ctx.client.request(
                'POST',
                f'chat/thread/{threadId}/member/{ctx.client.uid}',
                json=data
                )

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
