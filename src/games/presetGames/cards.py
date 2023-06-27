from .base import BaseInstance
from dataclasses import dataclass
import random
from src import utils


@dataclass
class EscobaCards:
    number:     int
    type:       int
    
    def __repr__(self):
        typeNames = ['Oro', 'Copa', 'Espada', 'Basto']
        numNames  = ['1', '2', '3', '4', '5', '6', '7', 'Sota', 'Caballo', 'Rey']
        return f"{numNames[self.number]} - {typeNames[self.type]}"

    def value(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        return values[self.number]

@dataclass
class CardsPlayerData:
    userId      : str
    escobas     : int
    
    def __init__(self, userId, cards):
        self.userId     = userId
        self.cards      = cards
        self.escobas    = 0
        self.takenCards = []
        return

@dataclass
class CardsCurrentSelect:
    def __init__(self):
        self.hand       = []
        self.board      = []
        self.executed   = 0
        self.leave      = 1
        return

    def reset(self):
        self.hand       = []
        self.board      = []
        self.executed   = 0
        self.leave      = 1
        return

@dataclass
class CardsGameData:
    minPlayers   = 1
    maxPlayers   = 6

    def __init__(self, players):
        self.cards          = []
        self.onBoardCards   = []
        self.playerData     = []
        self.cards = [EscobaCards(i % 10, i // 10) for i in range(0, 8)]
        random.shuffle(self.cards)
        for i in range(4): self.onBoardCards.append(self.cards.pop(0))
        self.turn  = 0

        print(players)
        for player in players:
            cards = [ self.cards.pop(0) for j in range(3) ]
            self.playerData.append( CardsPlayerData(player[0], cards) )

        self.select = CardsCurrentSelect()
        return


class Escoba(BaseInstance):
    
    def on_start(self):
        print(self.players)
        self.data = CardsGameData(self.players)
        return

    async def screen(self, ctx):
        remainCards  = len(self.data.cards)
        onBoardCards = [f'[c]{i+1}. {card}\n' for i,card in enumerate(self.data.onBoardCards)]

        return f"""
[c]Sala: {self.roomId} ---- Juego: Escoba
[c]----------------------------------------
[c]Turno de: {self.players[self.data.turn][1]}

[c]Cartas restantes: {remainCards}
[cb]Cartas en la mesa:
{''.join(onBoardCards)}
[cb]Comandos:
-j mano (número)
-j mesa (número)
-j dejar (número)
-j tomar
-j reiniciar
-j ver
-j ejecutar
"""

    def parseNumbers(self, key):
        print(key)
        nums = []
        key  = key.split(" ")
        for k in key:
            try:                nums.append(int(k) - 1)
            except ValueError:  pass
        print(nums)
        return nums

    async def hand(self, ctx, key):
        self.data.select.hand = self.parseNumbers(key)[:1]
        index                 = self.indexPlayer(ctx.msg.author.uid)

        for item in self.data.select.hand:
            if item > len(self.data.playerData[index].cards): return False
            if item < 0:                                      return False

        await ctx.send("Selección guardada.")
        return None 

    async def board(self, ctx, key):
        self.data.select.board = self.parseNumbers(key)

        for item in self.data.select.board:
            if item > len(self.data.onBoardCards): return False
            if item < 0:                           return False

        await ctx.send("Selección guardada.")
        return None

    async def reset(self, ctx, key):
        self.data.select.reset()
        await ctx.send("Selección reiniciada.")
        return None

    async def retrieve(self, ctx, key):
        index   = self.indexPlayer(ctx.msg.author.uid)
        hand    = [f"[c]{i+1}. {card}\n" for i,card in enumerate(self.data.playerData[index].cards)]
        handSelect  = [f"[c]{n+1}. {self.data.playerData[index].cards[n]}\n" for n in self.data.select.hand]
        boardSelect = [f"[c]{n+1}. {self.data.onBoardCards[n]}\n" for n in self.data.select.board]
        msg = f"""
[cb]Cartas en mano de {self.players[index][1]}
{"".join(hand)}

[cb]Seleccionadas:

[cu]Mano:
{''.join(handSelect)}

[cu]Mesa:
{''.join(boardSelect)}
"""
        await ctx.client.start_chat(invitee_ids=[ctx.client.uid, ctx.msg.author.uid], content=msg)
        return None

    async def remove(self, index):
        handCopy   = self.data.playerData[index].cards.copy()
        handSelect = list(set(self.data.select.hand))
        handSelect.sort(reverse=True)
        for i in handSelect:
            card = self.data.playerData[index].cards.pop(i)
            self.data.playerData[index].takenCards.append(card)

        boardCopy   = self.data.onBoardCards
        boardSelect = list(set(self.data.select.board))
        boardSelect.sort(reverse=True)
        for i in boardSelect:
            self.data.onBoardCards.pop(i)
            self.data.playerData[index].takenCards.append(card)


        return True

    def matchCards(self, index):
        hand  = self.data.playerData[index].cards
        board = self.data.onBoardCards

        value = 0
        for card in set(self.data.select.hand):
            value += hand[card].value()

        for card in set(self.data.select.board):
            value += board[card].value()

        print(f"Card values: {value}")
        if value == 15: return True
        return False

    async def execute(self, ctx, key):
        if self.data.select.executed == 1:
            await ctx.send("Ya ha ejecutado su acción. Debe dejar una carta para darle el pase al siguiente usuario.\n\n-j dejar (carta)")
            return False

        index   = self.indexPlayer(ctx.msg.author.uid)

        if self.data.select.hand == []:
            await ctx.send("Debe seleccionar una carta de su mano. Si no tiene ninguna para hacer 15, use -j dejar (carta)")
            return False
        if self.data.select.board == []:
            await ctx.send("Debe seleccionar al menos una carta de la mesa. Si no tiene ninguna para hacer 15, use -j dejar (carta)")
            return False

        if self.matchCards(index):
            await self.remove(index)
            self.data.playerData[index].escobas += 1
            await ctx.send("¡Excelente! Has hecho una escoba. Ahora debes dejar una carta con -j dejar (carta)")
            self.data.select.reset()

            if len(self.data.onBoardCards) == 0:
                self.data.select.leave = 0
                if len(self.data.cards) == 0: pass
                card = self.data.cards.pop(0)
                self.data.onBoardCards.append(card)
                return True

        else:
            await ctx.send("Que mal, las cartas seleccionadas no suman 15, :c. Seleccione otras cartas.")

        return None

    async def leave(self, ctx, key):
        num     = self.parseNumbers(key)[0]
        index   = self.indexPlayer(ctx.msg.author.uid)
        
        if   num < 0:
            await ctx.send("Esta carta es inválida. Seleccione otra.")
            return False
        elif num > len(self.data.playerData[index].cards):
            await ctx.send("Esta carta es inválida. Seleccione otra.")
            return False
        
        card = self.data.playerData[index].cards.pop(num)
        self.data.onBoardCards.append(card)
        return True

    async def take(self, ctx, key):
        index   = self.indexPlayer(ctx.msg.author.uid)
        if len(self.data.cards) == 0:
            await ctx.send("No puede tomar más cartas. El mazo está vacío.")
            return False

        card = self.data.cards.pop(0)
        self.data.playerData[index].cards.append(card)
        await ctx.send(f"{ctx.msg.author.nickname} ha tomado una carta del mazo. Revisa tus cartas con -j ver")
        return None

    async def logic(self, ctx, key):
        print("-------- logic --------")
        print(self.data.playerData)
        print(self.data.playerData[0])
        print(self.data.playerData[0].userId)
        print(self.players)
        print(self.data.turn)
        print(self.indexPlayer(ctx.msg.author.uid))
        print("--------       --------")
        if self.indexPlayer(ctx.msg.author.uid) != self.data.turn: return None

        key = ctx.msg.content.upper()
        r   = None
        if   key.find("MANO")  != -1 : r = await self.hand(ctx, key)
        elif key.find("MESA")  != -1 : r = await self.board(ctx, key)
        elif key.find("REINI") != -1 : r = await self.reset(ctx, key)
        elif key.find("VER")   != -1 : r = await self.retrieve(ctx, key)
        elif key.find("EJECU") != -1 : r = await self.execute(ctx, key)
        elif key.find("DEJAR") != -1 : r = await self.leave(ctx, key)
        elif key.find("TOMAR") != -1 : r = await self.take(ctx, key)

        # r is True  : pass turn
        # r is False : error
        # r is None  : no message

        if r is True:
            self.data.select.reset()
            self.data.turn = (self.data.turn + 1) % len(self.players)
            scr = await self.screen(ctx)
            await ctx.send(str(scr))

        print(r)
        return

    async def win(self, ctx):
        if len(self.data.cards) > 0: return None

        cardValue = {}
        for player in self.data.playerData:
            if player.userId not in cardValue.keys():  cardValue[player.userId] = 0
            for card in player.cards:
                cardValue[player.userId] += card.value()

        points = {}
        for player in self.data.playerData:
            if player.userId not in points.keys(): points[player.userId] = player.escobas
        
        key = max(cardValue, key=cardValue.get)
        points[key] += 1
        
        user  = max(points, key=points.get)
        index = self.indexPlayer(user)
        self.data.turn = index + 1
        return True

