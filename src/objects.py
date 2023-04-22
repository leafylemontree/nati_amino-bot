from __future__     import annotations
from dataclasses    import dataclass
from pydantic       import BaseModel
from typing         import List, Dict, Optional, Any, Tuple
from edamino.objects import Author

import logging
import time
import json
import os

m_error = {
        "error_2400" : "Error 2400: No ha ingresado los parámetros suficientes para el comando 'math'.",
        "error_2401" : "Error 2401: Uno o vario de los parámetros numéricos ingresados no corresponde a un número.",
        "error_2402" : "Error 2402: División por cero.",
        "error_2403" : "Error 2403: Raiz cuadrada de número negativo.",
        "error_2404" : "Error 2404: Variable no inicializada.",
        "error_2500" : "Error 2500: El comando 'blogs' espera un argumento de tipo entero o '-all'.",
        "error_2501" : "Error 2501: El parámetro ingresado no corresponde a las posibles entradas.\n\nIntente con: 1, 2, o -all."
    }

def error(num):
    return f"error_{m_error[str(num)]}"

@dataclass
class Reply:
    msg     :  str  = ""
    reply   :  bool = False

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

        #self.electron = threading.Thread(target=self.runElectron)
        #self.electron.start()

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

class Stats:
    time        = time.time()
    last_record = 0

    reset       = -1
    users       = -1
    messages    = -1

    sus_names   = -1
    spam_msg    = -1
    strange     = -1

    def __init__(self):
        with open("data/botstats.json", "r") as fp:
            a = json.load(fp)
        self.time      = time.time()
        self.reset     = a['reset'] + 1
        self.users     = a['users'] 
        self.messages  = a['messages'] 
        self.sus_names = a['sus_name'] 
        self.spam_msg  = a['spam_msg'] 
        self.strange   = a['strange'] 
        return

    def write(self):
        a = {
	        "users"    : self.users,
	        "reset"    : self.reset,
	        "messages" : self.messages,
	        "sus_name" : self.sus_names,
	        "spam_msg" : self.spam_msg,
	        "strange"  : self.strange
            }
        with open("data/botstats.json", "w+") as fp:
            json.dump(a, fp, indent=4 )
        self.last_record = time.time()
        return

    def register(self, mode):
        if   mode == 0: self.users     += 1
        elif mode == 1: self.reset     += 1
        elif mode == 2: self.messages  += 1
        elif mode == 3: self.sus_names += 1
        elif mode == 4: self.spam_msg  += 1
        elif mode == 5: self.strange   += 1
        return

botStats = Stats()
botStats.write()

class AntiSpam:
    banned_nicks = [
                    "MAMBLL",
                    "WHAT? 0)0)0)",
                    "COIN_PUB",
                    "ᴍᴀᴍʙʟʟ",
                    "ᴀᴍɪɴᴏ ᴄᴏɪɴs",
                    "CULT_OF_KOMARU",
                    "FOXY"
                    ]

    sexual_nicks = [
                    "FOLLAR",
                    "FOSHAR",
                    "COGER",
                    "COJER",
                    "VEN A",
                    "COJAMOS",
                    " RICO",
                    " RIKO"
            ]


    sus_keywords = [
                    "LIMON",
                    "LEMON",
                    "LEMMON",
            ]

    msg_desc = {
                "1"  : "Usuario con nombre baneado anteriormente",
                "2"  : "Contenido sexual en el nick",
                "3"  : "Palabras clave en nick",

                "101": "Spam a Telegram",
                "102": "Spam de comunidad",
                "103": "Spam de comunidad",
                "104": "Spam de Twitter",
                "111": "Mensaje reconocido por cerrar la app",
                "151": "Mensaje de gran longitud que cierra la app",
                "152": "Biografía que cierra la app",

                "200": "Mensaje fuera de lo común"

            }

class Bot_attributes:
    counter = 0
    loop  = False 
    instance = -1

    def kill(self, r):
        import os, sys, signal
        print("EXECUTION CLOSED")
        os.kill(os.getpid(), signal.SIGTERM)
        sys.exit(0)

ba = Bot_attributes()




# Missing objects in Edamino

class WallComment(BaseModel):
    author:                     Optional[Author]
    content:                    Optional[str]
    extensions:                 Any
    parentId:                   Optional[str]
    createdTime:                Optional[str]
    subCommentsCount:           Any
    commentType:                Optional[int]

class LeaderboardUserProfile(BaseModel):
    status:                     Optional[int]
    isNicknameVerified:         Any
    activeTime:                 Optional[int]
    uid:                        Optional[str]
    level:                      Optional[int]
    followingStatus:            Optional[int]
    accountMembershipStatus:    Optional[int]
    isGlobal:                   Any
    membershipStatus:           Optional[int]
    reputation:                 Optional[int]
    role:                       Optional[int]
    ndcId:                      Optional[int]
    membersCount:               Optional[int]
    nickname:                   Optional[str]
    icon:                       Optional[str]

