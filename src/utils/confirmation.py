import uuid
import time
import asyncio

class ConfirmerElement:
    def __init__(self, threadId, userId, ndcId, staff=False, timeout=30):
        self.threadId   = threadId
        self.userId     = [userId] if isinstance(userId, str) else userId
        self.ndcId      = ndcId
        self.staff      = staff
        self.timeout    = timeout
        self.timestamp  = int(time.time())
        self.response   = None

class Confirmer:

    def __init__(self):
        self.data = {}

    def new(self, threadId, userId, ndcId, staff, timeout):
        confirmId = str(uuid.uuid4())
        self.data[confirmId] = ConfirmerElement(
                    threadId=threadId,
                    userId=userId,
                    ndcId=ndcId,
                    staff=staff,
                    timeout=timeout)
        return confirmId

    def search(self, confirmId):
        if confirmId not in self.data.keys(): return None
        element = self.data[confirmId]
        
        if element.timeout is not False:
            if (int(time.time()) - element.timestamp) > element.timeout: return self.remove(confirmId)

        return element.response

    def remove(self, confirmId):
        response = self.data[confirmId].response
        self.data.pop(confirmId, None)
        return response

cf = Confirmer()


async def confirmation(ctx, threadId, userId, ndcId, staff=False, timeout=30):

    confirmId = cf.new(threadId, userId, ndcId, staff, timeout)

    while True:
        response = cf.search(confirmId)
        if response is not None:    return cf.remove(confirmId)
        
        await asyncio.sleep(3)
    return False

async def registerConfirmation(ctx, value):
    threadId = ctx.msg.threadId
    userId   = ctx.msg.author.uid
    ndcId    = ctx.msg.ndcId
    role     = ctx.msg.author.role
    
    for key,element in cf.data.items():
        if threadId != element.threadId:                                continue
        if element.userId is not True:
            if userId not in element.userId:                            continue
        if ndcId != element.ndcId:                                      continue
        if ((role not in [100, 101, 102]) and (element.staff is True)): continue
        element.response = value

