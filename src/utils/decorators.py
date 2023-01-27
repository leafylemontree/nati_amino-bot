from edamino import Context
from typing import List

leafId    =  "17261eb7-7fcd-4af2-9539-dc69c5bf2c76"
noMessage = "Usted no está autorizado para ejercer este comando"


def isStaff(func):
    async def check(*args, **kwargs):
        ctx = None
        for arg in args:
            if isinstance(arg, Context): ctx = arg
        if ctx is None: return

        if ctx.msg.author.role == 0 and ctx.msg.author.uid != leafId:
                await ctx.send(noMessage)
                return
        r = await func(*args, **kwargs)
        return r
    return check

def userId(func):
    async def check(ctx):
        uid = ctx.msg.author.uid
        msg = ctx.msg.content
        if ctx.msg.extensions.mentionedArray:
            uid = ctx.msg.extensions.mentionedArray[0].uid
            msg = msg.split("\u200e")[0]
        elif ctx.msg.extensions.replyMessage:             uid = ctx.msg.extensions.replyMessage.author.uid
        await func(ctx, uid, msg)
        return
    return check

def ban(func):
    async def check(ctx):
        if ctx.msg.author.role not in [100, 101, 102] and ctx.msg.author.uid != leafId:
            await ctx.send(noMessage)
            return

        msg = ctx.msg.content
        uid = ctx.msg.author.uid

        reason = msg.split(" ")
        if len(reason) == 1: reason = "Acción hecha a petición"
        else               :
            reason.pop(0)
            reason = " ".join(reason)
        replyMsg = ctx.msg.extensions.replyMessage
        userList = []

        if replyMsg:
            rep      = replyMsg.content.split("\n")
            for n,r in enumerate(rep):
                if r.upper().find("ID: ") == -1: continue
                userList.append(r.split(" ")[1])

            if userList == []:
                userList.append(replyMsg.author.uid)
        elif ctx.msg.extensions.mentionedArray:
            userList.append(ctx.msg.extensions.mentionedArray[0].uid)
            reason = reason.split("\u200e")[0]
        elif ctx.msg.content.find("http://aminoapps") != -1:
            userLink = ctx.msg.content.split("http://aminoapps.com/p/")
            link = await ctx.client.get_info_link(f"httpd://aminoapps.com/p/{userLink[-1]}")
            if link.linkInfo.objectType != 0: await ctx.send("Solo funciona con usuarios")
            userList.append(link.linkInfo.objectId)
            reason = userLink[0].split(" ")
            reason.pop(0)
            reason = " ".join(reason)
        else: return await ctx.send("Debe responde a un mensaje para banear al usuario.")
        
        fr = await func(ctx, userList[0], reason)
        return fr
    return check

def cutes(func):
    async def wrapper(ctx):
        uid = None
        if ctx.msg.extensions.mentionedArray:
            uid = ctx.msg.extensions.mentionedArray[0].uid
        elif ctx.msg.extensions.replyMessage:
            uid = ctx.msg.extensions.replyMessage.author.uid
        else:
            return await ctx.send("Debe usar este comando mencionando a alguien.\n\nLa sintaxis luce algo así: --cutes pat @usuario")
        
        msg = ctx.msg.content.split("\u200e")[0]
        msg = msg.upper().split(" ")
        msg = list(filter(("").__ne__, msg))
        if len(msg) == 1: return await ctx.send("Falta un argumento para la acción.\n\nPista: hug, pat, kiss")
        print(uid)
        await func(ctx, uid, msg)
    return wrapper

def safe(func):
    async def wrapper(ctx):
        from src.database import db
        chat = db.getChatConfig(ctx.msg.threadId)
        if chat.safe: return "Comando deshabilitado"
        r = await func(ctx)
        return r
    return wrapper

def checkFor(m=0, M=1, notcount=1, copy=1):
    def mn(func):
        async def wrapper(*args, **kwargs):
            ctx = None
            for arg in args:
                if isinstance(arg, Context): ctx = arg
            if ctx is None: return

            msg = ctx.msg.content 
            msg = msg.split(" ")
            if len(msg)-notcount < m:
                await ctx.send(f"¡Muy pocos argumentos! Se esperan: {m}")
                return None
            if len(msg)-notcount > M:
                await ctx.send(f"¡Demasiados argumentos! Se esperan: {M}")
                return None
            
            a = []
            for i in range(copy): a.append(args[i])
            a.append(msg[notcount:])
            r = await func(*a, **kwargs)
            return r
        return wrapper
    return mn

