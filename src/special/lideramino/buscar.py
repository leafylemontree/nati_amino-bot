from src.database import db
from dataclasses    import dataclass
import datetime

@dataclass
class Buscar:
    userId          : str
    nick            : str
    timestamp       : datetime.datetime
    agent           : bool
    profileLink     : str       # perfil LA
    profileLink2    : str       # perfil comunidad
    communityLink   : str       # link comunidad
    membersCount    : int
    communityName   : str
    activity        : int
    description     : str       
    members         : str
    membersType     : int       # 0: curador    1: líder    2: ambos
    limitDate       : str
    question1       : str       # ¿Qué cualidades crees que deba tener alguien para poder entrar a tu staff?
    question2       : str       # ¿Alguna pregunta o aclaración que le quieras hacer a los miembros que estén interesados en formar parte de tu staff?
    step            : int
    messageId       : str

   
    @classmethod
    def blank(Self, messageId=''):
        return Self('', '', datetime.datetime.now(), False, '', '', '', 0, '', 0, '', '', 0, '', '', '', 0, messageId)
    
    @classmethod
    def from_db(Self, data):
        return Self(*data, 0, '')
    
    def prepare(self):
        self.timestamp = datetime.datetime.now()
        query   = 'INSERT INTO BuscarStaff VALUES (?, ?, NOW(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        values  = (self.userId, self.nick, self.agent, self.profileLink, self.profileLink2, self.communityLink, self.membersCount, self.communityName, self.activity, self.description, self.members, self.membersType, self.limitDate, self.question1, self.question2,)
        return query, values

questions = [
    "Link de tu comunidad.",
    "Link de tu perfil en la comunidad antes ingresada.",
    "Descripción de la comunidad (incluir temática).",
    "¿Cuántos miembros buscas para tu staff?",
    "¿Qué tipo de miembros para tu staff estás buscando?\n\n[c]Opciones válidas:\n[c]CURADOR\n[c]LIDER\n[c]AMBOS",
    "¿Hay una fecha límite para el reclutamiento? ¿Cuál es?",
    "¿Qué cualidades crees que deba tener alguien para poder entrar a tu staff?",
    "¿Alguna pregunta o aclaración que le quieras hacer a los miembros que estén interesados en formar parte de tu staff?",
    "Ha concluído con éxito el proceso de registro. Muchas gracias por su tiempo u.u."
]

async def db_write(ctx, data):
    print(data)
    query, values = data.prepare()
    db.cursor.execute(query, values)
    return


async def registro(ctx, ins):
    if ctx.msg.messageId == ins.data.messageId: return

    if  ctx.msg.content.upper().find("-CANCELAR") == 0:
        await ctx.send("Proceso cancelado")
        return True
    
    print(ins.data.step, 'hitted:', ctx.msg.content)
    print(ins.data)

    if   ins.data.step == 0:
        ins.data.userId         = ctx.msg.author.uid
        ins.data.nick           = ctx.msg.author.nickname

        baseLink                = await ctx.client.get_from_id(object_id=ctx.msg.author.uid, object_type=0)
        ins.data.profileLink    = str(baseLink.shareURLShortCode)

        if ctx.msg.content.upper().find("-AGENTE") == 0:    ins.data.agent = True



    if ins.data.step != 200: await ctx.send(f'[c]Pregunta {ins.data.step + 1}\n[c]-------------\n\n[c]{questions[ins.data.step]}')

    if      ins.data.step   == 0:
        ins.data.step += 1

    if      ins.data.step   == 1:
        linkInfo        = await ctx.client.get_info_link(link=ctx.msg.content.split(" ")[0])
        if hasattr(linkInfo, 'community') and linkInfo.community is not None:
            print(linkInfo)
            ins.data.communityLink = ctx.msg.content.split(" ")[0]
            ins.data.communityName = linkInfo.community.name
            ins.data.membersCount = linkInfo.community.membersCount
            ins.data.step += 1
        else:   await ctx.send("El link ingresado no es válido")

    elif    ins.data.step   == 2:
        linkInfo        = await ctx.client.get_info_link(link=ctx.msg.content.split(" ")[0])
        print(linkInfo)
        if hasattr(linkInfo, 'linkInfo') and linkInfo.linkInfo is not None:

            if linkInfo.linkInfo.objectType != 0:       await ctx.send("El link ingresado no es válido")
            comInfo        = await ctx.client.get_info_link(ins.data.communityLink)
            ndcId          = comInfo.community.ndcId 
            if linkInfo.linkInfo.ndcId      != ndcId:   await ctx.send("El link ingresado no es válido")

            ins.data.profileLink2 = ctx.msg.content.split(" ")[0]
            ins.data.step += 1
        else:   await ctx.send("El link ingresado no es válido")

    elif    ins.data.step   == 3:
        ins.data.description    = ctx.msg.content
        ins.data.step          += 1

    elif    ins.data.step   == 4:
        ins.data.members        = ctx.msg.content
        ins.data.step          += 1

    elif    ins.data.step   == 5:
        if    ctx.msg.content.upper().find("CURADOR") != -1  :   ins.data.membersType = 0
        elif  ctx.msg.content.upper().find("LIDER")   != -1  :   ins.data.membersType = 1
        elif  ctx.msg.content.upper().find("AMBOS")   != -1  :   ins.data.membersType = 2
        else :   
            await ctx.send("Respuesta incorrecta\nCURADOR, LIDER O AMBOS")
            return
        ins.data.step          += 1

    elif    ins.data.step   == 6:
        ins.data.limitDate      = ctx.msg.content
        ins.data.step          += 1

    elif    ins.data.step   == 7:
        ins.data.question1      = ctx.msg.content
        ins.data.step          += 1

    elif    ins.data.step   == 8:
        ins.data.question2      = ctx.msg.content
        ins.data.step           = 200

    if    ins.data.step  == 200:
        await db_write(ctx, ins.data)
        await ctx.send("Escritura completada")
        return True
    
    print(ins.data.step)

