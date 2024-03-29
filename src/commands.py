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
from src import network
from src import challenges
from src import pet
from src.text import text
from src.special import TA, LA, PA
from . import database
import sys

def login():
    bot = Bot(email=sys.argv[1], password=sys.argv[2], prefix="")
    print("Session logged in!")
    sys.argv = (sys.argv[0])
    return bot

async def message(ctx: Context):
        #print(ctx.msg.content)
        reply = objects.Reply(None, False)
        msg = ctx.msg.content;
        com = msg.upper() if msg is not None else None
        nick = ctx.msg.author.nickname if ctx.msg.author is not None else None
        objects.botStats.register(2)

        await antispam.messageRegister(ctx)
        await antispam.checkIfNewChat(ctx)
        await antispam.detectAll(ctx)
        await utils.waitForCallback(ctx)

        if msg is not None:
            com = ctx.msg.content.upper()
            if      com.find("--CONFIG") == 0: await config.config(ctx)
            elif    com.find("--LOG") == 0:    await config.logConfig(ctx)

        message_event = await config.get(ctx)
        if   message_event == objects.MessageEvents.FORBIDDEN   : return None
        elif message_event == objects.MessageEvents.MEMBER_JOIN : return await subcommands.enter(ctx)
        elif message_event == objects.MessageEvents.MEMBER_LEAVE: return await subcommands.leave(ctx)

        if ctx.msg.mediaValue == "http://st1.aminoapps.com/8721/53476d74d00175fbc0b9df5593f50b133d303cbfr6-256-256_00.jpeg": await PA.results(ctx)

        if msg is None: return None;

        if objects.status.wordle.check_user(ctx.msg.author.uid):   reply = await subcommands.wordle(ctx, msg)
        elif com.find("--SETLOG") == 0 :                                            reply.msg = await antispam.set_logging(ctx)
        elif com.find("-SI") == 0:                                                  await utils.registerConfirmation(ctx, True)
        elif com.find("-NO") == 0:                                                  await utils.registerConfirmation(ctx, False)
        elif com.find("--BAN") == 0:                                                await antispam.ban_user(ctx)
        elif com.find("--UNBAN") == 0:                                              await antispam.unban_user(ctx)
        elif com.find("--WARN") == 0:                                               await antispam.warn_user(ctx)
        elif com.find("--STRIKE") == 0:                                             await antispam.strike_user(ctx)
        elif com.find("--ACTIVOSSEMANALE") == 0:                                    await admin.getLeaderboard(ctx)
        elif com.find("--CHECK") == 0:                                              reply.msg = await antispam.check_wall(ctx)
        elif com.find("--TEST2") == 0:                                              reply.msg = "Aqui estoy"
        elif com.find("@STAFF") == 0:                                               reply.msg = await subcommands.staff(ctx)
        elif com.find("--DADOS") == 0:                                              reply     = await subcommands.dices(ctx, msg)
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
        elif com.find("--INVITAR") == 0:                                            await admin.inviteEveryone(ctx)
        elif com.find("--CUTESALL") == 0:                                           await images.cutes_sendall(ctx)

        elif message_event != objects.MessageEvents.NO_FUN: 

            if   com.find("NATI")   == 0:                                               reply.msg = "¿Me llamaban? Utiliza --help para ver mis comandos, uwu."
            elif com.find("ARTEMIS") == 0:                                              reply.msg = "¿Me llamaban? Utiliza --help para ver mis comandos, uwu."
            elif com.find("EMMA") == 0 and ctx.msg.ndcId == 215907772:                  reply.msg = "¿Me llamaban? Utiliza --help para ver mis comandos, uwu."
            elif com.find("ANYA") == 0 and ctx.msg.ndcId == 139175768:                  reply.msg = "¿Me llamaban? Utiliza --help para ver mis comandos, uwu."
            elif com.find("--TESTWELCOME") == 0:                                        await subcommands.enter(ctx)
            elif com.find("--PUNTOS") == 0:                                             await shop.walletCard(ctx)
            elif com.find("--SOYTUNEKITA") == 0:                                        await subcommands.ayudaPsicologica(ctx)
            elif com.find("--ADVERTENCIA") == 0:                                        await antispam.warningInfo(ctx)

            elif com.find("--COPIARBLOG") == 0:                                         await subcommands.copyPost(ctx)
            elif com.find("--UNIRVC") == 0:                                             await subcommands.joinVC(ctx)
            elif com.find("--UNIRSALA") == 0:                                           await subcommands.joinSR(ctx)

            elif com.find("--STICKERS") == 0:                                           await subcommands.getStickerPacksInfo(ctx)
            elif com.find("--MONEDERO-HISTORIAL") == 0:                                 await shop.get_wallet_history(ctx, start=0, size=100)
            elif com.find("--NOTIFICACIONES") == 0:                                     await shop.get_notifications(ctx, start=0, size=100)
            elif com.find("--MIS-ULTIMAS-DONACIONES") == 0:                             await shop.myLastDonations(ctx)
            elif com.find("--NOTAS") == 0:                                              await subcommands.notes(ctx)
            elif com.find("--GATO") == 0:                                               await subcommands.tiktaktoe(ctx)

            elif com.find("--INVENTARIO") == 0:                                         await shop.inventory(ctx)
            #elif com.find("--AÑADIRITEM") == 0:                                         await shop.add_item(ctx, 'ADD', use_text=True)
            #elif com.find("--QUITARITEM") == 0:                                         await shop.add_item(ctx, 'DEL', use_text=True)
            #elif com.find("--RANDOMITEM") == 0:                                         await shop.giveRandomItem(ctx)
            elif com.find("--VACIARINVENTARIO") == 0:                                   await shop.clearInventory(ctx)

            elif com.find("--MENSAJES-HISTORIAL") == 0:                                 await subcommands.messageHistory1(ctx)
            elif com.find("--MENSAJES-BORRADOS-CHAT") == 0:                             await subcommands.messageHistory3(ctx)
            elif com.find("--MENSAJES-BORRADOS") == 0:                                 await subcommands.messageHistory2(ctx)

            elif com.find("--TEST-DONATION") == 0:                                      await shop.testDonation(ctx)
            elif com.find("--RECLAMAR-RECOMPENSA") == 0:                                await challenges.claimRewards(ctx)
            elif com.find("--PROBAR-CAJAS") == 0:                                       await pet.testBox(ctx)
            elif com.find("--EXP") == 0:                                                await images.expCardCreate(ctx, message=False)

            elif com.find("--VER-YINCANA") == 0:                                        await challenges.getChallenges(ctx)
            elif com.find("--ENTREGAR-YINCANA") == 0:                                   await challenges.validate(ctx)
            elif com.find("--RANKING-YINCANA") == 0:                                    await challenges.getYincanaRanking(ctx)
            elif com.find("--AVANZAR-YINCANA") == 0:                                    await challenges.advanceLevel(ctx)
            elif com.find("--RETROCEDER-YINCANA") == 0:                                 await challenges.rewindLevel(ctx)
            elif com.find("--NIVEL-YINCANA") == 0:                                      await challenges.setLevel(ctx)
            elif com.find("--YINCANA") == 0:                                            await challenges.giveHelpYincana(ctx)
            elif com.find("--RETOS-YINCANA") == 0:                                      await challenges.giveAllChallenges(ctx)

            elif com.find("--CREARRPITEM") == 0:                                        await subcommands.createRPItem(ctx)
            elif com.find("--RPITEMS") == 0:                                            await subcommands.retrieveRPItems(ctx)
            elif com.find("--EDITARRPITEM") == 0:                                       await subcommands.editRPItem(ctx)
            elif com.find("--REMOVERRPITEM") == 0:                                      await subcommands.removeRPItem(ctx)
            elif com.find("--RPINVENTARIO") == 0:                                       await subcommands.RPInventory(ctx)
            elif com.find("--RPAÑADIRITEM") == 0:                                       await subcommands.addRPItem(ctx)
            elif com.find("--RPQUITARITEM") == 0:                                       await subcommands.delRPItem(ctx)
            elif com.find("--RPEDITARNOTA") == 0:                                       await subcommands.editRPnote(ctx)
            elif com.find("--RPVERNOTA") == 0:                                       await subcommands.viewRPnote(ctx)

            elif com.find("--MASCOTA") == 0:                                            await pet.info(ctx)
            elif com.find("--NUEVA-MASCOTA") == 0:                                      await pet.initPet(ctx)
            elif com.find("--DAR-ITEM") == 0:                                           await pet.giveItem(ctx)
            elif com.find("--USAR-ITEM") == 0:                                          await pet.useItem(ctx)

            elif com.find("--FLAGS-HELP") == 0:                                         await admin.flagsHelp(ctx)
            elif com.find("--FLAGS") == 0:                                              await admin.getMyGlobalFlags(ctx)
            elif com.find("--SETFLAG") == 0:                                            await admin.setFlag(ctx)

            elif com.find("--CONTACTAR") == 0:                                          await subcommands.contactUser(ctx)
            elif com.find("--CONFESIONES") == 0:                                        await subcommands.confessionList(ctx)
            elif com.find("--CONFESI") == 0:                                            await subcommands.addConfession(ctx)

            elif com.find("--SOLICITUD-INGRESO") == 0:                                  await admin.joinRequest(ctx)
            elif com.find("--LISTA-NEGRA-COMUNIDAD") == 0:                              await admin.communityBlacklist(ctx)
            elif com.find("--REGISTRAR-BLOG-TEMA") == 0:                                await admin.registerBlogSubscription(ctx)
            elif com.find("--REPOSITORIO-TEMA") == 0:                                   await admin.getTopicSubscriptionRepository(ctx)

            elif com.find("--TABLA-EXPERIENCIA") == 0:                                  await challenges.getCommunityRank(ctx)
            elif com.find("--TABLA-GLOBAL-EXPERIENCIA") == 0:                           await challenges.getGlobalRank(ctx)
            elif com.find("--MODERACIONES") == 0:                                       await admin.moderations(ctx, mtype="NATI")
            elif com.find("--VALORES-PROPIOS") == 0:                                    await subcommands.imageEigenvalues(ctx)
            elif com.find("--LINK-INFO") == 0:                                          await subcommands.sendLinkInfo(ctx)
            elif com.find("--HISTORIAL") == 0:                                          await admin.get_history(ctx)
            elif com.find("--VERLIKES")  == 0:                                          await challenges.get_likes_from_link(ctx)
            elif com.find("--SUSCRIBIR") == 0:                                          await admin.subscribe(ctx)
            elif com.find("--DESUSCRIBIR") == 0:                                        await admin.desubscribe(ctx)
            elif com.find("--SUGERIR-TEMA") == 0:                                       await admin.sugest(ctx)
            elif com.find("--TEMAS-SUSCRITOS") == 0:                                    await admin.topicsSubscipted(ctx)
            elif com.find("--PUBLICAR-MASIVO") == 0:                                    await admin.publishMassive(ctx)
            elif com.find("--PUBLICAR-RESUMEN") == 0:                                    await admin.publishResume(ctx)
            elif com.find("--PREPARAR-RESUMEN") == 0:                                    await admin.prepareResume(ctx)
            elif com.find("--COMUNIDADES-SUSCRITAS") == 0:                              await admin.topicCommunityList(ctx)
            elif com.find("--UPTIME") == 0:                                             await admin.uptime(ctx)

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
            elif com.find("--USUARIOSACTIVOS") == 0:                                    await subcommands.userActivity.activeUsers(ctx)
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
            elif com.find("--ISINSTANCE") == 0:                                         await communication.is_instance_in(ctx)
            elif com.find("--REMOTECHAT") == 0:                                         await communication.rc.handler(ctx)
            elif com.find("--WORDLE") == 0:                                             reply     = await subcommands.wordle(ctx, com)
            elif ((com.find("--SIGUEME") == 0) | (com.find("--SÍGUEME") == 0)) :        reply     = await subcommands.follow(ctx)
            elif com.find("--COMPLETAR") == 0:                                          reply.msg = await subcommands.web_tools.generateText(ctx)
            elif com.find("--BIBLIA") == 0:                                             reply.msg = await subcommands.web_tools.bible(ctx)
            elif ((com.find("--HOROSCOPO")==0)|(com.find("--HORÓSCOPO")==0)):           reply.msg = await subcommands.web_tools.horoscopo(ctx)
            elif com.find("--LETRA") == 0                                   :           reply.msg = await subcommands.web_tools.lyrics(ctx, msg)
            elif com.find("--DEF") == 0:                                                reply.msg = await subcommands.web_tools.definition(ctx, msg)
            elif com.find("--WIKI") == 0:                                               reply.msg = await subcommands.web_tools.wiki(ctx)
            elif com.find("--NEWS") == 0:                                               await images.getNews(ctx)
            elif com.find("--MATRIX") == 0:                                             reply.msg = await subcommands._math.matrix(ctx, com)
            elif com.find("--ALIAS") == 0:                                              reply.msg = await subcommands.alias(ctx, msg)
            elif com.find("--GHOST") == 0:                                              reply.msg = await subcommands.ghost(ctx, msg)
            elif com.find("--CUTES") == 0:                                              await images.cutes(ctx)
            elif com.find("--MATAR") == 0:                                              await images.interaction(ctx, 'MATAR')
            elif com.find("--GOLPEAR") == 0:                                             await images.interaction(ctx, 'GOLPEAR')
            elif com.find("--GRAPH") == 0:                                              await images.plot(ctx)
            #elif com.find("--COPYPASTE") == 0:                                         reply     = await commands.copypaste(ctx, msg)
            elif com.find("--JOIN") == 0:                                               reply.msg     = await subcommands.joinChat(ctx)
            elif com.find("@EVERYONE") == 0:                                            reply     = await subcommands.everyone(ctx)
            elif com.find("--MATH") == 0:                                               reply.msg = await subcommands._math.mathfc(ctx, com)
            elif com.find("--BLOGS") == 0:                                              reply     = await subcommands.getBlogs(ctx, com)
            elif com.find("--INFO") == 0 :                                              await subcommands.userInfo(ctx)
            elif com.find("PLEBEYOS") == 0 :                                            reply.msg = f"{text['plebeyos']} {nick}"
            elif com.find("LA NAVE") == 0 :                                             reply.msg = text['la_nave']
            elif com == "--NOMBRE":                                                     reply.msg = f"[c]Tu nombre es:\n\n[c]{nick}";
            elif ((msg.find("--say") < 5) & (msg.find("--say") != -1)) :                reply.msg = msg[6:]
            elif ((com.find("KIWILATIGO") != -1) | (com.find("KIWILÁTIGO") != -1)):     reply     = await subcommands.kiwilatigo(ctx)
            elif com.find("--NORMAS") == 0  :                                           reply.msg = text['normas']
            elif com.find("--SOPORTE") == 0  :                                          await subcommands.aminoSupportForm(ctx)
            elif com.find("--CENTRO") == 0  :                                           reply.msg = "support.aminoapps.com/hc/es-419?from_aminoapp=1"
            elif com.find("--AYUDA") == 0  :                                            reply.msg = "https://leafylemontree.github.io/lider-amino/resume.html"
            elif msg.find("--Mensaje Oculto") == 0 :                                    reply.msg = text['msg_oculto']
            elif msg.find("👀") != -1:                                                  reply     = await subcommands.replyMsg(ctx, text['ojos'])
            elif msg.find("Toy Chica") != -1 :                                          reply     = await subcommands.replyMsg(ctx, text['toy_chica'])
            elif com.find("HOLA NATI") != -1 :                                          reply     = await subcommands.replyMsg(ctx, f"{text['hola']} {nick}.")
            elif com.find("UWU") != -1 :                                                reply     = await subcommands.replyMsg(ctx, text['uwu'])
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
            elif com.find("RESULTADOS") != -1 and ctx.msg.ndcId == 92:                  await PA.results(ctx)
            elif com.find("--TABLA-R-PALABRA") == 0 and ctx.msg.ndcId == 92:            await PA.resultTable(ctx)
            elif com.find("--REGISTRARHEXATLON") == 0 and ctx.msg.ndcId == 92:            await PA.registerHexatlon(ctx)
            elif com.find("--TABLA-HEXATLON") == 0 and ctx.msg.ndcId == 92:            await PA.hexatlonTable(ctx)
            elif com.find("--XKCD") != -1:                                              await subcommands.web_tools.xkcd(ctx)
            elif com.find("--PALETA") == 0:                                             await subcommands.imagePalette(ctx)
        
        if     reply is None                                             : return None
        elif ((reply.msg is not None) & (reply.reply is True))           : await ctx.reply(reply.msg)
        elif ((reply.msg is not None) & (reply.reply is False))          : await ctx.send(reply.msg)

        return None;
