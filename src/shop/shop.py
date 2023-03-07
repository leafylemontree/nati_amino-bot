from src import utils
from src import database
import asyncio
from . import helpers

VERSION = "0.5.2"

async def back(ctx, aw):
    await ctx.send("Vuelva pronto u.u")
    return True

async def buy(ctx, aw):
    await ctx.send("Próximamente")
    return False

async def sell2(ctx, aw):
    postId   = None
    postType = None
    postName = None
    
    blogs = await ctx.client.get_user_blogs(ctx.msg.author.uid)
    wikis = await ctx.client.get_user_wikis(ctx.msg.author.uid)
    if      wikis:
        postType = "wiki"
        postId   = wikis[0].itemId
        postName = wikis[0].label
    elif    blogs:
        postType = "blog"
        postId   = blogs[0].blogId
        postName = blogs[0].title
    else         :
        await ctx.send("No se encontraron blogs para donar :c")
        return True
    user = database.db.getUserData(ctx.msg.author)

    text = ctx.msg.content
    amount = None
    try:    amount = int(text)
    except: pass

    if amount is None:
        amount = user.points // 100
    
    if amount < 1:
        await ctx.send("Debe ingresar una cantidad mayor a 0")
        return True
    
    if amount > (user.points // 100):
        await ctx.send(f"Ha ingresado una cantidad mayor a los puntos que tiene, se le cambiará a {user.points // 100} AC.")
        amount = user.points // 100
    

    donation = helpers.getDonationList(amount)
    for i in donation:
        try:
            await asyncio.sleep(3)
            if   postType == "blog": await ctx.client.send_coins(coins=i, blog_id=postId)
            elif postType == "wiki": await ctx.client.send_coins(coins=i, object_id=postId)
        except Exception as e :
            print(e)
            await ctx.send("Ha ocurrido un error :c")
            return True
    
    database.db.modifyRecord(43, ctx.msg.author, amount * -100)
    await ctx.send(f"""
Ha cambiado exitosamente {amount * 100} por {amount} AC
Han sido donados a {helpers.postFormatString(postType, postName)}

La tienda ha sido cerrada por su seguridad""")
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
│☪჻│๑ ✎ Para compra r AC,
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
@utils.waitForMessage(message="-PIRAMIDE",  callback=pyramid)
@utils.waitForMessage(message="-BANCA",     callback=account)
@utils.waitForMessage(message="-SALIR",     callback=back)
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
░⃟⃟﹫◌*̥₊❀ -pirámide
░⃟⃟﹫◌*̥₊❀ -banca
░⃟⃟﹫◌*̥₊❀ -salir

. . . . . .˚ೃ(‧₊ Nati {VERSION}˚.ꦿ)⨾ੈ . . . . . .
︶︶︶︶︶︶︶︶︶︶︶︶︶︶︶""")
    return
