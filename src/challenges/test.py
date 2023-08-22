from src import objects
import datetime
from src.database import db
from src.utils.formatter import get_community_info
from src          import utils

newLine = '\n'

async def get_blog_likes(ctx, blogId=None, wikiId=None, start=0, size=100):
    response = None
    if   blogId:  response = await ctx.client.request('GET', f'blog/{blogId}/vote?cv=1.2&start={start}&size={size}')
    elif wikiId:  response = await ctx.client.request('GET', f'item/{blogId}/vote?cv=1.2&start={start}&size={size}')
    return objects.PostLikes(response)

@utils.userTracker("verlikes")
async def get_likes_from_link(ctx):
    link        = ctx.msg.content.split(" ")[1]
    linkInfo    = await ctx.client.get_info_link(link)
    objectId    = linkInfo.linkInfo.objectId
    objectType  = linkInfo.linkInfo.objectType

    likes   = None
    post    = None
    if objectType == 1: 
        likes   = await get_blog_likes(ctx, blogId=objectId)
        post    = await ctx.client.get_blog_info(objectId)
    if objectType == 2:
        likes   = await get_blog_likes(ctx, wikiId=objectId)
        post    = await ctx.client.get_wiki_info(objectId)

    
    timeDelta = datetime.datetime.now() - datetime.datetime.strptime(str(post.createdTime), '%Y-%m-%dT%H:%M:%SZ')
    await ctx.send(f"""
Información del blog:
--------------------
Título: {post.title if objectType == 1 else post.label}
Tipo: {'Blog' if objectType == 1 else 'Wiki'}
Comentarios: {post.commentsCount}
Likes: {post.votesCount}
Id: {post.blogId if objectType == 1 else post.itemId}
Autor: {post.author.nickname}
Creado hace: {timeDelta.days // 365} años, {timeDelta.days // 30} meses, {timeDelta.days} días, {(timeDelta.seconds // 3600) % 24 } horas, {(timeDelta.seconds // 60) % 60} minutos, {timeDelta.seconds % 60} segundos.

Usted {'' if ctx.msg.author.uid in likes.votedValueMap else 'no '}le ha dado like {'al blog' if objectType == 1 else 'la wiki'}.""")
    return

@utils.userTracker("ranking-yincana")
async def getYincanaRanking(ctx):
    userYincana = db.getYincanaDataCommunity(ctx.msg.ndcId)
    community   = await get_community_info(ctx, ctx.msg.ndcId)

    splitData = {}

    for data in userYincana:
        if data.level not in splitData.keys():   splitData[data.level] = []
        splitData[data.level].append(data)

    filteredData = {}
    for key,array in splitData.items():
        if key not in filteredData.keys():   filteredData[key] = []

        sortedArray = sorted(array, key=lambda item: item.timestamp)
        filteredData[key] = sortedArray

    keys = [key for key in filteredData.keys()]

    msg = ''
    i   = 0
    for key in keys:
        array  = [f'{i + j + 1}. {(await db.getUserNickname(ctx, ctx.msg.ndcId, userId=yincana.userId))[:16]} - {yincana.level + 1}\n' for j,yincana in enumerate(filteredData[key])] 
        msg   += '\n'.join(array)
        i += len(filteredData[key])

    print(filteredData)
    await ctx.send(f"""
[cb]Ranking
[c]——————«•»——————
[C]Comunidad: {community.name}
[c]Usuarios jugando: {len(userYincana)}

{msg}""")


@utils.userTracker("yincana")
async def giveHelpYincana(ctx):
    link = 'http://aminoapps.com/p/r2ap3z'
    await ctx.send(f"""La yincana es un sistema de recompensas que va por nivel. Cada nivel posee premios cada vez más altos, pero a su vez serán más complicados.

Comandos:
--ver-yincana: Muestra el reto actual dependiendo de tu nivel
--entregar-yincana: Para registrar si se cumplen los requisitos. Puede pedir información adicional.
--ranking-yincana: Muestra el ranking a nivel comunidad.

{('link del blog: ' + link) if ctx.msg.ndcId == 9999 else ''}""")

@utils.userTracker("retos-yincana")
async def giveAllChallenges(ctx):
    from src.challenges.register import challenges

    communityChallenge = None
    try: communityChallenge = challenges[ctx.msg.ndcId]
    except Exception:       return await ctx.send('Esta comunidad no tiene retos.')

    msg = f"[c]Estos son los retos de esta comunidada (Id: {ctx.msg.ndcId}):\n\n"
    for i,challenge in enumerate(communityChallenge.challenges):
        msg += f"[cu]Nivel: {i+1}\n[c]{communityChallenge.levelRepr(i)}\n".replace("\n", "\n[c]")

        if len(msg) > 1800:
            await ctx.send(msg)
            msg = ""

    if len(msg) > 0: await ctx.send(msg)



async def get_community_stickers(ctx):
    response = await ctx.client.request("GET", "sticker-collection?type=community-shared")
    return tuple(map(lambda stickerCollection: objects.StickerCollection(**stickerCollection), response['stickerCollectionList']))
