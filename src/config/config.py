from .data import Config, register, review
from src import utils
from src.database import db

@utils.isStaff
async def config(ctx):
        global temporal_disable
        msg     = ctx.msg.content
        msg     = msg.upper().split(" ")
        chatId  = ctx.msg.threadId

        if len(msg) == 1: return "Ayuda sobre configuración"
        if len(msg) == 2: return "Ayuda sobre esa función"

        out = None 

        if   msg[1] == "-CHECK":
            if    msg[2] in Config._true :
                    db.setChatConfig(chatId, "_check", 1, ctx.msg.ndcId)
                    out = "Revisión al entrar activada"
            elif  msg[2] in Config._false:
                    db.setChatConfig(chatId, "_check", 0, ctx.msg.ndcId)
                    out = "Revisión al entrar desactivada"

        elif msg[1] == "-TIMEOUT":
            if not review('chat', chatId):
                register("temporal", chatId, msg[2])
                out = f"El bot no responderá en este chat por {msg[2]} segundos"

        elif msg[1] == "-WELCOME":
            if    msg[2] in Config._true :
                    db.setChatConfig(chatId, "welcome", 0, ctx.msg.ndcId)
                    out = "Mensaje de bienvenida activado"
            elif  msg[2] in Config._false:
                    db.setChatConfig(chatId, "welcome", 1, ctx.msg.ndcId)
                    out = "Mensaje de bienvenida desactivado"

        elif msg[1] == "-GOODBYE":
            if    msg[2] in Config._true :
                    db.setChatConfig(chatId, "goodbye", 1, ctx.msg.ndcId)
                    out = "Mensaje de despedida activado"
            elif  msg[2] in Config._false:
                    db.setChatConfig(chatId, "goodbye", 0, ctx.msg.ndcId)
                    out = "Mensaje de despedida desactivado"

        elif msg[1] == "-BOT":
            if    msg[2] in Config._true :
                    db.setChatConfig(chatId, "bot", 0, ctx.msg.ndcId)
                    out = "Bot activado"
            elif  msg[2] in Config._false:
                    db.setChatConfig(chatId, "bot", 1, ctx.msg.ndcId)
                    out = "Bot desactivado"

        elif msg[1] == "-SLOW":
            if    msg[2] in Config._true :
                    db.setChatConfig(chatId, "slow", 1, ctx.msg.ndcId)
                    out = "Modo lento activado"
            elif  msg[2] in Config._false:
                    db.setChatConfig(chatId, "slow", 0, ctx.msg.ndcId)
                    out = "Modo lento desactivado"

        elif msg[1] == "-STAFF":
            if    msg[2] in Config._true :
                    db.setChatConfig(chatId, "staff", 1, ctx.msg.ndcId)
                    out = "Modo solo staff activado"
            elif  msg[2] in Config._false:
                    db.setChatConfig(chatId, "staff", 0, ctx.msg.ndcId)
                    out = "Modo solo staff desactivado"

        elif msg[1] == "-1984":
            if    msg[2] in Config._true :
                    db.setChatConfig(chatId, "nofun", 1, ctx.msg.ndcId)
                    out = "Modo Orwelliano activado\n\nEra la patrulla de policía encargada de vigilar a la gente a través de los balcones y ventanas. Sin embargo, las patrullas eran lo de menos. Lo que importaba verdaderamente era la Policia del Pensamiento."
            elif  msg[2] in Config._false:
                    db.setChatConfig(chatId, "nofun", 0, ctx.msg.ndcId)
                    out = "Modo Orwelliano desactivado"

        elif msg[1] == "-SAFE":
            if    msg[2] in Config._true :
                    db.setChatConfig(chatId, "safe", 1, ctx.msg.ndcId)
                    out = "Modo seguro activado"
            elif  msg[2] in Config._false:
                    db.setChatConfig(chatId, "safe", 0, ctx.msg.ndcId)
                    out = "Modo seguro desactivado"
        
        await ctx.send(out)
        return 
