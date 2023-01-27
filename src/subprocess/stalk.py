from src.antispam import findNickname, findContent, wallLog
from src.antispam.data import AS
from .getComs import get_my_communities
import asyncio
from asyncio import sleep
from .data import alreadyChecked
from .check import checkWall, checkBio, checkBlogs
from src import objects
from src.database import db

async def set_online(ctx):
        print("Try activity")
        comId = 92
        ctx.client.set_ndc(comId)
        data = {
                'onlineStatus' : 1,
                'duration'     : 86400,
            }
        await ctx.client.request('POST', f'user-profile/{ctx.client.uid}/online-status', json=data)
        await ctx.actions(actions=['Browsing'], thread_type=1, chat_id="05725b11-0eaf-4c79-ba8f-122e1a6fd571", ndc_id=ctx.client.ndc_id)
        return 

async def get_communities(ctx):
        coms = await get_my_communities(ctx, 0, 100)
        comList = []
        for i,j in enumerate(coms):
            log = db.getLogConfig(j.ndcId)
            if log.stalk: comList.append([j.ndcId, j.name])
        print(comList)
        return comList

async def get_active_users(ctx, comId):
        users = []
        isDoneGetting = False
        userCounter = 0
        while isDoneGetting is False:
            ctx.client.set_ndc(comId)
            usr_get = await ctx.client.get_online_users(start=userCounter, size=100)
            users.extend(usr_get)
            userCounter += len(usr_get)
            if len(usr_get) < 99: isDoneGetting = True 
        return users

async def stalk_run(ctx):
    print("Stalk begun")
    global alreadyChecked
    await sleep(15)
    print("Stalk begun")

    while True:
        await set_online(ctx) 
        comList = await get_communities(ctx)

        for i,j in enumerate(comList):
            print(f"Checking community------\nname: {j[1]}\nndcId: {j[0]}")
            users = await get_active_users(ctx, j[0])
            await sleep(10)
            
            for index,user in enumerate(users) :
                if user.uid in alreadyChecked: continue
                print('\t', index, user.nickname)
                s1 = await findNickname(user.nickname)
                s2 = await checkWall(ctx, user, j[0])
                s3 = await checkBio(ctx, user)
                s4 = await checkBlogs(ctx, user)
                warnings = [s1, s2, s3, s4]
                print("warnings:", warnings)
                if warnings == [[],{},[],[]] : continue
                await sleep(3)
                print("Amenaza detectada!")
                print('warnings:', warnings)
                await wallLog(ctx, user, warnings)
                print(f"checked: {objects.alreadyChecked}")
                if user.uid not in objects.alreadyChecked: objects.alreadyChecked.append(user.uid)
                print("Next community")  
                await sleep(10) 
            await sleep(600)

def stalk(loop, ctx):
    print("Stalk start")
    lp = asyncio.run_coroutine_threadsafe(stalk_run(ctx), loop)
    lp.result()
    print("Stalk ended")

