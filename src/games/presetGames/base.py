from __future__ import annotations
from dataclasses import dataclass
from typing import List, Any

@dataclass
class Auth:
    password    : str
    isOpen      : int
    mode        : int
    nickname    : str
    uid         : str

@dataclass
class BaseInstance:
    roomId  :   int
    threadId:   str
    ndcId   :   int
    players :   List
    game    :   str
    auth    :   Auth
    run     =   False

    def start(self):
        self.run         = True
        self.auth.isOpen = False

    def playerList(self):
        players = []
        for player in self.players: players.append(player[0])
        return players
    
    def end(self):
        self.run         = False
        self.auth.isOpen = True

    def indexPlayer(self, uid):
        for index, player in enumerate(self.players):
            if player[0] == uid:    return index

    async def screen(self):
        return
    async def logic(self, ctx, key):
        return
    async def win(self, ctx):
        return
    async def lose(self, ctx):
        return
