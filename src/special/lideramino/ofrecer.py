from src.database import db
from dataclasses    import dataclass
import datetime

@dataclass
class Ofrecer:
    userId      : str
    nick        : str
    timestamp   : datetime.datetime
    confirm     : bool
    profileLink : str
    globalLink  : str
    question1   : str       # ¿En qué tipo de comunidad te gustaría ser parte del staff? (Incluye temáticas).
    question2   : str       # ¿Por qué quieres formar parte de un staff?
    question3   : str       # ¡Cuéntanos de tu experiencia previa!
    question4   : str       # ¿Cuál es tu franja horaria?
    question5   : str       # ¡Cuéntanos sobre tus cualidades!
    question6   : str       # Si quieres agregar algo, puedes hacerlo aquí.
    moreInfo    : bool      # Puedes elegir que esta información se coloque como texto o puedes crear tu propia producción (una imagen, un video, una presentación, una carpeta de drive, una página web o lo que gustes). ¿Qué prefieres?
    image_cv    : str
    additional  : str
    step        : int
    messageId   : str
   
    @classmethod
    def blank(Self, messageId=''):
        return Self('', '', datetime.datetime.now(), False, '', '', '', '', '', '', '', '', False, '', '', 0, messageId)
    
    @classmethod
    def from_db(Self, data):
        return Self(*data, 0, '')
    
    def prepare(self):
        if not self.confirm: return None
        self.timestamp = datetime.datetime.now()
        query   = 'INSERT INTO OfrecerStaff VALUES (?, ?, NOW(), ?, ? ,? ,? ,? ,?, ?, ? ,? ,? ,? ,?)'
        values  = (self.userId, self.nick, self.confirm, self.profileLink, self.globalLink, self.question1, self.question2, self.question3, self.question4, self.question5, self.question6, self.moreInfo, self.image_cv, self.additional,)
        return query, values

