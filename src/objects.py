from __future__     import annotations
from dataclasses    import dataclass
from pydantic       import BaseModel
from typing         import List, Dict, Optional, Any, Tuple
from edamino.objects import Author, UserProfile

import logging
import time
import ujson as json
import os
import datetime
import random
import uuid

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

class Reply:
    def __init__(self, msg, reply=True):
        self.msg    = msg
        self.reply  = reply

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

        def check_user(self, userId):
            users = self.get_users()
            return userId in users

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

status = Status()

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
        self.time      = time.time()
        self.reset     = 0
        self.users     = 0
        self.messages  = 0
        self.sus_names = 0
        self.spam_msg  = 0
        self.strange   = 0 
        return

    def write(self):
        return

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

class MessageEvents:
    FORBIDDEN       =  -1
    MEMBER_JOIN     =   1
    MEMBER_LEAVE    =   2
    NO_FUN          =   100

class AntiSpam:
    banned_nicks = [
                    "MAMBLL",
                    "WHAT? 0)0)0)",
                    "COIN_PUB",
                    "ᴍᴀᴍʙʟʟ",
                    "ᴀᴍɪɴᴏ ᴄᴏɪɴs",
                    "CULT_OF_KOMARU",
                    "LUNAR",
                    "BOT",
                    "LUNARINFERNAL",
                    "LUNARBOT",
                    "TOXINA",
                    "𝕋ᴏ֟֯xɪɴᴀ!"
                    "FOXY",
                    "HEPHA",
                    "SAY_",
                    "KAI"
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
                "4"  : "Nombre del usuario contiene caracteres no ASCII. Posible spam",

                "101": "Spam de Telegram",
                "102": "Spam de comunidad",
                "103": "Spam de comunidad",
                "104": "Spam de Twitter",
                "105": "Spam de Discord",
                "106": 'Spam de "La app esa"',
                "107": "Spam de Whatsapp",
                "108": "Spam de link global",
                "109": "Link no identificado",

                "111": "Mensaje reconocido por cerrar la app",
                "151": "Mensaje de gran longitud que cierra la app",
                "152": "Biografía que cierra la app",

                "200": "Mensaje fuera de lo común",

                "300": "Usuario sin imagen. Cuenta creada de forma ilegal"
            }

class Bot_attributes:
    counter     = 0
    loop        = False 
    instance    = -1
    timestamp   = time.time()

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
    extensions:                 Optional[Any]
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
   
class AdminLogList(BaseModel):
    author:                     Author
    createdTime:                Optional[Any]
    objectType:                 Optional[int]
    operationName:              Optional[str]
    comId:                      Optional[int]
    referTicketId:              Optional[str]
    extData:                    Optional[Any]
    operationDetail:            Optional[Any]
    operationLevel:             Optional[Any]
    moderationLevel:            Optional[str]
    operation:                  Optional[Any]
    objectId:                   Optional[str]
    logId:                      Optional[str]
    objectUrl:                  Optional[str]
    content:                    Optional[str]
    value:                      Optional[Any]

class CommentList(BaseModel):
    author:                     Author
    votesSum:                   Optional[int]     
    votedValue:                 Optional[Any]     
    mediaList:                  Optional[Any]     
    parentComId:                Optional[int]     
    parentId:                   Optional[str]     
    parentType:                 Optional[Any]     
    content:                    Optional[str]  
    extensions:                 Optional[Any]     
    comId:                      Optional[int]     
    modifiedTime:               Optional[Any]     
    createdTime:                Optional[Any]     
    commentId:                  Optional[str]     
    subcommentsCount:           Optional[int]     
    type:                       Optional[Any]     

class VotedValueMapV2(BaseModel):
    createdTime:                Optional[Any]
    uid:                        Optional[str]
    value:                      Optional[int]

