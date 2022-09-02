from asyncio import sleep

class Functions:
    
    voteList = {}

    async def send(self, ctx, threadId, msg, ndcId, ghost=False, embed=None):
        chatList = []
        if type(threadId) == str: chatList.append(threadId)
        else                    : chatList.extend(threadId)
        msgList  = []
        if type(msg) == str     : msgList.append(msg)
        if len(msgList) == 1    :
            msgList.pop(0)
            for chat in chatList: msgList.append(msg)
        else                    : msgList.extend(msg)
        msgType = 0 if ghost is False else 109
        ctx.client.set_ndc(ndcId)
        await sleep(0.5)
        try:
            for chat,message in zip(chatList, msgList):
                await ctx.client.send_message(message=message,
                                    chat_id=chat,
                                    message_type=msgType,
                                    ref_id=None,
                                    mentions=None,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None )
        except:
            return False
        return True

    async def voting(self, ctx, instance, message):
        roomId  = instance.roomId
        players = instance.players

        if roomId not in self.voteList.keys(): self.voteList[roomId] = {}

        if self.voteList[roomId] == {}:
            for player in players:  self.voteList[roomId][player[0]] = None

        self.voteList[roomId][ctx.msg.author.uid] = message

        for vote in self.voteList[roomId]:
            if vote == None: return False

        return self.voteList[roomId]

