from src import utils
from src.database   import db
from src.shop.helpers import getDonationList, postFormatString
from src.shop.interface import add_item
import asyncio
import traceback

rewardTable = {

    9999:   [
                {
                    'AC'        : 10,
                    'POINTS'    : 10,
            },
                {
                    'AC'        : 20,
                    'POINTS'    : 30
            },
                {
                    'AC'        : 25,
                    'POINTS'    : 60
            },
                {
                    'AC'        : 40,
                    'POINTS'    : 100
            },
                {
                    'POINTS'    : 150,
                    'ITEM'      : 27        # 27 = Featured card
            },
                {
                    'AC'        : 60,
                    'POINTS'    : 200
            },
                {
                    'AC'        : 80,
                    'ITEM'      : 28        # 28 = Featured chat card
            },
                {
                    'AC'        : 100,
                    'ITEM'      : 29        # 29 = Notification card
            },
                {
                    'AC'        : 120,
                    'POINTS'    : 300
            },
                {
                    'ITEM'      : 30,       # 30 = Custom title card
                    'POINTS'    : 400
            },
        ],
    41001082: [
                {
                    "AC"        : 10,
            },
                {
                    "AC"        : 20,
            },
                {
                    "AC"        : 30,
            },
                {
                    "AC"        : 40,
            },
                {
                    "AC"        : 50,
            },
                {
                    "AC"        : 60,
            },
                {
                    "AC"        : 70,
            },
                {
                    "AC"        : 80,
            },
                {
                    "AC"        : 90,
            },
                {
                    "AC"        : 100,
            },
                {
                    "AC"        : 110,
            },
                {
                    "AC"        : 120,
            },
                {
                    "AC"        : 130,
            },
        ],
    111610163 : [
                {
                    "AC"        : 15,
            },
                {
                    "AC"        : 5,
                    "ITEM"      : 27
            },


        ],
    144321393:  [
                {
                    "AC"        : 10
            },
                {
                    "AC"        : 20
            },
                {
                    "AC"        : 30
            },
                {
                    "AC"        : 40
            },
                {
                    "AC"        : 50
            },
                {
                    "AC"        : 60
            },
                {
                    "AC"        : 70
            },
                {
                    "AC"        : 80
            },
                {
                    "AC"        : 90
            },
                {
                    "AC"        : 100
            },
                {
                    "AC"        : 110
            },
                {
                    "AC"        : 120
            },
                {
                    "AC"        : 130
            },
        ]
}


TA_SYSTEM_ID = "00000000-0000-0000-0000-000000000000"


async def donate_blog(ctx, blog, amount, blogId=None):
    if blog:
        if blog.extensions is None: return False
        if blog.content    is None: return False
    if blogId is None: blogId = blog.blogId
    if isinstance(amount, int): amount = getDonationList(amount)

    for i in amount:
        try:
            await asyncio.sleep(3)
            await ctx.client.send_coins(coins=i, blog_id=blogId)
        except Exception as e:
            return False
    return True


async def donate_wiki(ctx, wiki, amount, wikiId=None):
    if wiki:
        if wiki.author.uid == TA_SYSTEM_ID: return False
    if wikiId is None: wikiId = wiki.itemId
    if isinstance(amount, int): amount = getDonationList(amount)

    for i in amount:
        try:
            await asyncio.sleep(3)
            await ctx.client.send_coins(coins=i, object_id=wikiId)
        except Exception as e:
            return False
    return True


async def donateAC(ctx, userId, amount, silent=False):
    AC = amount
    if amount  < 0    : return None
    if amount is None : return None
    
    postId   = None
    postType = None
    postName = None
    
    blogs = await ctx.client.get_user_blogs(userId)
    wikis = await ctx.client.get_user_wikis(userId)
    if not wikis and not blogs:
        if silent is False: await ctx.send("No se encontraron blogs para donar :c. Selecciones otra opción o vuelva a ingresarla cuando tenga donde donar.")
        return False

    user = db.getUserData(None, userId)

    donation = getDonationList(AC)
    hasDonated = False
 
    for blog in blogs:
        if hasDonated: break
        r = await donate_blog(ctx, blog, amount)
        if r is False: continue

        hasDonated  = True
        postName    = blog.title
        postType    = 'blog'
        break

    for wiki in wikis:
        if hasDonated: break
        r = await donate_wiki(ctx, wiki, amount)
        if r is False: continue

        hasDonated  = True
        postName    = wiki.label
        postType    = 'wiki'
        break
    
    if hasDonated is False:
        db.setUserReward(userId, ctx.msg.ndcId, dtype=0, amount=AC)
        if silent is False: await ctx.send(f"Ha ocurrido un error donando. Nati ha guardado la recompensa hasta que sea reclamada.\nUse el comando --reclamar-recompensas (link de un blog donde donar).")
        return False
    
    if silent is False: await ctx.send(f"Han sido donados {AC} AC a {postFormatString(postType, postName)}")
    return True


async def donatePoints(ctx, userId, amount):
    points = amount
    db.modifyRecord(44, None, points, userId)
    await ctx.send(f"Han sido añadidos {points} puntos de actividad a su cuenta.")
    return True

async def getConfirmationLA(ctx, ins):
    print("Select reward")
    if ins.data['messageId'] == ctx.msg.messageId: return False
    r = True
    if ctx.msg.content.upper().find("-AC") == 0:       r = await donateAC(ctx, ins.data['userId'], ins.data['amount'])
    elif ctx.msg.content.upper().find("-PUNTOS") == 0: r = await donatePoints(ctx, ins.data['userId'], ins.data['amount'])
    return r


def labelReward(reward):
    if      reward == 'AC'      : return "Recibir premio en AC"
    elif    reward == 'POINTS'  : return "Recibir premio en punto de actividad"
    elif    reward == 'ITEM'    : return "Recibir premio como un item"

def multipleRewardMessage(ndcId, level):
    rewards = list(rewardTable[ndcId][level].keys())
    if len(rewards) > 1:
        yes = labelReward(rewards[0])
        no  = labelReward(rewards[1])

    msg = f"""
El premio para este nivel se puede escojer entre dos opciones. Ingrese -si o -no para elegir entre una de las dos.

-si : {yes}
-no : {no}
"""
    return msg

async def executeGive(ctx, userId, r, rewards):
    reward, amount = tuple(rewards)[r]
    if   reward == 'AC'        : await donateAC(ctx, userId, amount)
    elif reward == 'POINTS'    : await donatePoints(ctx, userId, amount)
    elif reward == 'ITEM'      : await add_item(ctx, objectId=amount, amount=1, mode="ADD", userId=userId)
    return


async def giveRewards(ctx, level, userId=None):
    print('giving reward')
    ndcId   = ctx.msg.ndcId
    if userId is None: userId = ctx.msg.author.uid

    if ndcId in rewardTable.keys():     rewards = rewardTable[ndcId][level].items()
    else                        :       rewards = [{ "AC" : (level + 1) * 10 }.items()]
    r = None

    if len(rewards) > 1:
        await ctx.send(multipleRewardMessage(ndcId, level))
        confirmation = await utils.confirmation(ctx, ctx.msg.threadId, userId, ctx.msg.ndcId, timeout=False)
        if      confirmation is True    : r = 0
        elif    confirmation is False   : r = 1

    else:
        r = 0
    
    await executeGive(ctx, userId, r, rewards)
    return


