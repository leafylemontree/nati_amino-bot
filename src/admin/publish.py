from src.subprocess.test    import  get_my_communities
from src.subcommands.copy   import  parseBlog, parseWiki, publishBlog, publishWiki, generateMediaList
from src.database           import  db
from src                    import  utils
from src.images.funcs       import  putText, rounded
from src.imageSend          import  send_image
from src.admin.leaderboard  import  get_leaderboard_info
from src.images.expCard     import  getLevel, getExp
from src                    import  objects
from aiofile                import  AIOFile
import cairocffi            as      cairo 
import matplotlib.pyplot    as      plt
import traceback
import asyncio
import io
import datetime
import traceback

async def prepareUpload(ctx, post, topic, com):
    ctx.client.set_ndc(com.ndcId)
    r = db.getCommunityTopic(com.ndcId, topic)
    if r is False and topic != "FORCE":
        print(f"Skipping {com.ndcId}")
        return

    print(f"Uploading in ndcId: {com.ndcId}")
    attempt = 0
    response = None

    post.mediaList = await generateMediaList(ctx, post.mediaList)
    await asyncio.sleep(3)

    while True:
        if attempt > 6: return
        try:
            url = ""
            if   post.type == 1:
                response = await publishBlog(ctx, post)
                url = f"ndc://x{com.ndcId}/blog/{response.blogId}"
            elif post.type == 2:
                response = await publishWiki(ctx, post)
                url = f"ndc://x{com.ndcId}/item/{response.itemId}"
            ctx.client.set_ndc(ctx.msg.ndcId)
            if isinstance(response, dict): raise Exception

            await ctx.send(f"Blog subido en {com.name}\n{url}")
            await asyncio.sleep(10)
            return
        except Exception as e:
            print("Errored!", com.ndcId, com.name)
            traceback.print_exc()
            print(response)
            
            if 'url' in response.keys():
                await ctx.send(f"Nati ha encontrado un error grave al subir. Verifica la cuenta en este enlace: {response['url']}")
                r = await utils.confirmation(ctx, ctx.msg.threadId, ctx.msg.author.uid, ctx.msg.ndcId, timeout=False)

            await asyncio.sleep(10)
            attempt += 1


@utils.isStaff
@utils.userTracker("publicar-masivo", isAdmin=True)
async def publishMassive(ctx):
    args = ctx.msg.content.split(" ")
    if len(args) < 3:   return await ctx.send("Debe añadir el tema y el enlace de un blog o una wiki tras el comando.")

    start = None
    if len(args) > 3:
        start = args[3]
        startLink    = await ctx.client.get_info_link(args[3])
        start = startLink.community.ndcId
        print(start)

    topic   = args[1]
    link    = await ctx.client.get_info_link(args[2])
    if link.linkInfo.objectType not in [1, 2]: return await ctx.send("El link que ingrese debe ser de una wiki.")

    objectId    = link.linkInfo.objectId
    objectType  = link.linkInfo.objectType
    postndcId   = link.linkInfo.ndcId

    if   objectType == 1:   post = await parseBlog(ctx, objectId, postndcId)
    elif objectType == 2:   post = await parseWiki(ctx, objectId, postndcId)

    print(topic, start, link, post)

    coms = await get_my_communities(ctx, start=0, size=100)
    keepGoing = False
    for c in coms:
        if start is not None and keepGoing is False:
            if c.ndcId == start :   keepGoing = True
            else                :   continue

        await prepareUpload(ctx, post, topic, c)
    ctx.client.set_ndc(ctx.msg.ndcId)
    await ctx.send("¡Subida completada!")


def imageBase(ct, name, scale=1, x=0, y=0, size=None):
    ct.move_to(x, y)
    base        = cairo.ImageSurface.create_from_png(name)
    px, py      = base.get_width(), base.get_height()

    if size is not None:
        scaleX = size / px
        scaleY = size / py
    else:
        scaleX = scale
        scaleY = scale

    ct.save()
    ct.translate(x, y)
    ct.scale(scaleX, scaleY)
    ct.set_source_surface(base)
    ct.paint()
    ct.restore()
    return

