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
import threading
import time
import asyncio
from aiofile import async_open, AIOFile

from antispam import AS
from manage import Image
from objects import Objects
import os
import sys

msg_text = None
status = None
messages = {}

class commands:

    global msg_text
    global status
    with open("src/json/text.json", "r") as textFile:
        msg_text = json.load(textFile)
        print("Texto cargado")
    status = bot_o.Status()
    print("Login open")

    def login():
        with open("src/json/login.json", "r") as loginFile:
            loginData = json.load(loginFile)
        bot = Bot(email=loginData['username'], password=loginData['password'], prefix=loginData['prefix'])
        print("Session logged in!")
        return bot

    async def message(ctx: Context):
        global status, msg_text
        reply = bot_o.Reply(None, False)
        img   = None

        if ctx.msg.type == 101:                     return       await subCommands.enter(ctx)
        #elif ctx.msg.type == 102:                   return       await subCommands.leave(ctx)
        #elif ctx.msg.type in [108, 109, 113, 114] : return       await subCommands.strange(ctx)
       
        await AS.detect_all(ctx)

        msg = ctx.msg.content;
        nick = ""
        if ctx.msg.author:   nick = ctx.msg.author.nickname
        if msg is None: return None;
        com = msg.upper()

        if   ctx.msg.author.uid in status.wordle.get_users() :                               reply = await commands.wordle(ctx, com)
        elif status.challenge.check_user(ctx.msg.author.uid) :                               reply = await commands.challenge(ctx, com, 1)
        #await subCommands.repetition(ctx, msg)
        #await subCommands.link_spam(ctx)

        if com.find("-CH_ID") == 0:
            reply.msg = ctx.msg.threadId
            print(ctx.msg.threadId)

        if   com.find("--SETLOG") == 0 :                                            reply.msg = await AS.set_logging(ctx)
        elif com.find("--BAN") == 0:                                                reply.msg = await AS.ban_user(ctx)
        elif com.find("--UNBAN") == 0:                                              reply.msg = await AS.unban_user(ctx)
        elif com.find("--CHECK") == 0:                                              reply.msg = await AS.check_wall(ctx)
        elif com.find("NATI")   == 0:                                               reply.msg = "¿Me llamaban? Utiliza --help para ver mis comandos, uwu."
        elif com.find("ARTEMIS") == 0:                                              reply.msg = "¿Me llamaban? Utiliza --help para ver mis comandos, uwu."
        elif com.find("--NANO") == 0 :                                              reply.msg = msg_text['nano']
        elif com.find("--WORDLE") == 0:                                             reply     = await commands.wordle(ctx, com)
        elif com.find("--RETAR") == 0:                                              reply     = await commands.challenge(ctx, com, 0)
        elif ((com.find("--SIGUEME") == 0) | (com.find("--SÍGUEME") == 0)) :        reply     = await subCommands.follow(ctx)
        elif com.find("--CHAT") == 0:                                               reply.msg = web_tools.generateText(msg[7:])
        elif com.find("--BIBLIA") == 0:                                             reply.msg = web_tools.bible(msg)
        elif ((com.find("--HOROSCOPO")==0)|(com.find("--HORÓSCOPO")==0)):           reply.msg = web_tools.horoscopo(msg)
        elif com.find("--CARTA") == 0                                   :           reply.msg = web_tools.birthChart(msg)
        elif com.find("--LETRA") == 0                                   :           reply.msg = web_tools.lyrics(msg)
        elif com.find("--DEF") == 0:                                                reply.msg = web_tools.definition(msg)
        elif com.find("--MATRIX") == 0:                                             reply.msg = c.matrix(com)
        elif com.find("--ALIAS") == 0:                                              reply.msg = await subCommands.alias(ctx, msg)
        elif com.find("--EMBED") == 0:                                              reply.msg = await subCommands.embed(ctx)
        elif com.find("--GHOST") == 0:                                            reply.msg = await subCommands.ghost(ctx, msg)
        elif com.find("--CUTES") == 0:                                              reply     = await commands.cutes(ctx, com)
        elif com.find("--COPYPASTE") == 0:                                          reply     = await commands.copypaste(ctx, msg)
        elif com.find("--JOIN") == 0:                                               reply     = await subCommands.join(ctx, msg)
        elif com.find("@EVERYONE") == 0:                                            reply     = await subCommands.chatInfo(ctx)
        elif com.find("--MATH") == 0:                                               reply     = subCommands.replyMsg( c.math(com) )
        elif com.find("--BLOGS") == 0:                                              reply     = await subCommands.getBlogs(ctx, com)
        elif com.find("--INFO") == 0 :                                              reply     = await subCommands.userInfo(ctx)
        elif com.find("PLEBEYOS") == 0 :                                           reply.msg = f"{msg_text['plebeyos']} {nick}"
        elif com.find("LA NAVE") == 0 :                                            reply.msg = msg_text['la_nave']
        elif com.find("--HELP") == 0:                                               reply     = subCommands.help(msg, ctx.msg.ndcId)
        elif com == "--NOMBRE":                                                     reply.msg = f"[c]Tu nombre es:\n\n[c]{nick}";
        elif ((msg.find("--say") < 5) & (msg.find("--say") != -1)) :                reply.msg = msg[6:]
        elif ((com.find("KIWILATIGO") != -1) | (com.find("KIWILÁTIGO") != -1)):     reply     = subCommands.kiwilatigo(ctx)
        elif com.find("--NORMAS") == 0  :                                           reply.msg = msg_text['normas']
        elif msg.find("--Mensaje Oculto") == 0 :                                    reply.msg = msg_text['msg_oculto']
        elif msg.find("👀") != -1:                                                  reply     = subCommands.replyMsg(msg_text['ojos'])
        elif msg.find("Toy Chica") != -1 :                                          reply     = subCommands.replyMsg(msg_text['toy_chica'])
        elif com.find("HOLA NATI") != -1 :                                          reply     = subCommands.replyMsg(f"{msg_text['hola']} {nick}.")
        elif com.find("UWU") != -1 :                                                reply     = subCommands.replyMsg(msg_text['uwu'])
        elif com.find("--PLATYPUS") == 0:                                           reply.msg = msg_text['platypus'][int(random() * 2)]
        elif com.find("--METH") == 0:                                               reply.msg = msg_text['meth']
        elif com.find("--DADOS") == 0:                                              reply     = subCommands.dices(msg)
        # elif com.find("--SUS") == 0:                                              reply['audio'] = 'media/amongus.mp3'
        elif com.find("--DOXX") == 0:                                               reply     = await commands.doxx(ctx, 0)
        elif com.find("DOXXEA A") != -1:                                            reply     = await commands.doxx(ctx, 1)
        elif com.find("--THREADID") == 0:                                           reply.msg = ctx.msg.threadId
        elif com.find("--COMID") == 0:                                              reply.msg = str(ctx.msg.ndcId)
        elif com.find("--LOG") == 0:                                                reply.msg = await AS.logConfig(ctx)
        elif com.find("--ABSTRACT") == 0:                                           img       = await subCommands.abstractImage(ctx)
