import mariadb
import json

class UserInfo:
    def __new__(self, cursor):
        cur = []
        for a in cursor: cur.append(a)
        try:
            cur = cur[0]
        except IndexError as e:
            return None

        self.userId,self.alias,self.hugs_r,self.hugs_g,self.kiss_r,self.kiss_g,self.pats_r,self.pats_g,self.doxx_r,self.doxx_g,self.kiwi,self.win,self.draw,self.lose,self.points,*self.unused = cur
        return self


class LogConfig:
    def __new__(self, cursor):
        cur = []
        for a in cursor: cur.append(a)
        try:
            cur = cur[0]
        except IndexError as e:
            return None
        self.comId, self.threadId, self.nowarn, self._ignore, self.ban, self.stalk, self.staff, self.bot, *self.unused = cur
        return self

class Config:
    def __new__(self, cursor):
        cur = []
        for a in cursor: cur.append(a)
        try:
            cur = cur[0]
        except IndexError as e:
            return None
        self.threadId, self._check, self.welcome, self.goodbye, self.bot, self.slow, self.staff, self.nofun, self.safe, *self.unused = cur
        return self

class Database:
    base   = None
    cursor = None

    def __init__(self):
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
        data = UserInfo(self.cursor)
        print(data)
        if data is None:
            self.setUserData(user)
            self.cursor.execute(f'SELECT * FROM UserInfo WHERE userId="{user.uid}"')
            data = UserInfo(self.cursor)
        return data

    def setUserData(self, user):
        self.cursor.execute(f'INSERT INTO UserInfo VALUES ("{user.uid}", "", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)')
    
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


        self.cursor.execute(f'SELECT {column} FROM UserInfo WHERE userId="{user.uid}";')
        data = self.cursor.fetchall()[0]
        if not data:
            self.cursor.execute(f'INSERT INTO UserInfo VALUES ("{user.uid}", "-", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)')
            data = 0
        else:
            data = data[0]

        if mode == 31 and value != 1:   data = f'"{value}"'.replace(";", "").replace("DROP TABLE", "").replace("drop table", "")
        else:                           data = data + value
        
        self.cursor.execute(f'UPDATE UserInfo SET {column}={data} WHERE userId="{user.uid}";')
        return data

    def setLogConfig(self, comId, mode, value):
        if mode not in ['threadId', 'nowarn', '_ignore', 'ban', 'stalk', 'staff', 'bot'] : return None
        self.cursor.execute(f'SELECT * FROM Log WHERE comId={comId};')
        a = []
        for c in self.cursor: a.append(c)
        if a == []: self.cursor.execute(f'INSERT INTO Log VALUES ({comId}, "", 0, 0, 0, 0, 0, 0);')
        if mode == "threadId" : value = f'"{value}"'
        self.cursor.execute(f'UPDATE Log SET {mode}={value} WHERE comId={comId};')
        return True

    def getLogConfig(self, comId):
        self.cursor.execute(f'SELECT * FROM Log WHERE comId={comId};')
        data = LogConfig(self.cursor)
        if not data:
            self.cursor.execute(f'INSERT INTO Log VALUES ({comId}, "", 0, 0, 0, 0, 0, 0, 1);')
            self.cursor.execute(f'SELECT * FROM Log WHERE comId={comId};')
            data = LogConfig(self.cursor)
        return data

    def setChatConfig(self, threadId, mode, value):
        if mode not in ['_check', 'welcome', 'goodbye', 'bot', 'slow', 'staff', 'nofun', 'safe'] : return None
        print(threadId, mode, value)
        self.cursor.execute(f'SELECT * FROM Chat WHERE threadId="{threadId}";')
        a = []
        for c in self.cursor: a.append(c)
        print(a, bool(a))
        if not a: self.cursor.execute(f'INSERT INTO Chat VALUES ("{threadId}", 0, 0, 0, 0, 0, 0, 0, 0);')
        self.cursor.execute(f'UPDATE Chat SET {mode}={value} WHERE threadId="{threadId}";')
        return True

    def getChatConfig(self, threadId):
        self.cursor.execute(f'SELECT * FROM Chat WHERE threadId="{threadId}";')
        data = Config(self.cursor)
        if not data:
            self.cursor.execute(f'INSERT INTO Chat VALUES ("{threadId}", 0, 0, 0, 0, 0, 0, 0, 0);')
            self.cursor.execute(f'SELECT * FROM Chat WHERE threadId="{threadId}";')
            data = Config(self.cursor)
        return data

    def registerReport(self, userId, comId, threadId, warnings):
        self.cursor.execute(f'INSERT INTO Reports VALUES ("{userId}", {comId}, "{threadId}", NOW(), {1 if "1" in warnings else 0}, {1 if "2" in warnings else 0}, {1 if "3" in warnings else 0}, {1 if "101" in warnings else 0}, {1 if "102" in warnings else 0}, {1 if "103" in warnings else 0}, {1 if "104" in warnings else 0}, {1 if "111" in warnings else 0}, {1 if "151" in warnings else 0}, {1 if "152" in warnings else 0}, {1 if "200" in warnings else 0});')
        return


db = Database()
