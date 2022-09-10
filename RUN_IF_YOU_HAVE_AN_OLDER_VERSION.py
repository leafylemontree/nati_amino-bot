from src.database import db
from src import utils
from src import objects
import os
import json
from dataclasses import dataclass

class User:
    uid = "ffffffff-ffff-ffff-ffff-fffffffffffa"

    def setuid(self, uid):
        uid = str(uid)
        uid = uid[:len(uid)-4]
        self.uid = uid
        print(self.uid)

@dataclass
class Log:
    comId    : int
    threadId : str
    nowarn   : bool
    _ignore  : bool
    ban      : bool
    stalk    : bool
    staff    : bool
    bot      : bool

def insertUsers():
    user = User()
    os.chdir("database")
    folder = os.listdir()
    os.chdir("..")
    oldDB = objects.Database_return()
    for num,file in enumerate(folder):
        print(num,file)
        user.setuid(file)
        data = utils.database(1, uid=user.uid, name=" ")
        oldDB.strToVal(data)
        print(oldDB.alias)
        db.cursor.execute(f'INSERT INTO UserInfo VALUES ("{user.uid}", "{oldDB.alias}", {oldDB.hugs_r}, {oldDB.hugs_g}, {oldDB.kiss_r}, {oldDB.kiss_g}, {oldDB.pats_r}, {oldDB.pats_g}, {oldDB.doxx_r}, {oldDB.doxx_g}, {oldDB.kiwi}, {oldDB.win}, {oldDB.derr}, {oldDB.draw}, {oldDB.points}, 0, 0, 0, 0, 1)')

    
def insertLogging():
    ban_no_warn  = {}
    ignore_coms  = {}
    no_warnings  = {}
    stalkList    = {}
    logging_chat = {}

    with open("data/comConfig.json", "r+") as fp:
        o = json.load(fp)
        ban_no_warn = o['ban']
        print("ban_no_warn:", ban_no_warn)
        ignore_coms = o['ignore']
        print("ignored:", ignore_coms)
        no_warnings = o['no-warning']
        print("no_warns:", no_warnings)
        stalkList   = o['stalk']
        print("stalks:", stalkList)
    with open("data/com_chatlist.json", "r") as fp:
        logging_chat = json.load(fp)
    
    coms = []
    coms.extend(ban_no_warn)
    coms.extend(ignore_coms)
    coms.extend(no_warnings)
    coms.extend(stalkList)
    
    c = []
    for com in logging_chat: c.append(int(com))
    coms.extend(c)

    print(coms)
    coms = set(coms)
    print(coms)

    for com in coms:
        log = Log(
                com,
                logging_chat[str(com)] if str(com) in logging_chat.keys() else "",
                1 if com in no_warnings else 0,
                1 if com in ignore_coms else 0,
                1 if com in ban_no_warn else 0,
                1 if com in stalkList   else 0,
                0, 0
                )

        print(log)
        db.cursor.execute(f'INSERT INTO Log VALUES ({log.comId}, "{log.threadId}", {log.nowarn}, {log._ignore}, {log.ban}, {log.stalk}, {log.staff}, {log.bot});')


def insertConfig():
    with open("data/config.json", "r+") as fp:
        o = json.load(fp)
        check   = o['check']
        welcome = o['welcome']
        goodbye = o['goodbye']
        bot     = o['bot']
        slow    = o['slow']
        staff   = o['staff']
        nofun   = o['1984']
        safe    = o['safe']

    chats = []
    chats.extend(check)
    chats.extend(welcome)
    chats.extend(goodbye)
    chats.extend(bot)
    chats.extend(slow)
    chats.extend(staff)
    chats.extend(nofun)
    chats.extend(safe)
    chats = set(chats)
    print(chats)

    for chat in chats:
        db.cursor.execute(f'INSERT INTO Chat VALUES ("{chat}", {1 if chat in check else 0}, {1 if chat in welcome else 0}, {1 if chat in goodbye else 0}, {1 if chat in bot else 0}, {1 if chat in slow else 0}, {1 if chat in staff else 0}, {1 if chat in nofun else 0}, {1 if chat in safe else 0});')

insertUsers()
insertLogging()
insertConfig()


