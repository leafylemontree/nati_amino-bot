from src import utils
import edamino
import time
from src import antispam
import asyncio
from src.database import db

comId = 116820518
threadId = "326b4d0f-e966-4f58-9e26-fdbc517ab745"

alreadyChecked = {
            "0" : []
        }


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
    #return tuple(map(lambda blog: edamino.objects.Blog(**blog), resp["featuredList"]))
    return resp['featuredList'][0]

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

            if str(com) not in alreadyChecked.keys(): alreadyChecked[str(com)] = []
            if blogId in alreadyChecked[str(com)]   : continue

            fnick = await antispam.findNickname(author.nickname)
            fcont = await antispam.findContent(content)

            alreadyChecked[str(com)].append(blog.blogId)
            if fnick or fcont: await antispam.blogLog(ctx, blog, [fnick, fcont]) 



async def send_active_obj(
                            ctx,
                            startTime       = int(time.time() * 1000),
                            endTime         = int((time.time() - 60) * 1000),
                            optInAdsFlags   = 27,
                            timezone        = -time.timezone // 1000,
                            timers          = None,
                            timestamp       = int(time.time() * 1000)):
        
        data = {
            "userActiveTimeChunkList": [{
                "start": startTime,
                "end": endTime
            }],
            "timestamp": timestamp,
            "optInAdsFlags": optInAdsFlags,
            "timezone": timezone,
            "uid": ctx.client.uid
        }

        if timers:
            data["userActiveTimeChunkList"] = timers

        resp = await ctx.client.request("POST", f"community/stats/user-active-time", json=data)
        return resp


def ws_activity_data(ndcId, objectId, objectType):
    return {
            "o": {
                "actions": ["Browsing"],
                "target": f'ndc://x{ndcId}/blog/{objectId}',
                "ndcId": ndcId,
                "params": {
                    "duration": 1800,
                    "blogType": 0
                    },
                "id": "363483",
            },
            "t": 306,
        }
    

async def activity_status(ctx, status=1):
    data = {
        "onlineStatus": status,
        "duration": 86400,
        "timestamp": int(time.time() * 1000)
    }

    await ctx.client.request("POST", f"user-profile/{ctx.client.uid}/online-status", json=data)
    return

@utils.runSubTask(pollingTime=600)
async def beActive(ctx):
    coms = await get_my_communities(ctx, start=0, size=100)
    comList = list(map(lambda com: com.ndcId, coms))
    
    for i,com in enumerate(comList):
        log = db.getLogConfig(com)
        if not log.active : continue

        await asyncio.sleep(15)
       
        try:
            ctx.client.set_ndc(com)
            blog = await get_featured_blogs(ctx, start=0, size=100)
            data = ws_activity_data(com, blog['refObjectId'], blog['refObjectType'])
            await ctx.ws.send_json(data)
            await activity_status(ctx, status=1)
        except Exception as e:
            print(e)
            pass