def checkType(*listargs):
    def mn(func):
        async def wrapper(*args, **kwargs):
            ctx = None
            msg = None
            for arg in args:
                print(type(arg), arg)
                if isinstance(arg, Context): ctx = arg
                elif type(arg) == list: msg = arg
            if ctx is None or msg is None: return

            typedArgs  = []
            failedArgs = []
            convert = True
            for i,(a,b) in enumerate(zip(listargs, msg)):
                if convert:
                    if   a == "i":
                        try     : typedArgs.append(int(b))
                        except  : failedArgs.append(i+1)
                    elif a == "s":
                        try     : typedArgs.append(str(b))
                        except  : failedArgs.append(i+1)
                    elif a == "f":
                        try     : typedArgs.append(float(b))
                        except  : failedArgs.append(i+1)
                    elif a == ".":
                        convert = False
                    else         :
                        typedArgs.append(b)
                if not convert:
                    typedArgs.append(str(b))

            if failedArgs:
                return await ctx.send(f"Los parámetros {failedArgs} no son del tipo correcto.")
            a = list(args)
            a.pop(-1)
            a.append(typedArgs)
            r = await func(*a, **kwargs)
            return 
        return wrapper
    return mn




###########################
#
#   Esperar por confirmación
#
###########################


class AW:
    def __init__(self, userId, ndcId, threadId, message, func, content, fcargs=None):
        self.userId     = userId
        self.ndcId      = ndcId
        self.threadId   = threadId
        self.message    = message
        self.func       = func
        self.content    = content
        self.data       = None
        self.fcargs     = fcargs

class Waiting:
    aw = []

    def add(self, userId, ndcId, threadId, message, func, content, fcargs):
        self.aw.append(
                AW(userId, ndcId, threadId, message, func, content, fcargs)
            )
        return

    def look(self, userId, ndcId, threadId, message):
        for index, ins in enumerate(self.aw):
            if ins.userId   != userId           : continue
            if ins.ndcId    != ndcId            : continue
            if ins.threadId != threadId         : continue
            print(ins.message, message)
            if (message.upper().find(ins.message.upper()) != 0) and (ins.message != '*')  : continue
            return index, ins
        return -1, None

    def delete(self, index):
        self.aw.pop(index)
        return
    
    def retrieve(self, userId, ndcId, threadId):
        for index, ins in enumerate(self.aw):
            if ins.userId   != userId   : continue
            if ins.ndcId    != ndcId    : continue
            if ins.threadId != threadId : continue
            return index
        return -1

    def editData(self, userId, ndcId, threadId, data=None):
       index = self.retrieve(userId, ndcId, threadId)
       if index == -1: return
       self.aw[index].data = data
       return self.aw[index]
   
    def eraseEverything(self):
       self.aw = []
       return

    def clearIfUserRegistered(self, userId):
        while True:
            awl     = self.aw.copy()
            f_match = False
            for i,aw in enumerate(awl):
                if aw.userId == userId:
                    self.aw.pop(i)
                    f_match = True
                    break
            if f_match is False : return True

waiting = Waiting()

async def clbdefault(ctx):
    print("CALLBACK NOT SET")
    return

def waitForMessage(message="-si", timeout=None, callback=clbdefault, fcargs=None):
    def main(func):
        async def wrapper(ctx, *args, **kwargs):
            threadId    = ctx.msg.threadId
            ndcId       = ctx.client.ndc_id
            userId      = ctx.msg.author.uid
            content     = ctx.msg.content.split(" ")

            index, ins = waiting.look(userId, ndcId, threadId, message.upper())
            if ins: return

            #waiting.clearIfUserRegistered(userId)
            waiting.add(userId, ndcId, threadId, message.upper(), callback, content, fcargs)
            response = await func(ctx, *args, **kwargs)
            if response: waiting.editData(userId, ndcId, threadId, data=response)
            return
        return wrapper
    return main


async def waitForCallback(ctx):
    threadId    = ctx.msg.threadId
    ndcId       = ctx.client.ndc_id
    userId      = ctx.msg.author.uid
    msg         = ctx.msg.content.upper()

    index, ins = waiting.look(userId, ndcId, threadId, msg.upper())
    if not ins: return
    
    response = False
    try:
        if ins.fcargs: response = await ins.func(ctx, ins, ins.fcargs)
        else         : response = await ins.func(ctx, ins)
    except Exception as e:
        print(e)

    if response:
        while True:
            index = waiting.retrieve(userId, ndcId, threadId)
            if index == -1: break
            waiting.delete(index)
    return 

async def clearAW(ctx):
    waiting.eraseEverything()
    await ctx.send("Se han limpiado los registros de mensajes en cadena")