@dataclass
class PostLikes:
    votedValueMap:              Optional[Tuple[str]]
    votedValueMapV2:            Optional[Tuple[VotedValueMapV2]]
    UserProfile:                Optional[Tuple[UserProfile]]
    votedCount:                 Optional[int]

    def __init__(self, response):
        self.votedValueMap      = tuple(response['votedValueMap'].keys())
        self.votedValueMapV2    = tuple(map(lambda voteMap: VotedValueMapV2(**voteMap[1]), response['votedValueMapV2'].items())) 
        self.UserProfile        = tuple(map(lambda userProfile: UserProfile(**userProfile), response['userProfileList'])) 
        self.votedCount         = len(self.votedValueMap)


class OriginalCommunity(BaseModel):
    status:                     Optional[int]
    icon:                       Optional[str]
    endpoint:                   Optional[str]
    name:                       Optional[str]
    ndcId:                      Optional[int]

class StickerExtensions(BaseModel):
    iconSourceStickerId:        Optional[str]
    originalAuthor:             Optional[Author]
    originalCommunity:          Optional[OriginalCommunity]

class StickerRestriction(BaseModel):
    discountStatus:             Optional[int]
    ownedUid:                   Optional[Any]
    ownerType:                  Optional[int]
    restrictType:               Optional[int]
    restrictValue:              Optional[int]
    availableDuration:          Optional[Any]
    discountValue:              Optional[Any]

class StickerCollection(BaseModel):
    status:                     Optional[int]
    isActivated:                Optional[bool]
    collectionType:             Optional[int]
    uid:                        Optional[str]
    modifiedTime:               Optional[Any]
    isNew:                      Optional[bool]
    bannerUrl:                  Optional[Any]
    smallIcon:                  Optional[str]
    stickersCount:              Optional[int]
    ownershipStatus:            Optional[Any]
    usedCount:                  Optional[int]
    availableNdcIds:            Optional[List[int]]
    icon:                       Optional[str]
    name:                       Optional[str]
    collectionId:               Optional[str]
    description:                Optional[str]
    author:                     Optional[Author]
    extensions:                 Optional[StickerExtensions]
    createdTime:                Optional[Any]
    isGloballyAvailable:        Optional[bool]
    restrictionInfo:            Optional[StickerRestriction]

class ExtData(BaseModel):
    subtitle:                   Optional[str]
    objectDeeplinkUrl:          Optional[str]
    description:                Optional[str]
    icon:                       Optional[str]

class CoinHistory(BaseModel):
    uid:                        Optional[str]
    extData:                    Optional[ExtData]
    originCoins:                Optional[int]
    bonusCoins:                 Optional[int]
    totalCoins:                 Optional[int]
    taxCoinsFloat:              Optional[float]
    bonusCoinsFloat:            Optional[float]
    totalCoinsFloat:            Optional[float]
    isPositive:                 Optional[bool]
    changedCoins:               Optional[int]
    sourceType:                 Optional[int]
    createdTime:                Optional[Any]
    originalCoinsFloat:         Optional[float]
    taxCoins:                   Optional[int]
    changedCoinsFloat:          Optional[float]

class Notification(BaseModel):
    parentText:                 Optional[str]
    objectId:                   Optional[str]
    contextText:                Optional[str]
    type:                       Optional[int]
    parentId:                   Optional[str]
    operator:                   Optional[Author]
    createdTime:                Optional[Any]
    parentType:                 Optional[int]
    objectSubType:              Optional[int]
    ndcId:                      Optional[int]
    notificationId:             Optional[str]
    objectText:                 Optional[str]
    contextValue:               Optional[int]
    contextNdcId:               Optional[int]
    objectType:                 Optional[int]

@dataclass
class NotificationList:
    notifications:              Tuple[Notification]
    nextPageToken:              Optional[str]

    def __init__(self, response):
        self.notifications = tuple(map(lambda notif: Notification(**notif), response["notificationList"]))
        self.nextPageToken = response["paging"]["nextPageToken"]
        return

class AdminUserProfile(UserProfile):
    adminLogCountIn7Days:       Optional[int]
    avgDailySpendTimeIn7Days:   Optional[int]


