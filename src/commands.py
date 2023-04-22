import json
from edamino import Bot, Context, logger, Client
from src import objects
from src import antispam
from src import config
from src import subcommands
from src import admin
from src import images
from src import games
from src import subprocess
from src import utils
from src import shop
from src import communication
from src.text import text
from src.special import TA, LA
from . import database
import sys

def login():
    bot = Bot(email=sys.argv[1], password=sys.argv[2], prefix="")
    print("Session logged in!")
    sys.argv = (sys.argv[0])
    return bot

async def message(ctx: Context):
        reply = objects.Reply(None, False)
        img   = None
        msg = ctx.msg.content;

        objects.botStats.register(2)
        await antispam.messageRegister(ctx)

        if ctx.msg.content is not None:  await utils.waitForCallback(ctx)
        response = await antispam.detectAll(ctx)
        #if response: return
        if msg is not None:
            com = ctx.msg.content.upper()
            if      com.find("--CONFIG") == 0: await config.config(ctx)
            elif    com.find("--LOG") == 0:    await config.logConfig(ctx)

        if ctx.msg.author: userDB = database.db.getUserData(ctx.msg.author)

        d = await config.get(ctx)
        if   d == -1: return None
        elif d ==  1: return await subcommands.enter(ctx)
        elif d ==  2: return await subcommands.leave(ctx)
        if msg is None: return None;
	
        com = msg.upper()
        nick = ""
        if ctx.msg.author:   nick = ctx.msg.author.nickname

        if   com.find("--SETLOG") == 0 :                                            reply.msg = await antispam.set_logging(ctx)
        elif com.find("-SI") == 0:                                                  await utils.registerConfirmation(ctx, True)
        elif com.find("-NO") == 0:                                                  await utils.registerConfirmation(ctx, False)
        elif com.find("--BAN") == 0:                                                await antispam.ban_user(ctx)
        elif com.find("--UNBAN") == 0:                                              await antispam.unban_user(ctx)
        elif com.find("--WARN") == 0:                                               await antispam.warn_user(ctx)
        elif com.find("--STRIKE") == 0:                                             await antispam.strike_user(ctx)
        elif com.find("--RANK") == 0:                                               await admin.getLeaderboard(ctx)
        elif com.find("--CHECK") == 0:                                              reply.msg = await antispam.check_wall(ctx)
        elif com.find("--TEST2") == 0:                                              reply.msg = "Aqui estoy"
        elif com.find("@STAFF") == 0:                                               reply.msg = await subcommands.staff(ctx)
        elif com.find("--DADOS") == 0:                                              reply     = subcommands.dices(msg)
        elif com.find("--SENDALL") == 0:                                            await antispam.send_all(ctx)
        elif com.find("--ADMIN") == 0:                                              await admin.nati(ctx)
        elif com.find("--DEEPANALYZE") == 0:                                        await antispam.deepAnalyze.run(ctx)
        elif com.find("--CHATANALYZE") == 0:                                        await antispam.chatAnalyze(ctx)
        elif com.find("--LISTATA_CA") == 0:                                         await TA.run(ctx)
        elif com.find("--REPORTES") == 0:                                           await images.botstats2(ctx)
        elif com.find("--BOTINFO") == 0:                                            await images.stats(ctx)
        elif com.find("--JOINPUBLICCHATS") == 0:                                    await admin.joinChats(ctx)
        elif com.find("--DELETEMSG") == 0:                                          await antispam.del_(ctx)
        elif com.find("--INSTANCE") == 0:                                           await admin.instance(ctx)
        elif com.find("--ACEPTARROL") == 0:                                         await admin.accept_role(ctx)
        elif com.find("--PURGA") == 0:                                              await admin.remove(ctx)
        elif com.find("--GOTOCOMMUNITY") == 0:                                      await admin.newCommunity(ctx)
        elif com.find("--QUITCOMMUNITY") == 0:                                      await admin.removeCommunity(ctx)
        elif com.find("--COMMUNITYANALYZE") == 0:                                   await antispam.communityanalyze(ctx)
        elif com.find("--CREARBLOG") == 0:                                          await admin.createBlog(ctx)
        elif com.find("--ELIMINARCOMENTARIOS") == 0:                                await admin.deleteComments(ctx)
        elif com.find("--NOTICE") == 0:                                             await admin.giveNotice(ctx)
        elif com.find("--CUTESALL") == 0:                                           await images.cutes_sendall(ctx)
        elif d != 100: 
            if   com.find("NATI")   == 0:                                               reply.msg = "¿Me llamaban? Utiliza --help para ver mis comandos, uwu."
            elif com.find("ARTEMIS") == 0:                                              reply.msg = "¿Me llamaban? Utiliza --help para ver mis comandos, uwu."
            elif com.find("EMMA") == 0 and ctx.msg.ndcId == 215907772:                  reply.msg = "¿Me llamaban? Utiliza --help para ver mis comandos, uwu."
            elif com.find("ANYA") == 0 and ctx.msg.ndcId == 139175768:                  reply.msg = "¿Me llamaban? Utiliza --help para ver mis comandos, uwu."
            elif com.find("--TESTWELCOME") == 0:                                        await subcommands.enter(ctx)
            elif com.find("--FORMAT") == 0:                                             await subcommands.fmt(ctx)
            elif com.find("--HELP") == 0:                                               await subcommands._help(ctx)
            elif com.find("--INTERACCI") == 0:                                          await subcommands._help(ctx, hType="INTERACCION")
            elif com.find("--IMAGENES") == 0 or com.find("--IMÁGENES") == 0:            await subcommands._help(ctx, hType="IMAGENES")
            elif com.find("--MATES") == 0:                                              await subcommands._help(ctx, hType="MATEMATICAS")
            elif com.find("--JUEGOS") == 0:                                             await subcommands._help(ctx, hType="JUEGOS")
            elif com.find("--STAFF") == 0:                                              await subcommands._help(ctx, hType="MODERACION")
            elif com.find("--ENVIARTODOS") == 0:                                        await admin.sendEveryone(ctx)
            elif com.find("--ANIMALES") == 0:                                           await images.animals(ctx)
            elif com.find("--SEX") == 0:                                                reply.msg = text['sex']
            elif com.find("--RATE") == 0:                                               await subcommands.rateBlog(ctx)
            elif com.find("--CRONÓMETRO") == 0:                                         await subcommands.stopwatch(ctx)
            elif com.find("--TEMPORIZADOR") == 0:                                       await subcommands.timer(ctx)
            elif com.find("--DOWNLOAD") == 0:                                           await subcommands.videoDownload(ctx)
            elif com.find("--TRIVIA") == 0:                                             await subcommands.trivia(ctx)
            elif com.find("--ESCUCHAR") == 0:                                           await subcommands.audioRecognize(ctx)
            elif com.find("--CHOCOLATE") == 0:                                          await subcommands.giveChocolate(ctx)
            elif com.find("--MATRIMONIO") == 0:                                         await subcommands.askMarry(ctx)
            elif com.find("--OFRECERSTAFF") == 0:                                       await LA.ofrecer(ctx)
            elif com.find("--BUSCARSTAFF") == 0:                                        await LA.buscar(ctx)
            elif com.find("--OFRECERPUBLICAR") == 0:                                    await LA.publish_ofrecer(ctx)
            elif com.find("--BUSCARPUBLICAR") == 0:                                     await LA.publish_buscar(ctx)
            elif com.find("--MEDIAVALUE") == 0:                                         await subcommands.mediaValue(ctx)
            elif com.find("--FROMSTICKER") == 0:                                        await subcommands.fromSticker(ctx)
            elif com.find("--BLOGINFO") == 0:                                           await subcommands.blogInfo(ctx)
            elif com.find("--NANO") == 0 :                                              reply.msg = text['nano']
            elif com.find("--CARD1") == 0:                                              await images.card(ctx)
            elif com.find("--CRAIYON") == 0:                                            await images.craiyon(ctx)
            elif com.find("--TIENDA") == 0:                                             await shop.shop(ctx)
            elif com.find("--TTS") == 0:                                                await subcommands.tts(ctx)
            elif com.find("--SALA") == 0:                                               await games.main(ctx)
            elif com.find("-J") == 0:                                                   await games.turn(ctx)
            elif com.find("--SOCKETSEND") == 0:                                         await communication.send(ctx)
            elif com.find("--SOCKETCOM") == 0:                                          await communication.get_communities(ctx)
            elif com.find("--SOCKETWALLET") == 0:                                       await communication.get_wallets(ctx)
            elif com.find("--SOCKETACTIVITY") == 0:                                     await communication.get_activity(ctx)
            elif com.find("--WORDLE") == 0:                                             reply     = await commands.wordle(ctx, com)
            elif ((com.find("--SIGUEME") == 0) | (com.find("--SÍGUEME") == 0)) :        reply     = await subcommands.follow(ctx)
            elif com.find("--COMPLETAR") == 0:                                          reply.msg = await subcommands.web_tools.generateText(ctx)
            elif com.find("--BIBLIA") == 0:                                             reply.msg = await subcommands.web_tools.bible(ctx)
            elif ((com.find("--HOROSCOPO")==0)|(com.find("--HORÓSCOPO")==0)):           reply.msg = await subcommands.web_tools.horoscopo(ctx)
            elif com.find("--LETRA") == 0                                   :           reply.msg = subcommands.web_tools.lyrics(msg)
            elif com.find("--DEF") == 0:                                                reply.msg = subcommands.web_tools.definition(msg)
            elif com.find("--WIKI") == 0:                                               reply.msg = await subcommands.web_tools.wiki(ctx)
            elif com.find("--NEWS") == 0:                                               await images.getNews(ctx)
            elif com.find("--MATRIX") == 0:                                             reply.msg = subcommands._math.matrix(com)
            elif com.find("--ALIAS") == 0:                                              reply.msg = await subcommands.alias(ctx, msg)
            elif com.find("--GHOST") == 0:                                              reply.msg = await subcommands.ghost(ctx, msg)
            elif com.find("--CUTES") == 0:                                              await images.cutes(ctx)
            elif com.find("--MATAR") == 0:                                              await images.interaction(ctx, 'MATAR')
            elif com.find("--GOLPEAR") == 0:                                              await images.interaction(ctx, 'GOLPEAR')
            elif com.find("--GRAPH") == 0:                                              await images.plot(ctx)
            #elif com.find("--COPYPASTE") == 0:                                         reply     = await commands.copypaste(ctx, msg)
            elif com.find("--JOIN") == 0:                                               reply.msg     = await subcommands.joinChat(ctx)
            elif com.find("@EVERYONE") == 0:                                            reply     = await subcommands.everyone(ctx)
            elif com.find("--MATH") == 0:                                               reply.msg = subcommands._math.mathfc(com)
            elif com.find("--BLOGS") == 0:                                              reply     = await subcommands.getBlogs(ctx, com)
            elif com.find("--INFO") == 0 :                                              await subcommands.userInfo(ctx)
            elif com.find("PLEBEYOS") == 0 :                                            reply.msg = f"{text['plebeyos']} {nick}"
            elif com.find("LA NAVE") == 0 :                                             reply.msg = text['la_nave']
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
            elif com.find("--ABSTRACT") == 0:                                           await images.abstractImage(ctx)
            elif com.find("--VIEW") == 0:                                               reply.msg = await antispam.view(ctx)
            elif com.find("--CUSTOMMSG") == 0:                                          await subcommands.customMsg(ctx)
            elif com.find("--ARTICLE") == 0:                                            await images.wiki(ctx) 
            elif com.find("--TWEET") == 0:                                              await images.tweet(ctx)
            elif com.find("--LINEART") == 0:                                            await images.lineart(ctx)
            elif com.find("--IMGMATRIX") == 0:                                          await subcommands._math.imgMatrix(ctx)
            elif com.find("--COUNTDOWN") == 0:                                          await subprocess.timer.main(ctx)
            elif com.find("--PAPULINCE") == 0:                                          await subcommands.papulince(ctx)
            elif com.find("Y LOS RESULTADOS?") != -1:                                   reply.msg = "Y los blogs?"
            elif com.find("--XKCD") != -1:                                              await subcommands.web_tools.xfcd(ctx)
        
        #print(ctx.msg.content, ctx.msg.author.nickname)

        if   ((reply.msg is not None) & (reply.reply is True))           : await ctx.reply(reply.msg)
        elif ((reply.msg is not None) & (reply.reply is False))          : await ctx.send(reply.msg)

        return None;
