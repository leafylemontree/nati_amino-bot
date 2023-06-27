from .data import Config, register, review 
from src.database import db
from src import objects

async def get(ctx):
        chatId = ctx.msg.threadId
        chat   = db.getChatConfig(chatId, ctx.msg.ndcId) 
        com    = db.getLogConfig(ctx.msg.ndcId)

        if ctx.msg.author is None:          return -1

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
