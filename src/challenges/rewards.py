from src import utils
from src.database   import db
from src.shop.helpers import getDonationList, postFormatString
import asyncio

rewardTable = {

    9999:   [
                {
                    'AC': 10,
                    'POINTS': 10
            },
                {
                    'AC': 20,
                    'POINTS': 30
            },
                {
                    'AC': 25,
                    'POINTS': 60
            },
                {
                    'AC': 40,
                    'POINTS': 100
            },
                {
                    'FEATURED': True,
                    'POINTS': 1050
            },
        ]
}





async def donateAC(ctx, userId, amount):
    AC = amount['AC']
    
    postId   = None
    postType = None
    postName = None
    
    blogs = await ctx.client.get_user_blogs(userId)
    wikis = await ctx.client.get_user_wikis(userId)
    if not wikis and not blogs:
        await ctx.send("No se encontraron blogs para donar :c. Selecciones otra opción o vuelva a ingresarla cuando tenga donde donar.")
        return False

    user = db.getUserData(None, userId)

    donation = getDonationList(AC)
    hasDonated = False
 
    if not hasDonated:
        for blog in blogs:
            for i in donation:
                if hasDonated: break
                try:
                    await asyncio.sleep(3)
                    await ctx.client.send_coins(coins=i, blog_id=blog.blogId)
                    hasDonated  = True
                    postName    = blog.title
                    postType    = 'blog'
                    break
                except Exception as e :
                    pass 

    if not hasDonated:
        for wiki in wikis:
            for i in donation:
                if hasDonated: break
                try:
                    await asyncio.sleep(3)
                    await ctx.client.send_coins(coins=i, object_id=wiki.itemId)
                    hasDonated  = True
                    postName    = wiki.label
                    postType    = 'wiki'
                except Exception as e :
                    pass
            break
    
    if not hasDonated:
        await ctx.send(f"Ha ocurrido un error donando. Asegure tener un blog o wiki donde donar. Seleccione otra opción o ingrese la misma nuevamente.")
        return False
    
    await ctx.send(f"Han sido donados {AC} AC a {postFormatString(postType, postName)}")
    return True


async def donatePoints(ctx, userId, amount):
    points = amount['POINTS']
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

async def giveRewards(ctx, level, userId=None):
    print('giving reward')
    ndcId   = ctx.msg.ndcId
    if userId is None: userId = ctx.msg.author.uid

    if ndcId == 9999:
        r = None
        amount = rewardTable[9999][level]
        await ctx.send("En esta comunidad, los premios debe escogerlos entre AC, o puntos de actividad. Puede recibir directamente el premio en metálico si acepta, o en cambio recibir puntos.\n\n-SI: Recibir el premio en AC\n-NO: Recibir el premio en puntos. ")
        confirmation = await utils.confirmation(ctx, ctx.msg.threadId, userId, ctx.msg.ndcId, timeout=False)
        if      confirmation is True    : r = await donateAC(ctx, userId, amount)
        elif    confirmation is False   : r = await donatePoints(ctx, userId, amount)

    else:
        amount = {'AC': level * 10}
        await donateAC(ctx, userId, amount)
    return


