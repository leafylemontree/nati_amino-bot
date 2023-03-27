import asyncio
import socket
import logging
import threading
import time
import random
import json
from src import objects
from .listener import listener
from src.communication import protocol

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(name)s - [%(levelname)s]: %(message)s')

class Socket:
    
    def __init__(self):
        self.running    = False
        self.conn       = None
        self.address    = None
        self.messages   = []
        self.host       = None
        self.port       = None
        self.socket     = None
        self.loop       = None
        self.context    = None
        self.instance   = objects.ba.instance

    def config(self, host='localhost', port='31000'):
        self.host = host
        self.port = port
       
    async def run(self, ctx):
        self.loop = asyncio.get_event_loop()
        self.context = ctx
        #self.loop.create_task(self.socketThread())
        await self.socketThread()

    async def socketThread(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            self.socket = s
            try:
                logging.info(f'Connecting to {self.host}:{self.port}')
                self.socket.connect((
                                    self.host,
                                    self.port  ))
                self.socket.setblocking(False)

                logging.info(f'Connected to {self.host}:{self.port}')
                await self.send(
                            dtype=5,
                            destinatary=-1,
                            request={ 'instance': objects.ba.instance }
                        )

                #self.loop.create_task(self.listen(self.socket))
                #self.running = True

                self.loop = asyncio.get_event_loop()
                while True:
                    try:
                        raw = await self.loop.sock_recv(self.socket, 4000)
                        if raw == b'':
                            running = False
                            continue
                        
                        #logging.info(f'{raw}')
                        data = objects.SocketResponse(**json.loads(raw.decode('utf-8')))
                        
                        self.loop.create_task(listener(data))
                        #await self.listen_handler(data)
                        #logging.info(f'response: {data.content}')
                    except Exception as e:
                        logging.error(f'Listener errored! {e}')
                        continue

            except Exception as e:
                logging.error(f'Socket errored! {e}')


    async def send(self, text='test', dtype=0, request=None, destinatary=-1, nodeId=None):
        raw = None
        try:
            if request is None  :       raw = (protocol.SocketInfo(text)).__dict__

            elif dtype == 0       :       raw = (protocol.SocketInfo(**request)).__dict__
            elif dtype == 1       :       raw = (protocol.SocketRequest(**request)).__dict__
            elif dtype == 2       :       raw = (protocol.SocketChat(**request)).__dict__
            elif dtype == 3       :       raw = (protocol.SocketRaw(request)).__dict__
            elif dtype == 4       :       raw = (protocol.SocketJoin(**request)).__dict__
            elif dtype == 5       :       raw = (protocol.SocketConfig(**request)).__dict__

            data = self.signature(dtype=dtype, raw=raw, destinatary=destinatary, nodeId=nodeId)
            await self.loop.sock_sendall(self.socket, data.encode())
        except Exception as e:
            logging.error(f"Sender Errored! {e}")

    def signature(self, dtype=1, raw=None, destinatary=-1, nodeId=None):
        try:
            data = {
                'dtype'     :   dtype,
                'timestamp' :   int(time.time() * 1000),
                'messageId' :   f'92{int(time.time()) ^ int(random.randint(0,0xFFFFFFFF))}',
                'content'   :   json.dumps(raw),
                'address'   :   str(self.address),
                'instance'  :   objects.ba.instance,
                'origin'    :   objects.ba.instance,
                'destinatary':  destinatary,
                'nodeId'    :   nodeId
            }
            print(data)
            j = json.dumps(data)
        except Exception as e:
            logging.error(f"Signature errored! {e}")
            return
        return j

sc = Socket()