async def resumePage1(ctx, com):
    imgIO   = io.BytesIO()
    image   = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1024, 1152, )
    ct      = cairo.Context(image)
    imageBase(ct, "media/templates/resume/1.png")
    
    ct.set_source_rgba(0.153, 0.082, 0.376, 1)
    ct.move_to(48, 80)
    putText(ct, text=com.name, size=60, width=2000, height=60, align="LEFT", font="Heavitas")

    print(com)

    ct.move_to(288, 272)
    putText(ct, text=str(com.ndcId), size=30, width=208, height=48, align="RIGHT", font="Heavitas")
    ct.move_to(288, 356)
    putText(ct, text=str(com.membersCount), size=30, width=208, height=48, align="RIGHT", font="Heavitas")
    ct.move_to(288, 440)
    joinType = "Abierta" if com.joinType == 0 else "Apr. Re." if com.joinType == 1 else "Privada"
    putText(ct, text=joinType, size=30, width=208, height=48, align="RIGHT", font="Heavitas")
    ct.move_to(288, 524)
    putText(ct, text=com.primaryLanguage, size=30, width=208, height=48, align="RIGHT", font="Heavitas")

    icon = await utils.getImageBytes(ctx, url=com.icon)
    imageBase(ct, name=icon, x=576, y=224, size=12*32)
    
    leaders  = await ctx.client.get_all_users(users_type="leaders")
    curators = await ctx.client.get_all_users(users_type="curators")
    users    = []
    users.extend(list(leaders))
    users.extend(list(curators))

    for i,user in enumerate(users):
        x = 48  + (i // 5) * 512
        y = 720 + (i %  5) * 80
        ct.move_to(x, y)
        putText(ct, text=user.nickname, size=24, width=448, height=48, align="LEFT", font="MADE TOMMY")

    ct.stroke()
    out     = io.BytesIO()
    image.write_to_png(f"media/export/resume/{objects.ba.instance}/{com.ndcId}-1.png")
    #image.write_to_png(imgIO)
    #imgIO.seek(0)
    #img     = imgIO.read()
    #url     = await ctx.client.upload_media(data=img, content_type="img/png")
    return

async def resumePage2(ctx, com):
    imgIO   = io.BytesIO()
    image   = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1024, 1152, )
    ct      = cairo.Context(image)

    leaderboard = await get_leaderboard_info(ctx, rankingType=2)
    if leaderboard == []: return None
    leaderboard = list(filter(lambda x: x.uid != ctx.client.uid, list(leaderboard)))
    if leaderboard == []: return None
    print(leaderboard)
    if leaderboard != () or leaderboard is not None or leaderboard != []: 
        totalSent   = db.getMessagesSentCommunity(com.ndcId)
        top         = leaderboard[0]
        bottom      = leaderboard[1:5]
        if top.icon:
            try:
                pfp         = await utils.getImageBytes(ctx, top.icon)
                imageBase(ct, name=pfp, x=128, y=224, size=224)
            except:
                pass
        for i,u in enumerate(bottom):
            if u.icon is None: continue
            try:
                pfp         = await utils.getImageBytes(ctx, u.icon)
                imageBase(ct, name=pfp, x=32, y=512 + i*160, size=224)
            except:
                continue
        imageBase(ct, "media/templates/resume/2.png")
        ct.set_source_rgba(0.18, 0.047, 0.082, 1)
        ct.move_to(384, 208)
        putText(ct, text=top.nickname, size=28, width=12*32, height=48, align="LEFT", font="Heavitas")
        ct.move_to(888, 208)
        putText(ct, text=str(top.level), size=28, width=12*32, height=48, align="RIGHT", font="Heavitas")
        ct.set_source_rgba(0.91, 0.573, 0.671, 1)
        if top.uid is not None:
            userInfo = db.getUserData(top, userId=top.uid)
            ct.move_to(388, 266)
            putText(ct, text=userInfo.alias, size=14, width=12*32, height=48, align="LEFT", font="Heavitas")
        ct.move_to(416, 320)
        putText(ct, text=f"Minutos semanales: {(top.activeTime / 60):.2f} ", size=18, width=20*32, height=48, align="LEFT", font="Heavitas")
        ct.move_to(416, 352)
        messages = db.getMessagesSent(com.ndcId, top.uid)
        putText(ct, text=f"Mensajes enviados: {messages}", size=18, width=12*32, height=48, align="LEFT", font="Heavitas")
        ct.move_to(416, 384)
        putText(ct, text=f"Porcentaje: {((messages / totalSent) * 100):.2f}%", size=18, width=12*32, height=48, align="LEFT", font="Heavitas")
        userExp     = db.getUserExp(com.ndcId, top.uid) 
        level       = getLevel(userExp)
        expUp       = getExp(level + 1)
        expDown     = getExp(level)
        ct.move_to(408, 444)
        putText(ct, text=str(userExp), size=20, width=12*32, height=48, align="LEFT", font="Heavitas")
        ct.move_to(469, 443)
        ct.rectangle(469, 443, (1002 - 469) * ((userExp - expDown) / (expUp - expDown)), 462 - 443)
        ct.fill()
        ct.stroke()
        
        for i, u in enumerate(bottom):
            ct.set_source_rgba(0.18, 0.047, 0.082, 1)
            ct.move_to(164, 516 + 160 * i)
            putText(ct, text=u.nickname, size=14, width=200*32, height=48, align="LEFT", font="Heavitas")
            ct.set_source_rgba(0.91, 0.573, 0.671, 1)
            ct.move_to(260, 570 + 160 * i)
            messages = db.getMessagesSent(com.ndcId, u.uid)
            putText(ct, text=str(messages), size=18, width=12*32, height=48, align="LEFT", font="Heavitas")
            ct.move_to(480, 570 + 160 * i)
            putText(ct, text=f"{(u.activeTime / 60):.2f}", size=18, width=12*32, height=48, align="LEFT", font="Heavitas")
            ct.move_to(736, 570 + 160 * i)
            putText(ct, text=f"{((messages * 100)/ totalSent):.2f}%", size=18, width=12*32, height=48, align="LEFT", font="Heavitas")
            userExp = db.getUserExp(com.ndcId, u.uid)
            level       = getLevel(userExp)
            expUp       = getExp(level + 1)
            expDown     = getExp(level)
            ct.rectangle(258, 608 + 160*i, (829 - 256) * ((userExp - expDown) / (expUp - expDown)), 16)
            ct.fill()
            ct.stroke()
    else:
        imageBase(ct, "media/templates/resume/2.png")

    ct.stroke()
    out     = io.BytesIO()
    image.write_to_png(f"media/export/resume/{objects.ba.instance}/{com.ndcId}-2.png")
    #image.write_to_png(imgIO)
    #imgIO.seek(0)
    #img     = imgIO.read()
    #url     = await ctx.client.upload_media(data=img, content_type="img/png")
    return

