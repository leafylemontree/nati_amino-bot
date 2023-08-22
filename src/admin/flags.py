from src import utils
from src import objects
from src.database import db

def showGLobalFlags(flag):
    msg = f"""
DeshabilitarBot:      {1 if flag.botDisable            else 0}
DesactivarYincana bot: {1 if flag.yincanaDisable        else 0}
DesactivarEXP:         {1 if flag.expDisable            else 0}
DesactivarMascota:     {1 if flag.petDisable            else 0}
DescativarInteraccion: {1 if flag.interactionDisable    else 0}
ModoStaff:             {1 if flag.staffCommandsEnable   else 0}
HabilitarModeracion:   {1 if flag.moderationEnable      else 0}
ModoDios:              {1 if flag.godMode               else 0}
"""
    return msg

@utils.userTracker("--flags-help")
async def flagsHelp(ctx):
    await ctx.send("""
[b]Banderas de usuario
[c]Estas permiten configurar parámetros de los usuarios para limitar su capacidad de utilizar al bot, o para darse poderes especiales. Estas banderas actuan de modo global.

[cu]DeshabilitarBot:
[c]El usuario no podrá usar el bot. Este no responderá a sus comandos.

[cu]DeshabilitarYincana:
[c]El usuario no podrá usar la Yincana del bot.

[cu]DeshabilitarExp:
[c]El usuario no podrá subir de nivel, ni tampoco tendrá acceso a la experiencia.

[cu]DeshabilitarMascota:
[c]El usuario no podrá interactuar con la mascota en ninguna comunidad.

[cu]DeshabilitarInteracción:
[c]Todos los comandos, salvo los de staff, serán desactivados para ese usuario.

[cu]ModoStaff:
[c]Solo quienes tengan modo staff fuera del staff de la comunidad puede usar estos comandos.

[cu]HabilitarModeracion:
[c]Permite a un usuario que no sea staff el usar los comandos de ban, unban, warn y strike para sancionar.

[cu]ModoDios:
[c]No tomarás el nombre de Jehová tu Dios en vano; porque no dará por inocente Jehová al que tomare su nombre en vano.
""")


@utils.isStaff
@utils.userTracker("--setFlag", ignore=True)
async def setFlag(ctx):
    from src.challenges.validate import isValidUserLink
    com = ctx.msg.content.upper().split(" ")
    if len(com) < 4:    return await ctx.send("Debe ingresar el comando, link del usuario y la bandera que quiere poner al usuario, junto al valor")

    userId = await isValidUserLink(ctx, text=ctx.msg.content)
    if   userId is None:  return await ctx.send("Debe ingresar el link de un usuario") 
    elif userId is False: return await ctx.send("Solo funciona con usuarios") 
    nickname    = await db.getUserNickname(ctx, ctx.msg.ndcId, userId=userId)

    if   com[2] == "DESHABILITARBOT"            : com[2] = objects.USER_FLAGS.botDisable
    elif com[2] == "DESHABILITARYINCANA"        : com[2] = objects.USER_FLAGS.yincanaDisable
    elif com[2] == "DESHABILITAREXP"            : com[2] = objects.USER_FLAGS.expDisable
    elif com[2] == "DESHABILITARMASCOTA"        : com[2] = objects.USER_FLAGS.petDisable
    elif com[2] == "DESHABILITARINTERACCION"    : com[2] = objects.USER_FLAGS.interactionDisable
    elif com[2] == "MODOSTAFF"                  : com[2] = objects.USER_FLAGS.staffCommandsEnable
    elif com[2] == "HABILITARMODERARCION"       : com[2] = objects.USER_FLAGS.moderationEnable
    elif com[2] == "MODODIOS"                   : com[2] = objects.USER_FLAGS.godMode

    if   com[3] == "0"              : com[3] = False
    elif com[3] == "1"              : com[3] = True
    else                            : return await ctx.send("Debe agregar un valor para la bandera. Este puede ser 1 o 0.")

    db.setUserGlobalFlag(userId, com[2], com[3])
    await ctx.send(f"Se han modificado las banderas de {nickname}. {com[2]} ahora tiene valor {com[3]}")
    return

@utils.userId
@utils.userTracker("--flags")
async def getMyGlobalFlags(ctx, userId, msg):
    userInfo    = db.getUserData(None, userId=userId)
    flags       = userInfo.parse_flags()
    nickname    = await db.getUserNickname(ctx, ctx.msg.ndcId, userId=userId)
    msg         = f"Estas son las banderas de {nickname}:\n\n"
    await ctx.send(msg + showGLobalFlags(flags))


