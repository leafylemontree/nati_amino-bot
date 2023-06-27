import  mariadb
import  ujson as json
import  redis
from    src     import  objects
import  aiofile
import  os
import  threading
import  datetime
import  uuid

class Database:
    base   = None
    cursor = None
    redis  = None

    r_chatTable     = 'chatConfig'
    r_logTable      = 'logConfig'
    r_comWelMsg     = 'CommunityWelcome'
    r_chatWelMsg    = 'ChatWelcome'
    r_userNickname  = "UserNickname"
    r_messageCom    = "MessagesSentCounter"
    r_userMsgCounter= "UserMessageCounter"
    r_userExp       = "UserEXP"

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

    def getUserData(self, user, userId=None):
        if not userId: userId = user.uid
        self.cursor.execute(f'SELECT * FROM UserInfo WHERE userId="{userId}";')
        resp = self.cursor.fetchall()
        if not resp:
            self.setUserData(user)
            self.cursor.execute(f'SELECT * FROM UserInfo WHERE userId="{userId}"')
            resp = self.cursor.fetchall()
        return objects.UserInfo(*resp[0])

    def setUserData(self, user, userId=None):
        if not userId: userId = user.uid
        self.cursor.execute(f'INSERT INTO UserInfo VALUES ("{userId}", "", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, "none")')
    
    def modifyRecord(self, mode, user, value=1, userId=None):
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
        elif mode == 44: column = "unused4"
        elif mode == 50: column = "marry"
        elif mode == 60: column = "unused5"
        elif mode == 70: column = "unused6"

        if not userId: userId = user.uid

        self.cursor.execute(f'SELECT {column} FROM UserInfo WHERE userId="{userId}";')
        data = self.cursor.fetchall()[0]
        if not data:
            self.cursor.execute(f'INSERT INTO UserInfo VALUES ("{userId}", "-", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, "none")')
            data = 0
        else:
            data = data[0]

        if mode in [31, 50] and value != 1:   data = f'{value}'.replace(";", "").replace("DROP", "").replace("drop", "")
        else:                           data = data + value
        
        self.cursor.execute(f'UPDATE UserInfo SET {column}=? WHERE userId="{userId}";', (data,))
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
        w300 = 1 if "300" in warnings else 0
        self.cursor.execute(f'INSERT INTO Reports VALUES ("{userId}", {comId}, "{threadId}", NOW(), {w001}, {w002}, {w003}, {w101}, {w102}, {w103}, {w104}, {w111}, {w151}, {w152}, {w200}, {w105}, {w106}, {w107}, {w108}, {w004}, {w109}, {w300});')
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
            #self.cursor.execute(f'INSERT INTO Yincana VALUES ("{userId}", {ndcId}, 0);')
            #self.cursor.execute(f'SELECT * FROM Yincana WHERE userId="{userId}" AND ndcId={ndcId}')
            #resp = self.cursor.fetchall()
            yincana = objects.Yincana.blank(userId, ndcId)
            return yincana

        yincana = objects.Yincana.from_db(*resp[0])
        return yincana

    def setYincanaData(self, userId, ndcId, level=0):
        yincana         = self.getYincanaData(userId, ndcId)
        yincana.level  += level
        if yincana.isBlank: self.cursor.execute(f'INSERT INTO Yincana VALUES ("{userId}", {ndcId}, 1, NOW());')
        else:               self.cursor.execute(f'UPDATE Yincana SET level={yincana.level} WHERE userId="{userId}" AND ndcId={ndcId};')
        return yincana

    def getYincanaDataCommunity(self, ndcId):
        self.cursor.execute(f'SELECT * FROM Yincana WHERE ndcId={ndcId}')
        resp = self.cursor.fetchall()
        return tuple(map(lambda data: objects.Yincana.from_db(*data), resp))

    def checkYincanaExist(self, objectType, objectId, ndcId):
        self.cursor.execute(f'SELECT * FROM YincanaCheck WHERE objectType={objectType} AND objectId="{objectId}" AND ndcId={ndcId}')
        resp = self.cursor.fetchall()
        return False if resp == [] else True

    def setYincanaObject(self, objectType, objectId, ndcId):
        resp = self.checkYincanaExist(objectType, objectId, ndcId)
        self.cursor.execute(f'INSERT INTO YincanaCheck VALUES ({objectType}, "{objectId}", {ndcId}, NOW());')

    
    def getNatiPetData(self, ndcId):
        from src.pet import helpers as petHelpers

        self.cursor.execute("SELECT * FROM NatiPet WHERE ndcId=?;", (ndcId, ))
        resp = self.cursor.fetchall()
        if resp == []: return None
        pet = objects.NatiPet(*resp[0])

        pet.level       = petHelpers.getLevelFromEXP(pet.exp)
        pet.maxHealth   = pet.maxHealth + (pet.level * 500)

        if self.redis.hexists(self.r_messageCom, f"?{ndcId}"):
            pet = objects.NatiPet(*resp[0])

            messages = self.redis.hget(self.r_messageCom, f"?{ndcId}")
            messages = int.from_bytes(messages, 'big')
            pet.care += messages // 10
            if pet.care < 0    : pet.care = 0

            timedelta = datetime.datetime.now() - pet.lastInteraction
            secs      = timedelta.seconds // 10
            if secs > pet.care:
                secs = secs - pet.care
                pet.care = 0
                pet.health = (pet.health - (secs * 2))
                if pet.health < 0    : pet.health = 0
            else:
                pet.care = pet.care - secs

            self.cursor.execute("UPDATE NatiPet SET lastInteraction=NOW(), health=?, care=? WHERE ndcId=?;", (pet.health, pet.care, ndcId, ))
            self.redis.hset(self.r_messageCom, f"?{ndcId}", (0).to_bytes(4, 'big'))
            self.cursor.execute("SELECT * FROM NatiPet WHERE ndcId=?;", (ndcId, ))
            resp = self.cursor.fetchall()

        return objects.NatiPet(*resp[0])


    def initNatiPet(self, ndcId):
        pet = self.getNatiPetData(ndcId)
        if pet: return pet
        self.cursor.execute("INSERT INTO NatiPet VALUES (?, NOW(), NOW(), 0, 0, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 0)", (ndcId,))
        pet = self.getNatiPetData(ndcId)
        return pet

    def updateNatiPet(self, ndcId, column, amount):
        pet = self.getNatiPetData(ndcId)
        if pet is None: return None
    
        if column == "health":
            amount = pet.health + amount
            if amount > pet.maxHealth: amount = pet.maxHealth

        elif column == "happiness": amount = pet.happiness + amount
        elif column == "energy":    amount = pet.energy    + amount
        elif column == "care":      amount = pet.care      + amount
        elif column == "hunger":    amount = pet.hunger    + amount
        elif column == "thirst":    amount = pet.thirst    + amount
        else                   :    return None
        
        if amount < 0                           : amount = 0

        self.cursor.execute(f"UPDATE NatiPet SET {column}=?, lastInteraction=NOW(), WHERE ndcId=?", (amount, ndcId, ))
        pet = self.getNatiPetData(ndcId)
        return pet

    def updateMultipleNatiPet(self, ndcId, data):
        pet = self.getNatiPetData(ndcId)
        query = f"UPDATE NatiPet SET "
        for i,(key, value) in enumerate(data.items()):
            if      key == "health":
                if (pet.health + value) > pet.maxHealth: value = pet.maxHealth
                else:                                    value += pet.health
                if value < 0: value = 0
                query += f"health={value}, "

            elif    key == "exp":
                value += pet.exp
                query += f"exp={value}, "

            elif    key == "happiness":
                value += pet.happiness
                if value < 0: value = 0
                query += f"happiness={value}, "

            elif    key == "energy":
                value += pet.energy
                if value < 0: value = 0
                query += f"energy={value}, "

            elif    key == "care":
                value += pet.care
                if value < 0: value = 0
                query += f"care={value}, "

            elif    key == "hunger":
                value += pet.hunger
                if value < 0: value = 0
                query += f"hungry={value}, "

            elif    key == "thirst":
                value += pet.thirst
                if value < 0: value = 0
                query += f"thirst={value}, "

            elif    key == "effects":
                if pet.effects != 0: query += f"effects={pet.effects}"
                else:   query += f"effects={value}"

        self.cursor.execute(f"{query} WHERE ndcId=?", (ndcId,) )
        pet = self.getNatiPetData(ndcId)
        return pet

    def getUserRewards(self, userId, ndcId):
        self.cursor.execute("SELECT * FROM Rewards WHERE userId=? AND ndcId=?;", (userId, ndcId,))
        resp = self.cursor.fetchall()
        return tuple(map(lambda reward: objects.Rewards(*reward), resp)) 

    def removeUserRewards(self, rewards):
        if isinstance(rewards, str): rewards = (rewards, )
        query = "DELETE FROM Rewards WHERE " + " OR ".join(f'rewardId=?' for r in rewards) + ";"
        self.cursor.execute(query, rewards)
        return

    def setUserReward(self, userId, ndcId, dtype=0, itemId=0, amount=0):
        rewardId = uuid.uuid4()
        self.cursor.execute("INSERT INTO Rewards VALUES (?, ?, ?, ?, ?, ?)", (userId, ndcId, dtype, itemId, amount, str(rewardId), ))
        return

    def getLastDonation(self, userId, ndcId):
        self.cursor.execute("SELECT * FROM ACDonations WHERE userId=? AND ndcId=?", (userId, ndcId,))
        resp = self.cursor.fetchall()
        if resp == []: return None
        return resp[0][1]

    def setLastDonation(self, userId, notificationId, amount, ndcId):
        if notificationId is None: return None
        oldNotificationId = self.getLastDonation(userId, ndcId)
        if oldNotificationId is None:
            self.cursor.execute("INSERT INTO ACDonations VALUES (?, ?, ?)", (userId, notificationId, ndcId))
        else:
            self.cursor.execute("UPDATE ACDonations SET notificationId=? WHERE userId=? AND ndcId=?", (notificationId, userId, ndcId,))

        data = self.modifyRecord(60, None, amount, userId=userId)
        return data

    def getUserExp(self, ndcId, userId):
        self.cursor.execute("SELECT * FROM UserEXP WHERE userId=? AND ndcId=?", (userId, ndcId,))
        resp = self.cursor.fetchall()
        
        delta = 0
        label = f"?{ndcId}&{userId}"
        if self.redis.hexists(self.r_userMsgCounter, label):
            raw   = self.redis.hget(self.r_userMsgCounter, label)
            delta = int.from_bytes(raw, 'big')
        
        counter = 0
        if resp != []:
            counter = resp[0][2] + delta
            self.cursor.execute("UPDATE UserEXP SET exp=? WHERE userId=? AND ndcId=?", (counter, userId, ndcId, ))
        else:
            counter = delta
            self.cursor.execute("INSERT INTO UserEXP VALUES (?, ?, ?)", (ndcId, userId, counter,))
        
        self.redis.hset(self.r_userMsgCounter, label, (0).to_bytes(4, 'big'))
        self.redis.hset(self.r_userExp, label, (counter).to_bytes(4, 'big'))
        return counter

    def getExpRank(self, ndcId):
        self.cursor.execute("SELECT * FROM UserEXP WHERE ndcId=?", (ndcId, ))
        resp = self.cursor.fetchall()
        userExp = list(map(lambda x: objects.UserEXP(*x), resp))
        for user in userExp:    user.exp = self.getUserExp(ndcId, user.userId)
        return userExp

db = Database()
