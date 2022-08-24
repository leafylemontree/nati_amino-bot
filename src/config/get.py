from .data import Config, register, review 

async def get(ctx):
        chatId = ctx.msg.threadId

        if review('chat', chatId)           : return -1 
        if chatId in Config.disable_bot     : return -1

        if chatId in Config.slow_mode       :
            if not review('user', ctx.msg.author.uid):
                register("slow", ctx.msg.author.uid, 30)
            else: return -1

        if chatId in Config.only_staff      :
            if ctx.msg.author.role not in [101, 102]: return -1
        
        if   ctx.msg.type == 101:
            print("welcome!")
            #if chatId in Config.check_on_enter  :
            #    await AS.review_user(ctx)
            if chatId in Config.disable_welcome :
                return -1
            return 1

        elif ctx.msg.type == 102:
            print("godbye")
            if chatId in Config.enable_goodbye  :
                return 2
        
        elif chatId in Config.no_fun          : return 100
        return 0
