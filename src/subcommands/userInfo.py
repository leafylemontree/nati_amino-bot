from src import objects
from src import utils
from edamino.api import Embed
from src.database import db
import time

async def get_user_checkins(ctx, userId):
    timezone = time.timezone
    resp = await ctx.client.request('GET', f"check-in/stats/{userId}?timezone={-timezone // 1000}")
    return resp['consecutiveCheckInDays']

@utils.userId
async def userInfo(ctx, uid, content):
        user = await ctx.client.get_user_info(uid)

        # print(user)
        role = "Curador" if user.role == 101 else "Líder" if user.role == 102 else "Ninguno"

        checkInDays = await get_user_checkins(ctx, user.uid)
        dia = ["día", "dias"]
        a = 1
        if checkInDays == 1: a = 0
        activo = "No activo" if user.onlineStatus == 0 else "Conectado"


        usr_db = db.getUserData(user)
        marry = None
        if usr_db.marry != 'none':
            try:
                resp = await ctx.client.get_user_info(usr_db.marry)
                marry = resp.nickname
            except:
                marry = 'No está en esta comunidad, unu.'
        msg = f"""[cu]Información de perfil:
       
Nick: {user.nickname}
Alias: {usr_db.alias}
Estado: {activo}
Nivel: {user.level}
Seguidores: {user.membersCount}
Siguiendo a: {user.joinedCount}
Chek-in: {checkInDays} {dia[a]}
Rol: {role}
uid: {user.uid}
Comunidad: {user.aminoId}
Reputación: {user.reputation}
Blogs: {user.blogsCount}
Comentarios: {user.commentsCount}
Unido en: {user.createdTime}
Última modificación: {user.modifiedTime}
Casado con: {'nadie' if marry is None else marry}

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
{usr_db.win}/{usr_db.draw}/{usr_db.lose}. Total: {usr_db.points} puntos.
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
