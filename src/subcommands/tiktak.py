from src import utils
import datetime
from src.subcommands.trivia.trivia import parseTime
from src.database import db

class Messages:
    INVALID     = 0
    ALREADY     = 1
    OK          = 2
    USER        = 3

class Win:
    NO          = None
    DRAW        = 0
    PLAYER1     = 1
    PLAYER2     = 2

class Cat:
    userId1:    str
    userId2:    str
    turn:       int
    data:       list
    last:       list
    timestamp:  datetime.datetime

    def __init__(self, userId1, userId2, nickname1, nickname2):
        self.userId1    = userId1
        self.userId2    = userId2
        self.nickname1  = nickname1
        self.nickname2  = nickname2
        self.turn       = 0
        self.data       = [0] * 9
        self.last       = (None, None)
        self.timestamp  = datetime.datetime.now()

    def parseMove(self, s):
        s = s.upper()[:2]
        y = 0 if s[0] == "A" else 1 if s[0] == "B" else 2 if s[0] == "C" else None
        x = 0 if s[1] == "1" else 1 if s[1] == "2" else 2 if s[1] == "3" else None
        return (x, y) 

    def arrayIndex(self, x, y):
        return x + (y * 3)

    def playerId(self, userId):
        if userId == self.userId1:  return 1
        if userId == self.userId2:  return 2
        return 0

    def play(self, userId, move):
        x, y = self.parseMove(move)
        if x is None or y is None:      return Messages.INVALID
        
        index = self.arrayIndex(x, y)
        if self.data[index] != 0:       return Messages.ALREADY

        player = self.playerId(userId)
        if player == 0:                 return Messages.USER

        self.data[index] = player
        self.turn += 1
        self.last = (x, y)
        return Messages.OK

    def win(self):
        player = ((self.turn - 1) & 0x1) + 1
    
        # horizontal
        c = 0
        for i in range(3):
            index = i + self.last[1] * 3
            if   self.data[index] == player : c += 1
            elif self.data[index] == 0      : return Win.NO
        if c == 3: return player

        # vertical
        c = 0
        for i in range(3):
            index = self.last[0] + i * 3
            if   self.data[index] == player : c += 1
            elif self.data[index] == 0      : return Win.NO
        if c == 3: return player

        if self.data[0] == self.data[1]:
            # \
            c = 0
            for i in range(3):
                index = i + i * 3
                if   self.data[index] == player : c += 1
                elif self.data[index] == 0      : return Win.NO
            if c == 3: return player

        if self.data[0] == (2 - self.data[1]):
            # \
            c = 0
            for i in range(3):
                index = (2 - i) + i * 3
                if   self.data[index] == player : c += 1
                elif self.data[index] == 0      : return Win.NO
            if c == 3: return player

        return Win.DRAW

    def piece(self, i):
        if   i == 0:  return " "
        elif i == 1:  return "O"
        elif i == 2:  return "X"
        return "?"

    def repr(self):
        a = self.piece(self.data[0])
        b = self.piece(self.data[1])
        c = self.piece(self.data[2])
        d = self.piece(self.data[3])
        e = self.piece(self.data[4])
        f = self.piece(self.data[5])
        g = self.piece(self.data[6])
        h = self.piece(self.data[7])
        i = self.piece(self.data[8])

        nick = self.nickname2 if (self.turn & 0x1) == 1 else self.nickname1

        return f"""
[c]Turno de: <$@{nick}$>
[c]----------------
[c]
[c].   1   2   3 
[c].  ---------------
[c]A   {a}  |  {b}  |  {c}  
[c].   -----+-----+-----
[c]B   {d}  |  {e}  |  {f}  
[c].   -----+-----+-----
[c]C   {g}  |  {h}  |  {i}  
[c]
"""

async def closeAwaiters(ctx, cat):
    utils.closeAwaiter(ctx.client.ndc_id, cat.userId1, ctx.msg.threadId)
    utils.closeAwaiter(ctx.client.ndc_id, cat.userId2, ctx.msg.threadId)
    return

async def drawCondition(ctx, cat):
    await ctx.send("¡Ha habido un empate!")
    await closeAwaiters(ctx, cat)
    db.modifyRecord(42, None, value=1,   userId=cat.userId1)
    db.modifyRecord(42, None, value=1,   userId=cat.userId2)
    return True

async def winCondition(ctx, cat, winner):
    nick    = cat.nickname1 if winner == 1 else cat.nickname2
    userIdW = cat.userId1   if winner == 1 else cat.userId2
    userIdL = cat.userId2   if winner == 1 else cat.userId1
    timerepr = parseTime(datetime.datetime.now() - cat.timestamp)
    await ctx.send(f"[c]¡{nick} ha ganado!\n\n[c]Tiempo:\n[c]{timerepr}")
    await closeAwaiters(ctx, cat)
    
    db.modifyRecord(40, None, value=1,   userId=userIdW)
    db.modifyRecord(41, None, value=1,   userId=userIdL)
    db.modifyRecord(43, None, value=500, userId=userIdW)
    return True

async def handler(ctx, ins):
    if ctx.msg.content.upper().find("-SALIR") == 0:
        await closeAwaiters(ctx, ins.data)
        await ctx.send(f"{ctx.msg.author.nickname} se ha retirado. El juego ha acabado.")
        return True

    if (ins.data.turn & 0x1) == 0 and ctx.msg.author.uid != ins.data.userId1: return False
    if (ins.data.turn & 0x1) == 1 and ctx.msg.author.uid != ins.data.userId2: return False
    userId = ins.data.userId2 if (ins.data.turn & 0x1) == 0 else ins.data.userId1

    r = ins.data.play(ctx.msg.author.uid, ctx.msg.content)
    if r == Messages.INVALID:
        await ctx.send("Ha ingresado su jugada de forma incorrecta. Debe ser así: A2")
        return False
    elif r == Messages.ALREADY:
        await ctx.send("La casilla ingresada ya está ocupada. Ingrese otra.")
        return False
    elif r == Messages.USER:
        await ctx.send("Es el turno del otro jugador. Espere su jugada.")
        return False
    elif r == Messages.OK:  await ctx.send(ins.data.repr(), mentions=[userId])
    
    winner = ins.data.win()
    if   winner == Win.NO               : return False
    elif winner == Win.DRAW             : return await drawCondition(ctx, ins.data)
    return await winCondition(ctx, ins.data, winner)

@utils.userId
@utils.userTracker("gato")
async def tiktaktoe(ctx, uid, msg):
    if ctx.msg.author.uid == uid:
        await ctx.send("Debes escoger a alguien más para jugar.")
        return -1

    user1 = await ctx.client.get_user_info(ctx.msg.author.uid)
    user2 = await ctx.client.get_user_info(uid)
    cat = Cat(user1.uid, user2.uid, user1.nickname, user2.nickname)
    ndcId       = ctx.client.ndc_id
    threadId    = ctx.msg.threadId

    await utils.createMessageAwaiter(ctx, ndcId, user1.uid, threadId, cat, handler)
    await utils.createMessageAwaiter(ctx, ndcId, user2.uid, threadId, cat, handler)
    await ctx.send(cat.repr(), mentions=[ctx.msg.author.uid])
    return

