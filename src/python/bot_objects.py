from dataclasses import dataclass
import socket
import threading
import pathlib
import sys
import subprocess
import json


@dataclass
class Reply():
    msg:    str  = ""
    reply:  bool = False

@dataclass
class Database_return:
    alias   : str   = ""
    hugs_r  : int   = 0
    hugs_g  : int   = 0
    kiss_r  : int   = 0
    kiss_g  : int   = 0
    pats_r  : int   = 0
    pats_g  : int   = 0

    def strToVal(self, msg):
        msg = msg.split("__$")
        self.alias   = msg[0]
        self.hugs_r  = int(msg[1])
        self.hugs_g  = int(msg[2])
        self.kiss_r  = int(msg[3])
        self.kiss_g  = int(msg[4])
        self.pats_r  = int(msg[5])
        self.pats_g  = int(msg[6])
        return

@dataclass
class Status:
    wordle      : int = 0
    quiz        : int = 0

    @dataclass
    class Wordle:
        word        : str   = "ARBOL"
        step_cnt    : int   = 6
        diff        : int   = 5
        instance            = []

        @dataclass
        class User():
            uid         : str
            step        : int   = 0
            data        : int   = 0

        def new_instance(self, _uid_):
            self.instance.append(Status.Wordle.User(_uid_))
            self.instance[-1].data = []
            return

        def get_users(self):
            user_list = []
            for i in self.instance:
                user_list.append(i.uid)
            return user_list

        def set_difficulty(self, number):
            self.diff = number
            return

        def change_word(self, word):
            self.word = word
            return

        def set_steps(self, number):
            self.step_cnt = number
            return

    @dataclass
    class Quiz:
        type : int = 0


    def __init__(self):
        self.wordle = Status.Wordle()
        self.wordle.instance = []
        return

@dataclass
class Server:
    host    : str = 'localhost'
    port    : int = 32509
    client  = {}
    address = {}
    server  = {}
    message = {
                "content"  : "",
                "nickname" : "",
                "chatid"   : ""
    }

    def __init__(self):
        self.server = socket.socket()
        print('Socket created!')
        self.server.bind((self.host, self.port))
        self.server.listen()
        print('Waiting for connection')

        handler_thread = threading.Thread(target=self.handler)
        handler_thread.start()

        electron = threading.Thread(target=self.runElectron)
        electron.start()

        return

    def handler(self):

        print("Server is listening...")
        while True:
            try:
                self.client, self.address = self.server.accept()
                print(f"New client: {self.address}")

                listen_handler = threading.Thread(target=self.listen)
                listen_handler.start()
            except KeyboardInterrupt:
                try:
                    print("You stopped me!")
                    self.client.close()
                except Exception:
                    print("No logged client. Closing")
                break

    def listen(self):
        while True:
                msg = self.client.recv(512).decode('ascii')
                print(f"recv: {msg}")

    def runElectron(self):
        path = pathlib.Path(__file__).parent.resolve()
        path = str(path)[:len(str(path))-10]
        sys.path.insert(0, path)
        with subprocess.Popen("npm start", stdout=subprocess.PIPE, bufsize=1, universal_newlines=True, shell=True) as p:
            print("Running Electron")

    def send(self, ctx):
        self.message['content']  = ctx.msg.content
        self.message['nickname'] = ctx.msg.author.nickname
        self.message['chatid']   = ctx.msg.threadId
        msg = json.dumps(self.message)
        self.client.send( bytes(msg, encoding='utf-8') )
        return
