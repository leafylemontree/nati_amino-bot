from src import utils
from src import database
import asyncio
from . import helpers
from src.shop.donations import lootboxes
from src.database import db
from src import objects
from src.challenges.rewards import donateAC

VERSION = "0.5.99.5"

async def back(ctx, aw):
    await ctx.send("Vuelva pronto u.u")
    return True


async def buy2(ctx, aw):
    aw.data += 1
    if aw.data > 3: return True

    msg = ctx.msg.content.upper().split(" ")

    if msg[0].find("-ITEM") != -1:
        if len(msg) < 3:
            await ctx.send("Debe ingresarlo de la siguiente manera: -item (posición) (cantidad)")
            return False

        inventory = await db.getUserInventory(ctx.msg.author.uid)
        inventoryIndex  = None
        inventoryAmount = None

        try:    inventoryIndex = int(msg[1])
        except: await ctx.send("La posición del objeto no es válida");  return False

        try:    inventoryAmount= int(msg[2])
        except: await ctx.send("La cantidad ingresada no es válida");  return False
        
        if inventoryIndex < 0: inventoryIndex = 1
        if inventoryAmount< 1: inventoryAmount= 1
        objectId = None
        objectAm = None

        try:
            objectId    = inventory.data[inventoryIndex - 1].objectId
            objectAm    = inventory.data[inventoryIndex - 1].amount
            if inventoryAmount > objectAm: inventoryAmount = objectAm
        except Exception as e: print(e); await ctx.send("No existe un item con esa posición");  return False

        inventory.add(objectId, -1 * inventoryAmount)
        await db.setUserInventory(inventory) 

        props   = objects.inventoryAPI.properties(objectId)
        points  = inventoryAmount * props.value
        db.modifyRecord(43, ctx.msg.author, points)
    
        await ctx.send(f"Ha cambiado {inventoryAmount}x {props.name} por {points} puntos.\n\nPuede seguir comprando, o cerrar la tienda con -salir.")
    elif msg[0].find("-S") != -1:
        await ctx.send("Vuelva pronto, u.u.")
        return True
    else:
        await ctx.send("No se reconoce este subcomando. Pruebe con -item 0 0")
    return




@utils.waitForMessage(message='*', callback=buy2)
async def buy(ctx, aw):
    user = database.db.getUserData(ctx.msg.author)
    await ctx.send(f"""
⚘ 𝐂𝐨𝐦𝐩𝐫𝐚 𝐝𝐞 𝐏𝐮𝐧𝐭𝐨𝐬 ⚘
﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́ ༅˻˳˯ₑ❛░⃟ ⃟°˟̫· · · ·

❛꙰̥᪶༘᪵ꪾꯪ՚̸꙰⃢🌼⃟⃟༘ꪳ⨾ 𝐂𝐚𝐦𝐛𝐢𝐨 𝐝𝐞 𝐨𝐛𝐣𝐞𝐭𝐨𝐬 𝐚 𝐩𝐮𝐧𝐭𝐨𝐬
❛꙰̥᪶༘᪵ꪾꯪ՚̸꙰⃢🌼⃟⃟༘ꪳ⨾ 𝐔𝐭𝐢𝐥𝐢𝐜𝐞 --𝐢𝐧𝐯𝐞𝐧𝐭𝐚𝐫𝐢𝐨 𝐩𝐚𝐫𝐚 𝐯𝐞𝐫
❛꙰̥᪶༘᪵ꪾꯪ՚̸꙰⃢🌼⃟⃟༘ꪳ⨾ 𝐜𝐮𝐚𝐥𝐞𝐬 𝐭𝐢𝐞𝐧𝐞

᪥ 𝐔𝐬𝐭𝐞𝐝 𝐩𝐨𝐬𝐞𝐞: {user.points} puntos ᪥
│☪჻╭———————————
│☪჻│๑ ✎ Para vender un item
│☪჻│๑ ✎ ingrese -item, luego el
│☪჻│๑ ✎ número y la cantidad
│☪჻│๑ ✎-item 0 0
│☪჻│๑ ✎
│☪჻│๑ ✎ Para salir, solo ponga
│☪჻│๑ ✎ -salir
╰ ☪ ╯

. . . . . .˚ೃ(‧₊ Nati {VERSION}˚.ꦿ)⨾ੈ . . . . . .
︶︶︶︶︶︶︶︶︶︶︶︶︶︶︶""")
    return 0

