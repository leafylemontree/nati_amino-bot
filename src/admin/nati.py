from src import utils
from src.text import reload as textReload
from src import subcommands
from src import objects

bio = """
[c]°•○●°•○●°•○●°•○●°•○●°•○●°•○●°•○●°•○●°•○●

[IMG=H7I]

[cbu]Hola, bella personita.
[c]↜∗≖≖≖≖∗↝☬↜ ∗≖≖≖≖∗↝

[c]Soy Nati, un bot creado por Leafy, el cual les proporcionará entretenimiento a ustedes, así como poder ayudar con seguridad en chats y algunas otras funciones que se irán añadiendo en el futuro.

[c]Ante consultas, contactar con [el autor y responsable.| http://aminoapps.com/u/Pink93 ]

[c]Si tiene dudas sobre el código del bot o quisiera echar un ojo para ver si no hay acciones maliciosas, puede revisar el repositorio de Github: [Aqui|https://github.com/leafylemontree/nati_amino-bot]

[c]Aquí les dejo algunos comandos útiles que le podrán ayudar.

[cb]--help
[c]——————«•»——————
[c]Muestra la lista de comandos del bot.

[cb]--help (comando)
[c]——————«•»——————
[c]Da una explicación detallada con ejemplo sobre lo que hace cada comando.

[cb]--sigueme
[c]——————«•»——————
[c]El bot le seguirá. Utilice esto para añadirlo a un chat tanto público como privado.

[cb]--info
[c]——————«•»——————
[c]Muestra su información de usuario.

[c]

[cb]Algunas recomendaciones:
[c]↜∗≖≖≖≖∗↝☬↜ ∗≖≖≖≖∗↝

[c]No poner el bot en un chat el cual sea importante, esto, ya que constantemente se hace mantenimiento del bot y puede que algo de lo que se converse en el chat pueda ser visto.

[c]No abusar de las funciones del bot.

[c]Ante cualquier anomalía, avisar al autor del bot.

[IMG=8CX]

[c]°•○●°•○●°•○●°•○●°•○●°•○●°•○●°•○●°•○●°•○"""

DEFAULT_NICK = "ไ⃟⁙⁛⃫. ካằꚍו⁛⁅💮⃟⁆⃩⚘ "

async def setProfileFromWiki(ctx):
    args = ctx.msg.content.split(" ")
    if len(args) < 3:   return await ctx.send("Debe añadir el enlace de una wiki tras el comando.")

    link = await ctx.client.get_info_link(args[2])
    if link.linkInfo.objectType != 2: return await ctx.send("El link que ingrese debe ser de una wiki.")

    wiki = await ctx.client.get_wiki_info(wiki_id=link.linkInfo.objectId)
    print(wiki)
    await ctx.client.edit_profile(
                nickname            = wiki.label,
                content             = wiki.content,
                icon                = wiki.mediaList[0][1],
                image_list_raw      = wiki.mediaList,
                background_color    = wiki.extensions['style']['backgroundColor'] if "backgroundColor" in wiki.extensions['style'].keys() else None,
                background_image    = wiki.extensions['style']['backgroundMediaList'][0][1] if "backgroundMediaList" in wiki.extensions['style'].keys() else None
            )
    await ctx.send("Perfil cambiado.")