async def resumePage3(ctx, com):
    imgIO   = io.BytesIO()
    image   = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1024, 1152, )
    ct      = cairo.Context(image)
    imageBase(ct, "media/templates/resume/3.png")
    
    chats   = db.getMessagesSentChatroom(com.ndcId)
    chatInfo = []
    for chat in chats:
        if len(chatInfo) > 4: break
        await asyncio.sleep(1)
        try:
            c = await ctx.client.get_chat_info(chat[0])
            if c.type != 2: continue
            chatInfo.append([c, chat[1]])
        except:
            continue

    if chatInfo == []: return None

    top = chatInfo[0]
    bottom = chatInfo[1:5]

    if top:
        ct.set_source_rgba(0.059, 0.208, 0.114, 1)
        ct.move_to(368, 240)
        putText(ct, text=top[0].title, size=32, width=30*32, height=48, align="LEFT", font="Heavitas")
        ct.set_source_rgba(0.573, 0.91, 0.757, 1)
        ct.move_to(360, 312)
        putText(ct, text=f"Miembros: {top[0].membersCount}", size=20, width=30*32, height=48, align="LEFT", font="Heavitas")
        ct.move_to(360, 360)
        putText(ct, text=f"Mensajes: {top[1]}", size=20, width=30*32, height=48, align="LEFT", font="Heavitas")
        ct.move_to(360, 408)
        putText(ct, text=f"{top[0].author.nickname}", size=20, width=30*32, height=48, align="LEFT", font="Heavitas")
        if top[0].icon:
            icon = await utils.getImageBytes(ctx, top[0].icon)
            imageBase(ct, icon, x=96, y=224, size=216)
    for i,b in enumerate(bottom):
        x = 64
        y = 512 + 160 * i
        ct.set_source_rgba(0.059, 0.208, 0.114, 1)
        ct.move_to(x + 48, y + 12)
        putText(ct, text=f"{b[0].title}", size=24, width=30*32, height=48, align="LEFT", font="Heavitas")
        ct.set_source_rgba(0.573, 0.91, 0.757, 1)
        ct.move_to(x + 128, y + 84)
        putText(ct, text=f"{b[1]}", size=24, width=30*32, height=48, align="LEFT", font="Heavitas")
        ct.move_to(x + 540, y + 84)
        putText(ct, text=f"{b[0].membersCount}", size=24, width=30*32, height=48, align="LEFT", font="Heavitas")

    ct.stroke()
    out     = io.BytesIO()
    image.write_to_png(f"media/export/resume/{objects.ba.instance}/{com.ndcId}-3.png")
    #image.write_to_png(imgIO)
    #imgIO.seek(0)
    #img     = imgIO.read()
    #url     = await ctx.client.upload_media(data=img, content_type="img/png")
    return

