from src import utils
from . import questions
from src import database
from src.games.base import BaseGame
import datetime
import math

class TriviaData(BaseGame):
    step            : int
    nextAnswer      : str
    questionArray   = []
    qType           = str
    start           = None

    def __init__(self, nick, userId, qType):
        self.userId         = userId
        self.nick           = nick
        self.data           = []
        self.step           = 0
        self.nextAnswer     = questions.random()
        self.qType          = qType
        self.questionArray  = questions.getQuestions(self.qType)
        self.startTime      = datetime.datetime.now()
        return
    
    def add(self, answer):
        self.data.append([answer, self.nextAnswer])
        if answer == self.nextAnswer : res = "¡Respuesta correcta! ✅"
        else                         : res = "Respuesta incorrecta ❌"

        self.step += 1
        self.nextAnswer = questions.random()
        return res

    def ended(self):
        if self.step == len(self.questionArray): return True
        return False

async def closeTrivia(ctx):
    await ctx.send(f"El usuario {ctx.msg.author.nickname} se ha retirado.")
    return True

def parseTime(deltatime):
    if isinstance(datetime, float):
        deltatime = datetime.timedelta(seconds=deltatime)

    m = ""
    if deltatime.days > 0: m += f"{deltatime.days} día"
    if deltatime.days > 1: m += f"s"

    seconds = deltatime.seconds
    minutes = (seconds // 60  ) % 60
    hours   = (seconds // 3600) % 24

    if hours    > 0: m += f" {hours} hora"
    if hours    > 1: m += f"s"
    if minutes  > 0: m += f" {minutes} minuto"
    if minutes  > 1: m += f"s"
    if seconds  > 0: m += f" {seconds % 60} segundo"
    if seconds  > 1: m += f"s"
    m += "."

    return m

def pointsCalculator(correct, wrong, timeElapsed):
    seconds = timeElapsed.seconds
    base    = correct * 100 - wrong * 50
    points  = base
    b = 0.572
    c = 0.969

    if      seconds < 10   : points = base * 2.5
    elif    seconds < 20   : points = base * 2
    elif    seconds < 30   : points = base * 1.75
    elif    seconds < 40   : points = base * 1.5
    elif    seconds < 60   : points = base * 1
    else                   :
        if base > 0:            points = base * (b ** ((seconds/60) - 1))
        else       :            points = (5000 + base) * (c ** ((seconds/60) - 1)) - 5000
    return base, int(points)


async def triviaEnding(ctx, data):
    correct = 0
    wrong   = 0
    chain   = ""

    for j,i in enumerate(data.data):
        if i[0] == i[1] :
            correct     += 1
            chain       += f"\n   {j + 1}. ✅"
        else            :
            wrong       += 1
            chain       += f"\n   {j + 1}. ❌ - {i[1]}"
        
    timeElapsed         = datetime.datetime.now() - data.startTime
    triviaTime          = parseTime(timeElapsed)
    basePoints, points  = pointsCalculator(correct, wrong, timeElapsed)
    ratio               = f"x{(points / basePoints):.2f}"
    message             = f"""
[bc]Trivia terminada
[c]--------------
[c]{ctx.msg.author.nickname}

[c]Resultados:{chain}

[c]Tiempo: {triviaTime}
[c]Has obtenido: {points} puntos
{('[c]Bonificación: ' + ratio) if basePoints < points else ('[c]Penalización: ' + ratio) if basePoints > points else ''}
"""
    database.db.modifyRecord(43, ctx.msg.author, points)
    await ctx.send(message)
    return True

async def register(ctx, ins):
    com = ctx.msg.content.upper()
    if com.find("-SALIR") == 0  : return await closeTrivia(ctx)

    res = ""
    if   com.find("-A") == 0      : res = ins.data.add("A")
    elif com.find("-B") == 0      : res = ins.data.add("B")
    elif com.find("-C") == 0      : res = ins.data.add("C")
    elif com.find("-D") == 0      : res = ins.data.add("D")
    elif com.find("-REPETIR") == 0: pass
    else                          : return False
   
    if ins.data.ended():
        return await triviaEnding(ctx, ins.data)
    
    qus = questions.question(ins.data.nick, ins.data.step, ins.data.nextAnswer, ins.data.questionArray)
    await ctx.send(f"[c]{res}\n\n{qus}")
    return False

@utils.waitForMessage("*", callback=register)
@utils.userTracker("trivia")
async def trivia(ctx):
    com     = ctx.msg.content.lower().split()
    qType   = com[1] if len(com) > 1 else 'none'

    trivia  = TriviaData(ctx.msg.author.nickname, ctx.msg.author.uid, qType)
    qus     = questions.question(trivia.nick, trivia.step, trivia.nextAnswer, trivia.questionArray)   
    await ctx.send(qus)
    return trivia
