from src import objects
from src import utils
from src.database import db
import edamino
import random

class FakeUser:
    def __init__(self, userId):
        self.uid = userId

def kiwilatigo(ctx):
        db.modifyRecord(32, ctx.msg.author)
        return objects.Reply(f"[ci]¡Oh no! Han hecho enfadar a {ctx.msg.author.nickname}\n\n[ci]/c skpa.", False)

async def alias(ctx, msg):
        if ctx.msg.extensions.mentionedArray:
            msg = msg.split("\u200e")[0]
            msg = msg.split(" ")
            msg.pop(0)
            user = ctx.msg.extensions.mentionedArray[0]
            msg = " ".join(msg)[:127]
            
            db.modifyRecord(31, user, value=msg)
            user = await ctx.client.get_user_info(user.uid)
            return f"El nuevo alias de {user.nickname} es {msg}."
        else:
            msg = msg.split(" ")
            if len(msg) < 2: return "Ingrese un nombre como alias."
            msg.pop(0)
            uid = ctx.msg.author.uid
            print(uid)
            print(msg)
            msg = " ".join(msg)[:127]
            db.modifyRecord(31, ctx.msg.author, value=msg)
            return f"El nuevo alias de {ctx.msg.author.nickname} es {msg}."
        return None

async def ghost(ctx, msg):
        msg = msg[8:]
        await ctx.client.send_message(  message=msg,
                                    chat_id=ctx.msg.threadId,
                                    message_type=109,
                                    ref_id=None,
                                    mentions=None,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None )
        return False
    
async def follow(ctx):
        await ctx.follow()
        msg = "Ya está, ya te he seguido, uwu."
        return objects.Reply(msg, True)

def replyMsg(msg):
        return objects.Reply(msg, True)

async def kick(ctx, msg):
        try:
            await ctx.client.kick_from_chat(ctx.msg.threadId, ctx.msg.uid, allow_rejoin=True)
        except:
            if msg is not None:
                msg += "\n\n[c]Nota: el bot no puede sacarte."

        return objects.Reply(msg, False)

async def papulince(ctx):

        grasa = [
                    ":V",
                    "V:",
                    "PAPU",
                    "ELFA",
                    "MOMAZO",
                    "MEMINGO",
                    "ALV",
                    "XDXDXD",
                    "PRRO",
                    "MAQUINOLA",
                    "LINCE",
                    "MEMEZUKI",
                    "GRASOSO",
                    "HAIL",
                    "GRASA",
                    "SDLG",
                    "PASA PACK",
                    "PASA EL PACK",
                    "MAMU",
                    "FIERA",
                    "SALVAJE",
                    "MAQUINÓN",
                    "PACMAN",
                    "VVVV"
                ]

        com = ctx.msg.content.upper().split(" ")
        if len(com) < 2: return await ctx.send("Debe colocar un texto después del comando.")
        msg = " ".join(com[1:])

        for word in grasa:
            if msg.find(word) != -1 : return await ctx.send("[CB]¡Papulince detectado! :v")
        return await ctx.send("No hay grasa en este mensaje")

async def customMsg(ctx):

        msg = ctx.msg.content
        msg = msg.split(" ")[1:]
        print(msg)

        await ctx.client.send_message(  message=f"Mensaje Tipo: {msg[0]}\n" + " ".join(msg[1:]),
                                    chat_id=ctx.msg.threadId,
                                    message_type=int(msg[0]),
                                    ref_id=None,
                                    mentions=None,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None) 
        return


@utils.userId
async def giveChocolate(ctx, userId, message):

    if userId == ctx.client.uid:    return await ctx.send("Lamentablemente, no se le pueden dar chocolates a Nati, unu")
    if userId == ctx.msg.author.uid: return await ctx.send("¿Te quieres dar un chocolate a ti mismo? Qué malote")

    user = await ctx.client.get_user_info(userId)
    await ctx.send(f"""
[c]{ctx.msg.author.nickname} quiere darle un chocolate a {user.nickname}
[c]¿Aceptas?
[c]-si -no
""")
    state = await utils.confirmation(ctx, ctx.msg.threadId, userId, ctx.msg.ndcId, timeout=False)
    if state: await ctx.send(f"{user.nickname} ha aceptado el chocolate, c:")
    else    : await ctx.send(f"{user.nickname} ha rechazado el chocolate, unu")