#elif subCommands.papulince(com):                                            reply = await subCommands.kick(ctx, msg_text['grasa'])
        elif com.find("Y LOS RESULTADOS?") != -1:                                   reply.msg = "Y los blogs?"
        elif com.find("--EXIT") != -1: sys.exit()

        if   ((reply.msg is not None) & (reply.reply is True))           : await ctx.reply(reply.msg)
        elif ((reply.msg is not None) & (reply.reply is False))          : await ctx.send(reply.msg)

        if  img:
            async with AIOFile(img, 'rb') as file:
                 img = await file.read()
                 await ctx.send_image(img)

        #if reply.msg is not None: print(ctx.msg.author.nickname, ctx.msg.content)
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

                c.database(14, uid)
                c.database(24, ctx.msg.author.uid)


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
        user = ""
        if ctx.msg.extensions.mentionedArray:
            user = await subCommands.getUser(ctx.msg.extensions.mentionedArray[0].uid, ctx)
        else:
            return bot_o.Reply("Debe mencionar a un usuario, u.u.", True)

        nick_usr_1 = ""
        nick_usr_2 = ""

        usr_db = bot_o.Database_return()
        usr_db.strToVal( c.database(1, ctx.msg.author.uid) )
        if usr_db.alias == "": nick_usr_1 = ctx.msg.author.nickname
        else                 : nick_usr_1 = usr_db.alias
        usr_db.strToVal( c.database(1, user.uid) )
        if usr_db.alias == "": nick_usr_2 = user.nickname
        else                 : nick_usr_2 = usr_db.alias

        print(nick_usr_1)
        print(nick_usr_2)
        num = int(random() * 16)
        print(f"num = {num}")

        if com[1].find("KISS") != -1:
            async with AIOFile(f'media/cutes/kiss/{str(num)}.gif', 'rb') as file:
                 gif = await file.read()
                 await ctx.send_gif(gif)

            c.database(12, user.uid)
            c.database(22, ctx.msg.author.uid)
            reply.msg = f"<$@{nick_usr_1}$> le da un beso a <$@{nick_usr_2}$>"
        elif com[1].find("HUG") != -1:
            async with AIOFile(f'media/cutes/hug/{str(num)}.gif', 'rb') as file:
                 gif = await file.read()
                 await ctx.send_gif(gif)

            c.database(11, user.uid)
            c.database(21, ctx.msg.author.uid)
            reply.msg = f"<$@{nick_usr_1}$> le da un abrazo a <$@{nick_usr_2}$>"
        elif com[1].find("PAT") != -1 :
            async with AIOFile(f'media/cutes/pat/{str(num)}.gif', 'rb') as file:
                 gif = await file.read()
                 await ctx.send_gif(gif)

            c.database(13, user.uid)
            c.database(23, ctx.msg.author.uid)
            reply.msg = f"<$@{nick_usr_1}$> acaricia a <$@{nick_usr_2}$>"


        await ctx.client.send_message(message=reply.msg,
                                    chat_id=ctx.msg.threadId,
                                    mentions=[ctx.msg.author.uid, user.uid])
        return bot_o.Reply(None, False)
    async def wordle(ctx, msg):
        global status

        reply = bot_o.Reply(None, True)


        msg = msg.split(" ")
        if len(msg) == 2:
            if ((msg[0] == "--WORDLE") & (msg[1] == "-INIT")):
                if ctx.msg.author.uid in status.wordle.get_users():  return subCommands.replyMsg("Usted ya está ingresado")
                status.wordle.new_instance(ctx.msg.author.uid)
                reply.msg = f"""
[cb]Wordle
[C]Nuevo usuario registtrado
[c]Nick:{ctx.msg.author.nickname}
[c]"""
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
                except Exception:
                    reply.msg = False

        elif len(msg) == 4:
            if ((msg[0] == "--WORDLE") & (msg[1] == "SUDO") & (msg[2] == "-WORD")):
                status.wordle.change_word(msg[3])
                return subCommands.replyMsg(f"Palabra cambiada por {status.wordle.word}")
        else:
            if msg[0] == "--WORDLE" :
                return subCommands.replyMsg("""
Los comandos disponibles para esta función son:
--WORDLE -INIT: inicia el juego
--WORDLE -INFO: entrega las normas""")
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
    async def challenge(ctx, com, mode):
        msg = com.split(" ")
        uid1 = ctx.msg.author.uid

        if len(msg) < 2:    return bot_o.Reply("""
Debe agregar un segundo parámetro después de '--retar'
Ejemplos:
--retar ahorcado @
--retar -r
--retar -j
--retar -s
""", False)
        if   msg[1] == '-R':    return bot_o.Reply("""
Reglas de los retos:
La inactividad tras tres turnos acabará el juego para ambos usuarios.
En caso de querer salir, debe hacerse usando --retar -s"""
, False)
        elif msg[1] == '-H':    return bot_o.Reply("""
Normas de los retos:

Añadir para el futuro...
""",False)
        elif msg[1] == '-S':    return status.challenge.remove_instance(uid1)
        elif mode == 0:
            if (not ctx.msg.extensions.mentionedArray): return bot_o.Reply("Debe mencionar a un usuario.", False)
            user = await subCommands.getUser(ctx.msg.extensions.mentionedArray[0].uid, ctx)
            uid2 = user.uid
            if status.challenge.check_user(uid1):    return bot_o.Reply("No puede iniciar otro juego.", False)
            if status.challenge.check_user(uid2):    return bot_o.Reply("No puede retar a otro juego a este usuario.", False)

            if   msg[1] == "AHORCADO":
                status.challenge.new_instance(uid1, uid2, 1)
                print(status.challenge.get_instance_data(-1))
                return bot_o.Reply(f"{ctx.msg.author.nickname} ha retado a {user.nickname} a un ahorcado.", False)
            elif msg[1] == "GATO":
                status.challenge.new_instance(uid1, uid2, 2)
                print(status.challenge.get_instance_data(-1))
                return bot_o.Reply(f"{ctx.msg.author.nickname} ha retado a {user.nickname} a un gato.", False)
        else:
            i = status.challenge.get_instance_number(uid1);
            instance = status.challenge.instances[i]

            if   (((instance.turn % 2) == 0) & (uid1 == status.challenge.instances[i].uid2)) : return bot_o.Reply(None, False)
            elif (((instance.turn % 2) == 1) & (uid1 == status.challenge.instances[i].uid1)) : return bot_o.Reply(None, False)

            if   instance.game == 1:
                return await commands.games.hangman(ctx, i)
            #elif instance.game == 2:
            #elif instance.game == 3:
            #elif instance.game == 4:
        return await bot_o.Reply(None, False)

    class games():

        async def hangman(ctx, i):
            msg = ctx.msg.content.upper().split(" ")
            if len(msg) < 2  : return bot_o.Reply(None, False)
            
            if msg[0] != "-R": return bot_o.Reply(None, False)
            
            ch = msg[1][0]
            if ch in status.challenge.instances[i].data[1] : return bot_o.Reply("La letra ya se encuentra puesta, intente con otra", False)

            status.challenge.instances[i].data[1].append(ch)

            msg = f"""
Ahorcado
Turno: {status.challenge.instances[i].turn}
[c]"""

            no = []

            for j, k in enumerate(status.challenge.instances[i].data[0]):
                if k in status.challenge.instances[i].data[1]: msg += f"{k} "
                else:
                    msg += "_ "

            for j, k in enumerate(status.challenge.instances[i].data[1]):
                if status.challenge.instances[i].data[0].find(k) == -1 : si.append[k] 

            if no:
                for j in no:
                    msg += f"{j} "

            print(status.challenge.instances[i])
            status.challenge.flip(i)
            return bot_o.Reply(msg, False)

