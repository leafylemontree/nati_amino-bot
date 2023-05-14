import datetime
from src.database import db

class ChallengeAPI:
    none            = 0
    reputation      = 1
    level           = 2
    blogUpload      = 3
    postComment     = 4
    wallComment     = 5
    follow          = 6
    chatMembers     = 7
    chatCreated     = 8
    dailyMinutes    = 9
    weeklyMinutes   = 10
    moderation      = 11
    warnings        = 12
    strikes         = 13
    bans            = 14
    profileChange   = 15
    nickname        = 16
    chatMessage     = 17
    postFeatured    = 18
    quizUpload      = 19
    profileDays     = 20
    like            = 21
    likeAndComment  = 22
    
    def getLabel(c):
            label = ''
            if   c.type == ChallengeAPI.none            : label = f"Reto no fijado."
            elif c.type == ChallengeAPI.reputation      : label = f"Alcanzar {c.args} de reputación."
            elif c.type == ChallengeAPI.level           : label = f"Llegar a nivel {c.args}."
            elif c.type == ChallengeAPI.blogUpload      : label = f"Subir {c.args} blog a la comunidad."
            elif c.type == ChallengeAPI.postComment     : label = f"Comenta {c.args} publicaciones."
            elif c.type == ChallengeAPI.wallComment     : label = f"Comenta el muro de {c.args} usuarios."
            elif c.type == ChallengeAPI.follow          : label = f"Sigue a {c.args} usuarios."
            elif c.type == ChallengeAPI.chatMembers     : label = f"Ten un chat público con {c.args} miembros."
            elif c.type == ChallengeAPI.chatCreated     : label = f"Ten un chat con al menos {c.args} días." 
            elif c.type == ChallengeAPI.dailyMinutes    : label = f"Está activo {c.args} minutos en un día."
            elif c.type == ChallengeAPI.weeklyMinutes   : label = f"Está activo {c.args} minutos en una semana."
            elif c.type == ChallengeAPI.moderation      : label = f"Ten {c.args} moderaciones en una semana."
            elif c.type == ChallengeAPI.warnings        : label = f"Ten al menos {c.args} advertencias."
            elif c.type == ChallengeAPI.strikes         : label = f"Ten al menos {c.args} faltas."
            elif c.type == ChallengeAPI.bans            : label = f"Ten al menos {c.args} expulsiones."
            elif c.type == ChallengeAPI.profileChange   : label = f"Cambia tu perfil de la comunidad."
            elif c.type == ChallengeAPI.nickname        : label = f"Ten el nick \"{c.args}\" en tu perfil de la comunidad."
            elif c.type == ChallengeAPI.chatMessage     : label = f"Deja este mensaje en un chat: \"{c.args}\"."
            elif c.type == ChallengeAPI.postFeatured    : label = f"Ten al menos {c.args} blogs destados."
            elif c.type == ChallengeAPI.quizUpload      : label = f"Sube al menos {c.args} quizzes."
            elif c.type == ChallengeAPI.profileDays     : label = f"Ten al menos {c.args} días en la comunidad."
            elif c.type == ChallengeAPI.like            : label = f"Dale link a {c.args} publicaciones."
            elif c.type == ChallengeAPI.likeAndComment  : label = f"Dale link y deja un comentario en {c.args} publicaciones."
            return label

class ChallengeRequirement:
    type:   int
    args:   int
    start:  datetime.datetime
    end:    datetime.datetime
    silent: bool

    def __init__(self, ctype, args, silent, start=None, end=None) :
        self.type   = ctype
        self.args   = args
        self.start  = start
        self.end    = end
        self.silent = False

