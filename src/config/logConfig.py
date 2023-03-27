from src.antispam.data import AS
from src import utils
from src.database import db

async def welcomeCallback(ctx, ins):
    if ins.data['messageId'] == ctx.msg.messageId: return False

    if ctx.msg.content.upper().find("-DESACTIVAR") != -1:
            db.setLogConfig(ctx.msg.ndcId, 'userWelcome', 0)
            await ctx.send("Bienvenida a usuarios desactivada")
            return True
    
    db.setLogConfig(ctx.msg.ndcId, 'userWelcome', 1)
    db.cursor.execute(f'SELECT * FROM WelcomeMsg WHERE comId="{ctx.msg.ndcId}"')
    data = db.cursor.fetchall()
    if data == []:  db.cursor.execute('INSERT INTO WelcomeMsg VALUES (?, ?, "-DEFAULT")', (ctx.msg.ndcId, ctx.msg.content))
    else         :  db.cursor.execute('UPDATE WelcomeMsg SET message=? WHERE comId=?', (ctx.msg.content, ctx.msg.ndcId))

    db.redis.hset(db.r_comWelMsg, f'?{ctx.msg.ndcId}', ctx.msg.content)
    await ctx.send(f"Mensaje de bienvenida activado y fijado a: {ctx.msg.content[:120]}...")
    return True

async def chatWelcomeCallback(ctx, ins):
    if ins.data['messageId'] == ctx.msg.messageId: return False
    
    if ctx.msg.content.upper().find("-CANCELAR") == 0:
        await ctx.send("Ha cancelado la edición del mensaje de bienvenida, :c.")
        return True

    if ctx.msg.content.upper().find("-VER") == 0:
        await ctx.send("Este es el mensaje que tiene para esta comunidad")
        chat = db.getWelcomeMessage(ctx.msg.ndcId, 'CHAT')
        await ctx.send(str(chat))
        return False
    
    db.cursor.execute(f'SELECT chat FROM WelcomeMsg WHERE comId="{ctx.msg.ndcId}"')
    data = db.cursor.fetchall()
    if data == []:  db.cursor.execute('INSERT INTO WelcomeMsg VALUES (?, ?, ?)', (ctx.msg.ndcId, ' ', ctx.msg.content))
    else         :  db.cursor.execute('UPDATE WelcomeMsg SET chat=? WHERE comId=?', (ctx.msg.content, ctx.msg.ndcId))
    await ctx.send(f"Mensaje de bienvenida de chats fijado a: {ctx.msg.content[:120]}...")
    
    db.redis.hset(db.r_chatWelMsg, f'?{ctx.msg.ndcId}', ctx.msg.content)
    return True

@utils.waitForMessage(message="*", callback=welcomeCallback)
async def welcome(ctx, com):
    return {
        "messageId" : ctx.msg.messageId
}

@utils.waitForMessage(message="*", callback=chatWelcomeCallback)
async def chatWelcome(ctx, com):
    return {
        "messageId" : ctx.msg.messageId
    }

welcomeMsg_default = """
Bienvenida de usuarios en muros:
---------------------------------

Cada media hora, Nati pasará revisando si hay usuarios nuevos en la comunidad para darles la bienvenida. Aquellos que ya hayan sido saludados no se les volverá a dar el mensaje, sin embargo, solo se les dará a los miembros más recientes que se hayan unido a la comunidad

Para activarlo:
El siguiente mensaje que coloque será aquel que se les será repartido a los usuarios

Para desactivarlo:
El siguiente mensaje que coloque debe ser el siguiente: -desactivar
"""

chatWelcomeMsg_default = """
Cambiar bienvenida de usuarios en chats:
----------------------------------

El siguiente mensaje que coloque será el que se pondrá como mensaje de bienvenida del bot en esta comunidad. Puede darle formato al mensaje poniendo lo siguiente:

Información general
-------------------------------
(NICK)     : Nick del usuario
(ALIAS)    : Alias del usuario
(USERID)   : Id de usuario
(COMUNIDAD): Nombre de la comunidad

Tiempo
-------------------------------
(HORA.HM)  : hora y minutos
(HORA.HMS) : hora, minutos y segundos
(FECHA.A)  : Año
(FECHA.M)  : Mes
(FECHA.D)  : Día del mes
(FECHA.F)  : Fecha en formato dd/mm/yy

Chat
-------------------------------
(CHAT.NOMBRE) : Nombre del chat
(CHAT.ANFI)   : Nick del anfitrión del chat
(CHAT.COAN.NL): Coanfitriones del chat, separador por salto de línea
(CHAT.COAN.CO): Coanfitriones del chat, separador por comas

Puede solicitar más informacipon si lo desea, tan solo hable con el autor.

Comandos:
-CANCELAR : Cancela la edición
-VER      : Ve el último mensaje de bienvenida guardado
"""

