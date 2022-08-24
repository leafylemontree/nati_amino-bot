from src import utils

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

@utils.isStaff
async def nati(ctx):
    com = ctx.msg.content.split(" ")
    if len(com) == 1: return await ctx.send("Parámetros disponibles: -setnick, -setpic, -setbio")  

    if   com[1].upper() == "-SETNICK":
        if len(com) > 2:
            com.pop(0)
            com.pop(0)
            await ctx.client.edit_profile(nickname=" ".join(com))
        else           :    await ctx.client.edit_profile(nickname="ไ⃟⁙⁛⃫. ካằꚍו⁛⁅💮⃟⁆⃩⚘ ")
    elif com[1].upper() == "-SETPIC":
        if not ctx.msg.extensions.replyMessage: return await ctx.send("Debe mencionar una imagen")
        await ctx.client.edit_profile(icon=ctx.msg.extensions.replyMessage.mediaValue)
    elif com[1].upper() == "-SETBIO":
        await ctx.client.edit_profile(content=bio)
    
        return