class USER_FLAGS:
    botDisable          =   0b00000001
    yincanaDisable      =   0b00000010
    expDisable          =   0b00000100
    petDisable          =   0b00001000
    interactionDisable  =   0b00010000
    staffCommandsEnable =   0b00100000
    moderationEnable    =   0b01000000
    godMode             =   0b10000000


class UserFlags:
    botDisable:                 bool
    yincanaDisable:             bool
    expDisable:                 bool
    petDisable:                 bool
    interactionDisable:         bool
    staffCommandsEnable:        bool
    moderationEnable:           bool
    godMode:                    bool

    def __init__(self, bitarray):
        self.botDisable             = bool(bitarray & 0b00000001)
        self.yincanaDisable         = bool(bitarray & 0b00000010)
        self.expDisable             = bool(bitarray & 0b00000100)
        self.petDisable             = bool(bitarray & 0b00001000)
        self.interactionDisable     = bool(bitarray & 0b00010000)
        self.staffCommandsEnable    = bool(bitarray & 0b00100000)
        self.moderationEnable       = bool(bitarray & 0b01000000)
        self.godMode                = bool(bitarray & 0b10000000)
        return

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
    LApoints:                   int
    ACBuffer:                   int
    userFlags:                  UserFlags
    unused7:                    int
    unused8:                    int
    marry:                      str

    def parse_flags(self):
        flags = UserFlags(self.userFlags)
        return flags


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
    calls:                      int
    biography:                  int

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
class Report:
    userId:                     str
    ndcId:                      str
    threadId:                   str
    timestamp:                  datetime.datetime
    registeredNick:             bool
    sexualNick:                 bool
    susNick:                    bool
    telegram:                   bool
    aminoCommunity:             bool
    aminoInvite:                bool
    twitter:                    bool
    crash:                      bool
    length:                     bool
    highLength:                 bool
    messageType:                bool
    discord:                    bool
    projz:                      bool
    whatsapp:                   bool
    globalLink:                 bool
    nonASCII:                   bool
    unidentifiedLink:           bool
    imageIsNone:                bool

@dataclass
class Note:
    userId:                     str
    noteId:                     str
    timestamp:                  datetime.datetime
    content:                    str

@dataclass
class SocketResponse:
    dtype:          int
    timestamp:      int
    messageId:      str
    content:        str
    checksum:       int
    address:        str
    instance:       int
    origin:         int
    destinatary:    int
    nodeId:         str

@dataclass
class InventoryElement:
    objectId:       int
    amount:         int
    metadata:       Any

    def export(self):
        return {
            "objectId": self.objectId,
            "amount":   self.amount,
            "metadata": self.metadata
        }


class UserInventory:
    userId:         str
    length:         int
    data:           Any

    def __init__(self, userId=None, length=None, data=None):
        self.userId     = userId
        self.length     = len(data)
        self.data       = [InventoryElement(**element) for element in data]

    @classmethod
    def Blank(Self, userId):
        return Self(userId, 0, [])
    
    def add(self, objectId, amount, data=None):
        if len(self.data) >= 32: return True
        remove = None
        found  = False

        for i,element in enumerate(self.data):
            if element.objectId != objectId: continue
            element.amount += amount
            if data: element.metadata = data
            if element.amount <= 0: remove = i
            found = True
       
        if remove is not None   :   self.data.pop(remove); return
        if found                :    return

        self.data.append(
                    InventoryElement(objectId, amount, data)
                )
        return

    def remove(self, objectId):
        index = None
        for i,element in enumerate(self.data):
            if element.objectId == objectId: index = i

        if index is not None: self.data.pop(i)
        return None if index is None else True

    def clear(self):
        self.data   = []
        self.length = 0

    def export(self):
        data_dict = {
                "userId":   self.userId,
                "length":   len(self.data),
                "data"  :   [element.export() for element in self.data]
            }
        return data_dict
    def exists(self, objectId):
        amount = 0
        for item in self.data:
            if item.objectId != objectId: continue
            amount = item.amount
        return amount

