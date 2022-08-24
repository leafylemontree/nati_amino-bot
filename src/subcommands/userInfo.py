from src import objects
from src import utils
from edamino.api import Embed

@utils.userId
async def userInfo(ctx, uid, content):
        user = await ctx.client.get_user_info(uid)

        # print(user)
        role = "Ninguno"
        if   user.role == 0:   role = "Ninguno"
        # elif user.role == 100: role = "Curador"
        elif user.role == 101: role = "Curador"
        elif user.role == 102: role = "Líder"

        dia = ["día", "dias"]
        a = 1
        if user.consecutiveCheckInDays == 1: a = 0
        activo = "No activo"
        if user.onlineStatus == 1: activo = "Conectado"

        usr_db = objects.Database_return()
        usr_db.strToVal( utils.database(1, user.uid) )
        msg = f"""[cu]Información de perfil:
       
Nick: {user.nickname}
Alias: {usr_db.alias}
Estado: {activo}
Nivel: {user.level}
Seguidores: {user.membersCount}
Siguiendo a: {user.joinedCount}
Chek-in: {user.consecutiveCheckInDays} {dia[a]}
Rol: {role}
uid: {user.uid}
Comunidad: {user.aminoId}
Reputación: {user.reputation}
Blogs: {user.blogsCount}
Comentarios: {user.commentsCount}
Unido en: {user.createdTime}
Última modificación: {user.modifiedTime}

[u]Ha recibido: 
    - {usr_db.hugs_r} abrazos. 
    - {usr_db.kiss_r} besos. 
    - {usr_db.pats_r} caricias.
    - {usr_db.doxx_r} doxxeos. 

[u]Ha dado:
    - {usr_db.hugs_g} abrazos.
    - {usr_db.kiss_g} besos.
    - {usr_db.pats_g} caricias.
    - {usr_db.doxx_g} doxeadas.

Este usuario ha hecho {usr_db.kiwi} furias del kiwi.
{usr_db.win}/{usr_db.derr}/{usr_db.draw}. Total: {usr_db.points} puntos.
"""

        embed = Embed(
                title="Información usuario",
                object_type=0,
                object_id=user.uid,
                content=user.nickname
            )

        return await ctx.client.send_message(message=msg,
                                    chat_id=ctx.msg.threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=[user.uid],
                                    embed=embed,
                                    link_snippets_list=None,
                                    reply=None )

        return