def createReportHistory(reports, daysSpan=7):
    history = []
    
    accumulator = 0
    for d in range(7):
        for h in range(24):
            for m in range(4):
                date1 = datetime.datetime.now() - datetime.timedelta(days=6-d, hours=23-h, minutes=59-m*15)
                date2 = date1 + datetime.timedelta(minutes=15)
                accumulator = 0
                for report in reports:
                    if report[3] >= date1 and report[3] < date2: accumulator += 1
                history.append(accumulator)
    return history



async def resumePage4(ctx, com):
    imgIO   = io.BytesIO()
    image   = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1024, 1152, )
    ct      = cairo.Context(image)
    imageBase(ct, "media/templates/resume/4.png")
    reportsResume   = db.getReportResume(com.ndcId)
    history         = createReportHistory(reportsResume.raw)
    
    x = 864
    y = 208 + 12
    dy = 56
    s  = 24
    ct.set_source_rgba(0.91, 0.643, 0.573, 1)
    ct.move_to(x, y + dy * 0)
    putText(ct, text=str(reportsResume.typed['101']), size=s, width=128, height=48, align="CENTER", font="Heavitas")
    ct.move_to(x, y + dy * 1)
    putText(ct, text=str(reportsResume.typed['102']), size=s, width=128, height=48, align="CENTER", font="Heavitas")
    ct.move_to(x, y + dy * 2)
    putText(ct, text=str(reportsResume.typed['103']), size=s, width=128, height=48, align="CENTER", font="Heavitas")
    ct.move_to(x, y + dy * 3)
    putText(ct, text=str(reportsResume.typed['104']), size=s, width=128, height=48, align="CENTER", font="Heavitas")
    ct.move_to(x, y + dy * 4)
    putText(ct, text=str(reportsResume.typed['105']), size=s, width=128, height=48, align="CENTER", font="Heavitas")
    ct.move_to(x, y + dy * 5)
    putText(ct, text=str(reportsResume.typed['106']), size=s, width=128, height=48, align="CENTER", font="Heavitas")
    ct.move_to(x, y + dy * 6)
    putText(ct, text=str(reportsResume.typed['107']), size=s, width=128, height=48, align="CENTER", font="Heavitas")
    ct.move_to(x, y + dy * 7)
    putText(ct, text=str(reportsResume.typed['108']), size=s, width=128, height=48, align="CENTER", font="Heavitas")
    ct.move_to(x, y + dy * 8)
    putText(ct, text=str(reportsResume.typed['109']), size=s, width=128, height=48, align="CENTER", font="Heavitas")

    
    ct.move_to(36, 288 + 24)
    putText(ct, text=str(reportsResume.week), size=108, width=320, height=48, align="CENTER", font="Heavitas")
    ct.move_to(36, 608 + 16)
    putText(ct, text=str(reportsResume.lastWeek), size=56, width=320, height=48, align="CENTER", font="Heavitas")

    plt.figure(figsize=(10, (11/3)), dpi=96)
    plt.plot(history, color="red", label="Reportes")
    plt.ylabel("Conteo de reportes")
    plt.xlabel("Tiempo")

    plotImage = io.BytesIO()
    plt.savefig(plotImage)
    plotImage.seek(0)
    imageBase(ct, name=plotImage, x=32, y=768)
    plt.cla()
    plt.clf()
    
    ct.stroke()
    out     = io.BytesIO()
    image.write_to_png(f"media/export/resume/{objects.ba.instance}/{com.ndcId}-4.png")
    #image.write_to_png(imgIO)
    #imgIO.seek(0)
    #img     = imgIO.read()
    #url     = await ctx.client.upload_media(data=img, content_type="img/png")
    return

