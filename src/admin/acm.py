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

@utils.userTracker("moderaciones")
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
   

async def get_join_requests(ctx, start=0, size=25):
    response = await ctx.client.request("GET", f"community/membership-request?status=pending&start={start}&size={size}")
    return tuple(map(lambda x: objects.CommunityMembershipRequest(**x), response["communityMembershipRequestList"]))
    print(response)


async def linkParser(message, key):
    if message is None:           return None
    if message.find(key) == -1: return None
    link = message.split(key)[1]
    link = link.split(" ")[0]
    return "http://aminoapps.com" + key + link


async def profileLink(message):
    return await linkParser(message, "/p/")

async def communityLink(message):
    return await linkParser(message, "/c/")

@utils.isStaff
async def joinRequest(ctx):
    joinRequests = await get_join_requests(ctx, start=0, size=100)
    await ctx.send(f"Hay {len(joinRequests)} solicitudes de ingreso:\n\n")
    ndcId = ctx.msg.ndcId

    for request in joinRequests:
        community_link = await communityLink(request.message)
        profile_link = await profileLink(request.message)
        
        objectId    = None
        objectType  = None
        objectNdc   = None

        linkAnalyze = ""
        comAnalyze  = ""

        if profile_link:
            linkInfo = await ctx.client.get_info_link(profile_link)
            print(linkInfo)
            objectId    = linkInfo.linkInfo.objectId
            objectType  = linkInfo.linkInfo.objectType
            objectNdc   = linkInfo.linkInfo.ndcId

            if objectType != 0:
                linkAnalyze = "El link ingresado no es de un perfil"
                pass
            else:
                try:
                    ctx.client.set_ndc(objectNdc)
                    profile = await ctx.client.get_user_info(objectId)
                    linkAnalyze = f"""
Nick: {profile.nickname}
Rol: {'Líder' if profile.role == 102 else 'Curador' if profile.role == 101 else 'Ninguno'}
Perfil: ndc://x{objectNdc}/user-profile/{objectId}
"""
                except:
                    ctx.client.set_ndc(ndcId)
                    
                try:
                    community = await utils.get_community_info(ctx, objectNdc)
                    comAnalyze = f"""
Nombre: {community.name}
Agente:
    Nick: {community.agent.nickname}
    Id: ndc://x{community.ndcId}/user-profile/{community.agent.uid}
"""
                except:
                    pass
        

        ctx.client.set_ndc(ndcId)

        msg = f"""
Nick:
{request.applicant.nickname}

Mensaje:
{request.message}

Link de perfil:
{profile_link}

Perfil global:
ndc://g/user-profile/{request.uid}

------- Análisis del link -------
Id: {objectId}
Tipo: {objectType}
Comunidad: ndc://x{objectNdc}/home

Link:
{linkAnalyze}

Comunidad:
{comAnalyze}
"""
        await ctx.send(msg)
    return


