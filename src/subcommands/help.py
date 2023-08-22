from src import objects
from src.text import text
from src.imageSend import send_image
from src import utils
from aiofile import AIOFile

def o_help(com, comId):
        msg = com.split(" ")
        print(msg)
        
        if ( (len(msg) == 1) & (comId == 112646170) ):            return objects.Reply(text['help']['default'].replace("Nati", "Artemis"), False)
        elif ( (len(msg) == 1) & (comId == 215907772) ):          return objects.Reply(text['help']['default'].replace("Nati", "Emma"), False)
        elif ( (len(msg) == 1) & (comId == 139175768) ):          return objects.Reply(text['help']['default'].replace("Nati", "Anya"), False)
        elif      len(msg) == 1:          return objects.Reply(text['help']['default'])

        msg = msg[1].lower()

        if msg in text['help']  :   return objects.Reply(text['help'][msg], False)
        return                                 objects.Reply("No existe este comando por el momento, :c", False)




pages = {
    "interaccion"   : 3,
    "imagenes"      : 1,
    "juegos"        : 1,
    "matematicas"   : 1,
    "moderacion"    : 2,
    "help"          : 0
}


async def showPicture(ctx, insData):
    filename = f'media/help/{insData["type"]}{insData["page"] if insData["type"] != "help" else ""}.png'
    async with AIOFile(filename, 'rb') as f:
        img = await f.read()
        await send_image(ctx, img)
    

async def rewindPage(ctx, ins):
    page    = ins.data['page']
    hType   = ins.data['type']

    if    page <= 1             : pass
    else                        : ins.data['page'] -= 1
    await showPicture(ctx, ins.data)
    return

async def advancePage(ctx, ins):
    page    = ins.data['page']
    hType   = ins.data['type']

    if    page >= pages[hType]  : pass
    else                        : ins.data['page'] += 1
    await showPicture(ctx, ins.data)
    return

async def quitPage(ctx, ins):
    return True

async def listener(ctx, ins):
    com = ctx.msg.content.upper()
    if com.find("-AV") == 0     : r = await advancePage(ctx, ins)
    elif com.find("-RE") == 0   : r = await rewindPage(ctx, ins)
    else                        : r = await quitPage(ctx, ins)
    return r

@utils.waitForMessage(message="*", callback=listener)
@utils.userTracker("help")
async def _help(ctx, hType=None):
    com = ctx.msg.content.upper().split(" ")
    if len(com) > 1 and hType is None:
        text = o_help(" ".join(com), ctx.msg.ndcId)
        await ctx.reply(text.msg)
    
    if hType is None:   h = "help"
    else            :   h = hType.lower()   

    insData = {
                "type"  :   h,
                "page"  :   1
            }
   
    await showPicture(ctx, insData)
    data = insData if h != "help" else -1
    return data
