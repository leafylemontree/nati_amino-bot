from src import utils
from src.database import db
from src import objects

async def subscribeHelp(ctx):
    topics = "".join([f" - {t}\n" for i,t in enumerate(objects.AVAILABLE_TOPICS)])
    await ctx.send(f"""
El sistema de suscripción de Nati le permite tener en su comunidad blogs subidos por la propia Nati, los cuales abarcan temas como novedades de Amino, un periódico bisemanal, novedades del bot, entre otras cosas.

--suscribir -info: Recibe información sobre el sistema de suscripción
--suscribir [tema]: Le permite suscribirse a uno o varios temas para que Nati publique estos en su comunidad.

Los temas disponibles son:
{topics}

--desuscribrir [tema]: El bot ya no subirá blogs sobre este tema en su comunidad
--sugerir-tema: Puede sugerir que en un futuro sean añadidos nuevos temas para publicar en su comunidad
""")

@utils.isStaff
@utils.userTracker("suscribir")
async def subscribe(ctx):
    com = ctx.msg.content.upper().split(" ")
    if len(com) < 2:    return await subscribeHelp(ctx)

    com = com[1]
    if com.find("INFO") != -1:   return await subscribeHelp(ctx)
    
    r = db.subscribeTopic(ctx.msg.ndcId, com.replace("-", ""))
    if r is True:   await ctx.send(f"Esta comunidad se ha suscrito al tema: {com.lower()}")
    else:           await ctx.send(f"El tema puesto ({com.lower()}) no está disponible. Puede ver aquellos que sí lo están con --suscribir -info")
    return

@utils.isStaff
@utils.userTracker("desuscribir")
async def desubscribe(ctx):
    com = ctx.msg.content.upper().split(" ")
    if len(com) < 2:    return await ctx.send("Debe ingresar un tema al cual quiere desuscribirse tras el comandos, ejemplo --desuscribirse news. Puede ver aquellos temas disponibles con --suscribir -info")

    com = com[1]
    r = db.unsubscribeTopic(ctx.msg.ndcId, com.replace("-", ""))
    if r is True:   await ctx.send(f"Esta comunidad se ha desuscrito del tema: {com.lower()}")
    else:           await ctx.send(f"El tema puesto ({com.lower()}) no está disponible. Puede ver aquellos que sí lo están con --suscribir -info")
    return

@utils.userTracker("sugerir-tema")
async def sugest(ctx):
    com = ctx.msg.content.split(" ")
    if len(com) < 2:    return await ctx.send("Ingrese una descripción del tema que quiere que sea agregado,")
    com = " ".join(com[1:])
    r = db.sugestTopic(ctx.msg.ndcId, com)
    await ctx.send("Se ha registrado su sugerencia. ¡Muchas gracias!")
    return

@utils.userTracker("temas-suscritos")
async def topicsSubscipted(ctx):
    topics = db.getAllCommunityTopics(ctx.msg.ndcId)
    await ctx.send("Esta comunidad está suscrita a los siguientes temas:\n" + "".join([f" - {t}\n" for t in topics]))
    return

@utils.isStaff
async def registerBlogSubscription(ctx):
    print("New blog in repository")
    args = ctx.msg.content.split(" ")
    if len(args) < 3: return await ctx.send("Debe añadir el tema y el enlace de un blog o una wiki tras el comando.")

    url = args[2]
    link = await ctx.client.get_info_link(url)
    if link.linkInfo.objectType not in [1, 2]: return await ctx.send("El link que ingrese debe ser de una wiki.")

    objectId    = link.linkInfo.objectId
    objectType  = link.linkInfo.objectType
    postndcId   = link.linkInfo.ndcId
    title       = None
    topic       = args[1].lower()

    if   objectType == 1:
        blog = await ctx.client.get_blog_info(objectId)
        title = blog.title
        response = db.addSubscriptionRepository(topic, title, url)
    elif objectType == 2:
        wiki = await ctx.client.get_wiki_info(objectId)
        title = wiki.label
        response = db.addSubscriptionRepository(topic, title, url)
    
    if response is True:
        await ctx.send(f"Se ha añadido {title} al canal {topic}.")
    else:
        await ctx.send("El tema ingresado ({topic}) no está registrado.")
    return

@utils.isStaff
async def getTopicSubscriptionRepository(ctx):
    args = ctx.msg.content.split(" ")
    if len(args) < 2: return await ctx.send("Debe añadir el tema tras el comando.")

    topic       = args[1].lower()
    repository  = db.getSubscriptionRepository(topic)
    msg         = f"Estos son los blogs disponibles para el repositorio de {topic}:\n\n"
    for post in repository:
        msg += f"""
Nombre: {post.title}
Subido: {post.timestamp}
Link: {post.url}

"""
    await ctx.send(msg)
    return

@utils.isStaff
async def topicCommunityList(ctx):
    com = ctx.msg.content.split(" ")
    if len(com) < 2: return await ctx.send("Debe poner el nombre del tema tras el comando.\nPor ejemplo --comunidades-suscritas amino")
    topic = com[1]
    communities = db.getTopicSubscriptionList(topic)
    if communities is None: return await ctx.send("El tema ingresado no está disponible.")

    msg = f"Hay {len(communities)} suscritas al tema \"{topic}\":\n\n"
    for community in communities:
        msg += f"\nndc://x{community}/home"

        if len(msg) > 1950:
            await ctx.send(msg)
            msg = ""

    if msg != "": await ctx.send(msg)
    return




