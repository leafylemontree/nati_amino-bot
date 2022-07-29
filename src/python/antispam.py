import json
import datetime
from edamino.api import Embed

class AS:
    
    banned_nicks = [
                    "MAMBLL",
                    "WHAT? 0)0)0)"
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

                "101": "Spam a Telegram",
                "102": "Spam de comunidad",
                "103": "Spam de comunidad",
                "104": "Spam de Twitter",

                "200": "Mensaje fuera de lo común"

            }

    logging_chat = {}
    
    last_user = {
                    #"9999" : [
                    #           [userId, datetime],
                    #           [userId, datetime],
                    #           [userId, datetime],
                    # ]
            }


    async def detect_all(ctx):
        if ctx.msg.content is None: return

        msg_type = []
        content = str(ctx.msg.content).upper()
        nick    = str(ctx.msg.author.nickname).upper() 
        comId   = str(ctx.msg.ndcId)

        for i in AS.banned_nicks:
            if ((i in nick) & ("1" not in msg_type)): msg_type.append("1") 
        for i in AS.sexual_nicks:
            if ((i in nick) & ("2" not in msg_type)): msg_type.append("2") 
        #for i in AS.sus_keywords:
        #    if ((i in nick) & ("3" not in msg_type)): msg_type.append("3") 

        if content.find("T.ME") != -1                  : msg_type.append("101")
        if content.find("AMINOAPPS.COM/C/") != -1      : msg_type.append("102")
        if content.find("AMINOAPPS.COM/INVITE/") != -1 : msg_type.append("103")
        if content.find("T.CO") != -1                  : msg_type.append("104")

        if ctx.msg.type in [108, 109, 110, 113, 114] :
            if ctx.msg.author.nickname is None: pass 
            if content.find("LIVE") != -1     : pass 
            msg_type.append("200")

        print(msg_type, ctx.msg.content, ctx.msg.author.nickname)

        if msg_type:
            if AS.logging_chat == {}: AS.load_keys()

            #print("Debe ir a este chat:", AS.logging_chat[comId])



            thread = await ctx.get_chat_info()
            
            try:
                await ctx.client.delete_message(
                    chat_id=ctx.msg.threadId,
                    message_id=ctx.msg.messageId)
                await ctx.client.kick_from_chat(ctx.msg.threadId, ctx.msg.uid, allow_rejoin=True)
            except Exception:
                pass
            
            chat = None
            
            print(AS.logging_chat.keys())
            print(comId, AS.logging_chat[comId])

            if comId in AS.logging_chat.keys(): chat = AS.logging_chat[comId]
            #else:                               return

            if await AS.register_user(ctx.msg.ndcId, ctx.msg.author.uid) : return
            
            base_msg = f"""Posible amenaza detectada:
------------------
Nick: {ctx.msg.author.nickname}
ID: {ctx.msg.author.uid}
Chat: {thread.title}
Tipo: {ctx.msg.type}
Mensaje:
{ctx.msg.content}
-----------------"""
            for i in msg_type:
                base_msg += f"\n- {i}: {AS.msg_desc[i]}"
                print(f"{i} - {AS.msg_desc[i]}")
            
            embed = Embed(
                title="Perfil del usuario",
                object_type=0,
                object_id=ctx.msg.author.uid,
                content=ctx.msg.author.nickname
            )

            await ctx.client.send_message(message=base_msg,
                                    chat_id=chat,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=embed,
                                    link_snippets_list=None,
                                    reply=None )

        return

    async def set_logging(ctx):

        user = await ctx.get_user_info()
        if ((user.role == 0) & (user.uid != "17261eb7-7fcd-4af2-9539-dc69c5bf2c76")): return "Usted no está autorizado para ejercer este comando"

        AS.logging_chat[str(ctx.msg.ndcId)] = ctx.msg.threadId

        with open("src/json/com_chatlist.json", "r+") as chatFile:
            json.dump(AS.logging_chat, chatFile, indent=4)
            print(AS.logging_chat)

        return "El chat para el log del bot ha sido cambiado con éxito"

    async def register_user(comId, userId):
        
        if comId not in AS.last_user.keys(): AS.last_user[comId] = [
                                                                [None, None],
                                                                [None, None],
                                                                [None, None]
                                                            ]
        
        AS.last_user[comId].pop(0)
        AS.last_user[comId].append([userId,
                                    int(datetime.datetime.now().timestamp())
                                    ])

        print(AS.last_user)


        if AS.last_user[comId][1] == [None, None]: return False
        dif = (AS.last_user[comId][2][1] - AS.last_user[comId][1][1])
        print("Time difference:", dif)

        if (AS.last_user[comId][2][0] != AS.last_user[comId][1][0]): return False
        if (dif > 30):  return False 
        return True

    def load_keys():
        with open("src/json/com_chatlist.json", "r+") as chatFile:
            lc = json.load(chatFile)
            #print(lc)
            for key, val in lc.items():
                AS.logging_chat[key] = val
        return
    async def ban_user(ctx):
        user = await ctx.get_user_info()
        if ((user.role != 102) & (user.uid != "17261eb7-7fcd-4af2-9539-dc69c5bf2c76")): return bot_o.Reply("Usted no está autorizado para ejercer este comando", False)
        if ((ctx.msg.extensions.replyMessage is None) & (not ctx.msg.extensions.mentionedArray)): return "Debe responde a un mensaje para banear al usuario."
        
        msg = ""
        if ctx.msg.extensions.replyMessage is not None: msg = ctx.msg.extensions.replyMessage.content

        uid = None

        reason = ctx.msg.content.split(" ")
        reason.pop(0)
        reason = " ".join(reason)
        if msg.find("ID: ") != -1:
            msg = msg.split("ID: ")[1]
            uid = msg.split("\n")[0]
        elif ctx.msg.extensions.mentionedArray:
            uid = ctx.msg.extensions.mentionedArray[0].uid
            reason = reason.split("<$@")[0]
        else:
            uid = ctx.msg.extensions.replyMessage.author.uid

        user = ctx
        user.msg.uid = uid
        user = await user.get_user_info()

        
        if AS.logging_chat == {}: AS.load_keys()
        try:
            await ctx.client.ban(
                        user_id=uid,
                        reason=reason
                    )
            await ctx.send(f"El usuario {user.nickname} ha sido baneado")
        except:
            await ctx.send("No puede banear al usuario")
            return
         
        chat =AS.logging_chat[str(ctx.msg.ndcId)]
        print(chat)

        await ctx.client.send_message(message=f"""
Se ha baneado a {user.nickname}
Motivo: {reason}
ID: {uid}
----------
Para desbanear, solo responda este mensaje y ponga --unban
""",
                                    chat_id=chat,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None )

        print(uid)
        print(user.nickname)
        print(reason)
        return

    async def unban_user(ctx):
        user = await ctx.get_user_info()
        if ((user.role != 102) & (user.uid != "17261eb7-7fcd-4af2-9539-dc69c5bf2c76")): return bot_o.Reply("Usted no está autorizado para ejercer este comando", False)
        if ctx.msg.extensions.replyMessage is None: return "Debe responde a un mensaje para desbanear al usuario."
        

        msg = ctx.msg.extensions.replyMessage.content 
        uid = None
        if msg.find("ID: ") != -1:
            msg = msg.split("ID: ")[1]
            uid = msg.split("\n")[0]
        else:
            uid = ctx.msg.extensions.replyMessage.author.uid

        user = ctx
        user.msg.uid = uid
        user = await user.get_user_info()
        
        if AS.logging_chat == {}: AS.load_keys()
        try:
            await ctx.client.unban(
                        user_id=uid,
                        reason="Miembro reintroducido manualmente"
                    )
            await ctx.send(f"El usuario {user.nickname} ha sido desbaneado")
        except:
            await ctx.send("No puede desbanear al usuario")
            return
       

        chat =AS.logging_chat[str(ctx.msg.ndcId)],
        print(chat)
        await ctx.client.send_message(message=f"""
Se ha desbaneado a {user.nickname}
ID: {uid}
""",
                                    chat_id=chat,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None )

        print(uid)
        print(user.nickname)
        return