async def resumePage5(ctx, com):
    imgIO   = io.BytesIO()
    image   = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1024, 1152, )
    ct      = cairo.Context(image)
    profile = await ctx.client.get_user_info(ctx.client.uid)
    if profile.icon:
        try:
            pfp     = await utils.getImageBytes(ctx, profile.icon)
            imageBase(ct, name=pfp, x=20.5*32, y=6*32, size=7*32)
        except:
            pass
    imageBase(ct, "media/templates/resume/5.png")
    log = db.getLogConfig(com.ndcId)

    x = 400
    y = 264 + 10
    dy = 48
    s  = 20
    w  = 96
    ct.set_source_rgba(0.573, 0.761, 0.91, 1)
    ct.move_to(x, y + dy * 0)
    putText(ct, text="No" if log.nowarn else "Sí", size=s, width=w, height=48, align="CENTER", font="Heavitas")
    ct.move_to(x, y + dy * 1)
    putText(ct, text="Sí" if log._ignore else "No", size=s, width=w, height=48, align="CENTER", font="Heavitas")
    ct.move_to(x, y + dy * 2)
    putText(ct, text="Sí" if log.ban else "No", size=s, width=w, height=48, align="CENTER", font="Heavitas")
    ct.move_to(x, y + dy * 3)
    putText(ct, text="Sí" if log.staff else "No", size=s, width=w, height=48, align="CENTER", font="Heavitas")
    ct.move_to(x, y + dy * 4)
    putText(ct, text="No" if log.bot else "Sí", size=s, width=w, height=48, align="CENTER", font="Heavitas")
    ct.move_to(x, y + dy * 5)
    putText(ct, text="Sí" if log.blogCheck else "No", size=s, width=w, height=48, align="CENTER", font="Heavitas")
    ct.move_to(x, y + dy * 6)
    putText(ct, text="Sí" if log.userWelcome else "No", size=s, width=w, height=48, align="CENTER", font="Heavitas")
    ct.move_to(x, y + dy * 7)
    putText(ct, text="Sí" if log.biography else "No", size=s, width=w, height=48, align="CENTER", font="Heavitas")
    ct.move_to(x, y + dy * 8)
    putText(ct, text="Sí" if log.calls else "No", size=s, width=w, height=48, align="CENTER", font="Heavitas")
    ct.move_to(x, y + dy * 9)
    putText(ct, text=str(objects.ba.instance), size=s, width=w, height=48, align="CENTER", font="Heavitas")
    
    if log.threadId == '': ct.set_source_rgba(1, 0, 0, 1)
    ct.move_to(360, 800)
    putText(ct, text="Sí" if log.threadId != '' else "NO", size=40, width=140, height=48, align="CENTER", font="Heavitas")

    topics = db.getAllCommunityTopics(ctx.msg.ndcId)
    for i,t in enumerate(topics):
        x = 40 + 24
        y = 946 + 8 + i * 24
        ct.move_to(x, y)
        putText(ct, text=t, size=16, width=140, height=48, align="LEFT", font="Heavitas")
    
    ct.move_to(17.5*32, 14*32)
    putText(ct, text=profile.nickname, size=22, width=13*32, height=48, align="CENTER", font="Heavitas")
    
    functionRanking = db.getFunctionRanking(com.ndcId)
    for i,function in enumerate(functionRanking):
        ct.move_to(18*32, 20*32 + 32*i)
        putText(ct, text=function.name[:16], size=22, width=12*32, height=48, align="LEFT", font="Heavitas")
        ct.move_to(18*32, 20*32 + 32*i)
        putText(ct, text=str(function.value), size=22, width=12*32, height=48, align="RIGHT", font="Heavitas")


    ct.stroke()
    out     = io.BytesIO()
    image.write_to_png(f"media/export/resume/{objects.ba.instance}/{com.ndcId}-5.png")
    #image.write_to_png(imgIO)
    #imgIO.seek(0)
    #img     = imgIO.read()
    #url     = await ctx.client.upload_media(data=img, content_type="img/png")
    return


