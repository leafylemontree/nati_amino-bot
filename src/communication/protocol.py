from __future__ import annotations
from dataclasses import dataclass
import json

####################################
#
#   data type = 0:
#   decription: Socket info
#   
#####################################

@dataclass
class SocketInfo:
    message: str


####################################
#
#   data type = 1:
#   decription: Request Data from instance
#   
#   objectId:               value:
#       0: communities          
#       1: coins                
#       2: status
#
#####################################

@dataclass
class SocketRequest:
    objectId: int
    value:    int


####################################
#
#   data type = 2:
#   decription: Send to chat
#   
#####################################

@dataclass
class SocketChat:
    instance:       int
    message:        str
    ndcId:          int
    threadId:       str


####################################
#
#   data type = 3:
#   decription: Raw data
#   
#####################################

class SocketRaw:
    data: str

    def __init__(self, data):
        if isinstance(data, str):   self.data = data
        else:                       self.data = json.dumps(data)


####################################
#
#   data type = 4
#   decription: Request join to com
#   
#####################################

@dataclass
class SocketJoin:
    ndcId:          int
    invitationId:   str
    leave:          int


####################################
#
#   data type = 5
#   decription: config
#   
#####################################

@dataclass
class SocketConfig:
    instance:       int




