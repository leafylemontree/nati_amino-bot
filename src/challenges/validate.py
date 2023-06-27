from src.challenges.register    import ChallengeAPI, challenges
from src                        import utils
from src.database               import db
from src.admin.leaderboard      import get_leaderboard_info
import datetime
from src.antispam               import get_wall_comments
from src.admin                  import moderation_history, get_user_moderation
from .test                      import get_blog_likes, get_community_stickers
from src                        import objects
import traceback
from .images                    import triggerLevelUp
from .rewards                   import giveRewards
import math
import asyncio

checkFurther = [
        ChallengeAPI.blogUpload,
        ChallengeAPI.postComment,
        ChallengeAPI.wallComment,
        ChallengeAPI.chatMembers,
        ChallengeAPI.chatCreated,
        ChallengeAPI.chatMessage,
        ChallengeAPI.postFeatured,
        ChallengeAPI.quizUpload,
        ChallengeAPI.like,
        ChallengeAPI.likeAndComment,
        ChallengeAPI.imagePost,
        ChallengeAPI.beInChat,
]

newLine = '\n'

async def get_comments(ctx, blogId=None, wikiId=None, sorting='newest', start=0, size=100):
    response = None
    if      blogId: response = await ctx.client.request('GET', f'blog/{blogId}/comment?sort={sorting}&start={start}&size={size}')
    elif    wikiId: response = await ctx.client.request('GET', f'item/{wikiId}/comment?sort={sorting}&start={start}&size={size}')
    return tuple(map(lambda comment: objects.CommentList(**comment), response['commentList']))

