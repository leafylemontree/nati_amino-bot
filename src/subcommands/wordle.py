from src import utils
from src import objects

status = objects.Status()

async def wordle(ctx, msg):
        global status

        reply = objects.Reply(None, True)


        msg = msg.split(" ")
        if len(msg) == 2:
            if ((msg[0] == "--WORDLE") & (msg[1] == "-INIT")):
                if ctx.msg.author.uid in status.wordle.get_users():  return objects.replyMsg("Usted ya está ingresado")
                status.wordle.new_instance(ctx.msg.author.uid)
                reply.msg = f"""
[cb]Wordle
[C]Nuevo usuario registtrado
[c]Nick:{ctx.msg.author.nickname}
[c]"""
                for i in status.wordle.word: reply.msg += "_   "
                return reply
            elif ((msg[0] == "--WORDLE") & (msg[1] == "-INFO")) :
                return objects.replyMsg("Placeholder normas")
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
                return objects.replyMsg(f"Palabra cambiada por {status.wordle.word}")
        else:
            if msg[0] == "--WORDLE" :
                return objects.replyMsg("""
Los comandos disponibles para esta función son:
--WORDLE -INIT: inicia el juego
--WORDLE -INFO: entrega las normas""")
            if msg[0] == "-EXIT":
                index = 0
                for i, j in enumerate(status.wordle.instance):
                    if j.uid == ctx.msg.author.uid :
                        status.wordle.instance.pop(i)
                        break
                return objects.replyMsg(f"[c]{ctx.msg.author.nickname} se ha retirado.")
            else:
                index = 0
                for i, j in enumerate(status.wordle.instance):
                    if j.uid == ctx.msg.author.uid :
                        index = i
                        break
                if ((len(msg[0]) != len(status.wordle.word)) & (msg[0].find("//") == -1)) : return objects.replyMsg("La palabra ingresada no es válida")

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
                    return objects.replyMsg(f"[c]{ctx.msg.author.nickname} ha perdido.")

        return reply