@dataclass
class InvAPrs: #Inventory API Preset
    name        : str
    limit       : int
    stackable   : bool
    value       : int
    weight      : float
    rarity      : int
    description : str

    # effects
    itemtype    : int # 0: food, 1: single use object, 2: key-object

    health      : int
    happiness   : int
    energy      : int
    care        : int
    hunger      : int
    thirst      : int
    effects     : int

    usable      : bool

    # Effects
    #0  : None
    #1  : Boozed
    #2  : Sleepy
    #3  : Tired

    #-1 : clear
    #-2 : leftovers

class InventoryAPI:
    data = {
    #   id          name                  limit stack val. wei.rarity  description                                                            type  health happin. energy   care    hunger  thirst  effect
        0  : InvAPrs("Botella de agua",     -1, True, 300,  50, 0, "Quita la sed.",                                                             0,  750,    0,      0,      0,      0,      2000,   0,      True),
        1  : InvAPrs("Botella de cerveza",  -1, True, 1200, 10, 1, "Quita la sed, pero, ¿a qué costo?",                                         0,  -1000,  750,    -1000,  500,    -500,   1250,   1,      True),
        2  : InvAPrs("Botella de leche",    -1, True, 500,  20, 1, "Quita todos los efectos de estado.",                                        0,  250,    250,    250,    0,      250,    1500,   -1,     True),
        3  : InvAPrs("Pastelito",           -1, True, 800,  15, 0, "Mucha azúcar hace a Nati doler la pancita.",                                0,  -500,   750,    1000,   750,    1000,   -250,   3,      True),
        4  : InvAPrs("Hamburguesa",         -1, True, 800,  15, 1, "Quita el hambre. Puede hacer a Nati perezosa.",                             0,  -1250,  1000,   1500,   125,    1250,   -750,   3,      True),
        5  : InvAPrs("Manzana",             -1, True, 300,  20, 0, "Quita el hambre y da energía a Nati.",                                      0,  500,    250,    750,    0,      1000,   200,    0,      True),
        6  : InvAPrs("Trozo de pizza",      -1, True, 1000, 10, 1, "Quita el hambre. Hace a Nati perezosa.",                                    0,  -1000,  750,    -1500,  400,    1000,   -1000,  3,      True),
        7  : InvAPrs("Sobras",              -1, True, 100,  7.5,1, "¿Quién sabe lo que hay aquí? Es un misterio",                               0,  0,      0,      0,      0,      0,      0,      -2,     True),
        8  : InvAPrs("Sopa de gato",        -1, True, 1500, 5,  2, "Ñom ñom ñom, delicious!",                                                   0,  500,    -500,   0,      -500,   1500,   750,    0,      True),
        9  : InvAPrs("Ensalada",            -1, True, 600,  5,  2, "Quita el hambre y da mucha energía a Nati.",                                0,  1000,   -300,   2500,   0,      750,    250,    0,      True),
        10 : InvAPrs("Peine",                1, False,2000, 5,  1, "¡La melena alineada como nunca!",                                           1,  0,      500,    0,      250,    0,      0,      0,      True),
        11 : InvAPrs("Espejo",               1, False,2500, 5,  1, "Cuidado, si eres muy feo se rompe.",                                        1,  0,      -750,   0,      250,    0,      0,      0,      True),
        12 : InvAPrs("Correa",               1, False,2500, 5,  2, "Saca a pasear a tu Nati, solo no la acerques a los perros.",                1,  -500,   500,    0,      750,    0,      0,      0,      True),
        13 : InvAPrs("Silla",               -1, True, 2000, 15, 3, "Corrije a tu Nati antes que sea tarde.",                                    1,  -1250,  -1000,  1000,   -500,   0,      0,      0,      True),
        14 : InvAPrs("Frasco de vidrio",    -1, True, 2500, 13, 2, "Química o alquimia, sea lo que sea, dale uno de estos y saldrán cosas.",    1,  0,      750,    0,      0,      0,      0,      0,      True),
        15 : InvAPrs("Reloj mecánico",      -1, True, 4000, 3.8,2, "Nati se calma al oir su tic tac.",                                          1,  500,    750,    -750,   750,    0,      0,      -1,     False),
        16 : InvAPrs("Mantita",             -1, True, 2200, 7.5,1, "El frío está fuerte. Cubre a tu Nati con ella.",                            1,  100,    250,    -1500,  500,    0,      0,      2,      True),
        17 : InvAPrs("Tenedor",              1, False,700,  5,  2, "No acercar a los enchufes.",                                                1,  0,      0,      0,      0,      0,      0,      0,      True),
        18 : InvAPrs("Plato",               -1, True, 1000, 5,  2, "¿A que no te apetece arrojarlo como frisbee?",                              1,  0,      0,      0,      0,      0,      0,      0,      True),
        19 : InvAPrs("Corneta",             -1, True, 1500, 2,  3, "Nati ruidosa ha ingresado al chat.",                                        1,  0,      250,    0,      0,      0,      0,      0,      True),
        20 : InvAPrs("Cuchillo",             1, False,700,  5,  2, "NO acercar a Nati o se enoja.",                                             1,  -1500,  1750,   0,      0,      0,      0,      0,      True),
        21 : InvAPrs("Bate",                 1, False,3000, 3,  2, "Las reglas están hechas para romperse.",                                    2,  0,      750,    750,    0,      0,      0,      0,      True),
        22 : InvAPrs("Martillo",             1, False,3500, 3,  3, "A este punto, ¿la corriges o la mandas al lobby?",                          2,  0,      0,      0,      0,      0,      0,      0,      True),
        23 : InvAPrs("Serrucho",             1, False,4500, 3,  3, "Dale a Nati una sierra y te hará una choza... con una persona dentro.",     2,  -1250,  2000,   0,      0,      0,      0,      0,      True),
        24 : InvAPrs("Atornillador",         1, False,2500, 3,  3, "Nati puede reparar cosas con esto.",                                        2,  -750,   1250,   0,      0,      0,      0,      0,      True),
        25 : InvAPrs("Llave Inglesa",        1, False,3500, 3,  3, "Nati puede reparar cosas con esto.",                                        2,  -1000,  1500,   0,      0,      0,      0,      0,      True),
        26 : InvAPrs("Tu vieja",            -1, True, 10000,0.5,4, "El objeto más masivo del universo.",                                        0,  999999, 10000,  10000,  10000,  10000,  10000,  -1,     True),
        27 : InvAPrs("Ticket de destacado", -1, True,   0,  0,  0, "Canjea este item por una publicación destacada con el staff.",              0, -999999, -9999,  -9999,  -9999,  -9999,  -9999,  -1,     False),
        28 : InvAPrs("Ticket de chat"     , -1, True,   0,  0,  0, "Canjea este item por un chat destacado con el staff.",                      0, -999999, -9999,  -9999,  -9999,  -9999,  -9999,  -1,     False),
        29 : InvAPrs("Ticket de notificación",-1, True, 0,  0,  0, "Canjea este item por una notifiación con el staff.",                        0, -999999, -9999,  -9999,  -9999,  -9999,  -9999,  -1,     False),
        30 : InvAPrs("Ticket de título", -1,    True,   0,  0,  0, "Canjea este item por un título personalizado con el staff.",                0, -999999, -9999,  -9999,  -9999,  -9999,  -9999,  -1,     False),
        31 : InvAPrs("Caja normal",         -1, True,   0,  0,  1, "Algo desconocido aguarda dentro de esta caja.",                             0, -999999, -9999,  -9999,  -9999,  -9999,  -9999, 301,     False),
        32 : InvAPrs("Caja rara",           -1, True,   0,  0,  2, "Un gran misterio oculta la madera, puede ser valioso.",                     0, -999999, -9999,  -9999,  -9999,  -9999,  -9999, 302,     False),
        33 : InvAPrs("Caja mágica",         -1, True,   0,  0,  3, "Riqueza inimaginable aguarda dentro del metal.",                            0, -999999, -9999,  -9999,  -9999,  -9999,  -9999, 303,     False),
    }

    def __init__(self):
        self.totalWeight    = self.getWeight()
        self.commonWeight   = self.getTypedWeight(0)
        self.casualWeight   = self.getTypedWeight(1)
        self.rareWeight     = self.getTypedWeight(2)
        self.strangeWeight  = self.getTypedWeight(3)
        self.legendaryWeight= self.getTypedWeight(4)
        return

    def getWeight(self):
        accumulator = 0
        for _,element in self.data.items():   accumulator += element.weight
        return accumulator

    def name(self, objectId):
        try             :    return self.data[objectId].name
        except Exception:    return "Error"

    def properties(self, objectId):
        try             :    return self.data[objectId]
        except Exception:    return "Error"

    def getRandomItem(self):
        r = random.random() * self.totalWeight
        accumulator = 0
        for key,element in self.data.items():
            accumulator += element.weight
            if r < accumulator: return key
        
        return None

    def getTypedWeight(self, rarity):
        weight = 0
        for key,element in self.data.items():
            if element.rarity != rarity: continue
            if element.weight == 0     : continue
            weight += element.weight
        return weight

    def getItemByRarity(self, rarity):
        r = random.random()
        if   rarity == 0: r = r * self.commonWeight
        elif rarity == 1: r = r * self.casualWeight
        elif rarity == 2: r = r * self.rareWeight
        elif rarity == 3: r = r * self.strangeWeight
        elif rarity == 4: r = r * self.legendaryWeight
        accumulator = 0

        for key,element in self.data.items():
            if element.rarity != rarity: continue
            if element.weight == 0     : continue
            print(element.name, element.rarity, r, accumulator)
            accumulator += element.weight
            if r < accumulator: return key
        return None


