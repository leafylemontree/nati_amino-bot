from src import utils
import edamino
import time
from src import antispam
import asyncio
from src.database import db
from src import objects
import random
from src.antispam import get_wall_comments
import logging
import traceback

async def get_my_communities(ctx, start=0, size=25):
        data = {"timestamp": int(time.time() * 1000)}
        response = await ctx.client.request(
            'GET', f'https://service.narvii.com/api/v1/g/s/community/joined?v=1&start={start}&size={size}', json=data, full_url=True)
        return tuple(
            map(lambda community: edamino.objects.Community(**community),
                response['communityList']))

async def get_recent_blogs(ctx, pageToken=None, start=0, size=25):
    data = {"timestamp": int(time.time() * 1000)}
    resp = await ctx.client.request("GET", f"feed/blog-all?pagingType=t{('&pageToken='+pageToken) if pageToken else ''}&start={start}&size={size}", json=data)
    return tuple(map(lambda recent: edamino.objects.Blog(**recent), resp["blogList"]))

async def get_featured_blogs(ctx, start=0, size=25):
    resp = await ctx.client.request("GET", f"feed/featured?start={start}&size={size}")
    return tuple(map(lambda blog: objects.Featured(**blog), resp["featuredList"]))





@utils.runSubTask(pollingTime=600)
async def blogs(ctx):
    coms = await get_my_communities(ctx, start=0, size=100)
    comList = list(map(lambda com: com.ndcId, coms))
    
    for i,com in enumerate(comList):
        log = db.getLogConfig(com)
        if not log.blogCheck : continue
        if not log.threadId  : continue

        await asyncio.sleep(15)
        
        ctx.client.set_ndc(com)
        blogs = await get_recent_blogs(ctx, start=0, size=100)
        
        for j,blog in enumerate(blogs):
            content = blog.content
            author  = blog.author
            title   = blog.title
            blogId  = blog.blogId
            
            if db.r_addBlog(com, blog.blogId): continue

            fnick = await antispam.findNickname(author.nickname)
            fcont = await antispam.findContent(content)

            if fnick or fcont: await antispam.blogLog(ctx, blog, [fnick, fcont]) 

def timers(amount=50):
    delta = 300
    return [{
            'start':    int(time.time() - (i+1) * delta) ,
            'end':      int(time.time() - (i  ) * delta)
            } for i in range(amount)]

async def send_active_obj(ctx, optInAdsFlags: int = 2147483647):
        data = {
            "userActiveTimeChunkList": timers(5),
            "timestamp": int(time.time() * 1000),
            "optInAdsFlags": optInAdsFlags,
            "timezone": -time.timezone // 1000,
            "uid": ctx.client.uid
        }

        await ctx.client.request('POST', f"community/stats/user-active-time", json=data)
        return

def ws_activity_data(ndcId, objectId, objectType):
    return {
            "o": {
                "actions": ["Browsing"],
                "target": f'ndc://x{ndcId}/featured',
                "ndcId": ndcId,
                "params": {
                    "duration": 27605,
                    "blogType": 0
                    },
                "id": "363483",
            },
            "t": 306,
        }

async def send_action(ctx, blogId):
        data = {
            "o": {
                "actions": ['Browsing', ],
                "target": f"ndc://x{ctx.client.ndc_id}/blog/{blogId}",
                "ndcId": ctx.client.ndc_id,
                "params": {
                    "topicIds": [45841, 17254, 26542, 42031, 22542, 16371, 6059, 41542, 15852],
                    "duration": 27605,
                    "blogType": 0
                    },
                "id": "831046"
            },
            "t": 306
        }
        return await ctx.ws.send_json(data)

async def activity_status(ctx, status=1):
    data = {
        "onlineStatus": status,
        "duration": 86400,
        "timestamp": int(time.time() * 1000)
    }

    await ctx.client.request("POST", f"user-profile/{ctx.client.uid}/online-status", json=data)
    return

@utils.runSubTask(pollingTime=300)
async def beActive(ctx):
    coms = await get_my_communities(ctx, start=0, size=100)
    comList = list(map(lambda com: com.ndcId, coms))
    
    for i,com in enumerate(comList):
        log = db.getLogConfig(com)
        if not log.active : continue
        await asyncio.sleep(5)
        status = 0

        try:
            ctx.client.set_ndc(com)
            blogs = await get_featured_blogs(ctx, start=0, size=100)
            blog  = blogs[int(random.random() * len(blogs))]
            data = ws_activity_data(com, blog.refObjectId, blog.refObjectType)
            status = 1
            await ctx.ws.send_json(data) 
            status = 2
            await activity_status(ctx, status=1)
            status = 3
            await send_active_obj(ctx)
            status = 4
            await send_action(ctx, blog.refObjectId)
            status = 5
            logging.info(f"{objects.ba.instance} Activity - {com}")
        except Exception as e:
            traceback.print_exc()
            logging.error(f"Errored $.{objects.ba.instance} beActive - {status} - {com} - {e}")



@utils.runSubTask(pollingTime=1800)
async def giveWelcome(ctx):
    coms = await get_my_communities(ctx, start=0, size=100)
    comList = list(map(lambda com: com.ndcId, coms))
    
    for i,com in enumerate(comList):
        log = db.getLogConfig(com)
        if log.userWelcome == 0: continue
        await asyncio.sleep(15)
        ctx.client.set_ndc(com)

        welcomeMsg = db.getWelcomeMessage(com, mode='COMMUNITY')
        welcomeMsg = await utils.formatter(ctx, welcomeMsg)
        logging.info(f"$.{objects.ba.instance} - Welcome ndcId={com}:")
        if welcomeMsg is None:
            logging.info(f"$.{objects.ba.instance} - Message not found for ndcId={com}")
            continue

        users = await ctx.client.get_all_users(users_type='recent', start=0, size=100)
        for user in users:
            try:
                if db.redis.hexists('usersWelcome', f'?{com}&{user.uid}'): continue
                await asyncio.sleep(3)
                alreadyCommented = False
                comments = await get_wall_comments(ctx, user_id=user.uid, sorting='oldest', start=0, size=100)
                if ctx.client.uid in tuple(map(lambda comment: comment.author.uid, comments)):
                    alreadyCommented = True
                    continue
            
                if alreadyCommented: continue
                await ctx.client.comment_profile(uid=user.uid, message=welcomeMsg)

            except Exception as e:
                logging.error(f"Errored $.{objects.ba.instance} giveWelcome - {com} - {user.uid}: {e}")
                pass
            
            db.redis.hset('usersWelcome', f'?{com}&{user.uid}', int(time.time() * 1000))

    return
