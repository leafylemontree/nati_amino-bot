from src.communication.client import sc
import uuid
from src import objects

class RemoteReceiver: # You

    def __init__(self, instance, remoteChatId, threadId, userId, ndcId):
        self.instance       = instance
        self.remoteChatId   = remoteChatId
        self.threadId       = threadId
        self.userId         = userId
        self.ndcId          = ndcId

    def generateData(self, status, message):
        return  {
            "remoteChatId" : self.remoteChatId,
            "content"      : message,
            "status"       : status.upper(),
            "threadId"     : threadId,
            "userId"       : userId,
            "ndcId"        : ndcId
            }

    async def send(self, message):
        data = self.generateData("SEND", message)
        await sc.send(
                dtype=6,
                request=data,
                destinatary=self.instance,
                nodeId=None
            )
        
    async def close(self, message):
        data = self.generateData("CLOSE", '\0')
        await sc.send(
                dtype=6,
                request=data,
                destinatary=self.instance,
                nodeId=None
            )


class RemoteSender: # The one talking

    def __init__(self, instance, remoteChatId, threadId, userId, ndcId):
        self.instance       = instance
        self.remoteChatId   = remoteChatId
        self.threadId       = threadId
        self.userId         = userId
        self.ndcId          = ndcId

    

class RemoteChatElement:

    def __init__(self, ndcId, threadId, userId, remoteChatId):
        self.ndcId          = ndcId,
        self.threadId       = threadId
        self.userId         = userId
        self.remoteChatId   = remoteChatId
        self.isReady        = False

    async def connectionReady(self, socketResponse):
        self.receiver = RemoteReceiver(
                    socketResponse.instance,
                    self.remoteChatId,
                    socketResponse.content.threadId,
                    socketResponse.content.userId,
                    socketResponse.content.ndcId
                )

        self.sender     = RemoteSender(
                    objects.ba.instance,
                    self.remoteChatId,
                    self.threadId,
                    self.userId,
                    self.ndcId
                )
        self.isReady = True
        return

    async def remoteClose(self, socketResponse):
        await self.receiver.close()
        return 

class RemoteChat:

    def __init__(self):
        self.chatrooms = []
        return

    async def newChatroom(self, ctx, code):
        ndcId       = ctx.msg.ndcId
        threadId    = ctx.msg.threadId
        userId      = ctx.msg.author.uid
        
        codes = [chat.remoteChatId for chat in self.chatrooms]
        if code in codes: return await ctx.send("Una sala con este código ya existe. Pruebe con otro")

        self.chatrooms.append(
                    RemoteChatElement(ndcId, threadId, userId, code)
                )
        
        await ctx.send(f"Sala de chat con código {code} creada. Esperando respuesta del servidor")
        return

    async def removeChatroom(self, ctx, code):
        userId      = ctx.msg.author.userId
        index       = None

        for i,chat in enumerate(self.chatrooms):
            if chat.remoteChatId != code: continue
            if chat.userId       != userId: return await ctx.send("No es el propietario de la sala")
            index   = i

        if index is None    :   return await ctx.send("No se ha encontrado el chat, unu")
        await self.chatrooms[i].close()
        self.chatrooms.pop(index)
        return await ctx.send("Sala cerrada")

    async def send(self, ctx, message):
        for chat in self.chatrooms:
            if chat.userId != ctx.msg.author.uid : continue

            if chat.isReady is False: return
            await chat.receiver.send(message)


    async def handler(self, ctx):
        
        for chat in self.chatrooms:
            if chat.userId != ctx.msg.author.uid : continue

            message = ctx.msg.content.split(" ")
            if len(message) < 2: return await ctx.send("Debe ingresar un mensaje a enviar")

            if message[1].upper() == '-CERRAR': return await removeChatroom(ctx, chat.remoteChatId)
            if hasattr(chat, 'receiver'): await chat.receiver.send(" ".join(message[1:]))
            await self.send(ctx, " ".join(message[1:]))

        code = ctx.msg.content.split(" ")
        if len(code) < 2: return await ctx.send("Debe ingresar un código de sala")
        await self.newChatroom(ctx, code[1])
        
        data = {
                "remoteChatId" : " ".join(ctx.msg.content.split(" ")[1]),
                "content"      : '',
                "status"       : "OPEN",
                "threadId"     : ctx.msg.threadId,
                "userId"       : ctx.msg.author.uid,
                "ndcId"        : ctx.msg.ndcId
            }

        await sc.send(
                dtype=6,
                request=data,
                destinatary=-1,
                nodeId=None
            )
        return
        
rc = RemoteChat()
