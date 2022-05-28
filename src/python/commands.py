import json
from random import random
from edamino import Bot, Context, logger, Client
from edamino.objects import UserProfile
from edamino.api import Embed
import math
from local_webscraping import web_tools
import bot_objects
from c_func import c
import bot_objects as bot_o


print("Login open")
status = bot_o.Status()

with open("src/json/text.json", "r") as textFile:
    msg_text = json.load(textFile)
    print("Texto cargado")

class commands:

    def log():
        global bot
        with open("src/json/login.json", "r") as loginFile:
            loginData = json.load(loginFile)

        bot = Bot(email=loginData['username'], password=loginData['password'], prefix=loginData['prefix'])
        bot.start();
        print("Session logged in!")
        return loginData, bot;

    async def message(ctx: Context):
        global status, msg_text
        reply = bot_o.Reply(None, False)

        try: print(f"--------------------------------\n{ctx.msg.author.nickname}\n{ctx.msg.content}\n{ctx.msg.isHidden} {ctx.msg.type}")
        except: pass
        # print(f"--------------------------------\n{ctx.msg}")

        if ctx.msg.type == 101:                                                     return         await subCommands.enter(ctx)
        elif ctx.msg.type == 102:                                                   return         await subCommands.leave(ctx)
        elif ctx.msg.type in [108, 109, 113, 114] :                                                   return         await subCommands.strange(ctx)


        msg = ctx.msg.content;
        nick = ctx.msg.author.nickname;
        if msg is None: return None;
        com = msg.upper()

        if ctx.msg.author.uid in status.wordle.get_users() :                               reply = await commands.wordle(ctx, com)

        if   com.find("NATI") == 0:                                                 reply.msg = "¿Me llamaban? Utiliza --help para ver mis comandos, uwu."
        elif com.find("--NANO") == 0 :                                              reply.msg = msg_text['nano']
        elif msg.find("http://aminoapps.com/c/Manhvi") == 0:                        reply.msg = "¡Alto ahi!\n\nEse mensaje parece ser spam."
        elif com.find("--WORDLE") == 0:                                             reply     = await commands.wordle(ctx, com)
        elif ((com.find("--SIGUEME") == 0) | (com.find("--SÍGUEME") == 0)) :        reply     = await subCommands.follow(ctx)
        elif com.find("--CHAT") == 0:                                               reply.msg = web_tools.generateText(msg[7:])
        elif com.find("--BIBLIA") == 0:                                             reply.msg = web_tools.bible(msg)
        elif ((com.find("--HOROSCOPO")==0)|(com.find("--HORÓSCOPO")==0)):           reply.msg = web_tools.horoscopo(msg)
        elif com.find("--CARTA") == 0                                   :           reply.msg = web_tools.birthChart(msg)
        elif com.find("--LETRA") == 0                                   :           reply.msg = web_tools.lyrics(msg)
        elif com.find("--DEF") == 0:                                                reply.msg = web_tools.definition(msg)
        elif com.find("--MATRIX") == 0:                                             reply.msg = c.matrix(com)
        elif com.find("--ALIAS") == 0:                                              reply.msg = await subCommands.alias(ctx, msg)
        # elif com.find("--GHOST") == 0:                                              reply.msg = await subCommands.ghost(ctx, msg)
        elif com.find("--CUTES") != -1:                                             reply     = await commands.cutes(ctx, com)
        elif com.find("--COPYPASTE") != -1 :                                        reply     = await commands.copypaste(ctx, msg)
        elif com.find("--JOIN") == 0:                                               reply     = await subCommands.join(ctx, msg)
        # elif com.find("--CHAT") != -1:                                              print(await ctx.get_chat_info())
        elif com.find("--MATH") == 0:                                               reply     = subCommands.replyMsg( c.math(com) )
        # elif com.find("--MATH") == 0:                                               reply.msg = "El comando math está deshabilitado por el momento, ya que está en mantención.\n\nLamentamos las molestias."
        elif com.find("--BLOGS") == 0:                                              reply     = await subCommands.getBlogs(ctx, com)
        elif com.find("--INFO") == 0 :                                              reply     = await subCommands.userInfo(ctx)
        elif com.find("PLEBEYOS") != -1 :                                           reply.msg = f"{msg_text['plebeyos']} {nick}"
        elif com.find("LA NAVE") != -1 :                                            reply.msg = msg_text['la_nave']
        elif com.find("--HELP") == 0:                                               reply     = subCommands.help(msg)
        elif com == "--NOMBRE":                                                     reply.msg = f"[c]Tu nombre es:\n\n[c]{nick}";
        elif ((msg.find("--say") < 5) & (msg.find("--say") != -1)) :                reply.msg = msg[6:]
        elif ((com.find("KIWILATIGO") != -1) | (com.find("KIWILÁTIGO") != -1)):     reply.msg = f"[ci]¡Oh no! Han hecho enfadar a {nick}\n\n[ci]/c skpa."
        elif com.find("--NORMAS") == 0  :                                           reply.msg = msg_text['normas']
        elif msg.find("--Mensaje Oculto") == 0 :                                    reply.msg = msg_text['msg_oculto']
        elif msg.find("👀") != -1:                                                  reply     = subCommands.replyMsg(msg_text['ojos'])
        elif msg.find("Toy Chica") != -1 :                                          reply     = subCommands.replyMsg(msg_text['toy_chica'])
        elif com.find("HOLA NATI") != -1 :                                          reply     = subCommands.replyMsg(f"{msg_text['hola']} {nick}.")
        elif com.find("UWU") != -1 :                                                reply     = subCommands.replyMsg(msg_text['uwu'])
        elif com.find("--PLATYPUS") == 0:                                           reply.msg = msg_text['platypus'][int(random() * 2)]
        elif com.find("--METH") == 0:                                               reply.msg = msg_text['meth']
        elif com.find("--DADOS") == 0:                                              reply     = subCommands.dices(msg)
        # elif com.find("--SUS") == 0:                                                reply['audio'] = 'media/amongus.mp3'
        elif com.find("--DOXX") == 0:                                               reply     = await commands.doxx(ctx, 0)
        elif com.find("DOXXEA A") != -1:                                            reply     = await commands.doxx(ctx, 1)
        elif com.find("BOKU NO PICO") != -1:                                        reply.msg = "[ci]Boku no pico el besto anime 10/10. La historia es muy romántica y emotiva. Recomendadísimo por Epstein y compañía."
        elif ((msg.find(":v") != -1) | (msg.find(" momo ") != -1) | (msg.find("xdxdxd") != -1) | (msg.find("momazo") != -1) | (msg.find("memingo") != -1) | (msg.find("v:") != -1) | (msg.find(" elfa ") != -1) | (msg.find(" alv ") != -1)) : reply = await subCommands.kick(ctx, msg_text['grasa'])


        if   ((reply.msg is not None) & (reply.reply is True))           : await ctx.reply(reply.msg)
        elif ((reply.msg is not None) & (reply.reply is False))          : await ctx.send(reply.msg)
        return None;

    async def mention(ctx: Context):
        await ctx.send("¿Me han llamado?")
        return None

    def math_func(msg):
    #     data = msg.split(" ")
    #
    #     if data[1] == "ADD" :
    #         proc = subCommands.checkInput_math(2, data)
    #         if proc is not True: return subCommands.error(proc)
    #         msg = str(data[2] + data[3])
    #     elif data[1] == "SUB" :
    #         proc = subCommands.checkInput_math(2, data)
    #         if proc is not True: return subCommands.error(proc)
    #         msg = str(data[2] - data[3])
    #     elif data[1] == "MUL" :
    #         proc = subCommands.checkInput_math(2, data)
    #         if proc is not True: return subCommands.error(proc)
    #         msg = str(data[2] * data[3])
    #     elif data[1] == "DIV" :
    #         proc = subCommands.checkInput_math(2, data)
    #         if proc is not True: return subCommands.error(proc)
    #         if data[3] == 0 : return subCommands.error(2402)
    #         msg = str(data[2] / data[3])
    #     elif data[1] == "POW" :
    #         proc = subCommands.checkInput_math(2, data)
    #         if proc is not True: return subCommands.error(proc)
    #         msg = str(data[2] ** data[3])
    #     elif data[1] == "SQR" :
    #         proc = subCommands.checkInput_math(1, data)
    #         if proc is not True: return subCommands.error(proc)
    #         if data[2] < 0 : return subCommands.error(2403)
    #         msg = str(math.sqrt(data[2]))
    #     elif data[1] == "TABLE":
    #         if len(data) < 5: return error_2400
    #         try:    data[4] = float(data[4])
    #         except:  return error_2401
    #         # min = data[2]
    #         # max = data[3]
    #         # step = data[4]
    #         # func = data[5]
    #         msg = calculate_table(data)
    #     elif data[1].find("{") != -1:
    #         data = msg.split("\n")
    #
    #         msg = ""
    #         vars = {}
    #         count = 1
    #         for line in data:
    #             count += 1
    #             print(f"line: {line}")
    #             op = line.split(" ")
    #             ls = []
    #             for i in range(len(op)):
    #                 if op[i] != "" : ls.append(op[i])
    #
    #             if ls[0] == "VAR":
    #                 if ((ls[2] in vars) is True) : vars[ls[1]] = vars[ls[2]]
    #                 else: vars[ls[1]] = int(ls[2]);
    #                 print(f"created variable {ls[1]} with value {str(vars[ls[1]])}")
    #             elif ls[0] == "ADD":
    #                 if ((ls[1] in vars) is False) : return f"Line: {count}\nCommand:{line}\n\n{subCommands.error(2404)}"
    #                 if ((ls[2] in vars) is True) : vars[ls[1]] = vars[ls[1]] + vars[ls[2]]
    #                 else:
    #                     try:  a = int(ls[2])
    #                     except: return f"Line: {count}\nCommand:{line}\n\n{subCommands.error(2401)}"
    #                     vars[ls[1]] = vars[ls[1]] + a
    #             elif ls[0] == "SUB":
    #                 if ((ls[1] in vars) is False) : f"Line: {count}\nCommand:{line}\n\n{subCommands.error(2404)}"
    #                 if ((ls[2] in vars) is True) : vars[ls[1]] = vars[ls[1]] - vars[ls[2]]
    #                 else:
    #                     try:  a = int(ls[2])
    #                     except: return f"Line: {count}\nCommand:{line}\n\n{subCommands.error(2401)}"
    #                     vars[ls[1]] = vars[ls[1]] - a
    #             elif ls[0] == "MUL":
    #                 if ((ls[1] in vars) is False) : f"Line: {count}\nCommand:{line}\n\n{subCommands.error(2404)}"
    #                 if ((ls[2] in vars) is True) : vars[ls[1]] = vars[ls[1]] * vars[ls[2]]
    #                 else:
    #                     try:  a = int(ls[2])
    #                     except: return f"Line: {count}\nCommand:{line}\n\n{subCommands.error(2401)}"
    #                     vars[ls[1]] = vars[ls[1]] * a
    #             elif ls[0] == "DIV":
    #                 if ((ls[1] in vars) is False) : f"Line: {count}\nCommand:{line}\n\n{subCommands.error(2404)}"
    #                 if ((ls[2] in vars) is True) :
    #                     if vars[ls[2]] == 0: return f"Line: {count}\nCommand:{line}\n\n{subCommands.error(2402)}"
    #                     vars[ls[1]] = vars[ls[1]] / vars[ls[2]]
    #                 else:
    #                     try:  a = int(ls[2])
    #                     except: return f"Line: {count}\nCommand:{line}\n\n{subCommands.error(2401)}"
    #                     if a == 0: return f"Line: {count}\nCommand:{line}\n\n{subCommands.error(2402)}"
    #                     vars[ls[1]] = vars[ls[1]] / a
    #             elif ls[0] == "POW":
    #                 if ((ls[1] in vars) is False) : return f"Line: {count}\nCommand:{line}\n\n{subCommands.error(2404)}"
    #                 if ((ls[2] in vars) is True) : vars[ls[1]] = vars[ls[1]] ** vars[ls[2]]
    #                 else:
    #                     try:  a = int(ls[2])
    #                     except: return f"Line: {count}\nCommand:{line}\n\n{subCommands.error(2401)}"
    #                     vars[ls[1]] = vars[ls[1]] ** a
    #             elif ls[0] == "SQR":
    #                 if ((ls[1] in vars) is False) : return f"Line: {count}\nCommand:{line}\n\n{subCommands.error(2404)}"
    #                 if (vars[ls[1]] < 0) : return f"Line: {count}\nValue of {ls[1]}: {vars[ls[1]]}\nCommand:{line}\n\n{subCommands.error(2403)}"
    #                 vars[ls[1]] = math.sqrt(vars[ls[1]])
    #             elif ls[0] == "PRINT":
    #                 if ((ls[1] in vars) is False) : return f"Line: {count}\nCommand:{line}\n\n{subCommands.error(2404)}"
    #                 msg += f"{ls[1]} = {str(vars[ls[1]])}\n"
    #             elif ls[0] == "#":
    #                 msg += ""
    #     return msg;
        return None;
    async def doxx(ctx, mode):
        uid = ctx.msg.author.uid
        nick = ctx.msg.author.nickname
        arr = ctx.msg.extensions.mentionedArray

        msg = ""
        if arr is None:
            msg = f"[cb]Doxxeando a:\n[c]{nick}\n"
            key = 0;
            uid2 = ""
            for i in uid:
                key = (key << 4) ^ (ord(i) & 0xFF)
                uid2 += chr(ord(i) ^ 0x42);
            key = key & 0xFFFFFFFF
            msg += f"\n[c]uid: {uid}"
            msg += f"\n[c]IP: {(key >> 24) & 0xFF}.{(key >> 16) & 0xFF}.{(key >> 8) & 0xFF}.{key & 0xFF}."
        else:
            msg = f"[cb]Doxxeando a:"
            for i in arr:
                user = await subCommands.getUser(i.uid, ctx)
                uid = i.uid
                key = 0;
                uid2 = ""
                msg += f"\n[c]{user.nickname}\n"
                for i in uid:
                    key = (key << 4) ^ (ord(i) & 0xFF)
                    uid2 += chr(ord(i) ^ 0x42);
                key = key & 0xFFFFFFFF
                msg += f"\n[c]uid: {uid}"
                msg += f"\n[c]IP: {(key >> 24) & 0xFF}.{(key >> 16) & 0xFF}.{(key >> 8) & 0xFF}.{key & 0xFF}\n"


        return bot_o.Reply(msg, False)
    async def copypaste(ctx, msg):
        with open("src/json/database.json", "r+") as hard_data:
            database = json.load(hard_data)
        reply = bot_o.Reply(None, False)

        com = msg.upper()
        msg = msg.split(" ")
        com = com.split(" ")
        msg = list(filter(("").__ne__, msg))
        num = -1

        if len(msg) < 1: text = database['copypaste']['default']
        elif com[1] == "-MK" :
            msg = msg[2:]
            msg = ' '.join(msg)
            database['copypaste']['stored'].append(msg)
            with open("src/json/database.json", "w+") as hard_data:
                json.dump(database, hard_data)
            reply.msg = f"Mensaje guardado en la posición {len(database['copypaste']['stored'])}."

        elif com[1] == "-RM" :
            try: num = int(msg[2])
            except:
                reply.msg = subCommands.error(2401)
                return reply
            database['copypaste']['stored'].pop(num-1)
            with open("src/json/database.json", "w+") as hard_data:
                json.dump(database, hard_data)

            reply.msg = f"Mensaje número {num} eliminado de la base de datos."
        elif com[1] == "-DS" :
            try: num = int(msg[2])
            except:
                reply.msg = subCommands.error(2401)
                return reply
            if database['copypaste']['stored'][num -1].find("{{--DIS--}}") == -1:
                database['copypaste']['stored'][num -1] = "{{--DIS--}}" + database['copypaste']['stored'][num -1]
                with open("src/json/database.json", "w+") as hard_data:
                    json.dump(database, hard_data)
                reply.msg = f"Mensaje número {num} deshabilitado de la base de datos."
            elif database['copypaste']['stored'][num-1].find("{{--DIS--}}") == 0:
                database['copypaste']['stored'][num-1] = database['copypaste']['stored'][num-1][11:]
                with open("src/json/database.json", "w+") as hard_data:
                    json.dump(database, hard_data)
                reply.msg = f"Mensaje número {num} habilitado."
        else:
            try: num = int(msg[1])
            except:
                reply.msg = subCommands.error(2401)
                return reply

            if num > len(database['copypaste']['stored']) :
                    num = len(database['copypaste']['stored'])
                    reply.msg = f'Número ingresago {msg[1]} es mayor a la cantidad almacenada. Regresando el último mensaje:\n\n'
            if database['copypaste']['stored'][num -1].find("{{--DIS--}}") == 0:
                reply.msg = "Este mensaje está deshabilitado."
                return reply

            reply.msg += f"{num}.-\n{database['copypaste']['stored'][num - 1]}"

        return reply
    async def cutes(ctx, msg):
        reply = bot_o.Reply(None, True)

        com = msg.upper()
        com = com.split(" ")
        com = list(filter(("").__ne__, com))
        user = await subCommands.getUser(ctx.msg.extensions.mentionedArray[0].uid, ctx)
        print(user.nickname)
        num = int(random() * 4)
        print(f"num = {num}")

        # await subCommands.embedImage(ctx, gif)

        if com[1] == "-KISS":
            with open(f'media/cutes/kiss/{str(num)}.gif', 'rb') as file:
                 gif = file.read()
                 await ctx.send_gif(gif)

            c.database(12, user.uid)
            c.database(22, ctx.msg.author.uid)
            reply.msg = f"{ctx.msg.author.nickname} le da un beso a {user.nickname}"
        elif com[1] == "-HUG":
            with open(f'media/cutes/hug/{str(num)}.gif', 'rb') as file:
                 gif = file.read()
                 await ctx.send_gif(gif)

            c.database(11, user.uid)
            c.database(21, ctx.msg.author.uid)
            reply.msg = f"{ctx.msg.author.nickname} le da un abrazo a {user.nickname}"
        elif com[1] == "-PAT":
            with open(f'media/cutes/pat/{str(num)}.gif', 'rb') as file:
                 gif = file.read()
                 await ctx.send_gif(gif)

            c.database(13, user.uid)
            c.database(23, ctx.msg.author.uid)
            reply.msg = f"{ctx.msg.author.nickname} acaricia a {user.nickname}"
        return reply
    async def wordle(ctx, msg):
        global status

        reply = bot_o.Reply(None, True)


        msg = msg.split(" ")
        if len(msg) == 2:
            if ((msg[0] == "--WORDLE") & (msg[1] == "-INIT")):
                if ctx.msg.author.uid in status.wordle.get_users():  return subCommands.replyMsg("Usted ya está ingresado")
                status.wordle.new_instance(ctx.msg.author.uid)
                reply.msg = f"[cb]Wordle\n\nNuevo usuario registtrado:\nNick:{ctx.msg.author.nickname}\n\n[c]"
                for i in status.wordle.word: reply.msg += "_   "
                return reply
            elif ((msg[0] == "--WORDLE") & (msg[1] == "-INFO")) :
                return subCommands.replyMsg("Placeholder normas")
            elif ((msg[0] == "--WORDLE") & (msg[1] == "-WORD")) :
                word = c.get_word(status.wordle.diff);
                status.wordle.change_word(word)
                reply.msg = "La palabra ha sido cambiada. ¿Podrán resolverla ahora? uwu."
                return reply
            else:
                try:
                    number = int(msg[1])
                    if ((number < 4) | (number > 20)):
                        reply.msg = "Esa longitud no es válida. Pruebe con una entre 4 y 20"
                        return reply
                    status.wordle.set_difficulty(number)
                    reply.msg = f"La dificultad ha sido cambiada a {status.wordle.diff}"
                except:
                    reply.msg = False

        elif len(msg) == 4:
            if ((msg[0] == "--WORDLE") & (msg[1] == "SUDO") & (msg[2] == "-WORD")):
                status.wordle.change_word(msg[3])
                return subCommands.replyMsg(f"Palabra cambiada por {status.wordle.word}")
        else:
            if msg[0] == "--WORDLE" :
                return subCommands.replyMsg("Los comandos disponibles para esta función son:\n\n-INIT: inicia el juego\n-INFO: entrega las normas")
            if msg[0] == "-EXIT":
                index = 0
                for i, j in enumerate(status.wordle.instance):
                    if j.uid == ctx.msg.author.uid :
                        status.wordle.instance.pop(i)
                        break
                return subCommands.replyMsg(f"[c]{ctx.msg.author.nickname} se ha retirado.")
            else:
                index = 0
                for i, j in enumerate(status.wordle.instance):
                    if j.uid == ctx.msg.author.uid :
                        index = i
                        break
                if ((len(msg[0]) != len(status.wordle.word)) & (msg[0].find("//") == -1)) : return subCommands.replyMsg("La palabra ingresada no es válida")

                status.wordle.instance[index].data.append(msg[0])

                reply.msg = f"[cb]Wordle:\n[c]{ctx.msg.author.nickname}\n\n"
                for i in status.wordle.instance[index].data:
                    reply.msg += "\n[c]: "
                    for a, j in enumerate(i):
                        if j == status.wordle.word[a]: reply.msg += f"[{j}]  "
                        else: reply.msg += f" {j}   "
                    reply.msg += "   :"

                    if i == status.wordle.word:
                        status.wordle.instance.pop(index)
                        reply.msg += f"\n\n[c]¡{ctx.msg.author.nickname} ha ganado!"
                        return reply

                if len(status.wordle.instance[index].data) > status.wordle.step_cnt:
                    status.wordle.instance.pop(index)
                    return subCommands.replyMsg(f"[c]{ctx.msg.author.nickname} ha perdido.")

        return reply

