from src import objects
from src import utils
from src.database import db


def kiwilatigo(ctx):
        utils.database(32, ctx.msg.author.uid)
        return objects.Reply(f"[ci]¡Oh no! Han hecho enfadar a {ctx.msg.author.nickname}\n\n[ci]/c skpa.", False)

async def alias(ctx, msg):
        if ctx.msg.extensions.mentionedArray:
            msg = msg.split("\u200e")[0]
            msg = msg.split(" ")
            msg.pop(0)
            user = ctx.msg.extensions.mentionedArray[0]
            msg = " ".join(msg)[:127]
            
            db.modifyRecord(31, user, value=msg)
            user = await ctx.client.get_user_info(user.uid)
            return f"El nuevo alias de {user.nickname} es {msg}."
        else:
            msg = msg.split(" ")
            if len(msg) < 2: return "Ingrese un nombre como alias."
            msg.pop(0)
            uid = ctx.msg.author.uid
            print(uid)
            print(msg)
            msg = " ".join(msg)[:127]
            db.modifyRecord(31, ctx.msg.author, value=msg)
            return f"El nuevo alias de {ctx.msg.author.nickname} es {msg}."
        return None

async def ghost(ctx, msg):
        msg = msg[8:]
        await ctx.client.send_message(  message=msg,
                                    chat_id=ctx.msg.threadId,
                                    message_type=109,
                                    ref_id=None,
                                    mentions=None,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None )
        return False
    
async def follow(ctx):
        await ctx.follow()
        msg = "Ya está, ya te he seguido, uwu."
        return objects.Reply(msg, True)

def replyMsg(msg):
        return objects.Reply(msg, True)

async def kick(ctx, msg):
        try:
            await ctx.client.kick_from_chat(ctx.msg.threadId, ctx.msg.uid, allow_rejoin=True)
        except:
            if msg is not None:
                msg += "\n\n[c]Nota: el bot no puede sacarte."

        return objects.Reply(msg, False)

def papulince(com):

        grasa = [
                    ":V",
                    "V:",
                    "PAPU",
                    "ELFA",
                    "MOMAZO",
                    "MEMINGO",
                    "ALV",
                    "XDXDXD",
                    "PRRO",
                    "MAQUINOLA",
                    "LINCE",
                ]

        com = com.split(" ")

        papuh = [-1, False]

        for i,j in enumerate(com):
            if j in grasa:
                papuh = [i, True] 
                break

        print(papuh)

        
        if len(com) < 8:
            return papuh[1]
        else:
            if ((papuh[0] < (len(com) / 4)) | (papuh[0] > (3*len(com) / 4))):
                return papuh[1]

        return False

async def customMsg(ctx):

        msg = ctx.msg.content
        msg = msg.split(" ")[1:]
        print(msg)

        await ctx.client.send_message(  message=f"Mensaje Tipo: {msg[0]}\n" + " ".join(msg[1:]),
                                    chat_id=ctx.msg.threadId,
                                    message_type=int(msg[0]),
                                    ref_id=None,
                                    mentions=None,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None) 
        return

