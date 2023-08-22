import cairocffi        as cairo 
from src.images.funcs import putText, rounded
from src.database import db
import io
from src import utils
import edamino
import math

base    = cairo.ImageSurface.create_from_png("media/templates/exp_card.png")

a = 75
b = 1.2

def getLevel(exp):
    return math.floor( math.log(1  - exp * (1 - b) / a) / math.log(b) )

def getExp(level):
    return math.floor(a * (1 - b ** level) / (1 - b))

def getExpLevel(level):
    minExp = getExp(level)
    maxExp = getExp(level + 1)
    return (minExp, maxExp)

def barFill(minExp, exp, maxExp):
    return (exp - minExp) / (maxExp - minExp)

@utils.userTracker("exp")
async def expCardCreate(ctx, message=True):
    imgIO   = io.BytesIO()
    image   = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1024, 448, )
    ct      = cairo.Context(image)
    isGlobal= True if ctx.msg.content.upper().find("-GLOBAL") != -1 else False

    exp     = db.getUserExp(ctx.msg.ndcId, ctx.msg.author.uid, isGlobal=isGlobal)
    level   = getLevel(exp)
    limits  = getExpLevel(level)

    profile   = await utils.getImageBytes(ctx, ctx.msg.author.icon)
    pfp       = cairo.ImageSurface.create_from_png(profile)
    px,py     = pfp.get_width(), pfp.get_height()
    scale     = 448/py if px > py else 448/px

    ct.save()
    ct.translate(0, 0)
    ct.scale(scale, scale)
    ct.set_source_surface(pfp)
    ct.paint()
    ct.restore()

    ct.save()
    ct.set_source_surface(base)
    ct.paint()
    ct.restore()

    ct.set_source_rgba(0, 0, 0, 0.23)
    ct.move_to(14.5 * 32 + 6, 3.25 * 32 + 6)
    putText(ct, text=ctx.msg.author.nickname, size=32, width=16 * 32, height= 3 * 32, align="CENTER", font="Heavitas")
    ct.stroke()
    ct.set_source_rgba(1, 1, 1, 1)
    ct.move_to(14.5 * 32, 3.25 * 32)
    putText(ct, text=ctx.msg.author.nickname, size=32, width=16 * 32, height= 3 * 32, align="CENTER", font="Heavitas")
    ct.stroke()


    ct.set_source_rgba(0.66, 0.31, 0.59, 1)

    ct.move_to(15 * 32, 6.75 * 32)
    putText(ct, text=f"Nivel {level + 1}", size=30, width=15 * 32, height= 3 * 32, align="CENTER", font="MADE TOMMY")
    ct.stroke()

    ct.move_to(14 * 32, 9.75 * 32)
    putText(ct, text=f"{exp}", size=30, width=4 * 32, height=1 * 32, align="CENTER", font="Heavitas")
    ct.stroke()
    ct.move_to(27.5 * 32, 9.75 * 32)
    putText(ct, text=f"{limits[1]}", size=30, width=4 * 32, height=1 * 32, align="CENTER", font="Heavitas")
    ct.stroke()

    rounded(ct, 15 * 32 + 4, 8.25 * 32 + 4, (15 * 32 - 8) * barFill(limits[0], exp, limits[1]), 32 - 8, 12)
    ct.fill()
    ct.stroke()

    ct.stroke()
    out = io.BytesIO()
    image.write_to_png(imgIO)
    imgIO.seek(0)
    img = imgIO.read()

    linkSnippet = edamino.api.LinkSnippet(
                link=f'ndc://x{ctx.msg.ndcId}/user-profile/{ctx.msg.author.uid}',
                media_upload_value=img,
            )

    msg =  "[c]"
    if message is True: msg = f"[ci]¡Felicidades! {ctx.msg.author.nickname} ha subido a nivel {level + 1}."
    
    await ctx.client.send_message(message=msg, chat_id=ctx.msg.threadId ,link_snippets_list=[linkSnippet])

