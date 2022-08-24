from .data      import AS
from .n_logging import sendLog
from src        import objects

async def findNickname(nick):
        warnings = []
        for i in objects.AntiSpam.banned_nicks:
            if ((i in nick) & ("1" not in warnings)): warnings.append("1") 
        for i in objects.AntiSpam.sexual_nicks:
            if ((i in nick) & ("2" not in warnings)): warnings.append("2") 
        #for i in objects.AntiSpam.sus_keywords:
        #    if ((i in nick) & ("3" not in warnings)): warnings.append("3") 
        return warnings

async def findContent(content, comId=None):
        warnings = []
        
        if content.find("T.ME") != -1                  : warnings.append("101")
        if content.find("AMINOAPPS.COM/C/") != -1      : warnings.append("102")
        if content.find("AMINOAPPS.COM/INVITE/") != -1 : warnings.append("103")
        if content.find("T.CO") != -1                  : warnings.append("104")
        if content.upper().find("{}") != -1            : warnings.append("111")
        if len(content) > 3200                         : warnings.append("151") 

        #if int(comId) in AS.ignore_coms:
        #    if "102" in warnings: warnings.remove("102")
        #    if "103" in warnings: warnings.remove("103")
        return warnings

async def msgType(mtype, content=None, author=None):
        warnings = []

        if mtype in [58, 108, 109, 110, 113, 114] :
            if author  is None                 : pass 
            if content is None                 : pass 
            warnings.append("200")
        return warnings

async def detectAll(ctx):
        if ctx.msg.author is None: return False
        if ctx.msg.author.uid in AS.whitelist: return

        warnings = []
        content = str(ctx.msg.content).upper()
        nick    = str(ctx.msg.author.nickname).upper() 
        comId   = str(ctx.msg.ndcId)
        uid     = str(ctx.msg.author.uid)

        if int(comId) in AS.no_warnings: return
        
        nick_warnings = await findNickname(nick)
        msg_warnings  = await findContent(content, comId)
        type_warnings = await msgType(ctx.msg.type, ctx.msg.content, ctx.msg.author)
        
        warnings.extend(nick_warnings)
        warnings.extend(msg_warnings)
        warnings.extend(type_warnings)
        
        if warnings: return await sendLog(ctx, warnings)
        return False