@utils.isStaff
async def logConfig(ctx):
        com = ctx.msg.content.upper().split(" ")
        
        msg = """
Esta opción debe usarse para configurar partes de moderación del bot. No funciona si quien lo efectúa no es staff en la comunidad:
---------------------------

--log -no-warn:
El bot no enviará reportes

--log -wAll   :
El bot enviará todos los reportes (por defecto)

--log -ignore :
EL bot no atacará ante spam de comunidades

--log -strict :
El bot expulsará inmediatamente

--log -normal :
El bot expulsará solo ante pedido (por defecto)

--log -stalk :
El bot revisará a cada momento perfiles de usuarios conectados.

--log -nostalk :
El bot dejará de ser Gran Hermana

--log -onlystaff :
El bot solo reacciona al staff

--log -everyone :
El bot reacciona a todos (por defecto)

--log -disable :
Desactiva el bot

--log -enable :
Reactiva el bot (por defecto)

--log -blogEnable:
El bot revisará recientes en búsqueda de spam

--log -blogEnable:
El bot ya no revisará recientes en búsqueda de spam (por defecto)

--log -beActive
El bot enviará cada 15 minutos una petición para estar activo. Esto significa que será más sensible a spam por privado, a cambio de que puede aparecer en la parte superior de miembros destacados, y esté más propenso a recibir ban de IP

--log -beInactive
El bot permanecerá con estado inactivo (por defecto)
    """
        
        if len(com) == 1: return await ctx.send(msg)
        comId = ctx.msg.ndcId

        if   com[1] == "-NO-WARN":
            db.setLogConfig(comId, 'nowarn', 1)
            msg = "El bot ya no enviará reportes en esta comunidad"

        elif com[1] == "-WALL"   :
            db.setLogConfig(comId, 'nowarn',  0)
            db.setLogConfig(comId, '_ignore', 0)
            msg = "El bot enviará reportes en esta comunidad desde ahora"
        
        elif com[1] == "-IGNORE" :
            db.setLogConfig(comId, '_ignore', 1)
            msg = "El bot dejará el spam de comunidades en la lista negra de los reportes en esta comunidad"

        elif com[1] == "-STRICT" :
            db.setLogConfig(comId, 'ban', 1)
            msg = "El bot expulsará a todo quien registre como amenaza en esta comunidad"

        elif com[1] == "-NORMAL" :
            db.setLogConfig(comId, 'ban', 0)
            msg = "El bot ya no expulsará a todo quien registre como amenaza en esta comunidad"
        
        elif com[1] == "-STALK" :
            db.setLogConfig(comId, 'ban', 1)
            msg = "El bot hará revisiones constantes en esta comunidad en busca de spam."
        
        elif com[1] == "-NOSTALK" :
            db.setLogConfig(comId, 'ban', 0)
            msg = "El bot ya no revisará esta comunidad"

        elif com[1] == "-ONLYSTAFF" :
            db.setLogConfig(comId, 'staff', 1)
            msg = "El bot solo reaccionará al staff en esta comunidad"
        
        elif com[1] == "-EVERYONE" :
            db.setLogConfig(comId, 'staff', 0)
            msg = "El bot reaccionará a todos en esta comunidad"
        
        elif com[1] == "-ENABLE" :
            db.setLogConfig(comId, 'bot', 0)
            msg = "El bot está encendido en esta comunidad"
        
        elif com[1] == "-DISABLE" :
            db.setLogConfig(comId, 'bot', 1)
            msg = "El bot está apagado en esta comunidad"

        elif com[1] == "-BLOGENABLE" :
            db.setLogConfig(comId, 'blogCheck', 1)
            msg = "El bot revisará los blogs recientes de esta comunidad"
        
        elif com[1] == "-BLOGDISABLE" :
            db.setLogConfig(comId, 'blogCheck', 0)
            msg = "El bot ya no revisará los blogs recientes en esta comunidad"

        elif com[1] == "-BEACTIVE" :
            db.setLogConfig(comId, 'active', 1)
            msg = "El bot enviará cada 15 minutos una petición para estar activo. Esto significa que será más sensible a spam por privado, a cambio de que puede aparecer en la parte superior de miembros destacados, y esté más propenso a recibir ban de IP."

        elif com[1] == "-BEINACTIVE" :
            db.setLogConfig(comId, 'active', 0)
            msg = "El bot permancerá con estado inactivo"

        elif com[1] == "-WELCOME" :
            await welcome(ctx, com)
            msg = welcomeMsg_default

        elif com[1] == "-CHAT" :
            await chatWelcome(ctx, com)
            msg = chatWelcomeMsg_default

        return await ctx.send(msg)
