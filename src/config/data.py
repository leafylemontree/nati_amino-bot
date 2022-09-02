from __future__ import annotations
import time
import threading
import json

users_reg = {}
temporal_disable = {}

def slow():
    global users_reg, temporal_disable
    while True:
        for i in list(users_reg.keys()):
            users_reg[i] -= 1
            if users_reg[i] == 0: users_reg.pop(i, None)
        
        for i in list(temporal_disable.keys()):
            temporal_disable[i] -= 1
            if temporal_disable[i] == 0:
                temporal_disable.pop(i, None)
                print(i, "timed out")
        time.sleep(1)

class Config:
    check_on_enter   = []
    disable_welcome  = []
    enable_goodbye   = []
    disable_bot      = []
    slow_mode        = []
    only_staff       = []
    no_fun           = []
    safe_mode        = []
    
    _true   = ["1", "ON", "TRUE", "ENABLE", "YES", "SI"]
    _false  = ["0", "OFF", "FALSE", "DISABLE", "NO"]
   
    slow_mode_thread = threading.Thread(target=slow)
    slow_mode_thread.start()
    
    def read():
        with open("data/config.json", "r") as fp:
            a = json.load(fp)
        if a == {}: return
        Config.check_on_enter  = a['check']
        Config.disable_welcome = a['welcome']
        Config.enable_goodbye  = a['goodbye']
        Config.disable_bot     = a['bot']
        Config.slow_mode       = a['slow']
        Config.only_staff      = a['staff']
        Config.no_fun          = a['1984']
        Config.safe_mode       = a['safe']
        return
    
    def write():
        a = {
            "check"  : Config.check_on_enter,
            "welcome": Config.disable_welcome,
            "goodbye": Config.enable_goodbye,
            "bot"    : Config.disable_bot,
            "slow"   : Config.slow_mode,
            "staff"  : Config.only_staff,
            "1984"   : Config.no_fun,
            "safe"   : Config.safe_mode,
                }
        with open("data/config.json", "w+") as fp:
            json.dump(a, fp, indent=4)
        return

def register(mode, chatId, time):
    global users_reg, temporal_disable
    if mode == "temporal":
        temporal_disable[chatId] = int(time)
    elif mode == "slow":
        users_reg[chatId] = 30
    return

def review(mode, chatId):
    global users_reg, temporal_disable
    if mode == 'user': return chatId in users_reg.keys()
    if mode == 'chat': return chatId in temporal_disable.keys()
    return None

Config.read()
