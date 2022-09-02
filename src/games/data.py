from __future__ import annotations
from dataclasses import dataclass
from src import utils
from typing import List, Any
from edamino import Context, Client
from .functions import Functions
from .presetGames import Hangman, Auth, Wordle
from asyncio import sleep

class GameRoom:
    instances   = []
    lastRoom    = -1
    ctx         = None
    functions   = Functions()

    def isInRoom(self, uid):
        for i,j in enumerate(self.instances):
            for k,m in enumerate(j.players):
                if m[0] == uid: return i
        return False

    def isAdminRoom(self, uid):
        for i,j in enumerate(self.instances):
            if j.auth.uid == uid: return i
        return False
    
    def getIndexById(self, Id):
        for i,j in enumerate(self.instances):
            if j.roomId == Id: return i
        return False
    
    async def printRoom(self, ctx, index):
        m = f"""
Id: {self.instances[index].roomId}
Creada por: {self.instances[index].auth.nickname}
Juego: {self.instances[index].game}
Jugadores:
"""
        for i,j in enumerate(self.instances[index].players):
            m += f"  {i+1}. {j[1]}\n"

        await ctx.client.send_message(message=m,
                                    chat_id=self.instances[index].threadId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None)
        return


    @utils.checkFor(m=1, M=3, notcount=2, copy=2)
    @utils.checkType('s', 's', 's')
    async def createRoom(self, ctx, msg):
        if self.ctx is None: self.ctx = ctx
        """
            0 : game
            1 : mode
            2 : password
        """
        if self.isInRoom(ctx.msg.author.uid) is not False:
            return await ctx.send("Usted ya está en una sala")
        
        if len(msg) > 1:
            if msg[1].upper() == "PRIVADA":
                if len(msg) > 3: return await ctx.send("Debe ingresar una contraseña para la sala")
                auth = Auth(msg[2], True, msg[1].upper(), ctx.msg.author.nickname, ctx.msg.author.uid)
        else:
            auth = Auth(None, True, "PUBLICA", ctx.msg.author.nickname, ctx.msg.author.uid)

        if   msg[0].upper() == "AHORCADO": data = Hangman
        if   msg[0].upper() == "WORDLE"  : data = Wordle
        else                             : data = None

        self.lastRoom += 1
        self.instances.append( data(
             self.lastRoom, ctx.msg.threadId, ctx.msg.ndcId, [[ctx.msg.author.uid, ctx.msg.author.nickname]], msg[0], auth))
        
        r = self.getIndexById(self.lastRoom)
        await self.printRoom(ctx, r)
        print(self)
        return

    @utils.checkFor(m=1, M=2, notcount=2, copy=2)
    @utils.checkType('i', 's')
    async def joinRoom(self, ctx, msg):
        if self.isInRoom(ctx.msg.author.uid) is not False:
            return await ctx.send("Usted ya está en una sala")
        r = self.getIndexById(msg[0])
        if r is False:
            return await ctx.send("Esta sala no existe")
        self.instances[r].players.append([ctx.msg.author.uid, ctx.msg.author.nickname])
        await self.printRoom(ctx, r)
        return

    @utils.checkFor(m=0, M=1, notcount=2, copy=2)
    async def leaveRoom(self, ctx, msg):
        s = self.isInRoom(ctx.msg.author.uid)
        print(s, type(s))
        if s is False:
            return await ctx.send("Usted no está en una sala")
        self.instances[s].players.remove([ctx.msg.author.uid, ctx.msg.author.nickname])
        await self.printRoom(ctx, s)
        return

    @utils.checkFor(m=1, M=1, notcount=2, copy=2)
    @utils.checkType('i')
    async def closeRoom(self, ctx, msg):
        r = self.getIndexById(msg[0])
        s = self.isAdminRoom(ctx.msg.author.uid)
        print(s, type(s))
        if s is False or r != s:
            return await ctx.send("Usted no es el administrador de la sala, o bien la sala no existe.")
        self.instances.pop(r)
        await ctx.send(f"Sala {msg[0]} eliminada")
        return

    @utils.checkFor(m=1, M=1, notcount=2, copy=2)
    @utils.checkType('i')
    async def start(self, ctx, msg):
        r = self.getIndexById(msg[0])
        s = self.instances[r].auth.uid
        if r is False               : return await ctx.send("La sala seleccionada no existe")
        if ctx.msg.author.uid != s  : return await ctx.send("Usted no es el dueño de esta sala")
        print(r)
        await self.functions.send(self.ctx, ctx.msg.threadId, f"El juego {self.instances[r].game} ha sido iniciado por {self.instances[r].auth.nickname}", self.instances[r].ndcId, ghost=True)
        self.instances[r].start()
        t = await self.instances[r].screen(ctx)
        if t: await self.functions.send(self.ctx, self.instances[r].threadId, t, self.instances[r].ndcId)
        return

    @utils.checkFor(m=1, M=24, notcount=1, copy=2)
    async def run(self, ctx, msg):
        r = self.isInRoom(ctx.msg.author.uid)
        if r is False: return await ctx.send("Usted no está jugando")
        
        t =  await self.instances[r].logic(ctx, msg[0])
        if t: await self.functions.send(self.ctx, self.instances[r].threadId, t, self.instances[r].ndcId)

        await sleep(1)
        if await self.instances[r].win():
            player = self.instances[r].players[(self.instances[r].data.turn-1) % len(self.instances[r].players)][1]
            await self.functions.send(self.ctx, self.instances[r].threadId, f"¡{player} es el ganador!", self.instances[r].ndcId)
            await sleep(1)
            await self.functions.send(self.ctx, self.instances[r].threadId, f"La sala {self.instances[r].roomId} ha finalizado el juego", self.instances[r].ndcId, ghost=True)
            self.instances[r].end()
        
        if await self.instances[r].lose():
            player = self.instances[r].players[(self.instances[r].data.turn-1) % len(self.instances[r].players)][1]
            await self.functions.send(self.ctx, self.instances[r].threadId, f"{player} ha perdido", self.instances[r].ndcId)
            await sleep(1)
        return

ga = GameRoom()
