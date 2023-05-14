import cairocffi        as cairo 
from src.images.funcs import putText
from src.database import db
import datetime
import io
import edamino
import time
from aiofile import AIOFile
from src          import objects

base    = cairo.ImageSurface.create_from_png("media/templates/card_wallet_base.png")
base2   = cairo.ImageSurface.create_from_png("media/templates/inventory_new.png")

async def walletCard(ctx):
    
    userDB  = db.getUserData(ctx.msg.author)
    dt      = datetime.datetime.now()

    class Data:
        nickname = ctx.msg.author.nickname
        alias    = userDB.alias
        userId   = ctx.msg.author.uid
        points   = userDB.points
        month    = dt.month
        day      = dt.day
    
    imgIO   = io.BytesIO()
    image   = cairo.ImageSurface(cairo.FORMAT_RGB24, 1024, 512, )
    ct      = cairo.Context(image)
    
    ct.save()
    ct.set_source_surface(base)
    ct.paint()
    ct.restore()

    ct.set_source_rgb(0.156, 0.136, 0.53)
    ct.move_to(80, 88)
    putText(ct,
            text=Data.nickname[:20],
            size=36,
            width=448,
            height=80,
            font="MADE TOMMY")

    ct.move_to(100, 172)
    putText(ct,
            text=Data.alias[:20],
            size=28,
            width=288,
            height=80,
            font="MADE TOMMY")
    
    ct.move_to(704, 304)
    putText(ct,
            text=Data.points,
            size=68,
            width=288,
            height=80,
            font="Heavitas")

    ct.set_source_rgb(0.8125, 0.814, 0.945)
    ct.move_to(72, 288)
    putText(ct,
            text=Data.userId,
            size=24,
            width=400,
            height=800,
            font="Heavitas")
    
    ct.move_to(80, 400)
    putText(ct,
            text=f'{Data.day}/{Data.month}',
            size=36,
            width=288,
            height=80,
            font="Heavitas")

    ct.stroke()
    out = io.BytesIO()
    image.write_to_png(imgIO)
    imgIO.seek(0)
    img = imgIO.read()

    linkSnippet = edamino.api.LinkSnippet(
                link=f'ndc://x{ctx.msg.ndcId}/user-profile/{ctx.msg.author.uid}',
                media_upload_value=img,
            )

    await ctx.client.send_message(message=f"[ci]¡Este es el monedero de\n[ci]{ctx.msg.author.nickname}!", chat_id=ctx.msg.threadId ,link_snippets_list=[linkSnippet])
    return


async def inventoryNewItemCard(ctx, objectId, amount):
    
    objectProps = objects.inventoryAPI.properties(objectId)

    imgIO   = io.BytesIO()
    image   = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1024, 512)
    ct      = cairo.Context(image)
    
    ct.save()
    ct.set_source_surface(base2)
    ct.paint()
    ct.restore()

    glare   = cairo.ImageSurface.create_from_png(f"media/templates/items/glare{objectProps.rarity}.png")
    ct.save()
    ct.translate(80, 64)
    ct.set_source_surface(glare)
    ct.paint()
    ct.restore()

    item   = cairo.ImageSurface.create_from_png(f"media/templates/items/item_{str(objectId).zfill(3)}.png")
    ct.save()
    ct.translate(132, 112)
    ct.set_source_surface(item)
    ct.paint()
    ct.restore()

    ct.set_source_rgba(0.114, 0.105, 0.273, 0.618)
    ct.move_to(524, 160)
    putText(ct,
            text=objectProps.name,
            size=42,
            width=432,
            height=128,
            font="Heavitas")


    ct.set_source_rgba(0.285, 0.262, 0.727, 1)
    ct.move_to(512, 144)
    putText(ct,
            text=objectProps.name,
            size=42,
            width=432,
            height=128,
            font="Heavitas")

    ct.set_source_rgba(0.442, 0.496, 0.816, 1)
    ct.move_to(512, 296)
    putText(ct,
            text=objectProps.description,
            size=42,
            width=432,
            height=128,
            font="Lemon Juice")
    
    ct.stroke()
    out = io.BytesIO()
    image.write_to_png(imgIO)
    imgIO.seek(0)
    img = imgIO.read()

    linkSnippet = edamino.api.LinkSnippet(
                link=f'ndc://x{ctx.msg.ndcId}/user-profile/{ctx.msg.author.uid}',
                media_upload_value=img,
            )
    
    return linkSnippet
