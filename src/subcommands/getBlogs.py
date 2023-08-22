from src import objects
from src import utils


@utils.userTracker("blogs")
async def getBlogs(ctx, msg):
        reply = objects.Reply(None, False)
        msg = msg[7:]
        if msg == "": return objects.Reply(objects.error(2500), False)
        blogs = ""

        if msg.find("-USER") != -1:
            blogs = await ctx.get_user_blogs()
            msg = msg[6:]

        #if msg == "":       return bot_o.Reply(subCommands.error(2500), False)

        text = ""
        offset = 1
        try:
            offset = int(msg)
        except:
            if msg.find("-ALL") != -1:
                for blog in blogs:
                    if blog.title is not None: text += f"\n[c]{offset}- {blog.title}"
                    offset += 1
                return bot_o.Reply(f"[c]Los blogs que tiene subidos son los siguientes:\n" + text, False)
            else:
                return objects.Reply(objects.error(2501), False)

        if offset > 0: offset -= 1;
        elif offset < 0: offset = 0;
        if offset > len(blogs): offset = len(blogs)

        blog = blogs[offset]
        reply.msg = f"""[c]Estos son los datos del blog seleccionado:
Título: {blog.title}
Autor: {blog.author.nickname}
Me gusta: {blog.votesCount}
Subido: {blog.createdTime}
Comentarios: {blog.commentsCount}
Etiquetas: {blog.keywords}
Id: {blog.blogId}
Visitas: {blog.viewCount}"""

        return reply
