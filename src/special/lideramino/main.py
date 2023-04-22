from __future__     import annotations
#from .ofrecer       import registro as ofrecer_registro
#from .ofrecer       import publish  as ofrecer_publish
#from .buscar        import registro as buscar_registro
#from .buscar        import publish  as buscar_publish
from src.database   import db
from src.special.lideramino import ofrecer
from src.special.lideramino import buscar
from src.special.lideramino import functions
from src            import objects
from src            import utils
import asyncio

class API:
    OFRECER = '0x0000'
    BUSCAR  = '0x0001'
    AYUDA   = '0x0010' 
    CONFIG  = '0x0020'

@utils.waitForMessage(message='*', callback=ofrecer.registro)
async def ofrecer_wrapper(ctx):
    await ctx.send("[c]Empezando proceso de registro: Ofrécete como staff\n\n[c]Si desea cancelar el registro, escriba\n[c]-CANCELAR\n\n[c]Por el contrario, si desea continuar, ponga\n[c]-CONTINUAR")
    return ofrecer.Ofrecer.blank(ctx.msg.messageId)

@utils.waitForMessage(message='*', callback=buscar.registro)
async def buscar_wrapper(ctx):
    await ctx.send("[c]Empezando proceso de registro: Buscar staff\n\n[c]Si usted es el agente de su comunidad, ponga\n[c]-AGENTE\n\n[c]Por el contrario, si desea continuar, ponga\n[c]-CONTINUAR")
    return buscar.Buscar.blank(ctx.msg.messageId)

class Lider:

    context = None
    loop    = None
    
    userId  = None


    def __init__(self):
        self.ofrecer_id = None
        self.buscar_id  = None
        self.ayuda_id   = None
        self.config_id  = None
        self.ndcId      = 9999
        #self.ndcId   = 111610163
        self.active      = False
        return

    async def config(self, ctx):
        if objects.ba.instance not in [0] : return

        self.loop       = asyncio.get_event_loop()
        self.context    = ctx
        ndcId           = ctx.msg.ndcId
        self.context.client.set_ndc(self.ndcId)
        self.userId     = self.context.client.uid
        
        wikis = await self.context.client.get_user_wikis(user_id=self.userId, start=0, size=100)
        for wiki in wikis:
            if wiki.content is None                   : continue
            if wiki.content.find("$BLOG_TYPE: ") == -1: continue
            wikiType = wiki.content.split("$BLOG_TYPE: ")[1]
            wikiType = wikiType.split("\n")[0]
            if   wikiType == API.OFRECER    : self.ofrecer_id  = wiki.itemId
            elif wikiType == API.BUSCAR     : self.buscar_id   = wiki.itemId 
            elif wikiType == API.AYUDA      : self.ayuda_id    = wiki.itemId 
            elif wikiType == API.CONFIG     : self.config_id   = wiki.itemId 
    
        self.active = True
        self.context.client.set_ndc(ndcId)
        return
    
    async def ofrecer(self, ctx):
        if ctx.msg.ndcId != self.ndcId: return await ctx.send("Esta función no está disponible para esta comunidad, :c")
        if not self.active:             return await ctx.send("Acción no permitida en esta instancia.")
        await ofrecer_wrapper(ctx)
    
    async def buscar(self, ctx):
        if ctx.msg.ndcId != self.ndcId: return await ctx.send("Esta función no está disponible para esta comunidad, :c")
        if not self.active:             return await ctx.send("Acción no permitida en esta instancia.")
        await buscar_wrapper(ctx)

    async def publish_ofrecer(self, ctx):
        if ctx.msg.ndcId != self.ndcId: return await ctx.send("Esta función no está disponible para esta comunidad, :c")
        if not self.active:             return await ctx.send("Acción no permitida en esta instancia.")

        print(self.__dict__)
        db.cursor.execute("SELECT * FROM OfrecerStaff;")
        data = db.cursor.fetchall()
        entries = tuple(map(lambda entry: ofrecer.Ofrecer.from_db(entry), data))
        
        image_list = [
                'http://mm1.narvii.com/8623/947b6e09587eab2c0b8bfc6e064a602529960df462815915r7-512-512_00.jpg',
                'http://mm1.narvii.com/8623/e1178106228106e3d75120a5da202b782032346aa92182e1r7-2048-2048v2_hq.jpg',
                'http://mm1.narvii.com/8623/50da3291aef2915ef2a12bf26b67f2c2f130346cd856d319r7-2048-2048v2_hq.jpg'
            ]

        text = await ofrecer.publish(ctx, entries)
        if self.ofrecer_id is not None:
            await ctx.send("Editando la wiki. Espere un momento")
            await functions.edit_wiki(ctx,
                        self.ofrecer_id,
                        title="Ofrécete como Staff",
                        content=text,
                        backgroundColor="#000000",
                        icon='http://mm1.narvii.com/8623/947b6e09587eab2c0b8bfc6e064a602529960df462815915r7-512-512_00.jpg',
                        image_list=image_list
                        )
        else:
            post = await ctx.client.post_wiki(
                        title="Ofrécete como Staff",
                        content=text,
                        backgroundColor="#000000",
                        icon='http://mm1.narvii.com/8623/947b6e09587eab2c0b8bfc6e064a602529960df462815915r7-512-512_00.jpg',
                        image_list=image_list
                    )
            self.ofrecer_id = post.itemId

        print("Wiki submit")
        await functions.submit_to_wiki(ctx, self.ofrecer_id, 'Actualizado automáticamente')
        await ctx.send(f"¡Wiki de ofrecer staff lista!.\nndc://item/{self.ofrecer_id}")

    async def publish_buscar(self, ctx):
        if ctx.msg.ndcId != self.ndcId: return await ctx.send("Esta función no está disponible para esta comunidad, :c")
        if not self.active:             return await ctx.send("Acción no permitida en esta instancia.")

        print(self.__dict__)
        db.cursor.execute("SELECT * FROM BuscarStaff;")
        data = db.cursor.fetchall()
        entries = tuple(map(lambda entry: buscar.Buscar.from_db(entry), data))
        
        image_list = [
                'http://mm1.narvii.com/8623/087b60f1585d68f53a097ddf74bfdf9429939667ec2ac497r7-512-512_00.jpg',
            ]
        icon = "http://mm1.narvii.com/8623/087b60f1585d68f53a097ddf74bfdf9429939667ec2ac497r7-512-512_00.jpg"

        text = await buscar.publish(ctx, entries)
        if self.buscar_id is not None:
            await ctx.send("Editando la wiki. Espere un momento")
            await functions.edit_wiki(ctx,
                        self.buscar_id,
                        title="Busca Staff",
                        content=text,
                        backgroundColor="#000000",
                        icon=icon,
                        image_list=image_list
                        )
        else:
            post = await ctx.client.post_wiki(
                        title="Busca Staff",
                        content=text,
                        backgroundColor="#000000",
                        icon=icon,
                        image_list=image_list
                    )
            self.buscar_id = post.itemId

        print("Wiki submit")
        await functions.submit_to_wiki(ctx, self.buscar_id, 'Actualizado automáticamente')
        await ctx.send(f"¡Wiki de buscar staff lista!.\nndc://item/{self.buscar_id}")

LA = Lider()
