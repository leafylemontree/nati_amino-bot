from src import utils


async def confirm(ctx, ins):
    msg = ctx.msg.content.upper().split(" ")[0]
    if msg.find("-NO") == 0 :
        await ctx.send("Rechazado")
        return True
    if msg.find("-SI") == -1:
        return 
    
    try:
        blog = await ctx.client.post_blog(
                title=ins.data['title'],
                content=ins.data['content']
            )
        await ctx.send(f"¡Publicado con éxito!\nlink: ndc://x{ctx.msg.ndcId}/blog/{blog.blogId}")
    except Exception as e:
        await ctx.send(f"¡Ha ocurrido un error!\n{e}")

    return True




@utils.isStaff
@utils.userTracker("crearblog")
@utils.waitForMessage(message="*", callback=confirm)
async def createBlog(ctx):
    lines   = ctx.msg.content.split("\n")
    content = None
    title   = None
    if len(lines) < 2:
        title   = f"Blog creado por {ctx.msg.author.nickname}"
        content = " ".join(
                            lines[0].split(" ")[1:]
                        );
    else            :
        title   = " ".join(
                            lines[0].split(" ")[1:]
                );
        content = "\n".join(lines[1:])

    data = {
            "title" : title,
            "content": content
        }

    await ctx.send(f"[bc]Confirme la petición:\n[c]-------------------\n\n[cu]Título:\n[c]{title}\n\n[cu]Contenido:\n[c]{content}\n\n[c]-si      -no")
    return data