class CommunityChallenges:
    def __init__(self, ndcId, challenges):
        self.challenges = challenges
        self.ndcId      = ndcId
        self.levels     = len(challenges)

    def getLevelChallenge(self, level):
        challenge = None
        try:                challenge = self.challenges[level]
        except Exception:   challenge = None
        return challenge

    def levelRepr(self, level):
        challenge = self.getLevelChallenge(level)

        if challenge is None: return "No hay retos para este nivel"
        msg = " "
        for c in challenge:
            label = ChallengeAPI.getLabel(c)
            msg += f' - {label}\n'
        return msg

    async def check(self, ctx, level, data): # data is dict
        challenge = self.getLevelChallenge(level)
        checks    = []
        print(data, level)

        for i,(c, d) in enumerate(zip(challenge, data)):

            if      c.type == ChallengeAPI.none:
                checks.append(True)

            elif    c.type == ChallengeAPI.reputation:
                if d['reputation'] >= c.args:           checks.append(True)
                else:                                   return i

            elif    c.type == ChallengeAPI.level:
                if d['level'] >= c.args:                checks.append(True)
                else:                                   return i
    
            elif    c.type == ChallengeAPI.blogUpload:
                if len(d['blog']) < c.args:             return i
                if d['leastCreatedTime'] < c.start:     return i
                checks.append(True)

            elif    c.type == ChallengeAPI.postComment:
                if len(d['comments']) < c.args:         return i
                if d['leastCreatedTime'] < c.start:     return i
                checks.append(True)

            elif    c.type == ChallengeAPI.wallComment:
                if len(d['comments']) < c.args:         return i
                if d['leastCreatedTime'] < c.start:     return i
                checks.append(True)

            elif    c.type == ChallengeAPI.follow:
                if d['follow'] >= c.args:               checks.append(True)
                else:                                   return i

            elif    c.type == ChallengeAPI.chatMembers:
                if d['chatMembers'] < c.args:           return i
                checks.append(True)

            elif    c.type == ChallengeAPI.chatCreated:
                if d['chatCreatedTime'] >= c.start:    checks.append(True)
                else:                                   return i

            elif    c.type == ChallengeAPI.dailyMinutes:
                if d['dailyMinutes'] >= c.args:         checks.append(True)
                else:                                   return i

            elif    c.type == ChallengeAPI.weeklyMinutes:
                if d['weeklyMinutes'] >= c.args:        checks.append(True)
                else:                                   return i

            elif    c.type == ChallengeAPI.moderation:
                if d['moderation'] >= c.args:           checks.append(True)
                else:                                   return i

            elif    c.type == ChallengeAPI.warnings:
                if d['warnings'] >= c.args:             checks.append(True)
                else:                                   return i

            elif    c.type == ChallengeAPI.strikes:
                if d['strikes'] >= c.args:              checks.append(True)
                else:                                   return i

            elif    c.type == ChallengeAPI.bans:
                if d['bans'] >= c.args:                 checks.append(True)
                else:                                   return i

            elif    c.type == ChallengeAPI.profileChange:
                if d['profileChangeTime'] >= c.args:    checks.append(True)
                else:                                   return i

            elif    c.type == ChallengeAPI.nickname:
                if d['nickname'].find(c.args) != -1:    checks.append(True)
                else:                                   return i

            elif    c.type == ChallengeAPI.chatMessage:
                if d['chatMessage'].find(c.args) != -1: checks.append(True)
                else:                                   return i

            elif    c.type == ChallengeAPI.postFeatured:
                if len(d['blog']) < c.args:             return i
                if d['leastFeaturedTime'] < c.start:    return i
                checks.append(True)

            elif    c.type == ChallengeAPI.quizUpload:
                if len(d['quiz']) < c.args:             return i
                if d['leastCreatedTime'] < c.start:     return i
                checks.append(True)

            elif    c.type == ChallengeAPI.profileDays:
                if d['profileCreatedTime'] >= c.args:   checks.append(True)
                else:                                   return i

            elif    c.type == ChallengeAPI.like:
                if len(d['likes']) < c.args:            return i
                checks.append(True)

            elif    c.type == ChallengeAPI.likeAndComment:
                if len(d['likes']) < c.args:            return i
                if len(d['comments']) < c.args:         return i
                if d['leastCreatedTime'] < c.start:     return i
                checks.append(True)

        if len(checks) < len(challenge):    return False
        return True


    def dbUpdate(self, challenge, data, ndcId):

        for i,(c, d) in enumerate(zip(challenge, data)):

            if      c.type == ChallengeAPI.blogUpload:
                for blog in d['blog']: db.cursor.execute('INSERT INTO YincanaCheck VALUES (?, ?, ?, NOW());', (1, blog, ndcId))

            elif    c.type == ChallengeAPI.postComment:
                for comment in d['comments']: db.cursor.execute('INSERT INTO YincanaCheck VALUES (?, ?, ?, NOW());', (3, comment, ndcId))

            elif    c.type == ChallengeAPI.wallComment:
                for comment in d['comments']: db.cursor.execute('INSERT INTO YincanaCheck VALUES (?, ?, ?, NOW());', (3, comment, ndcId))

            elif    c.type == ChallengeAPI.chatMembers:
                for chat in d['threadId']: db.cursor.execute('INSERT INTO YincanaCheck VALUES (?, ?, ?, NOW());', (12, chat, ndcId))

            elif    c.type == ChallengeAPI.chatCreated:
                for chat in d['threadId']: db.cursor.execute('INSERT INTO YincanaCheck VALUES (?, ?, ?, NOW());', (12, chat, ndcId))
            
            elif      c.type == ChallengeAPI.postFeatured:
                for blog in d['blog']: db.cursor.execute('INSERT INTO YincanaCheck VALUES (?, ?, ?, NOW());', (1, blog, ndcId))

            elif      c.type == ChallengeAPI.quizUpload:
                for quiz in d['quiz']: db.cursor.execute('INSERT INTO YincanaCheck VALUES (?, ?, ?, NOW());', (1, quiz, ndcId))

            elif      c.type == ChallengeAPI.like:
                for objectType,objectId in zip(d['likes'], d['objectType']): db.cursor.execute('INSERT INTO YincanaCheck VALUES (?, ?, ?, NOW());', (objectType, objectId, ndcId))

            elif      c.type == ChallengeAPI.likeAndComment:
                for objectType,objectId in zip(d['likes'], d['objectType']): db.cursor.execute('INSERT INTO YincanaCheck VALUES (?, ?, ?, NOW());', (objectType, objectId, ndcId))