class TipOption(BaseModel):
    value:                      Optional[int]
    icon:                       Optional[str]

class TipInfo(BaseModel):
    tipOptionList:              Optional[Tuple[TipOption, ...]]
    tipMaxCoin:                 Optional[int]
    tippersCount:               Optional[int]
    tippable:                   Any
    tipMinCoin:                 Optional[int]
    tipCustomOption:            Optional[TipOption]
    tippedCoins:                Optional[int]

class refObjectStyle(BaseModel):
    coverMediaIndexList:        Optional[Tuple[int]]

class refObjectExtensions(BaseModel):
    style:                      Optional[refObjectStyle]
    fansOnly:                   Any
    featuredType:               Optional[int]

class RefObject(BaseModel):
    globalVotesCount:           Optional[int]
    globalVotedValue:           Optional[int]
    votedValue:                 Optional[int]
    keywords:                   Optional[str]
    strategyInfo:               Optional[str]
    mediaList:                  Any
    style:                      Optional[int]
    totalQuizPlayCount:         Optional[int]
    title:                      Optional[str]
    tipInfo:                    Optional[TipInfo]
    contentRating:              Optional[int]
    content:                    Optional[str]
    needHidden:                 Any
    guestVotesCount:            Optional[int]
    type:                       Optional[int]
    status:                     Optional[int]
    globalCommentsCount:        Optional[int]
    modifiedTime:               Any
    widgetDisplayInterval:      Any
    totalPollVoteCount:         Optional[int]
    blogId:                     Optional[str]
    viewCount:                  Optional[int]
    author:                     Optional[Author]
    extensions:                 Optional[refObjectExtensions]
    votesCount:                 Optional[int]
    ndcId:                      Optional[int]
    createdTime:                Any
    endTime:                    Any
    commentsCount:              Optional[int]

class Featured(BaseModel):
    refObjectType:              Optional[int]
    refObjectId:                Optional[str]
    expiredTime:                Any
    featuredType:               Optional[int]
    createdTime:                Any
    refObject:                  Optional[RefObject]


class BackgroundColor(BaseModel):
    backgroundColor:            Optional[str]

class Operation(BaseModel):
    operationType:              Optional[int]
    text:                       Optional[str]

class NoticesConfig(BaseModel):
    showCommunity:              Optional[bool]
    showOperator:               Optional[bool]
    allowQuickOperation:        Optional[bool]
    operationList:              Optional[Tuple[Operation, ...]] 

class NoticeAttachedObjectInfo(BaseModel):
    objectType:                 Optional[int]
    objectId:                   Optional[str]
    title:                      Optional[str]
    content:                    Optional[str]
    extensions:                 Optional[int]
    link:                       Optional[str]
    mediaList:                  Optional[Any]

class NoticesExtensions(BaseModel):
    style:                      Optional[BackgroundColor]
    config:                     Optional[NoticesConfig]
    attachedObjectInfo:         Optional[NoticeAttachedObjectInfo]

class Notice(BaseModel):
    notificationId:             Optional[str]
    type:                       Optional[int]
    community:                  Optional[bool]
    title:                      Optional[str]
    ndcId:                      Optional[int]
    content:                    Optional[str]
    createdTime:                Any
    icon:                       Optional[str]
    targetUser:                 Optional[Author]
    modifiedTime:               Any
    status:                     Optional[int]
    operator:                   Optional[Author]
    extensions:                 Optional[NoticesExtensions]
    noticeId:                   Optional[str]
   
@dataclass
class UserInfo:
    userId:                     str
    alias:                      str
    hugs_r:                     int
    hugs_g:                     int
    kiss_r:                     int
    kiss_g:                     int
    pats_r:                     int
    pats_g:                     int
    doxx_r:                     int
    doxx_g:                     int
    kiwi:                       int
    win:                        int
    draw:                       int
    lose:                       int
    points:                     int
    unused4:                    int
    unused5:                    int
    unused6:                    int
    unused7:                    int
    unused8:                    int
    marry:                      str

@dataclass
class LogConfig:
    comId:                      int
    threadId:                   str
    nowarn:                     int
    _ignore:                    int
    ban:                        int
    stalk:                      int
    staff:                      int
    bot:                        int
    instance:                   int
    blogCheck:                  int
    active:                     int
    userWelcome:                int

@dataclass
class ChatConfig:
    threadId:                   str
    comId:                      int
    _check:                     int
    welcome:                    int
    goodbye:                    int
    bot:                        int
    slow:                       int
    staff:                      int
    nofun:                      int
    safe:                       int
   
@dataclass
class WelcomeMessage:
    comId:                      int
    message:                    str
    chat:                       str

@dataclass
class SocketResponse:
    dtype:          int
    timestamp:      int
    messageId:      str
    content:        str
    address:        str
    instance:       int
    origin:         int
    destinatary:    int
    nodeId:         str

logging.basicConfig(level=logging.INFO, fmt=f"%(asctime)s %(levelname)s : ins={ba.instance} - %(message)s")
alreadyChecked = []
