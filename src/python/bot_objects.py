from dataclasses import dataclass
import socket
import threading
import pathlib
import sys
import subprocess
import json
from c_func import c
from random import random


@dataclass
class Reply:
    msg     :  str  = ""
    reply   :  bool = False

@dataclass
class Database_return:
    alias   : str   = ""
    hugs_r  : int   = 0
    hugs_g  : int   = 0
    kiss_r  : int   = 0
    kiss_g  : int   = 0
    pats_r  : int   = 0
    pats_g  : int   = 0
    doxx_r  : int   = 0
    doxx_g  : int   = 0
    kiwi    : int   = 0
    win     : int   = 0
    derr    : int   = 0
    draw    : int   = 0
    points  : int   = 0


    def strToVal(self, msg):
        msg = msg.split("__$")
        self.alias   = msg[0]
        self.hugs_r  = int(msg[1])
        self.hugs_g  = int(msg[2])
        self.kiss_r  = int(msg[3])
        self.kiss_g  = int(msg[4])
        self.pats_r  = int(msg[5])
        self.pats_g  = int(msg[6])
        self.doxx_r  = int(msg[7])
        self.doxx_g  = int(msg[8])
        self.kiwi    = int(msg[9])
        self.derr    = int(msg[10])
        self.win     = int(msg[11])
        self.draw    = int(msg[12])
        self.points  = int(msg[13])
        return

@dataclass
class ThreadProperties:
    disabled = []



@dataclass
class Status:
    wordle      = None
    quiz        = None
    challenge   = None

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
            data                = []

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

    @dataclass
    class Challenge:
        instances = []
        active    = 0

        @dataclass
        class Challenge_instance:
            uid1    :   str
            uid2    :   str
            game    :   int
            turn            = 0
            data            = []

        def new_instance(self, uid1, uid2, game):
            self.instances.append(self.Challenge_instance(uid1, uid2, game))

            if   game == 1        :
                print(f"Juego {game}: ahorcado, {uid1} {uid2}")
                self.instances[-1].data = [ self.set_word(), [] ]

            elif game == 2        :   print(f"Juego {game}: ahorcado, {uid1} {uid2}")
            elif game == 3        :   print(f"Juego {game}: ahorcado, {uid1} {uid2}")
            elif game == 4        :   print(f"Juego {game}: ahorcado, {uid1} {uid2}")

            return

        def check_user(self, uid):
            for i in self.instances:
                if ((i.uid1 == uid) | (i.uid2 == uid)): return True
            return False

        def remove_instance(self, uid):
            if self.check_user(uid):
                i = self.get_instance_number(uid)
                self.instances.pop(i)
                return Reply(f"Ambos usuarios removidos del reto.", False)
            else:
                return Reply("Usted no está retando o siendo retado.", False)

        def get_instance_number(self, uid):
            i = 0
            for i, j in enumerate(self.instances):
                if ((j.uid1 == uid) | (j.uid2 == uid)) : return i
            return -1

        def get_instance_data(self, i):
            if len(self.instances) < i: return -1
            return [self.instances[i].uid1, self.instances[i].uid2, self.instances[i].game, self.instances[i].turn, self.instances[i].data]

        def set_word(self):
            i = int( random() * 12) + 4
            word = c.get_word(i)
            print(self.instances[-1])
            return word

        def flip(self, i):
            self.instances[i].turn += 1
            return

    def __init__(self):
        self.wordle     = self.Wordle()
        self.challenge  = self.Challenge()
        self.wordle.instance = []
        return

@dataclass
class Server:
    host    : str  = 'localhost'
    port    : int  = 32509
    client         = {}
    address        = {}
    server         = {}
    handler_thread = {}
    listen_thread  = {}
    electron       = {}
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

        self.handler_thread = threading.Thread(target=self.handler)
        self.handler_thread.start()

        self.electron = threading.Thread(target=self.runElectron)
        self.electron.start()

        return

    def handler(self):

        print("Server is listening...")
        while True:
            try:
                self.client, self.address = self.server.accept()
                print(f"New client: {self.address}")

                self.listen_handler = threading.Thread(target=self.listen)
                self.listen_handler.start()
            except KeyboardInterrupt:
                #try:
                print("You stopped me!")
                self.client.close()
                #except Exception:
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
