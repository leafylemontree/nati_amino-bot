import time
import asyncio
import threading

from src.antispam.data import AS
from src.antispam.detectMessage import findNickname, findContent
from edamino.api import Embed
from src import objects
from .n_logging import banUser
from src import utils
from src.database import db

class DeepAnalyze:

    queue       = [
                    # comId, comId...
            ]
    done        = {
                    # "comId" : time
            }
    lastAnalyze = 0
    ctx         = None

    @utils.isStaff
    async def run(self, ctx):
        comId = ctx.msg.ndcId

        if   comId in self.queue: return await ctx.send("La comunidad ya está en la cola")
        elif comId in self.done : return await ctx.send("Debe esperar al menos 5 minutos antes de pedir un análisis nuevo")

        await ctx.send(f"""
Nati - Análisis de comunidades
------------------------------

La comunidad ha sido puesto en la cola en el número {len(self.queue)+1}
Tiempo de espera promedio: {(len(self.queue)+1) * 12} minutos

El análisis de comunidades revisará a fondo todos y cada uno de los perfiles de los usuarios, en busca de perfiles que cierran la app y spam. Este análisis puede tardar un momento en ser llevado a cabo, ya que comunidades muy grandes pueden incluso tardar horas en completar su revisión. Es posible que mientras el análisis se lleve a cabo, el bot pueda dejar de responder o recibir un error 403, en caso de lo anterior, consultar con el dueño del bot.

Cuando empiece, se enviará un mensaje al chat de log del bot, por lo que si no ha sido puesto, deberá activarlo con este comando:
--setlog

Si tiene el modo estricto activo, el bot expulsará a quien haya detectado como spam. Si no desea aquello, puede desactivar el modo estricto así:

--log -normal
""")
        self.queue.append(comId)
        print("Lista:", self.queue)
        if self.ctx is None:
            self.ctx = ctx
            loop = asyncio.get_event_loop()
            awaiter = threading.Thread(target=self.as_thr, args=(loop,))
            awaiter.start()
        return

    def as_thr(self, loop):
        lp = asyncio.run_coroutine_threadsafe(self.awaiter(), loop)
        lp.result()

    async def awaiter(self):
        counter = 1
        while True:
            counter -= 1
            t = time.time()
            for com,clk in list(self.done.items()):
                if (t - clk) > 300: self.done.pop(com,None)
            if self.queue and counter == 0:
                await self.analyze()
                counter = 300
            elif counter == 0:
                counter = 1
            await asyncio.sleep(1)

    async def analyze(self):
        comId = self.queue[0]
        log = db.getLogConfig(comId)
        threadId = log.threadId
        banningToggle = log.ban 
        print("Anlizando ahora a:", comId, threadId, banningToggle)
        self.ctx.client.set_ndc(comId)

        users = []
        count = 0
        while True:
            getList = await self.ctx.client.get_all_users(users_type="recent", start=count, size=100)
            count += len(getList)
            users.extend(getList)
            print(f"Counted last - {count}", end="\r")
            if len(getList) < 100: break
       
        for index,user in enumerate(users):
            s1 = await findNickname(user.nickname)
            s2 = await findContent(user.content, comId)
            if "151" in s1: s2.remove("151")

            if s1 or s2:
                print("\t", index, user.uid, user.nickname, s1, s2)
                embed = Embed(title="Perfil del usuario", object_type=0, object_id=user.uid, content=user.nickname )
                msg = f"""
Nati Community Deep Analysis Technology v0.1
--------------------------------------------
Nombre: {user.nickname}
ID: {user.uid}
Unido: {user.createdTime}

Advertencias
------------
Nick:"""
                for w in s1: msg += f"\n\t{w}: {objects.AntiSpam.msg_desc[w]}"
                msg += "\n\nBiografía:"
                for w in s2: msg += f"\n\t{w}: {objects.AntiSpam.msg_desc[w]}"
                await self.ctx.client.send_message(message=msg,
                                    chat_id=threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=embed,
                                    link_snippets_list=None,
                                    reply=None )
                warnings = []
                warnings.extend(s1)
                warnings.extend(s2)
                if banningToggle: await banUser(self.ctx, user.uid, comId, warnings)
                db.registerReport(user.uid, comId, "DeepAnalyze", warnings)

        c = self.queue.pop(0)
        self.done[str(c)] = time.time()
        return    

deepAnalyze = DeepAnalyze()
