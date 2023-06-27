from src import objects
from src import utils

async def get_community_user_stats(ctx, userType, start=0, size=25):
        target = "curator"
        if      userType.lower() == "leader":   target = "leader"
        elif    userType.lower() == "curator":  target = "curator"
        else:   return None

        response = {"userProfileList": []}
        try:                    response = await ctx.client.request("GET", f"community/stats/moderation?type={target}&start={start}&size={size}")
        except Exception as e:
            print(e, response)
            pass

        return tuple(map(lambda user: objects.AdminUserProfile(**user), response['userProfileList']))

async def moderations(ctx, mtype="NATI"):
    if ctx.msg.content.upper().find("-STAFF") != -1 and ctx.msg.author.role != 0 : mtype="ALL"
    mods = {
        "curators": None,
        "leaders" : None
    }

    if   mtype == "NATI":
        mods['leaders'] = await get_community_user_stats(ctx, "leader", 0, 100)
        minutes = 0
        logs    = 0
        for user in mods['leaders']:
            if user.uid != ctx.client.uid: continue
            minutes = (user.avgDailySpendTimeIn7Days / 60) * 7
            logs    = user.adminLogCountIn7Days
        msg = f"En esta semana, Nati ha estado activa por {minutes:.2f} minutos, y ha hecho {logs} moderaciones."
        return await ctx.send(msg)

    elif mtype == "LEADERS":
        mods['leaders'] = await get_community_user_stats(ctx, "leader", 0, 100)
        msg = "Líderes:"
        for leader in mods['leaders']:
            msg += f"\n    Nick: {leader.nickname}\n    Mods: {leader.adminLogCountIn7Days}\n    Minutos: {((leader.avgDailySpendTimeIn7Days / 60) * 7):.2f}"
        return await ctx.send(msg)

    elif mtype == "CURATORS":
        mods['curators'] = await get_community_user_stats(ctx, "curator", 0, 100)
        msg = "Curadores:"
        for curator in mods['curators']:
            msg += f"\n    Nick: {curator.nickname}\n    Mods: {curator.adminLogCountIn7Days}\n    Minutos: {((curator.avgDailySpendTimeIn7Days / 60) * 7):.2f}\n"
        return await ctx.send(msg)

    elif mtype == "ALL":
        mods['curators'] = await get_community_user_stats(ctx, "curator", 0, 100)
        mods['leaders'] = await get_community_user_stats(ctx, "leader", 0, 100)

        msg = "Líderes:"
        for leader in mods['leaders']:
            msg += f"\n    Nick: {leader.nickname}\n    Mods: {leader.adminLogCountIn7Days}\n    Minutos: {((leader.avgDailySpendTimeIn7Days / 60) * 7):.2f}\n"
        msg += "\nCuradores:"
        for curator in mods['curators']:
            msg += f"\n    Nick: {curator.nickname}\n    Mods: {curator.adminLogCountIn7Days}\n    Minutos: {((curator.avgDailySpendTimeIn7Days / 60) * 7):.2f}\n"
        return await ctx.send(msg)
   


