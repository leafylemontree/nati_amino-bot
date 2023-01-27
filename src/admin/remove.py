# removes users from chat

from src import utils
import asyncio

@utils.isStaff
async def remove(ctx):
    chat  = await ctx.client.get_chat_info(chat_id=ctx.msg.threadId)

    level   = 5
    show    = True
    remove  = False

    if ctx.msg.content.upper().find("-L") != -1:
        msg = ctx.msg.content.upper().split("-L")[1]
        msg = msg.split(" ")[0]
        try     : level = int(msg)
        except  : level = 5
        if level > 10: level = 10
        if level < 1 : level = 1

    if ctx.msg.content.upper().find("-NS") != -1:
        show = False

    if ctx.msg.content.upper().find("-RF") != -1:
        remove = True


    usersToRemove = []
    for page in range((chat.membersCount // 100) + 1):
        users = await ctx.client.get_chat_users(chat_id=ctx.msg.threadId, start=page*100, size=100)
        for user in users:
            if user.level < level: usersToRemove.append([user.nickname, user.level, user.uid])

    if remove:
        for user in usersToRemove:
            try:
                await ctx.client.kick_from_chat(
                    chat_id     = ctx.msg.threadId,
                    uid         = user[2],
                    allow_rejoin= True
                    )
            except Exception:
                pass
            await asyncio.sleep(3)

    if show  :
        mout = "Usuarios para remover:\n\n"
        for user in usersToRemove:
            mout += f"{user[0][:24]}: {user[1]}\n"
        await ctx.send(mout[:2000])

    return
