import json
from edamino import Bot, Context, logger, Client
from src import objects
from src import antispam
from src import config
from src import subcommands
from src import admin
from src import images
from src import games
from src.text import text

def login():
    with open("data/login.json", "r") as loginFile:
        loginData = json.load(loginFile)
    bot = Bot(email=loginData['username'], password=loginData['password'], prefix=loginData['prefix'])
    print("Session logged in!")
    return bot

async def message(ctx: Context):
        reply = objects.Reply(None, False)
        img   = None
        msg = ctx.msg.content;

        objects.botStats.register(2)
        
        response = await antispam.detectAll(ctx)
        if response: return
        if msg is not None:
            if ctx.msg.content.upper().find("--CONFIG") == 0: await config.config(ctx)
        d = await config.get(ctx)
        if   d == -1: return None
        elif d ==  1: return await subcommands.enter(ctx)
        elif d ==  2: return await subcommands.leave(ctx)
        if msg is None: return None;

        com = msg.upper()
        nick = ""
        if ctx.msg.author:   nick = ctx.msg.author.nickname

        if   com.find("--SETLOG") == 0 :                                            reply.msg = await antispam.set_logging(ctx)
        elif com.find("--BAN") == 0:                                                reply.msg = await antispam.ban_user(ctx)
        elif com.find("--UNBAN") == 0:                                              reply.msg = await antispam.unban_user(ctx)
        elif com.find("--CHECK") == 0:                                              reply.msg = await antispam.check_wall(ctx)
        elif com.find("--TEST2") == 0:                                              reply.msg = "Aqui estoy"
        elif com.find("@STAFF") == 0:                                               reply.msg = await subcommands.staff(ctx)
        elif com.find("--DADOS") == 0:                                              reply     = subcommands.dices(msg)
        elif com.find("--SENDALL") == 0:                                            await antispam.send_all(ctx)
        elif com.find("--ADMIN") == 0:                                              await admin.nati(ctx)
        elif d != 100: 
            if   com.find("NATI")   == 0:                                               reply.msg = "¿Me llamaban? Utiliza --help para ver mis comandos, uwu."
            elif com.find("ARTEMIS") == 0:                                              reply.msg = "¿Me llamaban? Utiliza --help para ver mis comandos, uwu."
            elif com.find("EMMA") == 0 and ctx.msg.ndcId == 215907772:                  reply.msg = "¿Me llamaban? Utiliza --help para ver mis comandos, uwu."
            elif com.find("ANYA") == 0 and ctx.msg.ndcId == 139175768:                  reply.msg = "¿Me llamaban? Utiliza --help para ver mis comandos, uwu."
            elif com.find("--NANO") == 0 :                                              reply.msg = text['nano']
            elif com.find("--JUEGOS") == 0:                                             await games.main(ctx)
            elif com.find("-J") == 0:                                                   await games.turn(ctx)
            elif com.find("--WORDLE") == 0:                                           reply     = await commands.wordle(ctx, com)
            elif ((com.find("--SIGUEME") == 0) | (com.find("--SÍGUEME") == 0)) :        reply     = await subcommands.follow(ctx)
            elif com.find("--COMPLETAR") == 0:                                          reply.msg = await subcommands.web_tools.generateText(ctx)
            elif com.find("--BIBLIA") == 0:                                             reply.msg = await subcommands.web_tools.bible(ctx)
            elif ((com.find("--HOROSCOPO")==0)|(com.find("--HORÓSCOPO")==0)):           reply.msg = await subcommands.web_tools.horoscopo(ctx)
            elif com.find("--LETRA") == 0                                   :           reply.msg = subcommands.web_tools.lyrics(msg)
            elif com.find("--DEF") == 0:                                                reply.msg = subcommands.web_tools.definition(msg)
            elif com.find("--WIKI") == 0:                                               reply.msg = await subcommands.web_tools.wiki(ctx)
            elif com.find("--MATRIX") == 0:                                             reply.msg = subcommands._math.matrix(com)
            elif com.find("--ALIAS") == 0:                                              reply.msg = await subcommands.alias(ctx, msg)
            elif com.find("--GHOST") == 0:                                              reply.msg = await subcommands.ghost(ctx, msg)
            elif com.find("--CUTES") == 0:                                              reply     = await images.cutes(ctx)
            #elif com.find("--COPYPASTE") == 0:                                         reply     = await commands.copypaste(ctx, msg)
            elif com.find("--JOIN") == 0:                                               reply.msg     = await subcommands.joinChat(ctx)
            elif com.find("@EVERYONE") == 0:                                            reply     = await subcommands.everyone(ctx)
            elif com.find("--MATH") == 0:                                               reply.msg = subcommands._math.mathfc(com)
            elif com.find("--BLOGS") == 0:                                              reply     = await subcommands.getBlogs(ctx, com)
            elif com.find("--INFO") == 0 :                                              await subcommands.userInfo(ctx)
            elif com.find("PLEBEYOS") == 0 :                                            reply.msg = f"{text['plebeyos']} {nick}"
            elif com.find("LA NAVE") == 0 :                                             reply.msg = text['la_nave']
            elif com.find("--HELP") == 0:                                               reply     = subcommands._help(msg, ctx.msg.ndcId)
            elif com == "--NOMBRE":                                                     reply.msg = f"[c]Tu nombre es:\n\n[c]{nick}";
            elif ((msg.find("--say") < 5) & (msg.find("--say") != -1)) :                reply.msg = msg[6:]
            elif ((com.find("KIWILATIGO") != -1) | (com.find("KIWILÁTIGO") != -1)):     reply     = subcommands.kiwilatigo(ctx)
            elif com.find("--NORMAS") == 0  :                                           reply.msg = text['normas']
            elif com.find("--SOPORTE") == 0  :                                          reply.msg = "support.aminoapps.com/hc/es-419/requests/new?from_aminoapp=1"
            elif com.find("--CENTRO") == 0  :                                           reply.msg = "support.aminoapps.com/hc/es-419?from_aminoapp=1"
            elif msg.find("--Mensaje Oculto") == 0 :                                    reply.msg = text['msg_oculto']
            elif msg.find("👀") != -1:                                                  reply     = subcommands.replyMsg(text['ojos'])
            elif msg.find("Toy Chica") != -1 :                                          reply     = subcommands.replyMsg(text['toy_chica'])
            elif com.find("HOLA NATI") != -1 :                                          reply     = subcommands.replyMsg(f"{text['hola']} {nick}.")
            elif com.find("UWU") != -1 :                                                reply     = subcommands.replyMsg(text['uwu'])
            elif com.find("--PLATYPUS") == 0:                                           reply.msg = text['platypus'][int(random() * 2)]
            elif com.find("--METH") == 0:                                               reply.msg = text['meth']
            elif com.find("--SUS") == 0:                                                reply.msg = await subcommands.sus(ctx)
            elif com.find("--DOXX") == 0:                                               reply     = await subcommands.doxx(ctx, 0)
            elif com.find("DOXXEA A") != -1:                                            reply     = await subcommands.doxx(ctx, 1)
            elif com.find("--THREADID") == 0:                                           reply.msg = ctx.msg.threadId
            elif com.find("--COMID") == 0:                                              reply.msg = str(ctx.msg.ndcId)
            elif com.find("--LOG") == 0:                                                reply.msg = await config.logConfig(ctx)
            elif com.find("--ABSTRACT") == 0:                                          await images.abstractImage(ctx)
            elif com.find("--VIEW") == 0:                                               reply.msg = await antispam.view(ctx)
            elif com.find("--CUSTOMMSG") == 0:                                          await subcommands.customMsg(ctx)
            elif com.find("--ARTICLE") == 0:                                            await images.wiki(ctx) 
            elif com.find("--STATS") == 0:                                              await images.stats(ctx)
            elif com.find("--TWEET") == 0:                                              await images.tweet(ctx)
            elif com.find("--LINEART") == 0:                                              await images.lineart(ctx)
            elif com.find("--IMGMATRIX") == 0:                                            await subcommands._math.imgMatrix(ctx)
            #elif subCommands.papulince(com):                                            reply = await subCommands.kick(ctx, msg_text['grasa'])
            elif com.find("Y LOS RESULTADOS?") != -1:                                   reply.msg = "Y los blogs?"
        
        print(ctx.msg.content, ctx.msg.author.nickname)

        if   ((reply.msg is not None) & (reply.reply is True))           : await ctx.reply(reply.msg)
        elif ((reply.msg is not None) & (reply.reply is False))          : await ctx.send(reply.msg)

        return None;
