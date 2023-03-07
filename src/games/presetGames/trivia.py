from .base import BaseInstance
from src import utils
from src.subcommands.trivia.questions import *
from dataclasses import dataclass

@dataclass
class PlayerData:
    userId  :   str
    name    :   str
    correct :   int
    wrong   :   int
    points  :   int
    
    def c(self):
        self.correct += 1
        self.points  += 100
    
    def w(self):
        self.wrong   += 1
        self.points  -= 50

class Trivia(BaseInstance):
   
    class data:
        gameType    = 0
        q           = []
        answers     = []
        keys        = []
        turn        = 0
        lastKey     = ''
        control     = False
        minPlayers  = 1
        maxPlayers  = 12

    async def screen(self, ctx):
        key     = self.data.lastKey
        turn    = self.data.turn
        ansBy   = f"Respondido por: {ctx.msg.author.nickname}" 
        if turn == len(self.data.q)         : return
       
        print(key, self.data.answers[turn - 1])
        if key == self.data.answers[turn - 1]:  res = "¡Respuesta correcta! ✅"
        else                             :  res = "Respuesta incorrecta ❌"

        qt = question(None, turn, self.data.answers[turn], self.data.q)

        if self.data.lastKey != ''    : text = f'[c]{ansBy}\n[c]{res}\n\n{qt}'
        else                : text = qt
        return text

    
    async def logic(self, ctx, key):
        print(key)
        key         = key.upper().replace("-", "").split(" ")[0]
        turn        = self.data.turn
        playersuid  = [i[0] for i in self.players]
        if ctx.msg.author.uid not in playersuid       : return
        print(turn, len(self.data.q))
        if turn == len(self.data.q)         : return

        if key not in ['A', 'B', 'C', 'D']: return
        self.data.keys.append([key, self.indexPlayer(ctx.msg.author.uid)])
        self.data.turn += 1
        self.data.lastKey = key
        return await self.screen(ctx)

    async def win(self, ctx):
        if self.data.turn < len(self.data.q): return
        playerData = list(map(lambda p: PlayerData(p[0], p[1], 0, 0, 0), self.players))
        print(playerData)
        text = "[cb]Juego Terminado\n[c]--------------\n\n[cb]Sumario:\n"

        for i,(a,q) in enumerate(zip(self.data.answers, self.data.keys)):
            if a[0] == q[0]:
                playerData[q[1]].c()
                text += f"    - {i+1}: ✅ | {a} | {self.players[q[1]][1]}\n"
            else        :
                playerData[q[1]].w()
                text += f"    - {i+1}: ❌ | {a} | {self.players[q[1]][1]}\n"

        text += "\n\n[c]Jugadores:\n[c]--------------\n"
        
        pMostPoints = 0
        for i,p in enumerate(playerData):
            text += f"    - {p.name[:16]} : {p.correct} {'|' * p.correct}{' ' * p.wrong} {len(self.data.q)}\n"
            if p.points > playerData[pMostPoints].points:   pMostPoints = i

        self.data.turn = pMostPoints
        await ctx.send(text)
        return True

    async def lose(self, ctx):
        return

    def end(self):
        self.run         = False
        self.auth.isOpen = True
        self.data.keys = []
    
    def start(self):
        self.run            = True
        self.auth.isOpen    = False
        
        topics              = ['his', 'mat', 'cie', 'mus', 'pel', 'lib', 'cul']
        qst                 = []
        for topic in  topics: qst.extend(getQuestions(topic))
        self.data.q         = qst
        self.data.answers   = tuple(map( lambda a: random(),        range(len(topics) * 5) ))

