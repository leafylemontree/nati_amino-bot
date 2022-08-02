import json
import datetime
from edamino.api import Embed
from edamino.objects import Author
from pydantic import BaseModel
from typing import List, Dict, Optional, Any, Tuple

class WallComment(BaseModel):
    author          : Optional[Author]
    content         : Optional[str]
    extensions      : Any
    parentId        : Optional[str]
    createdTime     : Optional[str]
    subCommentsCount: Any
    commentType     : Optional[int]



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

    ban_no_warn = {
                    "comlist" : []
            }
    ignore_coms = {
                    "comlist" : []
            }
    no_warnings = {
                    "comlist" : []
            }

    with open("src/json/strict_list.json", "r+") as fp:
        ban_no_warn = json.load(fp)
        print("ban_no_warn:", ban_no_warn)
    with open("src/json/ignore_coms.json", "r+") as fp:
        ignore_coms = json.load(fp)
        print("ignored:", ignore_coms)
    with open("src/json/no_warn.json", "r+") as fp:
        no_warnings = json.load(fp)
        print("no_warns:", no_warnings)

    async def detect_all(ctx):
        if ctx.msg.content is None: return

        msg_type = []
        content = str(ctx.msg.content).upper()
        nick    = str(ctx.msg.author.nickname).upper() 
        comId   = str(ctx.msg.ndcId)

        if int(comId) in AS.no_warnings["comlist"]: return

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
        
        if int(comId) in AS.ignore_coms["comlist"]:
            if "102" in msg_type: msg_type.remove("102")
            if "103" in msg_type: msg_type.remove("103")

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
        
            if int(comId) in AS.ban_no_warn["comlist"]:
                #try:
                await ctx.client.ban(
                        user_id=ctx.msg.author.uid,
                        reason=f"Baneado automáticamente por razones: {msg_type}"
                        )
                user = ctx
                user.msg.uid = uid
                user = await user.get_user_info()
                await ctx.client.send_message(message=f"""
Se ha baneado a {user.nickname}
Motivo: {msg_type}
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
                return
                #except Exception:
                #    pass


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

        with open("src/json/com_chatlist.json", "w+") as chatFile:
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
        if ((user.role != 102) & (user.uid != "17261eb7-7fcd-4af2-9539-dc69c5bf2c76")): return "Usted no está autorizado para ejercer este comando"
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
    async def logConfig(ctx):
        com = ctx.msg.content.upper().split(" ")
        
        if len(com) == 1: return """
Esta opción debe usarse para configurar partes de moderación del bot. No funciona si quien lo efectúa no es staff en la comunidad:
---------------------------

--logConfig -no-warn:
El bot no enviará reportes

--logConfig -wAll   :
El bot enviará todos los reportes

--logConfig -ignore :
EL bot no atacará ante spam de comunidades

--logConfig -strict :
El bot expulsará inmediatamente

--logConfig -normal :
El bot expulsará solo ante pedido
    """
        
        user = await ctx.get_user_info()
        if ((user.role == 0) & (user.uid != "17261eb7-7fcd-4af2-9539-dc69c5bf2c76")): return "Usted no está autorizado para ejercer este comando"
        
        msg   = None 
        comId = ctx.msg.ndcId

        if   com[1] == "-NO-WARN":
            if comId not in AS.no_warnings["comlist"]:
                AS.no_warnings["comlist"].append(comId)
                msg = "El bot ya no enviará reportes en esta comunidad"
                with open("src/json/no_warn.json", "w+") as fp:
                    json.dump(AS.no_warnings, fp, indent=4)
            else:
                msg = "El bot actualmente no envía reportes en esta comunidad"

        elif com[1] == "-WALL"   :
            if comId in AS.no_warnings["comlist"]:
                AS.no_warnings["comlist"].remove(comId)
                msg = "El bot enviará reportes en esta comunidad desde ahora"
                with open("src/json/no_warn.json", "w+") as fp:
                    json.dump(AS.no_warnings, fp, indent=4)
            else:
                msg = "El bot actualmente envía todos los reportes"
        
            if comId in AS.ignore_coms["comlist"]:
                AS.ignore_coms["comlist"].remove(comId)
                with open("src/json/ignore_coms.json", "w+") as fp:
                    json.dump(AS.ignore_coms, fp, indent=4)

        elif com[1] == "-IGNORE" :
            if comId not in AS.ignore_coms["comlist"]:
                AS.ignore_coms["comlist"].append(comId)
                msg = "El bot dejará el spam de comunidades en la lista negra de los reportes en esta comunidad"
                with open("src/json/ignore_coms.json", "w+") as fp:
                    json.dump(AS.ignore_coms, fp, indent=4)
            else:
                msg = "El bot actualmente no envía reportes por spam de comunidades externas en esta comunidad"

        elif com[1] == "-STRICT" :
            if comId not in AS.ban_no_warn["comlist"]:
                AS.ban_no_warn["comlist"].append(comId)
                msg = "El bot expulsará a todo quien registre como amenaza en esta comunidad"
                with open("src/json/strict_list.json", "w+") as fp:
                    json.dump(AS.ban_no_warn, fp, indent=4)
            else:
                msg = "El bot actualmente expulsa a toda amenaza en esta comunidad"
        elif com[1] == "-NORMAL" :
            if comId in AS.ban_no_warn["comlist"]:
                AS.ban_no_warn["comlist"].remove(comId)
                msg = "El bot ya no expulsará a todo quien registre como amenaza en esta comunidad"
                with open("src/json/strict_list.json", "w+") as fp:
                    json.dump(AS.ban_no_warn, fp, indent=4)
            else:
                msg = "El bot actualmente no expulsa a toda amenaza en esta comunidad"

        print(AS.ban_no_warn)
        print(AS.ignore_coms)
        print(AS.no_warnings)
        return msg

    async def check_wall(ctx):
        uid = None

        if ctx.msg.extensions.mentionedArray:             uid = ctx.msg.extensions.mentionedArray[0].uid
        elif ctx.msg.extensions.replyMessage:             uid = ctx.msg.extensions.replyMessage.author.uid
        else:                                             uid = ctx.msg.author.uid

        user = await ctx.client.get_user_info(uid)

        print("uid:", uid)
        print("item.count:", user.commentsCount)
        
        sus_users = []
        for a in range( int(user.commentsCount / 100) + 1):
            c = await AS.get_wall_comments(ctx, user_id=uid, sorting="newest", start=(a*100), size=((a+1)*100))
            for b,i in enumerate(c):
                print(a*100+b, i.content)
                
                for j in AS.banned_nicks:
                    if ((j in i.author.nickname) & (i.author.uid not in sus_users)): sus_users.append(i.author.uid) 
                for j in AS.sexual_nicks:
                    if ((j in i.author.nickname) & (i.author.uid not in sus_users)): sus_users.append(i.author.uid) 

                if i.content.upper().find("T.ME") != -1                  : 
                    if i.author.uid not in sus_users: sus_users.append(i.author.uid)
                if i.content.upper().find("AMINOAPPS.COM/C/") != -1      : 
                    if i.author.uid not in sus_users: sus_users.append(i.author.uid)
                if i.content.upper().find("AMINOAPPS.COM/INVITE/") != -1 : 
                    if i.author.uid not in sus_users: sus_users.append(i.author.uid)
                if i.content.upper().find("T.CO") != -1                  : 
                    if i.author.uid not in sus_users: sus_users.append(i.author.uid)
                if i.content.upper().find("{}") != -1:
                    if i.author.uid not in sus_users: sus_users.append(i.author.uid)
        print(sus_users)
        for i in sus_users:
            u = await ctx.client.get_user_info(i)
            await ctx.send(f"""
Usuario: {u.nickname}
ID: {i}""")

        return f"""
Posee {user.commentsCount} comentarios
De los cuales hay {len(sus_users)} comentarios sus.
"""

    async def get_wall_comments(ctx, user_id=None, sorting="oldest", start=0, size=25):
        if sorting not in ["oldest", "newest"]: return None
        response = await ctx.client.request('GET', f"user-profile/{user_id}/comment?sort={sorting}&start={start}&size={size}")
        return tuple(map(lambda comment : WallComment(**comment), response['commentList'] ))
