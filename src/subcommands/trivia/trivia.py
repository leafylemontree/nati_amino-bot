from src import utils
from . import questions
from src import database
from src.games.base import BaseGame

class TriviaData(BaseGame):
    step            : int
    nextAnswer      : str
    questionArray   = []
    qType           = str

    def __init__(self, nick, userId, qType):
        self.userId = userId
        self.nick   = nick
        self.data   = []
        self.step   = 0
        self.nextAnswer = questions.random()
        self.qType  = qType
        self.questionArray = questions.getQuestions(self.qType)
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
        
    points = correct * 100 - wrong * 50
    message = f"[bc]Trivia terminada\n[c]--------------\n[c]{ctx.msg.author.nickname}\n\n[c]Resultados:{chain}\n\n[c]Has obtenido: {points} puntos"
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
async def trivia(ctx):
    com     = ctx.msg.content.lower().split()
    qType   = com[1] if len(com) > 1 else 'none'

    trivia  = TriviaData(ctx.msg.author.nickname, ctx.msg.author.uid, qType)
    qus     = questions.question(trivia.nick, trivia.step, trivia.nextAnswer, trivia.questionArray)   
    await ctx.send(qus)
    return trivia