class subCommands:
    global msg_text
    msg_error = {
        "error_2400" : "Error 2400: No ha ingresado los parámetros suficientes para el comando 'math'.",
        "error_2401" : "Error 2401: Uno o vario de los parámetros numéricos ingresados no corresponde a un número.",
        "error_2402" : "Error 2402: División por cero.",
        "error_2403" : "Error 2403: Raiz cuadrada de número negativo.",
        "error_2404" : "Error 2404: Variable no inicializada.",
        "error_2500" : "Error 2500: El comando 'blogs' espera un argumento de tipo entero o '-all'.",
        "error_2501" : "Error 2501: El parámetro ingresado no corresponde a las posibles entradas.\n\nIntente con: 1, 2, o -all."
    }

    def checkInput_math(value, data):
        a = True
        if (len(data) - value) < value: return 2400
        for i in range(len(data) - 2):
            try:
                 data[i + 2] = float(data[i + 2])
            except:
                a = 2401
        return a
    def error(err):
        global msg_error
        return msg_error[f"error_{str(err)}"]
    async def getUser(uid, ctx):
        ctx.msg.uid = uid
        return await ctx.get_user_info()
    async def getBlogs(ctx, msg):
        msg = msg[7:]
        if msg == "": return bot_o.Reply(subCommands.error(2500), False)
        blogs = ""

        if msg.find("-USER") != -1:
            blogs = await ctx.get_user_blogs()
            msg = msg[6:]
        elif msg.find("-FEATURED"):
            user = await ctx.get_user_info()

            print("Console")
            print(user)
            return bot_o.Reply(None, False)

        if msg == "":       return bot_o.Reply(subCommands.error(2500), False)

        text = ""
        offset = 1
        try:
            offset = int(msg)
        except:
            if msg.find("-ALL") != -1:
                for blog in blogs:
                    if blog.title is not None: text += f"\n[c]{offset}- {blog.title}"
                    offset += 1
                return f"[c]Los blogs que tiene subidos son los siguientes:\n" + text
            else:
                return bot_o.Reply(subCommands.error(2501), False)

        if offset > 0: offset -= 1;
        elif offset < 0: offset = 0;
        if offset > len(blogs): offset = len(blogs)

        blog = blogs[offset]
        reply.msg = f"[c]Estos son los datos del blog seleccionado:\n\nTítulo: {blog.title}\nAutor: {blog.author.nickname}\nMe gusta: {blog.votesCount}\nSubido: {blog.createdTime}\nComentarios: {blog.commentsCount}\nEtiquetas: {blog.keywords}\nId: {blog.blogId}\nVisitas: {blog.viewCount}\n"
        return reply
    async def userInfo(ctx):
        if ctx.msg.extensions.mentionedArray:
            user = await subCommands.getUser(ctx.msg.extensions.mentionedArray[0].uid, ctx)
        else :
            user = await ctx.get_user_info()
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

        usr_db = bot_o.Database_return()
        usr_db.strToVal( c.database(1, user.uid) )
        msg = f"[cu]Información de perfil:\n\nNick: {user.nickname}\nAlias: {usr_db.alias}\nEstado: {activo}\nNivel: {user.level}\nSeguidores: {user.membersCount}\nSiguiendo a: {user.joinedCount}\nChek-in: {user.consecutiveCheckInDays} {dia[a]}\nRol: {role}\nuid: {user.uid}\nComunidad: {user.aminoId}\nReputación: {user.reputation}\nBlogs: {user.blogsCount}\nComentarios: {user.commentsCount}\nUnido en: {user.createdTime}\nÚltima modificación: {user.modifiedTime}"
        msg += f"\n\n[u]Ha recibido: \n - {usr_db.hugs_r} abrazos. \n - {usr_db.kiss_r} besos. \n - {usr_db.pats_r} caricias.\n\n[u]Ha dado:\n - {usr_db.hugs_g} abrazos.\n - {usr_db.kiss_g} besos.\n - {usr_db.pats_g} caricias."
        return bot_o.Reply(msg, True)
    def dices(msg):
        global msg_text

        if len(msg) < 7:
            return bot_o.Reply("Debe ingresar un número después del comando, por ejemplo\n\n--dados 6", False)
        else :
            num = msg[8:]
            num = int(num)
            return bot_o.Reply(str(int(random() * num)), False)
    def replyMsg(msg):
        return bot_o.Reply(msg, True)
    async def follow(ctx):
        await ctx.follow()
        msg = "Ya está, ya te he seguido, uwu."
        return bot_o.Reply(msg, True)
    async def kick(ctx, msg):
        try:
            await ctx.client.kick_from_chat(ctx.msg.threadId, ctx.msg.uid, allow_rejoin=True)
        except:
            msg += "\n\n[c]Nota: el bot no puede sacarte."

        return bot_o.Reply(msg, False)
    async def enter(ctx):
        msg = f"[ci]Buenas {ctx.msg.author.nickname}, ¿en qué podemos ayudarle?"
        return await ctx.send(msg)
    async def leave(ctx):
        name = await ctx.get_user_info()
        name = name.nickname
        return await ctx.send(f"[ci]¡Adios {name}! Esperamos verte pronto.")
    async def strange(ctx):
        if ctx.msg.author is None:
            print("Nothing strange")
            return bot_o.Reply(None, True)

        await ctx.reply(f"Anomalía detectada\n\n{ctx.msg.author.nickname}\nMensaje tipo: {ctx.msg.type}")


        # embed = Embed(
        #         title="Atención: Mensaje extraño detectado de parte de:",
        #         object_type=0,
        #         object_id=ctx.msg.author.uid,
        #         content="Usuario"
        #     )
        # await ctx.send(embed=embed)
        return bot_o.Reply(None, True)
    def help(com):
        msg = com.split(" ")
        if      len(msg) == 1:          return bot_o.Reply(msg_text['help']['default'], False)

        msg = msg[1].lower()

        if msg in msg_text['help']  :   return bot_o.Reply(msg_text['help'][msg], False)
        return                                 bot_o.Reply("No existe este comando por el momento, :c", False)
    async def ghost(ctx, msg):
        msg = msg[8:]
        await ctx.client.send_message(  message=msg,
                                    chat_id=ctx.msg.threadId,
                                    message_type=109,
                                    ref_id=None,
                                    mentions=None,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None )
        return False;
    async def join(ctx, msg):

        if len(msg) < 7 :            return "Introduzca el comando sobre qué unirse:\n\n-C : comunidad\n-S : sala de chat\n\nSeguido, ponga el link del chat/comunidad."

        com = msg[7:].upper()
        com = com.split(" ")

        if   "-C" in com:
            msg = msg.split(" ")
            msg = msg[2:][0]
            print(msg)

            r = await ctx.client.get_info_link(msg)
            # r = await ctx.client.get_link_identify(msg)

            # agent = r.community.agent.uid
            # uid   = ctx.msg.author.uid

            # if agent != uid :                return "Usted no es el agente de aquella comunidad."

            print(dir(r))
            print(dir(r.community))

            print(r.dict)
            print(r.linkInfo)

            print(r.community.joinType)
            # print(r.community.name)
            # print(r.community.ndcId)
            # print(r.community.link)


            # try:
                # await ctx.client.join_community(invitation_code=msg)
                # return "Listo, ya me he unido a su comunidad, uwu"
            # except:
                # return "No me es posible unir a su comunidad, :c"

        elif "-S" in com:
            msg = msg.split(" ")
            msg = msg[:1]
            try:
                await ctx.join_chat(code=msg)
                return "Listo, ya me he unido a su comunidad, uwu"
            except:
                return "No me es posible unir a su comunidad, :c"
        else                    : return "El parámetro ingresado no es correcto"

        return ":)"
    async def alias(ctx, msg):

        if ctx.msg.extensions.mentionedArray:
            msg = msg.split("\u200e")[0]
            msg = msg.split(" ")
            msg.pop(0)
            uid = ctx.msg.extensions.mentionedArray[0].uid
            msg = " ".join(msg)[:31]
            c.database(31, uid, name=msg)
            user = await subCommands.getUser(uid,ctx)
            print(uid)
            print(msg)
            return f"El nuevo alias de {user.nickname} es {msg}."
        else:
            msg = msg.split(" ")
            if len(msg) < 2: return "Ingrese un nombre como alias."
            msg.pop(0)
            uid = ctx.msg.author.uid
            print(uid)
            print(msg)
            msg = " ".join(msg)[:31]
            c.database(31, uid, name=msg)
            return f"El nuevo alias de {ctx.msg.author.nickname} es {msg}."
