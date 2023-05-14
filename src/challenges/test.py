from src import objects
import datetime

async def get_blog_likes(ctx, blogId=None, wikiId=None, start=0, size=100):
    response = None
    if   blogId:  response = await ctx.client.request('GET', f'blog/{blogId}/vote?cv=1.2&start={start}&size={size}')
    elif wikiId:  response = await ctx.client.request('GET', f'item/{blogId}/vote?cv=1.2&start={start}&size={size}')
    return objects.PostLikes(response)

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