questions = [
    "¿En qué tipo de comunidad te gustaría ser parte del staff? (Incluye temáticas).",
    "¿Por qué quieres formar parte de un staff?",
    "¡Cuéntanos de tu experiencia previa!",
    "¿Cuál es tu franja horaria?",
    "¡Cuéntanos sobre tus cualidades!",
    "Si quieres agregar algo, puedes hacerlo aquí.",
    "Puedes elegir que esta información se coloque como texto o puedes crear tu propia producción (una imagen, un video, una presentación, una carpeta de drive, una página web o lo que gustes). ¿Qué prefieres?\n\n[c]-NORMAL : solo texto\n[c]-ADJUNTAR: adjuntar imagen/página.",
    "Para adjuntar una imagen, mande esta. Si en cambio desea anexar una página web, o información de contacto adicional, responda con aquella información.",
    "Prueba",
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
        ndcId                   = ctx.msg.ndcId
        ins.data.userId         = ctx.msg.author.uid
        ins.data.confirm        = True
        ins.data.nick           = ctx.msg.author.nickname

        baseLink                = await ctx.client.get_from_id(object_id=ctx.msg.author.uid, object_type=0)
        ins.data.profileLink    = str(baseLink.shareURLShortCode)

        ctx.client.set_ndc(0)
        globalLink              = await ctx.client.get_from_id(object_id=ctx.msg.author.uid, object_type=0)
        ins.data.globalLink     = str(globalLink.shareURLShortCode)
        ctx.client.set_ndc(ndcId)

    await ctx.send(f'[c]Pregunta {ins.data.step + 1}\n[c]-------------\n\n[c]{questions[ins.data.step]}')

    if      ins.data.step   == 1:   ins.data.question1 = ctx.msg.content
    elif    ins.data.step   == 2:   ins.data.question2 = ctx.msg.content
    elif    ins.data.step   == 3:   ins.data.question3 = ctx.msg.content
    elif    ins.data.step   == 4:   ins.data.question4 = ctx.msg.content
    elif    ins.data.step   == 5:   ins.data.question5 = ctx.msg.content
    elif    ins.data.step   == 6:   ins.data.question6 = ctx.msg.content
    elif    ins.data.step   == 7:
        if   ctx.msg.content.upper().find("-NORMAL") == 0:
            ins.data.moreInfo   = False
            ins.data.step = 200
        elif ctx.msg.content.upper().find("-ADJUNTAR") == 0: ins.data.moreInfo = True
    elif    ins.data.moreInfo:
        if ctx.msg.mediaValue   :   ins.data.image_cv   = ctx.msg.mediaValue
        else                    :   ins.data.additional = ctx.msg.content
        ins.data.step = 200
     
    if    ins.data.step  == 200:
        await ctx.send(questions[9])
        print("Writting to db")
        await db_write(ctx, ins.data)
        await ctx.send("Escritura completada")
        return True
    
    ins.data.step += 1
    print(ins.data.step)


def generate_link(text, link):
    text = text.replace('[', '').replace(']', '').replace('|', '').replace('\n', ' ').replace(':', '')
    return f'[{text}|{link}]'


async def publish(ctx, entries):
    date = datetime.datetime.now()
    text = f"""
[c]$BLOG_TYPE: 0x0000
[cb][Actualizado: {date.day}/{date.month}/{date.year}]

[c]

[c]¡Hola, líderes y curadores! Hace un tiempo se permitió la búsqueda de staff por medio de blogs, esto debido a que el formato anterior estaba teniendo un par de inconvenientes a la hora de actualizar. Ahora, hemos traído este formato de una forma renovada, y que sea de manera automática, en vez de cada quince días (o más).

[c]Sumado a esto, hemos notado que recientemente, es mayor la cantidad de personas que necesitan personal para su staff, y para facilitar esta labor y que además los propios usuarios pudieran tener más interacción, es que hemos revivido esta sección.

[c]Esta, junto con las búsquedas de staff, estarán siendo automatizadas, y si bien no se prohibirá que se creen blogs para esto, les incentivamos a que utilicen nuestras wikis.

[c]Recordar:En esta wiki, puedes OFRECERTE para ser staff.

[c]

[cb]¿Cómo funcionará esto?

[c]Deben abrir privado a la cuenta del bot Nati, y poner el comnando --ofrecerstaff. Luego, esta le hará una serie de preguntas, las cuales deberá responder en orden, de acuerdo a lo que ella ponga. El blog será actualizado frecuentemente.

[c]Si poseen alguna duda sobre cómo realizarlo, aqui les va un pequeño tutorial:

[IMG=001]
[IMG=002]

[c]

[cb]Lista:"""

    for i,data in enumerate(entries):
        if data.userId == 'test': continue
        text += f"""

[c]

[c]

[cb]🌸 Usuario N°{i} 🌸
[c]↜∗≖≖≖≖∗↝☬↜ ∗≖≖≖≖∗↝

[c]Perfil: {generate_link(data.nick, data.profileLink)}
[c]Global: {generate_link("link", data.globalLink)}

[c]🍂 ; Temáticas que busca:
[c]≻───── ⋆✩⋆ ─────≺
[c]{data.question1}

[c]🍂 ; ¿Por qué quieres ser parte de un staff?
[c]≻───── ⋆✩⋆ ─────≺
[c]{data.question2}

[c]🍂 ; Experiencia Previa
[c]≻───── ⋆✩⋆ ─────≺
[c]{data.question3}

[c]🍂 ; Franja Horaria
[c]≻───── ⋆✩⋆ ─────≺
[c]{data.question4}

[c]🍂 ; Cualidades
[c]≻───── ⋆✩⋆ ─────≺
[c]{data.question5}

[c]🍂 ; Comentario Adicional
[c]≻───── ⋆✩⋆ ─────≺
[c]{data.question6}
"""
    
    if data.moreInfo:   text += "\n\n[c]Información adicional:\n[c]Imagen:{data.image_cv}\n\n[c]Texto:\n{data.additional}"

    return text