async def furtherRegister(ctx, ins):
    print(ins.data['needsUserInput'])
    print(ins.data)
    index = ins.data['needsUserInput'][0]
    c     = ins.data['challenge'][index]
    links = ctx.msg.content.split("\n")
    linkData = [await ctx.client.get_info_link(link) for link in links]
    objects  = [(link.linkInfo.objectId, link.linkInfo.objectType) for link in linkData]

    if      c.type == ChallengeAPI.blogUpload:
        ins.data['data'][index]['blog']             = []
        leastCreatedTime                            = datetime.datetime.now()
        for objectId,objectType in objects:
            if objectType != 1:                                     continue
            if db.checkYincanaExist(1, objectId, ctx.msg.ndcId):    continue
            ins.data['data'][index]['blog'].append(objectId)
            blog = await ctx.client.get_blog_info(objectId)
            if len(blog.content) < 2000:                            continue
            if blog.author.uid != ctx.msg.author.uid:               continue
            createdTime = datetime.datetime.strptime(str(blog.createdTime), '%Y-%m-%dT%H:%M:%SZ')
            if leastCreatedTime > createdTime: leastCreatedTime = createdTime
        ins.data['data'][index]['leastCreatedTime'] = leastCreatedTime

    elif    c.type == ChallengeAPI.postComment:
        ins.data['data'][index]['comments']             = []
        leastCreatedTime                                = datetime.datetime.now()
        for objectId,objectType in objects:
            comments = None
            if      objectType == 1: comments = await get_comments(ctx, blogId=objectId)
            elif    objectType == 2: comments = await get_comments(ctx, wikiId=objectId)
            if comments is None: continue
            for comment in comments:
                if comment.author.uid != ctx.msg.author.uid:                    continue
                if db.checkYincanaExist(3, comment.commentId, ctx.msg.ndcId):   continue
                ins.data['data'][index]['comments'].append(comment.commentId)
                createdTime = datetime.datetime.strptime(str(comment.createdTime), '%Y-%m-%dT%H:%M:%SZ')
                if leastCreatedTime > createdTime: leastCreatedTime = createdTime
                ins.data['data'][index]['leastCreatedTime'] = leastCreatedTime
                break

    elif    c.type == ChallengeAPI.wallComment:
        ins.data['data'][index]['comments']             = []
        leastCreatedTime                                = datetime.datetime.now()
        for objectId,objectType in objects:
            comments = await get_wall_comments(ctx, user_id=objectId, sorting='newest', size=100)
            if comments is None: continue
            for comment in comments:
                if comment.author.uid != ctx.msg.author.uid:                    continue
                if db.checkYincanaExist(3, comment.commentId, ctx.msg.ndcId):   continue
                ins.data['data'][index]['comments'].append(comment.commentId)
                createdTime = datetime.datetime.strptime(str(comment.createdTime), '%Y-%m-%dT%H:%M:%SZ')
                if leastCreatedTime > createdTime: leastCreatedTime = createdTime
                ins.data['data'][index]['leastCreatedTime'] = leastCreatedTime
                break

    elif    c.type == ChallengeAPI.chatMembers:
        ins.data['data'][index]['chatMembers']      = 0
        ins.data['data'][index]['threadId']         = []
        for objectId,objectType in objects:
            if objectType != 12:                                    continue
            if db.checkYincanaExist(12, objectId, ctx.msg.ndcId):   continue
            chat = await ctx.client.get_chat_info(objectId)
            if chat.author.uid != ctx.msg.author.uid:               continue
            ins.data['data'][index]['chatMembers'] = chat.membersCount
            ins.data['data'][index]['threadId'] = chat.threadId
            #createdTime = datetime.datetime.strptime(str(chat.createdTime), '%Y-%m-%dT%H:%M:%SZ')
            #if leastCreatedTime > createdTime: leastCreatedTime = createdTime
    
    elif    c.type == ChallengeAPI.chatCreated:
        leastCreatedTime                            = datetime.datetime.now()
        ins.data['data'][index]['threadId']         = []
        for objectId,objectType in objects:
            if objectType != 12:                                    continue
            if db.checkYincanaExist(12, objectId, ctx.msg.ndcId):   continue
            chat = await ctx.client.get_chat_info(objectId)
            if chat.author.uid != ctx.msg.author.uid:               continue
            createdTime = datetime.datetime.strptime(str(chat.createdTime), '%Y-%m-%dT%H:%M:%SZ')
            if leastCreatedTime > createdTime: leastCreatedTime = createdTime
            ins.data['data'][index]['threadId'] = chat.threadId
        ins.data['data'][index]['chatCreatedTime'] = leastCreatedTime

    elif    c.type == ChallengeAPI.chatMessage:
        leastCreatedTime                            = datetime.datetime.now()
        for objectId,objectType in objects:
            if objectType != 12:                                    continue
            messages = await ctx.client.get_chat_messages(chat_id=objectId, size=100)
            if messages.messageList is None: continue
            for message in messages.messageList:
                if message.content is None:                                         continue
                if message.author.uid != ctx.msg.author.uid:                        continue
                if message.content.find(ins.data['challenge'][index].args) == -1:   continue
                ins.data['data'][index]['chatMessage'] = message.content
                break

    elif    c.type == ChallengeAPI.postFeatured:
        ins.data['data'][index]['blog']             = []
        leastFeaturedTime                           = datetime.datetime.now()
        for objectId,objectType in objects:
            if objectType != 1:                                     continue
            if db.checkYincanaExist(1, objectId, ctx.msg.ndcId):    continue
            adminLogList = await moderation_history(ctx, blogId=objectId, size=100)
            if adminLogList is None: continue
            print(adminLogList)
            blog = await ctx.client.get_blog_info(objectId)
            if blog.author.uid != ctx.msg.author.uid:               continue
            if db.checkYincanaExist(6, objectId, ctx.msg.ndcId):    continue
            for log in adminLogList:
                print(log.operation, log.createdTime)
                if log.operation != 114:                            continue
                featuredTime = datetime.datetime.strptime(str(log.createdTime), '%Y-%m-%dT%H:%M:%SZ')
                if leastFeaturedTime > featuredTime: leastFeaturedTime = featuredTime
                ins.data['data'][index]['blog'].append(objectId)
                break
        ins.data['data'][index]['leastFeaturedTime'] = leastFeaturedTime
     
    elif    c.type == ChallengeAPI.quizUpload:
        ins.data['data'][index]['quiz']             = []
        leastCreatedTime                            = datetime.datetime.now()
        for objectId,objectType in objects:
            if objectType != 1:                                  continue
            if db.checkYincanaExist(1, objectId, ctx.msg.ndcId): continue
            ins.data['data'][index]['quiz'].append(objectType)
            blog = await ctx.client.get_blog_info(objectId)
            createdTime = datetime.datetime.strptime(str(blog.createdTime), '%Y-%m-%dT%H:%M:%SZ')
            if leastCreatedTime > createdTime: leastCreatedTime = createdTime
        ins.data['data'][index]['leastCreatedTime'] = leastCreatedTime

    elif    c.type == ChallengeAPI.like:
        ins.data['data'][index]['likes']            = []
        ins.data['data'][index]['objectType']       = []
        for objectId,objectType in objects:
            if objectType not in [1, 2]:                                  continue
            likes = []

            if objectType == 1:
                if db.checkYincanaExist(1, objectId, ctx.msg.ndcId): continue
                likes = await get_blog_likes(ctx, blogId=objectId)
            elif objectType == 2:
                if db.checkYincanaExist(2, objectId, ctx.msg.ndcId): continue
                likes = await get_blog_likes(ctx, wikiId=objectId)

            if likes.votedValueMap == ():                           break
            if ctx.msg.author.uid not in likes.votedValueMap:       break
            ins.data['data'][index]['likes'].append(objectId)
            ins.data['data'][index]['objectType'].append(objectType)
    
    elif    c.type == ChallengeAPI.likeAndComment:
        ins.data['data'][index]['likes']            = []
        ins.data['data'][index]['comments']         = []
        ins.data['data'][index]['objectType']       = []
        leastCreatedTime                            = datetime.datetime.now()
        for objectId,objectType in objects:
            if objectType not in [1, 2]:                                  continue
            likes = []

            if objectType == 1:
                likes = await get_blog_likes(ctx, blogId=objectId)
            elif objectType == 2:
                likes = await get_blog_likes(ctx, wikiId=objectId)

            if likes.votedValueMap == ():                               continue
            if ctx.msg.author.uid not in likes.votedValueMap:           continue

            comments = None
            if      objectType == 1: comments = await get_comments(ctx, blogId=objectId)
            elif    objectType == 2: comments = await get_comments(ctx, wikiId=objectId)
            com         = None
            if comments is None: continue
            for comment in comments:
                print(comment.content)
                if comment.author.uid != ctx.msg.author.uid:                    continue
                if db.checkYincanaExist(3, comment.commentId, ctx.msg.ndcId):   continue
                com = comment
                break

            if com is None: break
            ins.data['data'][index]['likes'].append(objectId)
            ins.data['data'][index]['comments'].append(com.commentId)
            ins.data['data'][index]['objectType'].append(objectType)
            createdTime = datetime.datetime.strptime(str(com.createdTime), '%Y-%m-%dT%H:%M:%SZ')
            if leastCreatedTime > createdTime: leastCreatedTime = createdTime
        ins.data['data'][index]['leastCreatedTime'] = leastCreatedTime


    elif    c.type == ChallengeAPI.imagePost:
        ins.data['data'][index]['imagePost']        = []
        leastCreatedTime                            = datetime.datetime.now()
        for objectId,objectType in objects:
            if objectType != 1:                                  continue
            if db.checkYincanaExist(1, objectId, ctx.msg.ndcId): continue
            ins.data['data'][index]['imagePost'].append(objectType)
            blog = await ctx.client.get_blog_info(objectId)
            createdTime = datetime.datetime.strptime(str(blog.createdTime), '%Y-%m-%dT%H:%M:%SZ')
            if leastCreatedTime > createdTime: leastCreatedTime = createdTime
        ins.data['data'][index]['leastCreatedTime'] = leastCreatedTime

    elif    c.type == ChallengeAPI.beInChat:
        ins.data['data'][index]['isInChat']         = []
        for i,(objectId,objectType) in enumerate(objects):
            if objectType != 12:                                    continue
            chat = await ctx.client.get_chat_info(objectId)
            threadId = chat.threadId
            for i in range(10):
                users = await ctx.client.get_chat_info(threadId, start=i*100, size=100)
                for user in users:
                    if user.uid != ctx.msg.author.uid:              continue
                    ins.data['data'][index]['isInChat'].append(threadId)
                    break
                if len(ins.data['data'][index]['isInChat']) >= (i+1): break 
                await asyncio.sleep(3)

    ins.data['needsUserInput'].pop(0)

    if ins.data['needsUserInput'] == []:
        response = False
        try:        response = await ins.data['community'].check(ctx, ins.data['yincana'].level, ins.data['data'])
        except Exception as e:
            traceback.print_exc()
            response = False

        if response is True:
            db.setYincanaData(ctx.msg.author.uid, ctx.msg.ndcId, level=1)

            #await ctx.send(f"Felicidades, {ctx.msg.author.nickname}, has superado el nivel {ins.data['yincana'].level + 1} de los retos con éxito.")
            ins.data['community'].dbUpdate(ins.data['challenge'], ins.data['data'], ctx.msg.ndcId)
            await triggerLevelUp(ctx, ins.data['yincana'].level + 1, ins.data['community'] )
            level = ins.data['yincana'].level
            utils.waiting.look_and_delete(ctx.msg.author.uid, ctx.client.ndc_id, ctx.msg.threadId)
            await giveRewards(ctx, level)
        else       :
            await ctx.send(f"""
Que mal, no cumple con los requisitos del nivel {ins.data['yincana'].level + 1}. Intente otra vez

Ha fallado en: {ChallengeAPI.getLabel(ins.data['challenge'][response])}""")

        return True
    else:
        await ctx.send(f"""
Nati necesita que ingreses información adicional para la siguiente tarea:
{ChallengeAPI.getLabel(ins.data['challenge'][ins.data['needsUserInput'][0]])}

Ingresa solo los enclaces de los blogs en una linea diferente cada uno. Ejemplo:
aminoapps...
aminoapps...
aminoapps...""")
        return False

    return False

