from .data import Config, register, review 
from src.database import db

async def get(ctx):
        chatId = ctx.msg.threadId
        chat   = db.getChatConfig(chatId) 
        com    = db.getLogConfig(ctx.msg.ndcId)

        if review('chat', chatId)           : return -1 
        if chat.bot : return -1


        if com.bot:     return -1
        if com.staff and ctx.msg.author.role not in [100, 101, 102]:     return -1

        if chatId in Config.slow_mode       :
            if not review('user', ctx.msg.author.uid):
                register("slow", ctx.msg.author.uid, 30)
            else: return -1

        if chat.staff      :
            if ctx.msg.author.role not in [100, 101, 102]: return -1
       
        if   ctx.msg.type == 101:
            print("welcome!")
            #if chatId in Config.check_on_enter  :
            #    await AS.review_user(ctx)
            if chat.welcome : return -1
            return 1

        elif ctx.msg.type == 102:
            print("goodbye")
            if chat.goodbye  : return 2
        
        elif chat.nofun           : return 100
        return 0
