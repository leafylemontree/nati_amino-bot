from .data import Config, register, review
from src import utils

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
                if chatId not in Config.check_on_enter:
                    Config.check_on_enter.append(chatId)
                    out = "Revisión al entrar activada"
            elif  msg[2] in Config._false:
                if chatId in Config.check_on_enter:
                    Config.check_on_enter.remove(chatId)
                    out = "Revisión al entrar desactivada"
        elif msg[1] == "-TIMEOUT":
            if not review('chat', chatId):
                register("temporal", chatId, msg[2])
                out = f"El bot no responderá en este chat por {msg[2]} segundos"
        elif msg[1] == "-WELCOME":
            if    msg[2] in Config._true :
                if chatId in Config.disable_welcome:
                    Config.disable_welcome.remove(chatId)
                    out = "Mensaje de bienvenida activado"
            elif  msg[2] in Config._false:
                if chatId not in Config.disable_welcome:
                    Config.disable_welcome.append(chatId)
                    out = "Mensaje de bienvenida desactivado"
        elif msg[1] == "-GOODBYE":
            if    msg[2] in Config._true :
                if chatId not in Config.enable_goodbye:
                    Config.enable_goodbye.append(chatId)
                    out = "Mensaje de despedida activado"
            elif  msg[2] in Config._false:
                if chatId in Config.enable_goodbye:
                    Config.enable_goodbye.remove(chatId)
                    out = "Mensaje de despedida desactivado"
        elif msg[1] == "-BOT":
            if    msg[2] in Config._true :
                if chatId in Config.disable_bot:
                    Config.disable_bot.remove(chatId)
                    out = "Bot activado"
            elif  msg[2] in Config._false:
                if chatId not in Config.disable_bot:
                    Config.disable_bot.append(chatId)
                    out = "Bot desactivado"
        elif msg[1] == "-SLOW":
            if    msg[2] in Config._true :
                if chatId not in Config.slow_mode:
                    Config.slow_mode.append(chatId)
                    out = "Modo lento activado"
            elif  msg[2] in Config._false:
                if chatId in Config.slow_mode:
                    Config.slow_mode.remove(chatId)
                    out = "Modo lento desactivado"
        elif msg[1] == "-STAFF":
            if    msg[2] in Config._true :
                if chatId not in Config.only_staff:
                    Config.only_staff.append(chatId)
                    out = "Modo solo staff activado"
            elif  msg[2] in Config._false:
                if chatId in Config.only_staff:
                    Config.only_staff.remove(chatId)
                    out = "Modo solo staff desactivado"
        elif msg[1] == "-1984":
            if    msg[2] in Config._true :
                if chatId not in Config.no_fun:
                    Config.no_fun.append(chatId)
                    out = "Modo Orwelliano activado\n\nEra la patrulla de policía encargada de vigilar a la gente a través de los balcones y ventanas. Sin embargo, las patrullas eran lo de menos. Lo que importaba verdaderamente era la Policia del Pensamiento."
            elif  msg[2] in Config._false:
                if chatId in Config.no_fun:
                    Config.no_fun.remove(chatId)
                    out = "Modo Orwelliano desactivado"
        elif msg[1] == "-SAFE":
            if    msg[2] in Config._true :
                if chatId not in Config.safe_mode:
                    Config.safe_mode.append(chatId)
                    out = "Modo seguro activado"
            elif  msg[2] in Config._false:
                if chatId in Config.safe_mode:
                    Config.safe_mode.remove(chatId)
                    out = "Modo seguro desactivado"
        
        Config.write()
        await ctx.send(out)
        return 
