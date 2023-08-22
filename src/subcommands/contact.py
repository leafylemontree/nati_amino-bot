from src.database import db
from src import utils
from src.imageSend import send_image
import asyncio
from dataclasses import dataclass

async def receiver(ctx, ins):
    if ctx.msg.content is not None:
        if ctx.msg.content.upper().find("-SALIR") == 0:
            await ins.data.quit(ctx)
            return True
        elif ctx.msg.content.upper().find("-AUTOR") == 0:
            await ctx.send(f"Este usuario ha sido quien ha iniciado la llamada\nndc://x{ctx.msg.ndcId}/user-profile/{ins.data.host.userId}")
            return False

    await ins.data.send(ctx)
    return False


async def sender(ctx, ins):
    if ctx.msg.content is not None:
        if ctx.msg.content.upper().find("-SALIR") == 0:
            await ins.data.quit(ctx)
            return True

    await ins.data.send(ctx)
    return False

class MessageType:
    bidirectional   = 0
    unidirectional  = 1

class CallHost:
    threadId:   str
    userId:     str
    ndcId:      int
    nickname:   str

    def __init__(self, ctx):
        self.threadId   =   ctx.msg.threadId
        self.ndcId      =   ctx.msg.ndcId
        self.userId     =   ctx.msg.author.uid
        self.nickname   =   ctx.msg.author.nickname
        return

class CallGuest(CallHost):
    status:     int

    def __init__(self, userId):
        self.status     = None
        self.userId     = userId
        self.ndcId      = None
        self.threadId   = None
        return