@utils.waitForMessage(message='*', callback=furtherRegister)
async def validate(ctx):

    communityChallenge =    None
    try:                    communityChallenge = challenges[ctx.msg.ndcId]
    except Exception:
        await ctx.send('Esta comunidad no tiene retos.')
        return -1

    yincana             =   db.getYincanaData(ctx.msg.author.uid, ctx.msg.ndcId)
    challenge           =   communityChallenge.getLevelChallenge(yincana.level)
    data                =   []
    needsUserInput      =   []

    if challenge is None:
        await ctx.send(f"No hay retos para el nivel {yincana.level + 1} en esta comunidad. Está en el nivel más alto.")
        return -1

    for i,c in enumerate(challenge):

        if      c.type == ChallengeAPI.none:
            data.append({}) 

        elif    c.type == ChallengeAPI.reputation:
            data.append({ 'reputation' : ctx.msg.author.reputation })

        elif    c.type == ChallengeAPI.level:
            data.append({ 'level' : ctx.msg.author.level })
        
        elif    c.type == ChallengeAPI.follow:
            user    = await ctx.get_user_info()
            data.append({ 'follow' : user.joinedCount })

        elif    c.type == ChallengeAPI.dailyMinutes:
            users = await get_leaderboard_info(ctx, rankingType=1)
            user  = None
            for u in users:
                if u.uid != ctx.msg.author.uid: continue
                data.append({ 'dailyMinutes' : u.activeTime })
                break

        elif    c.type == ChallengeAPI.weeklyMinutes:
            users = await get_leaderboard_info(ctx, rankingType=2)
            user  = None
            for u in users:
                if u.uid != ctx.msg.author.uid: continue
                data.append({ 'weeklyMinutes' : u.activeTime })
                break

        elif    c.type == ChallengeAPI.warnings:
            data.append({ 'warnings' :  await get_user_moderation(ctx, ctx.msg.author.uid, 'WARN') })

        elif    c.type == ChallengeAPI.strikes:
            data.append({ 'strikes' :   await get_user_moderation(ctx, ctx.msg.author.uid, 'STRIKE') })

        elif    c.type == ChallengeAPI.bans:
            data.append({ 'bans' :      await get_user_moderation(ctx, ctx.msg.author.uid, 'BAN') })

        elif    c.type == ChallengeAPI.profileChange:
            user    = await ctx.get_user_info()
            modifiedTime = datetime.datetime.strptime(str(user.modifiedTime), '%Y-%m-%dT%H:%M:%SZ')
            data.append({ 'profileChangeTime' : modifiedTime })

        elif    c.type == ChallengeAPI.nickname:
            data.append({ 'nickname' : ctx.msg.author.nickname })

        elif    c.type == ChallengeAPI.profileDays:
            user        = await ctx.get_user_info()
            createdTime = datetime.datetime.strptime(str(user.createdTime), '%Y-%m-%dT%H:%M:%SZ')
            days        = (datetime.datetime.now() - createdTime).days
            data.append({ 'profileCreatedTime' : days })

        elif    c.type == ChallengeAPI.checkIn:
            from src.subcommands.userInfo import get_user_checkins
            days = await get_user_checkins(ctx, ctx.msg.author.uid)
            data.append({ 'checkIn' : days })

        elif    c.type == ChallengeAPI.followStaff:
            following   = []
            staffFollow = []
            user        = await ctx.get_user_info()
            for i in range(0, math.ceil(user.joinedCount / 100)):
                await asyncio.sleep(3)
                u = await ctx.client.get_user_following(user_id=user.uid, start=i*100, size=100)
                following.extend(u)
            for u in following:
                if u.role == 0:     continue
                staffFollow.append(u.uid)
            data.append({ 'follow' : staffFollow })

        elif    c.type == ChallengeAPI.stickerPack:
            packs = 0
            stickerCollections = await get_community_stickers(ctx)
            for stickerPack in stickerCollections: packs += 1
            data.append({'stickerPack': packs})

        elif    c.type == ChallengeAPI.nicknameStart:
            data.append({ 'nickname' : ctx.msg.author.nickname })

        elif    c.type == ChallengeAPI.likeFeatured:
            from src.subprocess.test import get_recent_blogs 
            from src.challenges.test import get_blog_likes
            
            likes = []
            featured = await get_recent_blogs(ctx, start=0, size=100)
            for blog in featured:
                if   blog.refObjectType == 1: postLikes = await  get_blog_likes(ctx, blogId=blog.refObjectId)
                elif blog.refObjectType == 2: postLikes = await  get_blog_likes(ctx, wikiId=blog.refObjectId)

                for like in postLikes.votedValueMapV2:
                    if like.uid != ctx.msg.author.uid: continue
                    likes.append(featured.refObjectId)
                    break

                await asyncio.sleep(3)
            data.append({ 'likes' : [] })

        elif c.type in checkFurther:
            data.append({})
            needsUserInput.append(i)
                
    if needsUserInput == []:
        response = await communityChallenge.check(ctx, yincana.level, data)
        if response is True:
            db.setYincanaData(ctx.msg.author.uid, ctx.msg.ndcId, level=1)
            await triggerLevelUp(ctx, yincana.level + 1, communityChallenge)
            utils.waiting.look_and_delete(ctx.msg.author.uid, ctx.client.ndc_id, ctx.msg.threadId)
            await giveRewards(ctx, yincana.level)
        else       :    await ctx.send(f"Que mal, no cumple con los requisitos del nivel {yincana.level + 1}.")
        return -1
    else:
        await ctx.send(f"""
Nati necesita que ingreses información adicional para la siguiente tarea:
{ChallengeAPI.getLabel(challenge[needsUserInput[0]])}

Ingresa solo los enclaces de los blogs en una linea diferente cada uno. Ejemplo:
aminoapps...
aminoapps...
aminoapps...""")

    return {
            'data'          : data,
            'needsUserInput': needsUserInput,
            'yincana'       : yincana,
            'challenge'     : challenge,
            'community'     : communityChallenge
        }


