from aiofile import async_open, AIOFile
from src import utils
from src import objects
from random import random
from src.database import db

@utils.cutes
async def cutes(ctx, uid, com):
        reply = objects.Reply(None, True)
        user = await ctx.client.get_user_info(uid)

        nick_usr_1 = ""
        nick_usr_2 = ""

        usr_db = db.getUserData(ctx.msg.author)
        if usr_db.alias == "" : nick_usr_1 = ctx.msg.author.nickname
        else                  : nick_usr_1 = usr_db.alias
        usr_db = db.getUserData(user)
        if usr_db.alias == "" : nick_usr_2 = user.nickname
        else                  : nick_usr_2 = usr_db.alias

        num = int(random() * 16)
        fol = ""
        msg = ""

        if com[1].find("KISS") != -1:
            fol = "kiss"
            msg = "le ha dado un beso a"
            db.modifyRecord(12, user)
            db.modifyRecord(22, ctx.msg.author)
        elif com[1].find("HUG") != -1:
            fol = "hug"
            msg = "le ha dado un abrazo a"
            db.modifyRecord(11, user)
            db.modifyRecord(21, ctx.msg.author)
        elif com[1].find("PAT") != -1 :
            fol = "hug"
            msg = "acaricia a"
            db.modifyRecord(13, user)
            db.modifyRecord(23, ctx.msg.author)
        elif com[1].find("SMILE") != -1 :
            fol = "smile"
            msg = "le sonrie a"
        elif com[1].find("BITE") != -1 :
            fol = "bite"
            msg = "ha mordido a"
        elif com[1].find("BLUSH") != -1 :
            fol = "blush"
            msg = "se ha sonrojado por"
        

        reply.msg = f"<$@{nick_usr_1}$> {msg} <$@{nick_usr_2}$>"
        async with AIOFile(f'media/cutes/{fol}/{str(num)}.gif', 'rb') as file:
            gif = await file.read()
            from src.imageSend import send_gif
            await send_gif(ctx, gif)
        
        db.modifyRecord(43, user, 100)
        db.modifyRecord(43, ctx.msg.author, 100)

        await ctx.client.send_message(message=reply.msg,
                                    chat_id=ctx.msg.threadId,
                                    mentions=[ctx.msg.author.uid, user.uid])
        return None
