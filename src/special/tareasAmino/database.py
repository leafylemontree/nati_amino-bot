import mariadb
import json
from edamino.api import Embed

class Tareas:
    base   = None
    cursor = None

    def __init__(self):
        with open("data/base.json", "r") as fp:
            data = json.load(fp)
        try:
            self.base = mariadb.connect(
                    host     = data["host"],
                    user     = data["user"],
                    password = data["password"],
                    database = "_tareasAmino"
                )
        except mariadb.Error as e:
            print("Error during TA database read:", e)
        else:
            self.cursor = self.base.cursor()
            self.base.autocommit = True

    async def run(self, ctx):
        if ctx.msg.ndcId != 51158068: return
        text = ctx.msg.content.upper().split(" ")
        
        if   text[1].find("AÑADIR") != -1: await self.add(ctx)
        elif text[1].find("QUITAR") != -1: await self.remove(ctx)
        elif text[1].find("VER")    != -1: await self.get(ctx)
        
        return

    async def add(self, ctx):
        text = ctx.msg.content.split("\n")
        userId = ''
        link = await ctx.client.get_info_link(text[1])
        if link.linkInfo.objectType != 0:   await ctx.send("Solo funciona con usuarios")
        else                            :   userId = link.linkInfo.objectId
        self.cursor.execute(f"SELECT * FROM User WHERE userId='{userId}'")
        data = self.cursor.fetchall()
        if data:    return await ctx.send("El usuario ya está añadido")
        
        name    = text[2]
        subject = text[3]
        country = text[4]
        hrtime  = text[5]
        titles  = text[6].upper().split(" ")
        tutor   = 1 if "TUTOR"          in titles else 0
        aux     = 1 if "AUXILIAR"       in titles else 0
        verify  = 1 if "VERIFICADO"     in titles  else 0
        cert    = 1 if "CERTIFICADO"    in titles  else 0

        caseId = "None"
        wikis = await ctx.client.get_user_wikis(userId)
        for wiki in wikis:
            if wiki.label.upper().find("MONE") != -1:
                caseId=wiki.itemId
                break
        
        self.cursor.execute(f"INSERT INTO User VALUES ('{userId}', '{name}', '{subject}', '{caseId}', '{country}', '{hrtime}', {tutor}, {aux}, {verify}, {cert});")
        return await ctx.send("Usuario añadido exitosamente")
        
    async def remove(self, ctx):
        text = ctx.msg.content.split(" ")
        link = ""
        for word in text:
            if word.upper().find("HTTP") != -1:
                link = word
                break

        userId = ''
        link = await ctx.client.get_info_link(link)
        if link.linkInfo.objectType != 0:   await ctx.send("Solo funciona con usuarios")
        else                            :   userId = link.linkInfo.objectId
        self.cursor.execute(f"SELECT * FROM User WHERE userId='{userId}'")
        data = self.cursor.fetchall()
        if data:
            self.cursor.execute(f"DELETE FROM User WHERE userId='{userId}';")
            return await ctx.send("El usuario ha sido removido")
        else: return await ctx.send("El usuario no está ingresado")

    async def get(self, ctx):
        text = ctx.msg.content.split(" ")
        link = ""
        for word in text:
            if word.upper().find("HTTP") != -1:
                link = word
                break

        userId = ''
        link = await ctx.client.get_info_link(link)
        if link.linkInfo.objectType != 0:   await ctx.send("Solo funciona con usuarios")
        else                            :   userId = link.linkInfo.objectId
        self.cursor.execute(f"SELECT * FROM User WHERE userId='{userId}'")
        data = self.cursor.fetchall()
        if not data: return await ctx.send("El usuario no está ingresado")
        userId, name, subject, caseId, country, hrtime, tutor, aux, verify, cert = data[0]
        user = await ctx.client.get_user_info(userId)  

        embed = Embed(
                title="Usuario",
                object_type=0,
                object_id=userId,
                content=user.nickname
            )

        msg = f'''
Usuario: {user.nickname}
Nombre : {name}
Asignatura: {subject}
País: {country}
Zona horaria: {hrtime}

Títulos
Tutor           : {"SÍ" if tutor else "No"}
Auxiliar        : {"SÍ" if aux else "No"}
Verificado    : {"SÍ" if verify else "No"}
Certificado   : {"SÍ" if cert else "No"}

{('Monedero: ndc://item/' + caseId) if caseId != "None" else ''}
'''
        return await ctx.client.send_message(message=msg,
                                    chat_id=ctx.msg.threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=embed,
                                    link_snippets_list=None,
                                    reply=None )
        




TA = Tareas()