inventoryAPI = InventoryAPI()


@dataclass
class Yincana:
    userId:             str
    ndcId:              int
    level:              int
    timestamp:          datetime.datetime
    isBlank:            bool

    @classmethod
    def from_db(Self, userId, ndcId, level, timestamp):
        self = Self(userId, ndcId, level, timestamp, False)
        return self

    @classmethod
    def blank(Self, userId, ndcId):
        self = Self(userId, ndcId, 0, datetime.datetime.now(), True)
        return self


logging.basicConfig(level=logging.INFO, fmt=f"%(asctime)s %(levelname)s : ins={ba.instance} - %(message)s")
alreadyChecked = []


class AdHeaders:
    def __init__(self, userId):
        self.data = {
            "reward": {
                "ad_unit_id": "t00_tapjoy_android_master_checkinwallet_rewardedvideo_322",
                "credentials_type": "publisher",
                "custom_json": {
                    "hashed_user_id": userId
                },
                "demand_type": "sdk_bidding",
                "event_id": str(uuid.uuid4()),
                "network": "tapjoy",
                "placement_tag": "default",
                "reward_name": "Amino Coin",
                "reward_valid": True,
                "reward_value": 2,
                "shared_id": "4d7cc3d9-8c8a-4036-965c-60c091e90e7b",
                "version_id": "1569147951493",
                "waterfall_id": "4d7cc3d9-8c8a-4036-965c-60c091e90e7b"
            },
            "app": {
                "bundle_id": "com.narvii.amino.master",
                "current_orientation": "portrait",
                "release_version": "3.4.33585",
                "user_agent": "Dalvik\/2.1.0 (Linux; U; Android 10; G8231 Build\/41.2.A.0.219; com.narvii.amino.master\/3.4.33567)"
            },
            "device_user": {
                "country": "US",
                "device": {
                    "architecture": "aarch64",
                    "carrier": {
                        "country_code": 255,
                        "name": "Vodafone",
                        "network_code": 0
                    },
                    "is_phone": True,
                    "model": "GT-S5360",
                    "model_type": "Samsung",
                    "operating_system": "android",
                    "operating_system_version": "29",
                    "screen_size": {
                        "height": 2300,
                        "resolution": 2.625,
                        "width": 1080
                    }
                },
                "do_not_track": False,
                "idfa": "0c26b7c3-4801-4815-a155-50e0e6c27eeb",
                "ip_address": "",
                "locale": "ru",
                "timezone": {
                    "location": "Asia\/Seoul",
                    "offset": "GMT+02:00"
                },
                "volume_enabled": True
            },
            "session_id": "7fe1956a-6184-4b59-8682-04ff31e24bc0",
            "date_created": 1633283996
        }
        self.headers = {
            "cookies": "__cfduid=d0c98f07df2594b5f4aad802942cae1f01619569096",
            "authorization": "Basic NWJiNTM0OWUxYzlkNDQwMDA2NzUwNjgwOmM0ZDJmYmIxLTVlYjItNDM5MC05MDk3LTkxZjlmMjQ5NDI4OA==",
            "X-Tapdaq-SDK-Version": "android-sdk_7.1.1",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 9 Pro Build/QQ3A.200805.001; com.narvii.amino.master/3.4.33585)"
        }


