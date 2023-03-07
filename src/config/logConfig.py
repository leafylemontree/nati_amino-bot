from src.antispam.data import AS
from src import utils
from src.database import db

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
            db.setLogConfig(comId, 'active', 1)
            msg = "El bot permancerá con estado inactivo"

        return await ctx.send(msg)