@dataclass
class ContactInfo:
    host:               CallHost
    guests:             CallGuest
    chatType:           int
    threadId:           str

    def __init__(self, ctx, guestIds, chatType):
        if isinstance(guestIds, str): guestIds = [guestIds]
        self.host       = CallHost(ctx)
        self.guests     = list(map(lambda x: CallGuest(x), guestIds)) if chatType == MessageType.bidirectional else []
        self.threadId   = guestIds[0] if chatType == MessageType.unidirectional else None
        self.chatType   = chatType
        return
    
    def startMessage(self):
        return f"{self.host.nickname} solicita hablar contigo.\nPerfil: ndc://x{self.host.ndcId}/user-profile/{self.host.userId}\n\n-si: aceptar la llamada.\n-no: rechazar la llamada."

    async def createListener(self, ctx, guest):
        r = await utils.createMessageAwaiter(
                ctx,
                guest.ndcId,
                guest.userId,
                guest.threadId,
                self,
                receiver
                )
        return r

    async def createHostListener(self, ctx):
        r = await utils.createMessageAwaiter(
                ctx,
                self.host.ndcId,
                self.host.userId,
                self.host.threadId,
                self,
                sender
                )
        return r

    async def start_bidirectional(self, ctx):
        nicknames = []
        for guest in self.guests:
            chat = await ctx.client.start_chat(
                    invitee_ids=[guest.userId],
                    content=self.startMessage())
            guest.threadId  = chat.threadId
            guest.ndcId     = ctx.client.ndc_id
            guest.status    = await utils.confirmation(ctx, guest.threadId, guest.userId, ctx.msg.ndcId, timeout=300) 

            if guest.status is True:
                await self.createListener(ctx, guest)
                nicknames.append(await db.getUserNickname(ctx, guest.ndcId, user=None, userId=guest.userId))
            await asyncio.sleep(3)
        s = f"Iniciando llamada con {', '.join(nicknames)}." if len(nicknames) > 0 else None
        return s

    async def start_unidirectional(self, ctx):
        from src.subcommands.join import join_chat
        try:
            await join_chat(ctx, threadId=self.threadId)
        except Exception as e:
            await ctx.send("Error uniendo al chat.")
            return

        chat = await ctx.client.get_chat_info(self.threadId)
        s = f"Conectando llamada con el chat {chat.title}."
        return s

    async def start(self, ctx):
        self.host.threadId = ctx.msg.threadId
        if   self.chatType == MessageType.bidirectional  : s = await self.start_bidirectional(ctx)
        elif self.chatType == MessageType.unidirectional : s = await self.start_unidirectional(ctx)
        if s is not None:
            await self.createHostListener(ctx)
            await ctx.send(s)
        else:
            await ctx.send("La conexión ha sido cancelada por el contrario, o no ha respondido.")
        return self if s is not None else -1

    async def send_message(self, ctx, threadId, ndcId, message, mType):
        ctx.client.set_ndc(ndcId)
        if mType == "TEXT":     await ctx.client.send_message(
                                            message=message,
                                            chat_id=threadId
                                        )
        elif mType == "IMAGE":
            from src.imageSend import send_image
            await send_image(ctx, media=message, threadId=threadId)
        return
    
    async def send_bidirectional(self, ctx, userId, ndcId, message, mType):
        for guest in self.guests:
            if guest.userId == userId   :   continue
            if guest.status is not True :   continue
            await self.send_message(ctx, guest.threadId, ndcId, message, mType)

        if self.host.userId != userId:   await self.send_message(ctx, self.host.threadId, ndcId, message, mType)
        return

    async def send_unidirectional(self, ctx, userId, ndcId, message, mType):
        await self.send_message(ctx, self.threadId, ndcId, message, mType)
        return

    async def send(self, ctx, message=None, mType="TEXT"):
        userId  = ctx.msg.author.uid
        ndcId   = ctx.msg.ndcId

        if ctx.msg.content and message is None:
            message = ctx.msg.content
            mType   = "TEXT"
        elif ctx.msg.mediaValue and message is None:
            message = ctx.msg.mediaValue
            mType   = "IMAGE"
        elif message is None:
            return

        if   self.chatType == MessageType.bidirectional  :  await self.send_bidirectional(ctx, userId, ndcId, message, mType)
        elif self.chatType == MessageType.unidirectional :  await self.send_unidirectional(ctx, userId, ndcId, message, mType)
        return

    async def quit(self, ctx):
        userId      = ctx.msg.author.uid
        ndcId       = ctx.client.ndc_id
        threadId    = ctx.msg.threadId

        await ctx.send("Saliendo del modo contacto.")
        await self.send(ctx, message=f"{ctx.msg.author.uid} ha cerrado la conexión.")
        for guest in self.guests:
            if guest.userId == userId: guest.status = False
            utils.closeAwaiter(guest.ndcId, guest.userId, guest.threadId)
        
        utils.closeAwaiter(self.host.ndcId, self.host.userId, self.host.threadId)
        return

async def getLinkInfo(ctx, text):
    if text.find("pps.com/p/") == -1: return None
    userLink = text.split("pps.com/p/")[1]
    userLink = userLink.split(" ")[0]
    link = await ctx.client.get_info_link(f"http://aminoapps.com/p/{userLink}")
    return link.linkInfo.objectType, link.linkInfo.objectId


@utils.waitForMessage(message="*", callback=sender)
@utils.userTracker("--contactar")
async def contactUser(ctx):

    log = db.getLogConfig(ctx.msg.ndcId)
    if log.calls == 0:
        await ctx.send("Las llamadas están desactivadas en esta comunidad.")
        return -1

    if len(ctx.msg.content.split(" ")) < 2:
        await ctx.send("Debe añadir el link de un chat público, o de un usuario con el que quiera hablar.")
        return -1

    messageType = MessageType.bidirectional
    if ctx.msg.content.upper().find("-U") != -1:    messageType = MessageType.unidirectional

    objectType, objectId = await getLinkInfo(ctx, ctx.msg.content)

    if objectType not in [0, 12]:
        await ctx.send("El link ingresado no es válido. Para usar este comando, debe colocar el link de un usuario con el cual quiere hablar.")
        return -1
    
    chatType = 0
    if   objectType == 0 : chatType = MessageType.bidirectional
    elif objectType == 12: chatType = MessageType.unidirectional
    
    contactInfo = ContactInfo(ctx, objectId, chatType)
    response    = await contactInfo.start(ctx)
    return response
