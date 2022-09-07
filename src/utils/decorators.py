from edamino import Context
from typing import List

leafId    =  "17261eb7-7fcd-4af2-9539-dc69c5bf2c76"
noMessage = "Usted no está autorizado para ejercer este comando"


def isStaff(func):
    async def check(ctx):
        if ctx.msg.author.role == 0 and ctx.msg.author.uid != leafId:
                await ctx.send(noMessage)
                return
        r = await func(ctx)
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
            msg.pop(0)
            reason = " ".join(msg)
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
        from src.config.data import Config
        if ctx.msg.threadId in Config.safe_mode: return "Comando deshabilitado"
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
                await ctx.send(f"¡Muy pocos argemntos! Se esperan: {m}")
                return None
            if len(msg)-notcount > M:
                await ctx.send(f"¡Denasiados argemntos! Se esperan: {M}")
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
            for i,(a,b) in enumerate(zip(listargs, msg)):
                if   a == "i":
                    try     : typedArgs.append(int(b))
                    except  :failedArgs.append(i+1)
                elif a == "s":
                    try     : typedArgs.append(str(b))
                    except  :failedArgs.append(i+1)
                elif a == "f":
                    try     : typedArgs.append(float(b))
                    except  :failedArgs.append(i+1)
                else         :
                    typedArgs.append(b)

            if failedArgs:
                return await ctx.send(f"Los parámetros {failedArgs} no son del tipo correcto.")
            a = list(args)
            a.pop(-1)
            a.append(typedArgs)
            r = await func(*a, **kwargs)
            return 
        return wrapper
    return mn