@dataclass
class NatiPet:
    ndcId:              int
    createdTime:        datetime.datetime
    lastInteraction:    datatime.datetime
    exp:                int
    level:              int

    health:             int
    maxHealth:          int
    happiness:          int
    energy:             int
    care:               int
    hunger:             int
    thirst:             int

    effects:            int


@dataclass
class Rewards:
    userId:             str
    ndcId:              int
    type:               int
    itemId:             int
    amount:             int
    rewardId:           str

@dataclass
class UserEXP:
    ndcId:              int
    userId:             str
    exp:                int

AVAILABLE_TOPICS = [
        "news",
        "amino",
        "nati",
        "resumen",
        "formadores",
        "cambio",
        "unidosporamino",
        "edicion",
        "confesiones"
    ]

@dataclass
class RoleplayItem:
    itemId:         int
    ndcId:          int
    name:           str
    level:          int
    price:          int
    description:    str

    def __init__(self, itemId, ndcId, name, level, price, description):
        self.itemId         = itemId
        self.ndcId          = ndcId
        self.name           = name
        self.level          = level
        self.price          = price
        self.description    = description
        return

    @classmethod
    def error(Self):
        self = Self(-1, 0, "Error", -1, -1, "Algo está mal con este item. No existe o ha habido un error.")
        return self