@utils.isStaff
@utils.userTracker("admin")
async def nati(ctx):
    com = ctx.msg.content.split(" ")
    if len(com) == 1: return await ctx.send("""
Este comando se utiliza para cambiar la apariencia del bot, principalmente.

Nombre: --admin -setnick (nombre)
Biografía: --admin -setbio (biografía)
Color del fondo: --admin -setbg (color en hexadecimal)

Los siguientes comandos se utilizan respondiendo a una imagen que haya enviado anteriormente en el chat.
Foto de perfil: --admin -setpic
Banner: --admin -setbanner
Foto del fondo: --admin --setbg

Adicionalmente, puede cargar el perfil desde una wiki:
--admin -setprofilefromwiki""")  

    if   com[1].upper() == "-SETNICK":
        if len(com) > 2:
            com.pop(0)
            com.pop(0)
            await ctx.client.edit_profile(nickname=" ".join(com))
            await ctx.send(f"Nick cambiado a: {' '.join(com)}")
        else :
            await ctx.client.edit_profile(nickname=DEFAULT_NICK)
            await ctx.send(f"Nick cambiado a: {DEFAULT_NICK}")
    elif com[1].upper() == "-SETPICURL":
        url = ctx.msg.content.split(" ")[-1]
        await ctx.client.edit_profile(icon=url)
        await ctx.send(f"Imagen de perfil cambiada a: {url}")
    elif com[1].upper() == "-SETPIC":
        if not ctx.msg.extensions.replyMessage: return await ctx.send("Debe usar este comando respondiendo a una imagen")
        if not ctx.msg.extensions.replyMessage.mediaValue: return await ctx.send("Solo funciona este comando si responde a una imagen")
        raw = await utils.getImageBytes(ctx, ctx.msg.extensions.replyMessage.mediaValue)
        url = await ctx.client.upload_media(raw, "image/jpg")
        await ctx.client.edit_profile(icon=url)
        await ctx.send(f"Imagen de perfil cambiada a: {url}")
    elif com[1].upper() == "-SETBANNER":
        if not ctx.msg.extensions.replyMessage: return await ctx.send("Debe usar este comando respondiendo a una imagen")
        if not ctx.msg.extensions.replyMessage.mediaValue: return await ctx.send("Solo funciona este comando si responde a una imagen")
        await ctx.client.edit_profile(image_list=[ctx.msg.extensions.replyMessage.mediaValue])
        await ctx.send(f"Imagen secunadria del perfil cambiada a: {ctx.msg.extensions.replyMessage.mediaValue}")
    elif com[1].upper() == "-SETBG":
        if not ctx.msg.extensions.replyMessage and len(com) < 3: return await ctx.send("Debe usar este comando respondiendo a una imagen, o bien ingresando un valor hexadecimal para el color")
        if ctx.msg.extensions.replyMessage:
            await ctx.client.edit_profile(background_image=ctx.msg.extensions.replyMessage.mediaValue)
            await ctx.send(f"Imagen de fondo cambiada a: {ctx.msg.extensions.replyMessage.mediaValue}")
        else:
            await ctx.client.edit_profile(background_color=com[2])
            await ctx.send(f"Color del perfil cambiado a: {com[2]}")

    elif com[1].upper() == "-SETBIO":
        content = bio
        if len(com) > 2:
            com.pop(0)
            com.pop(0)
            content = " ".join(com)
        await ctx.client.edit_profile(content=content)
        await ctx.send("Biografía cambiada.")
    
    elif com[1].upper() == "-SETPROFILEFROMWIKI":
        await setProfileFromWiki(ctx)

    elif com[1].upper() == "-RELOADTEXT":
        textReload()
    elif com[1].upper() == "-CLEARAWAITER":
        await utils.clearAW(ctx)
    elif com[1].upper() == "-RELOADQUESTIONS":
        subcommands.updateQuestions()
        await ctx.send("Preguntas recargadas")
    elif com[1].upper() == "-RESETSUBTASKTIMER":
        await utils.st.reset(ctx)
        await ctx.send("Contador de subtareas reiniciado")
    elif com[1].upper() == "-ASKSUBTASKTIMER":
        await ctx.send(f"Contador: {utils.st.timeCounter}")
    return

@utils.userTracker("uptime")
async def uptime(ctx):
    import time
    from src.subcommands.trivia.trivia import parseTime
    import datetime

    seconds   = time.time() - objects.ba.timestamp
    timedelta = datetime.timedelta(seconds=seconds)
    time_repr = parseTime(timedelta)

    await ctx.send(f"[c]Nati instancia {objects.ba.instance + 1} ha estado activa por:\n[c]{time_repr}")
