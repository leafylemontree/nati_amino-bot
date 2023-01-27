import ctypes
import math

path = 'src/subcommands/_math/c/'
rt   = ctypes.cdll.LoadLibrary(f'{path}rate.so')
rt.argtypes = (ctypes.c_char_p, ctypes.c_int)
rt.restype  = ctypes.c_double

async def like_wiki(ctx, postId):
    data = {"value": 4, "eventSource": "PostDetailView"}
    return await ctx.client.request('POST',
                                  f"item/{postId}/vote?cv=1.2",
                                  json=data)


async def rateBlog(ctx):
    link = ctx.msg.content.split(" ")
    if len(link) == 1: return "Debe poner el link de un blog"

    try:
        blogLink = await ctx.client.get_info_link(link=link[1])
        postType = blogLink.linkInfo.objectType
        blogId = blogLink.linkInfo.objectId
    except:
        return ctx.send("Se ha producido un error :c")
    
    print("POST-TYPE:", postType)
    if   postType == 0:    blog = await ctx.client.get_user_info(blogId)
    elif postType == 1:    blog = await ctx.client.get_blog_info(blogId)
    elif postType == 2:    blog = await ctx.client.get_wiki_info(blogId)
    else              :    return await ctx.send("Algo ha fallado :c")

    content = blog.content
    text = content.encode("utf-8")
    l    = len(content)

    score = rt.rate(text, l)
    
    score = math.sin(score)
    score = (2/((math.e ** score) + (math.e ** -score)))**2
    print(score)

    if score < 0.5: return await ctx.send(f"A Nati no le ha gustado tu blog. Lo ha calificado con:\n[b]{(score*10):.2}/10")
    
    await ctx.send(f"A Nati le ha gustado tu {'biografía' if postType == 0 else 'blog' if postType == 0 else 'wiki' if postType == 2 else 'cosa'}. Lo ha calificado con:\n[b]{(score*10):.2}/10\n\nAdemás, {'le ha dado like' if postType != 0 else 'te ha seguido'}.")
    
    if   postType == 0: await ctx.client.follow(uids=[blogId])
    elif postType == 1: await ctx.client.like_blog(blog_id=blogId)
    elif postType == 2: await like_wiki(ctx, blogId)
    return
    