def generate_link(text, link):
    text = text.replace('[', '').replace(']', '').replace('|', '').replace('\n', ' ').replace(':', '')
    return f'[{text}|{link}]'

def membersTypeStr(membersType):
    return {
        0   :    'Curador',
        1   :    'Líder',
        2   :    'Ambos'
    }[membersType]

async def publish(ctx, entries):
    date = datetime.datetime.now()
    text = f"""
[c]$BLOG_TYPE: 0x0001
[cb][Actualizado: {date.day}/{date.month}/{date.year}]

[c]

[c]¡Hola, líderes y curadores! Hace un tiempo se permitió la búsqueda de staff por medio de blogs, esto debido a que el formato anterior estaba teniendo un par de inconvenientes a la hora de actualizar. Ahora, hemos traído este formato de una forma renovada, y que sea de manera automática, en vez de cada quince días (o más).

[c]Sumado a esto, para hacer el proceso de publicar una comunidad abierta para buscar staff un poco más ordenado, es que hemos traído un sistema donde automáticamente puede llenar los datos, y estos se verán reflejados en la wiki.

[c]Esta, junto con las de ofrecerse como staff, estarán siendo automatizadas, y si bien no se prohibirá que se creen blogs para esto, les incentivamos a que utilicen nuestras wikis.

[c]Recordar:En esta wiki, puedes BUSCAR miembros para ser staff.

[c]

[cb]¿Cómo funcionará esto?

[c]Deben abrir privado a la cuenta del bot Nati, y poner el comnando --buscarstaff. Luego, esta le hará una serie de preguntas, las cuales deberá responder en orden, de acuerdo a lo que ella ponga. El blog será actualizado frecuentemente.

[c]

[cb]Lista:"""

    for i,data in enumerate(entries):
        if data.userId == 'test': continue
        text += f"""

[c]

[c]

[cb]🌸 Comunidad N°{i} 🌸
[c]↜∗≖≖≖≖∗↝☬↜ ∗≖≖≖≖∗↝

🌷 ; {'Agente' if data.agent else 'Staff representativo'}: {generate_link(data.nick, data.profileLink)}
🌷 ; Comunidad: {generate_link(data.communityName, data.communityLink)}
🌷 ; Temática: {data.description}
🌷 ; Cantidad de miembros: {data.membersCount}
🌷 ; Qué puestos se buscan: {membersTypeStr(data.membersType)}
🌷 ; Barras de actividad: (no disponible)
🌷 ; Fecha límite: {data.limitDate}
🌷 ; Requisitos: {data.question1}
🌷 ; Aclaración: {data.question2}
"""
    return text
