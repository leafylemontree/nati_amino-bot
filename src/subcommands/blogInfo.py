async def blogInfo(ctx):
    links       = ctx.msg.content.split("\n")[1:]
    linkInfo    = [await ctx.client.get_info_link(link) for link in links]
    blogs       = [await ctx.client.get_blog_info(link.linkInfo.objectId) for link in linkInfo]
    titles      = [f"{i+1}. {blog.title}" for i,blog in enumerate(blogs)]
    await ctx.send("\n".join(titles))
