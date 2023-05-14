from src import utils
from src.objects import status
from src import objects
from src.database import db

async def wordle(ctx, msg):
        global status

        reply = objects.Reply(None, True)

        msg = msg.upper()
        msg = msg.split(" ")
        if len(msg) == 2:
            if ((msg[0] == "--WORDLE") & (msg[1].find("INI") != -1)):
                if ctx.msg.author.uid in status.wordle.get_users():  return objects.Reply("Usted ya está ingresado")
                status.wordle.new_instance(ctx.msg.author.uid)
                reply.msg = f"""
[cb]Wordle
[C]Nuevo usuario registtrado
[c]Nick:{ctx.msg.author.nickname}
[c]"""
                for i in status.wordle.word: reply.msg += "_   "
                return reply
            elif ((msg[0] == "--WORDLE") & (msg[1] == "-INFO")) :
                return objects.Reply("""
[cb]Normas del Wordle:
[c]Se le será dado un espacio de cinco letras, el cual oculta una palabra de cinco letras. Su misión es encontrarla antes de los cinco intentos, si no, habrá perdido.

[c]¿Cómo jugar?
[c]Ponga el comando --wordle -iniciar, y Nati les dará un tablero de juego, que es único para cada jugador.

[c]Para contestar, solo ponga la palabra que quiera añadir, por ejemplo:
[c]acosa
[c]torno

[c]Si una de las letras ha coincidido exactamente con la de la palabra oculta, se pondrá un [] alrededor de la letra. Por ejemplo:

[c] Palabra: C   o   r   t   e
[c] [c] [o]  s   e   r
[c]  p  [o] [r] [t] [e]
 
[c]Para salir, solo pongan -SALIR
""")
            elif ((msg[0] == "--WORDLE") & (msg[1] == "-WORD")) :
                word = utils.get_word(status.wordle.diff);
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
                return objects.Reply(f"Palabra cambiada por {status.wordle.word}")
        else:
            if msg[0] == "--WORDLE" :
                return objects.Reply("""
Los comandos disponibles para esta función son:
--WORDLE -INICIAR: inicia el juego
--WORDLE -INFO: entrega las normas""")
            if msg[0] == "-EXIT" or msg[0] == '-SALIR':
                index = None
                for i, j in enumerate(status.wordle.instance):
                    if j.uid == ctx.msg.author.uid :
                        status.wordle.instance.pop(i)
                        break
                return objects.Reply(f"[c]{ctx.msg.author.nickname} se ha retirado.")
            else:
                index = 0
                for i, j in enumerate(status.wordle.instance):
                    if j.uid == ctx.msg.author.uid :
                        index = i
                        break
                if ((len(msg[0]) != len(status.wordle.word)) & (msg[0].find("//") == -1)) : return objects.Reply("La palabra ingresada no es válida")

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
                        word = utils.get_word(status.wordle.diff);
                        status.wordle.change_word(word)
                        db.modifyRecord(43, ctx.msg.author, 500)
                        return reply

                if len(status.wordle.instance[index].data) > status.wordle.step_cnt:
                    status.wordle.instance.pop(index)
                    db.modifyRecord(43, ctx.msg.author, -250)
                    return objects.Reply(f"[c]{ctx.msg.author.nickname} ha perdido.")

        return reply