date = datetime.datetime(2023, 5, 1)


challenges = {
    9999 : CommunityChallenges(9999, [
                [
                    ChallengeRequirement(ChallengeAPI.blogUpload,       1, True, start=date)
                ],
                [
                    ChallengeRequirement(ChallengeAPI.level,           12, True),
                ],
                [
                    ChallengeRequirement(ChallengeAPI.likeAndComment,   3, True)
                ],
                [
                    ChallengeRequirement(ChallengeAPI.profileChange,    0, False, start=date)
                ],
                [
                    ChallengeRequirement(ChallengeAPI.level,            9, True),
                    ChallengeRequirement(ChallengeAPI.weeklyMinutes,  200, True)
                ],
                [
                    ChallengeRequirement(ChallengeAPI.level,           10, True),
                    ChallengeRequirement(ChallengeAPI.postFeatured,     1, True, start=date)
                ],
        ]),
    111610163: CommunityChallenges(111610163, [
                [
                    ChallengeRequirement(ChallengeAPI.level,           3, False)
                ],
                [
                    ChallengeRequirement(ChallengeAPI.level,           4, False)
                ],
                [
                    ChallengeRequirement(ChallengeAPI.nickname,     'aaaa', False),
                    ChallengeRequirement(ChallengeAPI.reputation,    3000, False),
                ],
                [
                    ChallengeRequirement(ChallengeAPI.blogUpload,    1, False, start=date),
                    ChallengeRequirement(ChallengeAPI.reputation,    3200, False),
                ],
                [   ChallengeRequirement(ChallengeAPI.blogUpload,    1, False, start=date) ],
                [   ChallengeRequirement(ChallengeAPI.postComment,    1, False, start=date) ],
                [   ChallengeRequirement(ChallengeAPI.wallComment,    1, False, start=date) ],
                [   ChallengeRequirement(ChallengeAPI.chatMembers,    1, False, start=date) ],
                [   ChallengeRequirement(ChallengeAPI.chatMessage,    'Hola', False, start=date) ],
                [   ChallengeRequirement(ChallengeAPI.postFeatured,    1, False, start=date) ],
                [   ChallengeRequirement(ChallengeAPI.like,    1, False, start=date) ],
                [   ChallengeRequirement(ChallengeAPI.likeAndComment,    1, False, start=date) ],
        ])
}
