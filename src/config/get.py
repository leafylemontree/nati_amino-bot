from .data import Config, register, review 
from src.database import db
from src import objects

ignore  = [ 
            "7d470c61-c596-4b1c-a0b6-ffd7c9e581c6",
            #"aee422dc-8357-44b8-b5ae-c69abeb4979e",
            "dea19b7c-90fa-44c4-b657-960231ef6e2a",
            "228fd92f-ae31-42e9-bd0c-4af87a4b8f9b",
            "899b60c3-c3d7-46a2-b446-8681c6790e90"
           ]


async def get(ctx):
        chatId = ctx.msg.threadId
        chat   = db.getChatConfig(chatId, ctx.msg.ndcId) 
        com    = db.getLogConfig(ctx.msg.ndcId)

        if ctx.msg.author is None:          return -1

        if ctx.msg.author.uid in ignore:
            try:                    await ctx.client.kick_from_chat(chat_id=ctx.msg.threadId, uid=ctx.msg.author.uid, allow_rejoin=False)
            except Exception as e:  pass
            return objects.MessageEvents.FORBIDDEN

        if review('chat', chatId)           : return -1 
        if chat.bot : return -1


        if com.bot:     return -1
        if com.staff and ctx.msg.author.role not in [100, 101, 102]:     return -1

        #if chatId in Config.slow_mode       :
        if chat.slow       :
            if not review('user', ctx.msg.author.uid):
                register("slow", ctx.msg.author.uid, 30)
            else: return objects.MessageEvents.FORBIDDEN

        if chat.staff      :
            if ctx.msg.author.role not in [100, 101, 102]: return -1
       
        if   ctx.msg.type == 101:
            if not chat.welcome: return objects.MessageEvents.FORBIDDEN
            return objects.MessageEvents.MEMBER_JOIN

        elif ctx.msg.type == 102:
            if chat.goodbye  : return objects.MessageEvents.MEMBER_LEAVE
        
        elif chat.nofun           : return 100
        return 0
