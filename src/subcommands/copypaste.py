from src import utils
from src import objects

async def copypaste(ctx, msg):
        with open("data/database.json", "r+") as hard_data:
            database = json.load(hard_data)
        reply = objects.Reply(None, False)

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
            with open("data/database.json", "w+") as hard_data:
                json.dump(database, hard_data)
            reply.msg = f"Mensaje guardado en la posición {len(database['copypaste']['stored'])}."

        elif com[1] == "-RM" :
            try: num = int(msg[2])
            except:
                reply.msg = subCommands.error(2401)
                return reply
            database['copypaste']['stored'].pop(num-1)
            with open("data/database.json", "w+") as hard_data:
                json.dump(database, hard_data)

            reply.msg = f"Mensaje número {num} eliminado de la base de datos."
        elif com[1] == "-DS" :
            try: num = int(msg[2])
            except:
                reply.msg = subCommands.error(2401)
                return reply
            if database['copypaste']['stored'][num -1].find("{{--DIS--}}") == -1:
                database['copypaste']['stored'][num -1] = "{{--DIS--}}" + database['copypaste']['stored'][num -1]
                with open("data/database.json", "w+") as hard_data:
                    json.dump(database, hard_data)
                reply.msg = f"Mensaje número {num} deshabilitado de la base de datos."
            elif database['copypaste']['stored'][num-1].find("{{--DIS--}}") == 0:
                database['copypaste']['stored'][num-1] = database['copypaste']['stored'][num-1][11:]
                with open("data/database.json", "w+") as hard_data:
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
