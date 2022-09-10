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

        print(nick_usr_1)
        print(nick_usr_2)
        num = int(random() * 16)
        print(f"num = {num}")

        if com[1].find("KISS") != -1:
            async with AIOFile(f'media/cutes/kiss/{str(num)}.gif', 'rb') as file:
                 gif = await file.read()
                 await ctx.send_gif(gif)
            
            db.modifyRecord(12, user)
            db.modifyRecord(22, ctx.msg.author)
            reply.msg = f"<$@{nick_usr_1}$> le da un beso a <$@{nick_usr_2}$>"
        elif com[1].find("HUG") != -1:
            async with AIOFile(f'media/cutes/hug/{str(num)}.gif', 'rb') as file:
                 gif = await file.read()
                 await ctx.send_gif(gif)

            db.modifyRecord(11, user)
            db.modifyRecord(21, ctx.msg.author)
            reply.msg = f"<$@{nick_usr_1}$> le da un abrazo a <$@{nick_usr_2}$>"
        elif com[1].find("PAT") != -1 :
            async with AIOFile(f'media/cutes/pat/{str(num)}.gif', 'rb') as file:
                 gif = await file.read()
                 await ctx.send_gif(gif)

            db.modifyRecord(13, user)
            db.modifyRecord(23, ctx.msg.author)
            reply.msg = f"<$@{nick_usr_1}$> acaricia a <$@{nick_usr_2}$>"


        await ctx.client.send_message(message=reply.msg,
                                    chat_id=ctx.msg.threadId,
                                    mentions=[ctx.msg.author.uid, user.uid])
        return objects.Reply(None, False)
