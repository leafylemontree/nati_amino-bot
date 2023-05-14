import  mariadb
import  ujson as json
import  redis
from    src     import  objects
import  aiofile
import  os
import  threading

class Database:
    base   = None
    cursor = None
    redis  = None

    r_chatTable = 'chatConfig'
    r_logTable  = 'logConfig'
    r_comWelMsg = 'CommunityWelcome'
    r_chatWelMsg= 'ChatWelcome'
    r_userNickname = "UserNickname"

    def __init__(self):
        self.redis = redis.Redis()
        with open("data/base.json", "r") as fp:
            data = json.load(fp)
        try:
            self.base = mariadb.connect(
                    host     = data["host"],
                    user     = data["user"],
                    password = data["password"],
                    database = data["database"]
                )
        except mariadb.Error as e:
            print("Error during database read:", e)
        else:
            print("Database read done!")
            self.cursor = self.base.cursor()
            self.base.autocommit = True

    def getUserData(self, user):
        self.cursor.execute(f'SELECT * FROM UserInfo WHERE userId="{user.uid}";')
        resp = self.cursor.fetchall()
        if not resp:
            self.setUserData(user)
            self.cursor.execute(f'SELECT * FROM UserInfo WHERE userId="{user.uid}"')
            resp = self.cursor.fetchall()
        return objects.UserInfo(*resp[0])

    def setUserData(self, user):
        self.cursor.execute(f'INSERT INTO UserInfo VALUES ("{user.uid}", "", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, "none")')
    
    def modifyRecord(self, mode, user, value=1):
        column = "version"
        if   mode == 11: column = "recvHugs"
        elif mode == 21: column = "givenHugs"
        elif mode == 12: column = "recvKiss"
        elif mode == 22: column = "givenKiss"
        elif mode == 13: column = "recvPats"
        elif mode == 23: column = "givenPats"
        elif mode == 14: column = "recvDoxx"
        elif mode == 24: column = "givenDoxx"
        elif mode == 31: column = "alias"
        elif mode == 43: column = "unused3"
        elif mode == 50: column = "marry"

        self.cursor.execute(f'SELECT {column} FROM UserInfo WHERE userId="{user.uid}";')
        data = self.cursor.fetchall()[0]
        if not data:
            self.cursor.execute(f'INSERT INTO UserInfo VALUES ("{user.uid}", "-", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, "none")')
            data = 0
        else:
            data = data[0]

        if mode in [31, 50] and value != 1:   data = f'"{value}"'.replace(";", "").replace("DROP", "").replace("drop", "")
        else:                           data = data + value
        
        self.cursor.execute(f'UPDATE UserInfo SET {column}=? WHERE userId="{user.uid}";', (data,))
        return data

    def setLogConfig(self, comId, mode, value):
        self.cursor.execute(f'SELECT * FROM Log WHERE comId="{comId}";')
        data = self.cursor.fetchall()
        if data == []: self.cursor.execute(f'INSERT INTO Log VALUES ({comId}, "", 0, 0, 0, 0, 0, 0, 0, 0);')
        self.cursor.execute(f'UPDATE Log SET {mode}=? WHERE comId={comId};', (value,))

        self.cursor.execute(f'SELECT * FROM Log WHERE comId="{comId}";')
        resp = self.cursor.fetchall()
        data = objects.LogConfig(*resp[0])
        self.redis.hset(self.r_logTable, f'?{comId}', json.dumps(data.__dict__))
        return data

    def getLogConfig(self, comId):
        if self.redis.hexists(self.r_logTable, f'?{comId}'):
            data = self.redis.hget(self.r_logTable, f'?{comId}')
            return objects.LogConfig(**json.loads(data))

        self.cursor.execute(f'SELECT * FROM Log WHERE comId="{comId}";')
        resp = self.cursor.fetchall()
        if not resp:
            self.cursor.execute(f'INSERT INTO Log VALUES ({comId}, "", 0, 0, 0, 0, 0, 0, 1, 0, 0, 0);')
            self.cursor.execute(f'SELECT * FROM Log WHERE comId={comId};')
            resp = self.cursor.fetchall()
        
        data = objects.LogConfig(*resp[0])
        self.redis.hset(self.r_logTable, f'?{comId}', json.dumps(data.__dict__))
        return data

    def setChatConfig(self, threadId, mode, value, ndcId):
        self.cursor.execute(f'SELECT * FROM Chat WHERE threadId="{threadId}";')
        data = self.cursor.fetchall()
        if data == []: self.cursor.execute(f'INSERT INTO Chat VALUES ("{threadId}", {ndcId}, 0, 0, 0, 0, 0, 0, 0, 0, 0);')
        self.cursor.execute(f'UPDATE Chat SET {mode}={value} WHERE threadId="{threadId}";')

        self.cursor.execute(f'SELECT * FROM Chat WHERE threadId="{threadId}";')
        resp = self.cursor.fetchall()
        data = objects.ChatConfig(*resp[0])
        self.redis.hset(self.r_chatTable, f'?{ndcId}&{threadId}', json.dumps(data.__dict__))
        return data

    def getChatConfig(self, threadId, ndcId, exists=False):
        if self.redis.hexists(self.r_chatTable, f'?{ndcId}&{threadId}'):
            data = self.redis.hget(self.r_chatTable, f'?{ndcId}&{threadId}')
            return objects.ChatConfig(**json.loads(data))

        self.cursor.execute(f'SELECT * FROM Chat WHERE threadId="{threadId}" AND comId="{ndcId}";')
        resp = self.cursor.fetchall()
        if not resp:
            if exists: return None
            self.cursor.execute(f'INSERT INTO Chat VALUES ("{threadId}", {ndcId}, 0, 0, 0, 0, 0, 0, 0, 0);')
            self.cursor.execute(f'SELECT * FROM Chat WHERE threadId="{threadId}";')
            resp = self.cursor.fetchall()
        
        data = objects.ChatConfig(*resp[0])
        if not data.comId:
            data.comId = ndcId
            self.cursor.execute(f'UPDATE Chat SET comId={ndcId} WHERE threadId="{threadId}";')
        self.redis.hset(self.r_chatTable, f'?{ndcId}&{threadId}', json.dumps(data.__dict__))
        return data

    def registerReport(self, userId, comId, threadId, warnings):
        w001 = 1 if "1"   in warnings else 0
        w002 = 1 if "2"   in warnings else 0
        w003 = 1 if "3"   in warnings else 0
        w004 = 1 if "4"   in warnings else 0
        w101 = 1 if "101" in warnings else 0
        w102 = 1 if "102" in warnings else 0
        w103 = 1 if "103" in warnings else 0
        w104 = 1 if "104" in warnings else 0
        w105 = 1 if "105" in warnings else 0
        w106 = 1 if "106" in warnings else 0
        w107 = 1 if "107" in warnings else 0
        w108 = 1 if "108" in warnings else 0
        w109 = 1 if "109" in warnings else 0
        w111 = 1 if "111" in warnings else 0
        w151 = 1 if "151" in warnings else 0
        w152 = 1 if "152" in warnings else 0
        w200 = 1 if "200" in warnings else 0
        self.cursor.execute(f'INSERT INTO Reports VALUES ("{userId}", {comId}, "{threadId}", NOW(), {w001}, {w002}, {w003}, {w101}, {w102}, {w103}, {w104}, {w111}, {w151}, {w152}, {w200}, {w105}, {w106}, {w107}, {w108}, {w004}, {w109});')
        return

    def r_addBlog(self, ndcId, blogId):
        hashName    = 'viewedBlogs'
        entry       = f'?{ndcId}&{blogId}'
        resp        = self.redis.hexists(hashName, entry)
        self.redis.hset(hashName, entry, 1)
        return resp

    def getWelcomeMessage(self, ndcId, mode='ALL'):
        if mode.upper() not in ['ALL', 'COMMUNITY', 'CHAT']:
            raise Exception('Incorrect Value for getWelcomeMessage')
            return

        output = objects.WelcomeMessage(ndcId, None, None)

        if not (self.redis.hexists(self.r_comWelMsg, f'?{ndcId}') or self.redis.hexists(self.r_chatWelMsg, f'?{ndcId}')): 
            self.cursor.execute(f'SELECT * FROM WelcomeMsg WHERE comId={ndcId}')
            resp = self.cursor.fetchall()
            if resp == []:  output.chat = '-DEFAULT'
            else:
                data = objects.WelcomeMessage(*resp[0])
                self.redis.hset(self.r_comWelMsg,  f'?{ndcId}', data.message)
                self.redis.hset(self.r_chatWelMsg, f'?{ndcId}', data.chat   )

        if mode.upper() in ['ALL', 'COMMUNITY']:
                message         = self.redis.hget(self.r_comWelMsg,  f'?{ndcId}')
                if message      : output.message = message.decode('utf-8')
        if mode.upper() in ['ALL', 'CHAT']:
                chat            = self.redis.hget(self.r_chatWelMsg, f'?{ndcId}')
                if not chat     : output.chat = '-DEFAULT'
                else            : output.chat = chat.decode('utf-8')

        if mode.upper() == 'COMMUNITY'  : return output.message
        if mode.upper() == 'CHAT'       : return output.chat
        if mode.upper() == 'ALL'        : return output
        return output 

    async def getUserNickname(self, ctx, ndcId, user=None, userId=None):
        if user:
            if self.redis.hexists(self.r_userNickname, f'?{ndcId}&{user.uid}'):
                data = self.redis.hget(self.r_userNickname, f'?{ndcId}&{user.uid}')
                return data.decode()
        elif userId:
            if self.redis.hexists(self.r_userNickname, f'?{ndcId}&{userId}'):
                data = self.redis.hget(self.r_userNickname, f'?{ndcId}&{userId}')
                return data.decode()

        if ctx is None and user is None: return None

        if not user and userId is not None:  user = await ctx.client.get_user_info(userId)
        self.redis.hset(self.r_userNickname, f'?{ndcId}&{user.uid}', f'{user.nickname}')
        return user.nickname

    def dumpAllChats(self):
        self.cursor.execute('SELECT * FROM Chat')
        data = self.cursor.fetchall()
        chats = tuple(map(lambda chat: objects.ChatConfig(*chat), data))

        for chat in chats:
            chatData = json.dumps(chat.__dict__)
            self.redis.hset(self.r_chatTable, f'?{chat.comId}&{chat.threadId}', chatData)
    print("Dump complete")


    async def getUserInventory(self, userId):
        path = 'database/'

        try:
            async with aiofile.async_open(f'{path}{userId}.json', 'r+') as f:
                text        = await f.read()

                if not text: raise FileNotFoundError
                response    = json.loads(text)
                inventory   = objects.UserInventory(**response)
                return inventory

        except FileNotFoundError:
            inventory = objects.UserInventory.Blank(userId)
            return inventory

    
    async def setUserInventory(self, inventory):
        path = 'database/'

        with open(f'{path}{inventory.userId}.json', 'w+') as f:
            json.dump(inventory.export(), f, indent=4)

    def getYincanaData(self, userId, ndcId):
        self.cursor.execute(f'SELECT * FROM Yincana WHERE userId="{userId}" AND ndcId={ndcId}')
        resp = self.cursor.fetchall()
        if resp == []:
            self.cursor.execute(f'INSERT INTO Yincana VALUES ("{userId}", {ndcId}, 0);')
            self.cursor.execute(f'SELECT * FROM Yincana WHERE userId="{userId}" AND ndcId={ndcId}')
            resp = self.cursor.fetchall()

        yincana = objects.Yincana(*resp[0])
        return yincana


    def setYincanaData(self, userId, ndcId, level=0):
        yincana         = self.getYincanaData(userId, ndcId)
        yincana.level  += level
        self.cursor.execute(f'UPDATE Yincana SET level={yincana.level} WHERE userId="{userId}" AND ndcId={ndcId};')
        return yincana

    def checkYincanaExist(self, objectType, objectId, ndcId):
        self.cursor.execute(f'SELECT * FROM YincanaCheck WHERE objectType={objectType} AND objectId="{objectId}" AND ndcId={ndcId}')
        resp = self.cursor.fetchall()
        return False if resp == [] else True

    def setYincanaObject(self, objectType, objectId, ndcId):
        resp = self.checkYincanaExist(objectType, objectId, ndcId)
        self.cursor.execute(f'INSERT INTO YincanaCheck VALUES ({objectType}, "{objectId}", {ndcId}, NOW());')

        




db = Database()