@dataclass
class RoleplayInventory:
    ndcId:          int
    userId:         str
    itemId:         int
    quantity:       int

@dataclass
class RoleplayNote:
    ndcId:          int
    userId:         str
    content:        str

    def __init__(self, ndcId, userId, content):
        self.ndcId      = ndcId
        self.userId     = userId
        self.content    = content
        return

    @classmethod
    def blank(Self):
        self = Self(0, None, None)
        return self

@dataclass
class FunctionCounter:
    value:      int
    name:       str

@dataclass
class WeeklyFunctionCounter:
    ndcId:      int
    name:       str
    value:      int

@dataclass
class PAResults:
    ndcId:      int
    userId:     str
    value:      int

@dataclass
class PABlogs:
    userId:     str
    nickname:   str
    link:       str

@dataclass
class MessageHistory:
    ndcId:      int
    threadId:   str
    userId:     str
    messageId:  str
    instance:   int
    timestamp:  datetime.datetime
    content:    str

@dataclass
class ReportsResume:
    week:       int
    lastWeek:   int
    typed:      dict
    raw:        Report

@dataclass
class Confession:
    ndcId:      int
    userId:     str
    timestamp:  datetime.datetime
    content:    str

class Applicant(BaseModel):
    status:             Optional[int]
    uid:                Optional[str]
    isGlobal:           Optional[bool]
    role:               Optional[int]
    isStaff:            Optional[bool]
    nickname:           Optional[str]
    icon:               Optional[str]


class CommunityMembershipRequest(BaseModel):
    status:             Optional[int] 
    requestId:          Optional[str]
    modifiedTime:       Optional[datetime.datetime]
    ndcId:              Optional[int]
    createdTime:        Optional[datetime.datetime]
    message:            Optional[str]
    applicant:          Optional[Applicant]
    uid:                Optional[str]

@dataclass
class SubscriptionRepository:
    topic:              str
    title:              str
    url:                str
    timestamp:          datetime.datetime