async def sell2(ctx, aw):
    postId   = None
    postType = None
    postName = None
    
    blogs = await ctx.client.get_user_blogs(ctx.msg.author.uid)
    wikis = await ctx.client.get_user_wikis(ctx.msg.author.uid)
    if not wikis and not blogs:
        await ctx.send("No se encontraron blogs para donar :c")
        return True
    user = database.db.getUserData(ctx.msg.author)

    if user.points < 0:
        await ctx.send("No se pueden cambiar puntos a AC cuando tiene una cantidad negativa de puntos.")
        return True

    text = ctx.msg.content
    amount = None
    try:    amount = int(text)
    except: pass

    if amount is None:
        amount = user.points // 100
    
    if amount < 1:
        await ctx.send("Debe ingresar una cantidad mayor a 0")
        return False
    
    if amount > (user.points // 100):
        await ctx.send(f"Ha ingresado una cantidad mayor a los puntos que tiene, se le cambiará a {user.points // 100} AC.")
        amount = user.points // 100

    r = await donateAC(ctx, ctx.msg.author.uid, amount)
    print("Donation response:", r, amount)
    if r is not None:
        database.db.modifyRecord(43, ctx.msg.author, amount * -100)
        await ctx.send(f"""
Ha cambiado exitosamente {amount * 100} por {amount} AC
Han sido donados a {helpers.postFormatString(postType, postName)}

La tienda ha sido cerrada por su seguridad""")
    elif r is False:
        await ctx.send("Ha ocurrido un error donando. Puede intentar recuperar la recompensa poniendo --reclamar-recompensas")
    return True

@utils.waitForMessage(message='*', callback=sell2, instantKill=True)
async def sell(ctx, aw):
    user = database.db.getUserData(ctx.msg.author)
    await ctx.send(f"""
[b]   ⚘ 𝐕𝐞𝐧𝐭𝐚 𝐝𝐞 𝐏𝐮𝐧𝐭𝐨𝐬 ⚘
﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́ ༅˻˳˯ₑ❛░⃟ ⃟°˟̫· · · ·

❛꙰̥᪶༘᪵ꪾꯪ՚̸꙰⃢🌼⃟⃟༘ꪳ⨾ 𝐂𝐚𝐦𝐛𝐢𝐨 𝐝𝐞 𝐩𝐮𝐧𝐭𝐨𝐬 𝐚 𝐀𝐂
❛꙰̥᪶༘᪵ꪾꯪ՚̸꙰⃢🌼⃟⃟༘ꪳ⨾ 1 AC = 100 puntos

᪥ 𝐔𝐬𝐭𝐞𝐝 𝐩𝐨𝐬𝐞𝐞: {user.points} puntos ᪥
│☪჻╭———————————
│☪჻│๑ ✎ Para comprar AC,
│☪჻│๑ ✎ ingrese la cantidad
│☪჻│๑ ✎ de monedas a cambiar
│☪჻│๑ ✎
│☪჻│๑ ✎ Para salir, solo ponga
│☪჻│๑ ✎ -salir
╰ ☪ ╯

. . . . . .˚ೃ(‧₊ Nati {VERSION}˚.ꦿ)⨾ੈ . . . . . .
︶︶︶︶︶︶︶︶︶︶︶︶︶︶︶""")
    return False



async def pyramid(ctx, aw):
    await ctx.send("Próximamente")
    return False

async def account(ctx, aw):
    user    = database.db.getUserData(ctx.msg.author)
    coins   = user.points
    
    await ctx.send(f"""
[b]    ⚘ 𝐃𝐚𝐭𝐨𝐬 𝐝𝐞 𝐂𝐮𝐞𝐧𝐭𝐚 ⚘
﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́ ༅˻˳˯ₑ❛░⃟ ⃟°˟̫· · · ·

.......🌸/░ 𝐍𝐨𝐦𝐛𝐫𝐞
..⁛᪥  {ctx.msg.author.nickname}

.......🌸/░ 𝐀𝐥𝐢𝐚𝐬
..⁛᪥  {user.alias}

.......🌸/░ 𝐒𝐚𝐥𝐝𝐨
..⁛᪥  {coins} puntos

. . . . . .˚ೃ(‧₊ Nati {VERSION}˚.ꦿ)⨾ੈ . . . . . .
︶︶︶︶︶︶︶︶︶︶︶︶︶︶︶""")
    return False


@utils.waitForMessage(message="-COMPRAR",   callback=buy)
@utils.waitForMessage(message="-VENDER",    callback=sell)
@utils.waitForMessage(message="-CAJAS",     callback=lootboxes)
@utils.waitForMessage(message="-PIRAMIDE",  callback=pyramid)
@utils.waitForMessage(message="-BANCA",     callback=account)
@utils.waitForMessage(message="-SALIR",     callback=back)
@utils.userTracker("tienda")
async def shop(ctx):
    if ctx.msg.content.upper().find("-BANCA") != -1:
        return await account(ctx, None)
    await ctx.send(f"""
[b]⚘ 𝐓𝐢𝐞𝐧𝐝𝐚 𝐍𝐚𝐭𝐢 ⚘
﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́ ༅˻˳˯ₑ❛░⃟ ⃟°˟̫· · · ·

⌒͙⌒͙⌒͙˚ꫬꪳ❛ꯪꪴ𐨆᪥⃟┊ ¡𝐁𝐢𝐞𝐧𝐯𝐞𝐧𝐢𝐝𝐨𝐬 𝐚 𝐥𝐚 𝐭𝐢𝐞𝐧𝐝𝐚
⌒͙⌒͙⌒͙˚ꫬꪳ❛ꯪꪴ𐨆᪥⃟┊ 𝐝𝐞 𝐍𝐚𝐭𝐢!
⌒͙⌒͙⌒͙˚ꫬꪳ❛ꯪꪴ𐨆᪥⃟┊ Su bot de confianza les
⌒͙⌒͙⌒͙˚ꫬꪳ❛ꯪꪴ𐨆᪥⃟┊ tiene unas ofertas muy
⌒͙⌒͙⌒͙˚ꫬꪳ❛ꯪꪴ𐨆᪥⃟┊ grandes para quienes
⌒͙⌒͙⌒͙˚ꫬꪳ❛ꯪꪴ𐨆᪥⃟┊ osen a confiar en mí.
⌒͙⌒͙⌒͙˚ꫬꪳ❛ꯪꪴ𐨆᪥⃟┊ Así que vamos, son li-
⌒͙⌒͙⌒͙˚ꫬꪳ❛ꯪꪴ𐨆᪥⃟┊ bres de revisar mis
⌒͙⌒͙⌒͙˚ꫬꪳ❛ꯪꪴ𐨆᪥⃟┊ precios, uwu.
⌒͙⌒͙⌒͙˚ꫬꪳ❛ꯪꪴ𐨆᪥⃟╰┈━═┈━═┈━═┈━ꔚ⃢⃟ೃ༄

⃫᪥⚘⁛ 𝐂𝐨𝐦𝐚𝐧𝐝𝐨𝐬 ⁛⚘᪥⃫
︿︿︿︿︿︿︿︿(🌸)︿︿︿︿︿︿︿︿

░⃟⃟﹫◌*̥₊❀ -comprar
░⃟⃟﹫◌*̥₊❀ -vender
░⃟⃟﹫◌*̥₊❀ -cajas
░⃟⃟﹫◌*̥₊❀ -pirámide
░⃟⃟﹫◌*̥₊❀ -banca
░⃟⃟﹫◌*̥₊❀ -salir

. . . . . .˚ೃ(‧₊ Nati {VERSION}˚.ꦿ)⨾ੈ . . . . . .
︶︶︶︶︶︶︶︶︶︶︶︶︶︶︶""")
    return
