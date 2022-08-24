from src.antispam.data import AS
from src import utils

@utils.isStaff
async def logConfig(ctx):
        com = ctx.msg.content.upper().split(" ")
        
        if len(com) == 1: return """
Esta opción debe usarse para configurar partes de moderación del bot. No funciona si quien lo efectúa no es staff en la comunidad:
---------------------------

--log -no-warn:
El bot no enviará reportes

--log -wAll   :
El bot enviará todos los reportes

--log -ignore :
EL bot no atacará ante spam de comunidades

--log -strict :
El bot expulsará inmediatamente

--log -normal :
El bot expulsará solo ante pedido

--log -stalk :
El bot revisará a cada momento perfiles de usuarios conectados.

--log -nostalk :
El bot dejará de ser Gran Hermana.
    """
        
        msg   = None 
        comId = ctx.msg.ndcId

        if   com[1] == "-NO-WARN":
            if comId not in AS.no_warnings:
                AS.no_warnings.append(comId)
                msg = "El bot ya no enviará reportes en esta comunidad"
            else:
                msg = "El bot actualmente no envía reportes en esta comunidad"

        elif com[1] == "-WALL"   :
            if comId in AS.no_warnings:
                AS.no_warnings.remove(comId)
                msg = "El bot enviará reportes en esta comunidad desde ahora"
                msg = "El bot actualmente envía todos los reportes"
        
            if comId in AS.ignore_coms:
                AS.ignore_coms.remove(comId)

        elif com[1] == "-IGNORE" :
            if comId not in AS.ignore_coms:
                AS.ignore_coms.append(comId)
                msg = "El bot dejará el spam de comunidades en la lista negra de los reportes en esta comunidad"
            else:
                msg = "El bot actualmente no envía reportes por spam de comunidades externas en esta comunidad"

        elif com[1] == "-STRICT" :
            if comId not in AS.ban_no_warn:
                AS.ban_no_warn.append(comId)
                msg = "El bot expulsará a todo quien registre como amenaza en esta comunidad"
            else:
                msg = "El bot actualmente expulsa a toda amenaza en esta comunidad"
        elif com[1] == "-NORMAL" :
            if comId in AS.ban_no_warn:
                AS.ban_no_warn.remove(comId)
                msg = "El bot ya no expulsará a todo quien registre como amenaza en esta comunidad"
            else:
                msg = "El bot actualmente no expulsa a toda amenaza en esta comunidad"
        elif com[1] == "-STALK" :
            if comId not in AS.stalkList:
                AS.stalkList.append(comId)
                msg = "El bot hará revisiones constantes en esta comunidad en busca de spam."
            else:
                msg = "El bot ya está en modo vigilia."
        elif com[1] == "-NOSTALK" :
            if comId in AS.stalkList:
                AS.stalkList.remove(comId)
                msg = "El bot ya no revisará esta comunidad"
            else:
                msg = "El bot actualmente no hace revisiones continuas en la comunidad"

        await AS.save_config()
        print(AS.ban_no_warn)
        print(AS.ignore_coms)
        print(AS.no_warnings)
        return msg
