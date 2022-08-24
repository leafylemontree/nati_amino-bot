from src import objects
from src.text import text

def _help(com, comId):
        msg = com.split(" ")
        print(msg)
        
        if ( (len(msg) == 1) & (comId == 112646170) ):            return objects.Reply(text['help']['default'].replace("Nati", "Artemis"), False)
        elif ( (len(msg) == 1) & (comId == 215907772) ):          return objects.Reply(text['help']['default'].replace("Nati", "Emma"), False)
        elif ( (len(msg) == 1) & (comId == 139175768) ):          return objects.Reply(text['help']['default'].replace("Nati", "Anya"), False)
        elif      len(msg) == 1:          return objects.Reply(text['help']['default'])

        msg = msg[1].lower()

        if msg in text['help']  :   return objects.Reply(text['help'][msg], False)
        return                                 objects.Reply("No existe este comando por el momento, :c", False)