async def getChallenges(ctx):
    communityChallenge =    None
    try:                    communityChallenge = challenges[ctx.msg.ndcId]
    except Exception:       return await ctx.send('Esta comunidad no tiene retos.')

    yincana             =   db.getYincanaData(ctx.msg.author.uid, ctx.msg.ndcId)
    s                   =   communityChallenge.levelRepr(yincana.level)
    await ctx.send(f"""
Estos son tus retos

[c]Retos nivel {yincana.level + 1}:
{s}""")
    return


async def isValidUserLink(ctx, text=None):
    if text is None: text = ctx.msg.content

    if text.find("pps.com/p/") == -1: return None
    userLink = text.split("pps.com/p/")[1]
    userLink = userLink.split(" ")[0]
    link = await ctx.client.get_info_link(f"http://aminoapps.com/p/{userLink}")
    if link.linkInfo.objectType != 0: return False
    return link.linkInfo.objectId

def parseNumbers(text):
    nums  = []
    words = text.split(" ")
    for word in words:
        try:    nums.append(int(word))
        except: pass
    return nums

@utils.isStaff
async def advanceLevel(ctx):
    
    userId = await isValidUserLink(ctx, text=ctx.msg.content)
    if   userId is None:  return await ctx.send("Debe ingresar el link de un usuario") 
    elif userId is False: return await ctx.send("Solo funciona con usuarios") 
    
    communityChallenge =    None
    try:                    communityChallenge = challenges[ctx.msg.ndcId]
    except Exception:
        await ctx.send('Esta comunidad no tiene retos.')
        return -1

    yincana             =   db.getYincanaData(userId, ctx.msg.ndcId)
    db.setYincanaData(userId, ctx.msg.ndcId, level=1)
    await triggerLevelUp(ctx, yincana.level + 1, communityChallenge, userId=userId)
    await giveRewards(ctx, yincana.level, userId=userId)

