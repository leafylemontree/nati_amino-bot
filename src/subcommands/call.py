from src import objects
from src import utils




@utils.isStaff
async def everyone(ctx):
        user = await ctx.get_user_info()
        if ((user.role == 0) & (user.uid != "17261eb7-7fcd-4af2-9539-dc69c5bf2c76")): return bot_o.Reply("Usted no está autorizado para ejercer este comando", False)
        thread = await ctx.get_chat_info()
        userCount = thread.membersCount

        uidList = []
        for i in range(userCount % 100):
            users = await ctx.client.get_chat_users(
                                                ctx.msg.threadId,
                                                i * 25,
                                                100
                                                )
            for j in users:
                uidList.append(j.uid)


        await ctx.client.send_message(  message="Mencionando usuarios...",
                                    chat_id=ctx.msg.threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=uidList,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None )

        return objects.Reply(f"{len(uidList)} usuarios mencionados.", False)

async def staff(ctx):

        leaders  = list(await ctx.client.get_all_users("leaders", 0, 100))
        curators = list(await ctx.client.get_all_users("curators", 0, 100))

        users = []
        if leaders: users.extend(leaders)
        if curators: users.extend(curators)

        userList = []
        nameList = ""
        for i,j in enumerate(users):
            userList.append(j.uid)
            nameList += f" <$@{j.nickname}$>"

        await ctx.client.send_message(  message=f"{ctx.msg.author.nickname} solicita al staff. {nameList}",
                                    chat_id=ctx.msg.threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=userList,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None)       

        return objects.Reply(None, False) 