async def drawPagesResume(ctx, com):
    pages = []

    for i in range(5):
        try:
            async with AIOFile(f"media/export/resume/{objects.ba.instance}/{com.ndcId}-{i+1}.png", "rb") as file:
                img = await file.read()
                url = await ctx.client.upload_media(data=img, content_type="img/png")
                if url is not None: pages.append(url)
                await asyncio.sleep(1)
        except Exception:
            pass

    print("Pages done!")
    medialist = [[100, url, None, str(i).zfill(3)] for i,url in enumerate(pages)]
    content   = "[ci]Publicación el canal resumen\n[ci]Si ya no desea recibir blogs de este canal, coloque este comando: --desuscribir resumen\n\n" + "\n".join([ "[IMG=" + str(i).zfill(3) + "]" for i,url in enumerate(pages)])
    
    front = [
                [100, "http://mm1.aminoapps.com/8732/28dc19c414f8b68b9cb673e9b68b7a23ec32b6e0503043a1r7-896-1024_hq.jpg", None],
                [100, "http://mm1.aminoapps.com/8732/949494949494949494949494949494949494b6ed0034d6e4r7-1024-1024_hq.jpg", None],
                [100, "https://mm1.aminoapps.com/8732/949494949494949494949494949494949494ba2702f72130r7-1024-1024_hq.jpg", None]
            ]
    front  = await generateMediaList(ctx, front)
    front.extend(medialist)
    
    date = datetime.datetime.now()
    title = f"Resumen de la comunidad {com.name}: {date.day}-{date.month}-{date.year}"
    bg = "#5E68A5"
    
    return await ctx.client.post_blog(
               title=title,
               content=content,
               image_list_raw=front,
               backgroundColor=bg
        )

async def publishResume(ctx):
    communities     = await get_my_communities(ctx, start=0, size=100)
    com             = ctx.msg.content.split(" ")
    startNdc        = None

    found = False
    if len(com) > 1:
        startNdc = int(com[1])
    for com in communities:
        r  = db.getCommunityTopic(com.ndcId, "resumen")
        if r is False:
            print(f"skipping {com.name}")
            continue
        print(f"Publishin resume in {com.name}")
        if startNdc is not None and found is False and com.ndcId != startNdc: continue
        if startNdc is not None and found is False and com.ndcId == startNdc: found = True
        try:
            ctx.client.set_ndc(com.ndcId)
            response = await drawPagesResume(ctx, com)
            print(response)
            ctx.client.set_ndc(ctx.msg.ndcId)
            await ctx.send(f"Blog publicado en {com.name}\nndc://x{com.ndcId}/blog/{response.blogId}\nndcId: {com.ndcId}")
            await asyncio.sleep(5)
        except:
            ctx.client.set_ndc(ctx.msg.ndcId)
            traceback.print_exc()
            await ctx.send(f"Ha ocurrido un error subiendo en {com.name}\nndcId: {com.ndcId}")

async def prepareResume(ctx):
    communities     = await get_my_communities(ctx, start=0, size=100)
    com             = ctx.msg.content.split(" ")
    startNdc        = None
    if len(com) > 1:
        startNdc = int(com[1])

    found = False
    for com in communities:
        r  = db.getCommunityTopic(com.ndcId, "resumen")
        if r is False:
            print(f"skipping {com.name}")
            continue
        if startNdc is not None and found is False and com.ndcId != startNdc: continue
        if startNdc is not None and found is False and com.ndcId == startNdc: found = True
        print(f"Publishin resume in {com.name}")
        try:
            ctx.client.set_ndc(com.ndcId)
            await resumePage1(ctx, com)
            await resumePage2(ctx, com)
            await resumePage3(ctx, com)
            await resumePage4(ctx, com)
            await resumePage5(ctx, com)
            ctx.client.set_ndc(ctx.msg.ndcId)
            await ctx.send(f"Blog publicado en {com.name}\nndcId: {com.ndcId}")
            await asyncio.sleep(5)
        except Exception:
            ctx.client.set_ndc(ctx.msg.ndcId)
            traceback.print_exc()
            await ctx.send(f"Ha ocurrido creando imágenes para {com.name}\nndcId: {com.ndcId}")
