from src import objects
from src.communication import protocol
import logging
import uuid
import json
import asyncio
import time

from src.subprocess.test import get_my_communities
from src.admin.community import join_community, leave_community


logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')


class SocketNode:
    nodeId  = None
    data    = []
    done    = False
    length  = 1
    created = None

    def __init__(self, nodeId, data, length=1, timeout=False):
        self.nodeId = nodeId
        self.data   = []
        if data     : self.data.append(data)
        self.done   = False
        self.length = length
        self.timeout= timeout
        self.created= int(time.time())

    def new(self, data):
        self.data.append(data)
        if self.length <= len(self.data):   self.end()

    def end(self):
        self.done = True

class SocketPool:

    def __init__(self):
        self.nodes = []
        return

    def register(self, data=None, length=1, timeout=False):
        nodeId = None

        # existing uuid
        if data:
            nodeId = data.nodeId
            resp = self.get_by_id(data.nodeId)
            if resp is not None:
                index,node = resp
                node.new(data)
                return nodeId

        # generate uuid
        else: nodeId = str(uuid.uuid4())

        self.nodes.append(SocketNode(nodeId, data, length, timeout))
        return nodeId
    
    def get_by_id(self, nodeId):
        if nodeId is None: return None
        for i,node in enumerate(self.nodes):
            if node.nodeId != nodeId: continue
            if node.length <= len(node.data): node.end()
            return (i,node)
        return None

    async def retrieve(self, nodeId, delete=False):
        node  = None 
        index = None
    
        while True:
            try:
                await asyncio.sleep(2)
                response = self.get_by_id(nodeId)
                if response is None:    continue
                index,node  = response
                
                # Node exists
                timestamp = int(time.time())
                if node.timeout is not False:
                    if (timestamp - node.created) > node.timeout: return node

                if node.done is False:  continue
                return node

            except Exception as e:
                logging.error(f'Retrieve task {nodeId} - {e}')
        return None

    def remove(self, nodeId):
        resp = self.get_by_id(nodeId)
        self.nodes.pop(index)
        return

socketPool = SocketPool()


async def socketInfo(data):
    from .client import sc
    content = protocol.SocketInfo(**json.loads(data.content)) 
    logging.info(f'{content}')
    return


async def socketRequest(data):
    from .client import sc
    content = protocol.SocketRequest(**json.loads(data.content)) 
    
    if content.objectId == 0:
        from .client import sc
        communities = await get_my_communities(sc.context, start=0, size=100) 
        comList     = list(map(lambda com: com.ndcId, communities))
        await sc.send(
                dtype = 3,
                destinatary=-1,
                request = { 'comList' : comList },
                nodeId=data.nodeId
        )

    elif content.objectId == 1:
        from .client import sc
        wallet      = await sc.context.client.get_wallet_info()
        await sc.send(
                dtype = 3,
                destinatary = -1,
                request = { 'coins' : wallet.totalCoins },
                nodeId=data.nodeId
            )
    
    elif content.objectId == 2:
        from .client import sc
        await sc.send(
                dtype = 3,
                destinatary = -1,
                request = { 'status' : 'active' },
                nodeId=data.nodeId
            )

    return


async def socketChat(data):
    from .client import sc
    content = protocol.SocketChat(**json.loads(data.content)) 
    sc.context.client.set_ndc(content.ndcId)
    message = await sc.context.client.send_message(
               message=content.message,
               chat_id=content.threadId
            )

    if message: await sc.send(
                dtype=0,
                destinatary=-1,
                request = { 'message' : 'Message sent' },
                nodeId=data.nodeId
            )
    return


async def socketRaw(data):
    from .client import sc
    data.content = protocol.SocketRaw(**json.loads(data.content))
    socketPool.register(data=data)


async def socketJoin(data):
    from .client import sc
    content = protocol.SocketJoin(**json.loads(data.content)) 
    try:
        if community.leave == 1:    await leave_community(
                                            sc.context,
                                            ndcId
                                            )
        else:                       await join_community(
                                            sc.context,
                                            content.ndcId,
                                            content.invitationId
                                            )
    except Exception as e:
        await sc.send(
                    dtype=3,
                    destinatary=-1,
                    request = {
                        'message': 'Errored',
                        'instance': objects.ba.instance,
                        'error': str(e)
                        },
                    nodeId=data.nodeId)

async def listener(data):

    if   data.dtype == 0: await socketInfo(data)
    elif data.dtype == 1: await socketRequest(data)
    elif data.dtype == 2: await socketChat(data)
    elif data.dtype == 3: await socketRaw(data)
    elif data.dtype == 4: await socketJoin(data)
    
    return