@utils.userId
async def askMarry(ctx, userId, message):

    if userId == ctx.client.uid:     return await ctx.send("Por fin alguien se quiere casar conmigo, uwu.")
    if userId == ctx.msg.author.uid: return await ctx.send("Dile no al autoamor, espera, ¿eso existe?")

    user = await ctx.client.get_user_info(userId)
    await ctx.send(f"""
[c]{ctx.msg.author.nickname} quiere proponerle matrimonio a {user.nickname}
[c]¿Aceptas?
[c]-si -no
""")
    state = await utils.confirmation(ctx, ctx.msg.threadId, userId, ctx.msg.ndcId, timeout=False)

    if state: await ctx.send(f"{user.nickname} ha aceptado el matrimonio, c:")
    else    : return await ctx.send(f"{user.nickname} ha rechazado el matrimonio, unu")
   
    u_db = db.getUserData(user)
    a_db = db.getUserData(ctx.msg.author)

    if u_db.marry != 'none': db.modifyRecord(50, FakeUser(u_db.marry), value='none')
    if a_db.marry != 'none': db.modifyRecord(50, FakeUser(a_db.marry), value='none')

    db.modifyRecord(50, user,           value=ctx.msg.author.uid)
    db.modifyRecord(50, ctx.msg.author, value=user.uid)
    await ctx.send(f"{ctx.msg.author.nickname}, {user.nickname}, los declaro marido y mujer.\n[c]Puede besar a la novia")
    return
async def fmt(ctx):
    msg = ctx.msg.content.split('\n')

    if len(msg) < 2: return await ctx.send("Debe colocar el mensaje que desee dar formato tras un salto de línea.")

    msg.pop(0)
    
    message = await utils.formatter(ctx, '\n'.join(msg))
    await ctx.send(message)


async def mediaValue(ctx):
    if not ctx.msg.extensions.replyMessage:             return await ctx.send("Debe ejecutar este comando respondiendo a otro")
    if not ctx.msg.extensions.replyMessage.mediaValue:  return await ctx.send("El mensaje no posee mediaValue")
    
    mediaValue      = ctx.msg.extensions.replyMessage.mediaValue
    mediaValueFix   = mediaValue.replace('narvii', 'aminoapps')


    await ctx.client.send_message(message=f"Normal: {mediaValue}\n\nArreglado: {mediaValueFix}", chat_id=ctx.msg.threadId, linkSnippetRaw=mediaValueFix)


async def fromSticker(ctx):
    if not ctx.msg.extensions.replyMessage:             return await ctx.send("Debe ejecutar este comando respondiendo a otro")
    if not ctx.msg.extensions.replyMessage.mediaValue:  return await ctx.send("El mensaje no posee mediaValue")

    print(ctx.msg.extensions.replyMessage.mediaValue)
    from src.imageSend import send_image, send_gif
    if ctx.msg.extensions.replyMessage.mediaValue.find(".png") != -1: await send_gif(ctx, media=ctx.msg.extensions.replyMessage.mediaValue)
    else                                    : await send_image(ctx, media=ctx.msg.extensions.replyMessage.mediaValue)
    return

async def activeUsers(ctx):
    users = await ctx.client.get_online_users(start=0, size=100)

    userFormattedList = "\n".join(list(map(lambda user: f'{user.uid} - {user.nickname[:12]}', users)))

    await ctx.send(f"Estos son los usuarios que están activos:\n\n{userFormattedList}"[:2000])


