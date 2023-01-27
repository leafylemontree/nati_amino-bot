from src   import utils
from .data import AS
from src.database import db
from time import time

@utils.ban
async def ban_user(ctx, userId, reason):
        user = await ctx.client.get_user_info(user_id=userId)
        
        try:
            await ctx.client.ban(
                        user_id=userId,
                        reason=reason
                    )
            await ctx.send(f"El usuario {user.nickname} ha sido baneado")
        except Exception:
            await ctx.send("No puede banear al usuario")
            return
        
        log = db.getLogConfig(ctx.msg.ndcId)
        if log.threadId:
            await ctx.client.send_message(message=f"""
Se ha baneado a {user.nickname}
Motivo: {reason}
ID: {userId}
----------
Para desbanear, solo responda este mensaje y ponga --unban
""",
                                    chat_id=log.threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None )

        return

@utils.ban
async def unban_user(ctx, userId, reason):
        user = await ctx.client.get_user_info(user_id=userId)
        try:
            await ctx.client.unban(
                        user_id=userId,
                        reason=reason
                    )
            await ctx.send(f"El usuario {user.nickname} ha sido desbaneado")
        except Exception:
            await ctx.send("No puede desbanear al usuario")
            return
       
        log = db.getLogConfig(ctx.msg.ndcId)
        if log.threadId:
            await ctx.client.send_message(message=f"""
Se ha desbaneado a {user.nickname}
ID: {userId}
""",
                                    chat_id=log.threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None )

        return
async def warn(ctx, user_id, reason):
    data = {
        "uid": user_id,
        "title": "Custom",
        "content": reason,
        "attachedObject": {
            "objectId": user_id,
            "objectType": 0
                    },
        "penaltyType": 0,
        "adminOpNote": {},
        "noticeType": 7,
        "timestamp": int(time() * 1000)
        }

    response = await ctx.client.request("POST", "notice", json=data)
    return

async def strike(ctx, user_id, reason):
    data = {
        "uid": user_id,
        "title": "Custom",
        "content": reason,
        "attachedObject": {
            "objectId": user_id,
            "objectType": 0
                    },
        "penaltyType": 1,
        "penaltyValue": 86400,
        "adminOpNote": {},
        "noticeType": 4,
        "timestamp": int(time() * 1000)
        }

    response = await ctx.client.request("POST", "notice", json=data)
    return

@utils.ban
async def warn_user(ctx, userId, reason):
        user = await ctx.client.get_user_info(user_id=userId)

        try:
            await warn(
                        ctx,
                        user_id=userId,
                        reason=reason
                    )
            await ctx.send(f"El usuario {user.nickname} ha sido advertido")
        except Exception as e:
            print(e)
            await ctx.send("No puede sancionar al usuario")
            return

        log = db.getLogConfig(ctx.msg.ndcId)
        if log.threadId:
            await ctx.client.send_message(message=f"""
Se le ha dado una sanción a {user.nickname}
Motivo: {reason}
ID: {userId}
""",
                                    chat_id=log.threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None )
        return

@utils.ban
async def strike_user(ctx, userId, reason):
        user = await ctx.client.get_user_info(user_id=userId)

        try:
            await strike(
                        ctx,
                        user_id=userId,
                        reason=reason
                    )
            await ctx.send(f"El usuario {user.nickname} ha sido advertido")
        except Exception as e:
            print(e)
            await ctx.send("No puede sancionar al usuario")
            return

        log = db.getLogConfig(ctx.msg.ndcId)
        if log.threadId:
            await ctx.client.send_message(message=f"""
Se le ha dado una sanción a {user.nickname}
Motivo: {reason}
ID: {userId}
""",
                                    chat_id=log.threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None )
        return
