

leafId    =  ""
# Change this for your userId
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
            msg = msg.split("\u200c")[0]
            msg = msg.split("\u200e")[0]
        elif ctx.msg.extensions.replyMessage:             uid = ctx.msg.extensions.replyMessage.author.uid
        await func(ctx, uid, msg)
        return
    return check

def ban(func):
    async def check(ctx):
        if ctx.msg.author.role != 102:
            await ctx.send(noMessage)
            return
        elif ctx.msg.author.uid != leafId:
            await ctx.send(noMessage)
            return

        msg = ctx.msg.content
        uid = ctx.msg.author.uid

        reason = msg.split(" ")[1]
        if len(reason) == 1: reason = "Acción hecha a petición"
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