psico_list = [
    "No tienes que hacer esto solo",
    "Busca otras maneras en las cuales canalizar tus fuertes deseo que te llevan aconsumir de forma excesiva",
    "¿Alguna vez has pensado en salir a tocar el pasto?",
    "Dime, ¿te sientes bien contigo mismo?",
    "¿Hay algo que te incomode? Cuéntame",
    "Deberías dejar de lado la vida en Amino y salir a ver si está lloviendo en la esquina",
    "¿Hace cuanto no ves a tus padres y les dices como eres?",
    "Si alguna vez necesitas a alguien, cuenta conmigo",
    "No puedo ayudarte por este medio, pero",
    "Ten presente un par de cosas",
    "¿Te sientes mejor al escuchar esto?",
    "Deja anoto lo que me digas",
    "Necesito que te acomodes, para tener una mejor experiencia.",
    "¿Desde cuando crees que comenzaron tus malestares?",
    "¿Puedes decirme tu nombre?",
    "Ajá, excelente. Cuéntame más",
    "De momento, la sesión queda hasta acá.",
    "¿Alguna pregunta que quieras hacerme?",
    "Soy Santiago, y estoy aquí para ayudarte",
    "Yo no soy Nati, pero...",
    "Huh, ya veo.",
    "Percibo algo raro en ti, mira",
    "Te voy a pedir algo: puedes ser sincero conmigo",
    "¿Cómo prefieres que te llame?",
    "Súper",
    "Me alegro mucho por ti, sí.",
    "¿Quieres lo mejor para tu vida?",
    "No es mucho, pero es algo",
    "No te dejes vencer por la tentación",
    "sé más fuerte",
    "Si nadie te ha dicho te quiero, yo lo haré por ti; Te quiero",
    "Eres una escoria",
    "Hasta un cesto de basuta tiene más modales que tú",
    "Cerdo asqueroso",
    "Voy a avisarle de esto a las autoridades. Dame un momento",
    "Esto que has dicho es demasiado fuerte"
]



async def AP_callback(ctx, ins):
    if   ctx.msg.content.upper().find("-ESCUCHAR") == 0:
        msg = [random.choice(psico_list) for i in range(random.randint(1, 7))]
        await ctx.send('. '.join(msg))
        return False

    elif ctx.msg.content.upper().find("-SALIR") == 0:
        await ctx.send("[ci]Vuelva pronto, u.u.")
        return True
    return False


@utils.waitForMessage(message='*', callback=AP_callback)
async def ayudaPsicologica(ctx):
    user = db.getUserData(user=ctx.msg.author)
    await ctx.send(f"""[ci]Buenas, {ctx.msg.author.nickname}, más conocido/a como {user.alias}

[ci]Se está contactando con el servicio de ayuda psicológica de Nati, ya que hemos detectado comportamiento inusual de su persona, asociado a una fuerte dependencia al Anime y a las chicas neko. Puede elegir las siguientes opciones para su consulta:

[ci]-ESCUCHAR: Seguir en línea. Un psicólogo se pondrá en contacto con usted por medio de Nati.
[ci]-SALIR: Termina la sesión.""")


async def sendLinkInfo(ctx):
    words = ctx.msg.content.split(" ")
    if len(words) < 2: return await ctx.send("Debe colocar un link tras el comando.")
    
    link = words[1]
    linkInfo    = await ctx.client.get_info_link(link=link)
    objectId    = linkInfo.linkInfo.objectId
    objectType  = linkInfo.linkInfo.objectType
    ndcId       = linkInfo.linkInfo.ndcId
    
    ctx.client.set_ndc(ndcId)
    o = None
    if   objectType == 0:   o = await ctx.client.get_user_info(objectId)
    elif objectType == 1:   o = await ctx.client.get_blog_info(objectId)
    elif objectType == 2:   o = await ctx.client.get_wiki_info(objectId)
    ctx.client.set_ndc(ctx.msg.ndcId)

    print(o)
    await ctx.send(str(o)[:2000])


async def getStickerPacksInfo(ctx):
    from src.challenges.test import get_community_stickers
    stickerCollections = await get_community_stickers(ctx)

    own = 0
    stickers = ""
    for stickerPack in stickerCollections:
        if stickerPack.extensions.originalAuthor.uid == ctx.msg.author.uid:
            own += 1
            stickers += f"\n[c]ndc://x{ctx.msg.ndcId}/sticker-collection/{stickerPack.collectionId}"

    await ctx.send(f"[c]Usted es autor de {own} pack de stickers en esta comunidad.\n{stickers}"[:2000])
