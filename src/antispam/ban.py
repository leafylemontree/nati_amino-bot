from src   import utils
from .data import AS
from src.database import db

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