class subCommands:
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
            except Exception:
                a = 2401
        return a
    def error(err):
        global msg_error
        return msg_error[f"error_{str(err)}"]
    async def getUser(uid, ctx):
        ctx.msg.uid = uid
        return await ctx.get_user_info()
    async def getBlogs(ctx, msg):
        reply = bot_o.Reply(None, False)
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
                return bot_o.Reply(f"[c]Los blogs que tiene subidos son los siguientes:\n" + text, False)
            else:
                return bot_o.Reply(subCommands.error(2501), False)

        if offset > 0: offset -= 1;
        elif offset < 0: offset = 0;
        if offset > len(blogs): offset = len(blogs)

        blog = blogs[offset]
        reply.msg = f"""[c]Estos son los datos del blog seleccionado:
Título: {blog.title}
Autor: {blog.author.nickname}
Me gusta: {blog.votesCount}
Subido: {blog.createdTime}
Comentarios: {blog.commentsCount}
Etiquetas: {blog.keywords}
Id: {blog.blogId}
Visitas: {blog.viewCount}"""

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

        return bot_o.Reply(None, True)
    def dices(msg):
        global msg_text

        if len(msg) < 7:
            return bot_o.Reply("Debe ingresar un número después del comando, por ejemplo\n\n--dados 6", False)
        else :
            num = msg[8:]
            num = int(num)
            return bot_o.Reply(str(int(random() * (num - 1)) + 1), False)
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
            if msg is not None:
                msg += "\n\n[c]Nota: el bot no puede sacarte."

        return bot_o.Reply(msg, False)
    async def enter(ctx):
        if ctx.msg.author.nickname.find("mamb") != -1 : return None
        thread = await ctx.get_chat_info()
        msg = f"{msg_text['enter'][0]}{thread.membersCount}{msg_text['enter'][1]}<$@{ctx.msg.author.nickname}$>"
        
        #try:
        
        #await subCommands.wait_to_disable(ctx)
        
        #except:
        #    pass

        embed = Embed(
                title="Bella personita",
                object_type=0,
                object_id=ctx.msg.author.uid,
                content="se ha unido, uwu."
            )

        return await ctx.client.send_message(  message=msg,
                                    chat_id=ctx.msg.threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=[ctx.msg.author.uid],
                                    embed=embed,
                                    link_snippets_list=None,
                                    reply=None )
    async def leave(ctx):
        name = await ctx.get_user_info()
        name = name.nickname
        return await ctx.send(f"[ci]¡Adios {name}! Esperamos verte pronto.")
    async def strange(ctx):
        if ctx.msg.author is None:
            print("Nothing strange")
            return bot_o.Reply(None, True)

        msg = f"""
[cb]Anomalía detectada

[c]Al parecer alguien ha enviado un mesaje fuera de lo normal. Puede que se trate de un script, por lo que aquí tiene su perfil.
"""

        embed = Embed(
                title="Malhechor:",
                object_type=0,
                object_id=ctx.msg.author.uid,
                content=f"Mensaje tipo: {ctx.msg.type}"
            )
        await ctx.client.send_message(  message=msg,
                                    chat_id=ctx.msg.threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=embed,
                                    link_snippets_list=None,
                                    reply=None)       
        print("Fantasma")

        embed = Embed(
                title="Malhechor:",
                object_type=0,
                object_id=ctx.msg.author.uid,
                content=f"Mensaje tipo: {ctx.msg.type}"
            )
        await ctx.client.send_message( message=msg,
                                    chat_id="ba533e76-a58e-0e2d-28d1-b939968a356b",
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=embed,
                                    link_snippets_list=None,
                                    reply=None)     
        print("Enviado")
        return bot_o.Reply(None, True)
    def help(com, comId):
        msg = com.split(" ")
        
        if ( (len(msg) == 1) & (comId == 112646170) ):          return bot_o.Reply(msg_text['help']['default'].replace("Nati", "Artemis"), False)
        elif      len(msg) == 1:          return bot_o.Reply(msg_text['help']['default'], False)

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
            msg = " ".join(msg)[:127]
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
            msg = " ".join(msg)[:127]
            c.database(31, uid, name=msg)
            return f"El nuevo alias de {ctx.msg.author.nickname} es {msg}."
    def kiwilatigo(ctx):
        c.database(32, ctx.msg.author.uid)
        return bot_o.Reply(f"[ci]¡Oh no! Han hecho enfadar a {ctx.msg.author.nickname}\n\n[ci]/c skpa.", False)
    async def chatInfo(ctx):
        user = await ctx.get_user_info()
        if ((user.role == 0) & (user.uid != "17261eb7-7fcd-4af2-9539-dc69c5bf2c76")): return bot_o.Reply("Usted no está autorizado para ejercer este comando", False)
        thread = await ctx.get_chat_info()
        userCount = thread.membersCount

        uidList = []
        for i in range(userCount % 25):
            users = await ctx.client.get_chat_users(
                                                ctx.msg.threadId,
                                                i * 25,
                                                (i + 1) *25
                                                )
            for j in users:
                uidList.append(j.uid)


        await ctx.client.send_message(  message="Mencionando usuarios...",
                                    chat_id=ctx.msg.threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=uidList,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None )

        return bot_o.Reply(f"{len(uidList)} usuarios mencionados.", False)
    async def embed(ctx):
        embed = Embed(
                title="Bella personita",
                object_type=0,
                object_id=ctx.msg.author.uid,
                content="se ha unido"
            )
        await ctx.client.send_message(  message="Hola",
                                    chat_id=ctx.msg.threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=embed,
                                    link_snippets_list=None,
                                    reply=None )

        await ctx.send(embed=embed)
        return None
    def papulince(com):

        grasa = [
                    ":V",
                    "V:",
                    "PAPU",
                    "ELFA",
                    "MOMAZO",
                    "MEMINGO",
                    "ALV",
                    "XDXDXD",
                    "PRRO",
                    "MAQUINOLA",
                    "LINCE",
                ]

        com = com.split(" ")

        papuh = [-1, False]

        for i,j in enumerate(com):
            if j in grasa:
                papuh = [i, True] 
                break

        print(papuh)

        
        if len(com) < 8:
            return papuh[1]
        else:
            if ((papuh[0] < (len(com) / 4)) | (papuh[0] > (3*len(com) / 4))):
                return papuh[1]

        return False
    async def repetition(ctx, msg):
        global messages
        threadId = ctx.msg.threadId

        if threadId not in messages:
            messages[threadId] = []

        messages[threadId].append([msg.upper(), ctx.msg.author.uid])
        #print(messages[threadId])

        if len(messages[threadId]) < 3: return
       
        #print(messages[threadId])
        if ((messages[threadId][0] == messages[threadId][1]) & (messages[threadId][1] == messages[threadId][2])):
           
            print("Mensajes iguales")
            msg = """
Alerta: ¡Hay un usuario colocando un mismo mensaje varias veces!
"""

            await subCommands.kick(ctx, None)
            try:
                await ctx.client.set_view_only_chat(
                                            threadId,
                                            "enable"
                )
                sub_m = "Eliminado por: flood"
                msg += """

Para evitar más incidentes, ha sido removido del chat, junto con poner este en modo visualización"""
            except Exception:
                sub_m = "Ha hecho: flood"
                msg += """
Este es el usuario"""


            embed = Embed(
                title=ctx.msg.author.nickname,
                object_type=0,
                object_id=ctx.msg.author.uid,
                content=sub_m
                 )
            await ctx.client.send_message(  message=msg,
                                    chat_id=ctx.msg.threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=embed,
                                    link_snippets_list=None,
                                    reply=None)       
            
            messages[threadId] = [None]
        
        else:
            messages[threadId].pop(0)

        return
    async def wait_to_disable(ctx):
        await ctx.client.set_view_only_chat(
                    chat_id=ctx.msg.threadId,
                    view_only='enable'
                )
        time.sleep(3)
        await ctx.client.set_view_only_chat(
                    chat_id=ctx.msg.threadId,
                    view_only='disable'
                )
        return
    async def abstractImage(ctx):
        steps = 64

        msg = ctx.msg.content
        if msg.find(" ") != -1:
            msg = msg.split(" ")[1]
            try:
                steps = int(msg)
            except:
                pass
            if steps > 100000: steps = 100000 
       
        
        #def imgPscLoop(loop, ctx, steps):
        #    asyncio.set_event_loop(loop)
        #    asyncio.run(subCommands.abstractImageProcessing(ctx, steps))
        await subCommands.abstractImageProcessing(ctx, steps)   

        return "result.png"

    async def abstractImageProcessing(ctx, steps):
        img = Image("test", 512, 512)
        col = Objects.c_Color(255, 255, 255, 255)
        img.generate(col)
        print(f"steps {steps}")
        
        a = [1, 510, 510]
        b = [1, 510, 510]

        try:

            for i in range(steps):
                col = Objects.c_Color(
                int(random()*255),
                int(random()*255),
                int(random()*255),
                255)

                a = [
                    a[1],
                    a[2], 
                1+int(random()*510),
                    ]

                b = [
                    a[1],
                    a[2], 
                1+int(random()*510),
                    ]
            
                img.draw.triangle(img, col, 
                    a[0],
                    b[0],
                    a[1],
                    b[1],
                    a[2],
                    b[2],
                    )
            img.write()
            img.free()
        except Exception:
            pass
        return "result.png" 
