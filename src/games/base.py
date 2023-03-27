class BaseGame:
    userId          : str
    nick            : str
    data            : []
    step            : int

    def __init__(self, nick, userId):
        self.userId = userId
        self.nick   = nick
        self.data   = []
        self.step   = 0
    
    def doEveryStep(self):
        return

    def turn(self):
        self.step  += 1
        self.doEveryStep()
        return
