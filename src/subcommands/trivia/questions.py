import random as rd

ANSWER      = ['A', 'B', 'C', 'D']
qTypes = [
            ['history',     'Historia'],
            ['math',        'Matemática'],
            ['science',     'Ciencia'],
            ['culture',     'Cultura'],
            ['movies',      'Películas'],
            ['books',       'Literatura'],
            ['music',       'Música'],
        ]

def updateQuestions():
    import json

    with open('src/subcommands/trivia/data.json') as f:
        data = json.load(f)

    return data["questions"]

questions = updateQuestions()

def addQuestion(questionData):
    newQuestion = {
                "question"  : questionData.question,
                "correct"   : questionData.correct,
                "wrong"     : questionData.wrong,
                "type"      : questionData.qType
            }
    return

def getTopic(qType):
    for i,q in enumerate(qTypes):
        if q[0] == qType: return q[1]
    return None

def getFromLoc(loc):
    for i,q in enumerate(qTypes):
        if q[1].lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').find(loc[:3].replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')) == 0: return q[0]
    return None

def question(nick, step, answer, qArray):
    q = qArray[step][0]
    qType = qArray[step][1]

    header  = questions[qType][q]['question']
    correct = questions[qType][q]['correct']
    wrong   = questions[qType][q]['wrong']

    response = f"[cb]Pregunta {step + 1}:\n[c]--------------\n[c]{nick}\n[c]Tema: {getTopic(qType)}\n\n[c]{header}\n\n"

    answers = wrong.copy()
    answers.insert(ANSWER.index(answer), correct)

    for i, (letter, ans) in enumerate(zip(ANSWER, answers)):
        response += f"\n    -{letter} : {ans}"

    response += f"\n\n[c]{step} - {'| ' * step}_ {'. ' * (len(qArray) - step - 1)}- {len(qArray)}"

    return response

def random():
    num     = rd.random()
    letter  = ['A', 'B', 'C', 'D']
    return letter[ int(num * 4) ]

def getQuestions(loc):
    loc   = loc.lower()
    qType = getFromLoc(loc)
    o = []

    if qType is None:
        for i in range(5):
            while True:
                topic       = qTypes[int(len(questions) * rd.random())][0]
                question    = [int(len(questions[topic]) * rd.random()), topic]

                if question not in o:
                    o.append(question)
                    break
    else:
        fullList = [*range(len(questions[qType]))]
        rd.shuffle(fullList)
        fullList = fullList[:5]
        for i in fullList: o.append([i, qType])
    return o