@utils.isStaff
async def rewindLevel(ctx):
    
    userId = await isValidUserLink(ctx, text=ctx.msg.content)
    if   userId is None:  return await ctx.send("Debe ingresar el link de un usuario") 
    elif userId is False: return await ctx.send("Solo funciona con usuarios") 
    
    communityChallenge =    None
    try:                    communityChallenge = challenges[ctx.msg.ndcId]
    except Exception:
        await ctx.send('Esta comunidad no tiene retos.')
        return -1

    yincana             =   db.getYincanaData(userId, ctx.msg.ndcId)
    if yincana.level == 0: return await ctx.send("Ya está en el nivel mas bajo.")
    db.setYincanaData(userId, ctx.msg.ndcId, level=-1)
    return await ctx.send(f"Se ha retrocedido de nivel al {yincana.level}")

@utils.isStaff
async def setLevel(ctx):
    
    userId = await isValidUserLink(ctx, text=ctx.msg.content)
    if   userId is None:  return await ctx.send("Debe ingresar el link de un usuario") 
    elif userId is False: return await ctx.send("Solo funciona con usuarios") 
    
    communityChallenge =    None
    try:                    communityChallenge = challenges[ctx.msg.ndcId]
    except Exception:
        await ctx.send('Esta comunidad no tiene retos.')
        return -1

    yincana             =   db.getYincanaData(userId, ctx.msg.ndcId)
    nums                =   parseNumbers(ctx.msg.content)
    if nums == []: return await ctx.send("Debe ingresar el nivel del usuario de esta forma: --nivel-yincana (link) (nivel)")
    newLevel            =   nums[-1] - 1
    if newLevel >= communityChallenge.levels: newLevel = communityChallenge.levels - 1
    if newLevel < 0: newLevel = 0
    difference          = newLevel - yincana.level

    db.setYincanaData(userId, ctx.msg.ndcId, level=difference)
    return await ctx.send(f"Se ha cambiado el nivel del usuario a nivel {newLevel + 1}")

