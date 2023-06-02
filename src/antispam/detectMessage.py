from .data      import AS
from .n_logging import sendLog
from src        import objects
from src.database import db
import re
import traceback

async def findNickname(nick):
        warnings = []
        nick = nick.upper()
        for i in objects.AntiSpam.banned_nicks:
            if ((i.upper() in nick) & ("1" not in warnings)): warnings.append("1") 
        for i in objects.AntiSpam.sexual_nicks:
            if ((i.upper() in nick) & ("2" not in warnings)): warnings.append("2") 
        #for i in objects.AntiSpam.sus_keywords:
        #    if ((i in nick) & ("3" not in warnings)): warnings.append("3") 
        #try:    e = nick.encode("ascii")
        #except Exception:
        #    if ("4" not in warnings): warnings.append("4")
        return warnings

async def findContent(content, comId=None):
        warnings = []
        if content is None: return warnings
        else: content = content.upper()

        if content.find("T.ME/") != -1                 : warnings.append("101")
        if content.find("AMINOAPPS.COM/C/") != -1      : warnings.append("102")
        if content.find("AMINOAPPS.COM/INVITE/") != -1 : warnings.append("103")
        if content.find("T.CO/") != -1                 : warnings.append("104")
        if content.find("DISCORD.") != -1              : warnings.append("105")
        if content.find("PROJZ") != -1                 : warnings.append("106")
        if content.find("CHAT.WHATSAPP.") != -1        : warnings.append("107")
        if content.find("AMINOAPPS.COM/U/") != -1      : warnings.append("108")
        if content.upper().find("{}") != -1            : warnings.append("111")
        if len(content) > 3200                         : warnings.append("151") 
        if len(content) > 32000                        : warnings.append("152") 
        
        #try:
            #pz = re.search(r"((PRO[JY])*.*?[zZ](PRO[JY])*(?![a-zA-Z0-9ñÑ]))", content, re.IGNORECASE)
            #if pz and "106" not in warnings: warnings.append("106")
        #except Exception as e:
            #print(e)
            #traceback.print_exc()

        normalSpam = list(map(lambda w: str(w), range(101, 109)))
        if not any(map(lambda w: True if w in normalSpam else False, warnings)):
            if   content.find("AMINOAPPS")    != -1: pass
            elif content.find("YOUTU")        != -1: pass
            elif content.find("GOOGLE")       != -1: pass
            elif re.search('.*\.[^ \n]*\/.*', content): warnings.append('109')

        if not comId: return warnings
        log = db.getLogConfig(comId)
        if log._ignore:
            if "102" in warnings: warnings.remove("102")
            if "103" in warnings: warnings.remove("103")
        return warnings

async def msgType(mtype, content=None, author=None):
        warnings = []

        if mtype not in [0, 1, 2 ,3, 100, 101, 102, 103, 104]:
            if author  is None                 : pass 
            if content is None                 : pass 
            else                               : warnings.append("200")
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
        
        chat = db.getChatConfig(ctx.msg.threadId, ctx.msg.ndcId, exists=True)

        nick_warnings = await findNickname(nick)
        msg_warnings  = await findContent(content, comId)
        type_warnings = await msgType(ctx.msg.type, ctx.msg.content, ctx.msg.author)

        if chat is not None and "4" in nick_warnings: nick_warnings.remove("4")

        warnings.extend(nick_warnings)
        warnings.extend(msg_warnings)
        warnings.extend(type_warnings)
        
        if warnings: return await sendLog(ctx, warnings)
        return False
