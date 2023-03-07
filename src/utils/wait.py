import asyncio

class CN:

    def __init__(self, chatId, messageId, userId, isStaff=False):
        self.chatId     = chatId
        self.messageId  = messageId
        self.userId     = list(userId) if type(userId) == str else userId
        self.isStaff    = isStaff
        self.register   = None
    
    async def reg(self, ctx, data):
        cn.register = data
        return

    async def yes(self, ctx):
        await self.reg(ctx, True)
        return

    async def no(self, ctx):
        await self.reg(ctx, False)
        return
        
class Confirmator:

    cn = []
    def __init__(self):
        self.cn = []

    async def getCN(self, ctx):
        threadId    = ctx.msg.threadId
        messageId   = ctx.msg.messageId
        
        rcn = self.cn.copy()
        rcn.reverse()
        for cn in rcn:
            if cn.chatId != threadId: continue
            #if cn.messageId != messageId: continue
            return cn
        return None


    async def new(self, ctx, userId="*", isStaff=False):
        threadId    = ctx.msg.threadId
        messageId   = ctx.msg.messageId
        self.cn.append(
                CN(threadId, messageId, userId, isStaff)
                )
        return

    async def remove(self):
        removeList = []
        for i,cn in enumerate(self.cn):
            if cn.register is not None: removeList.append(i)
        
        rl = removeList.reverse()
        for r in rl: self.cn.pop(r)
        return

confirmator = Confirmator()


async def waitConfirmation(ctx, userList='*', isStaff=False):
    await confirmator.new(ctx, userList, isStaff)
    while True:
        cn = await confirmator.getCN(ctx)
        r = cn.register
        print(r)
        if r is not None: break
        await asyncio.sleep(1)
    await confirmator.remove()
    return r


async def confirm(ctx, state):
    cn = await confirmator.getCN(ctx)
    if ctx.msg.author.uid not in cn.userId and cn.userId != ['*']: return
    if cn.isStaff and ctx.msg.author.role < 100: return
    await cn.reg(state)
    return


