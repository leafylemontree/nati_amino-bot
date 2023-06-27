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
base3   = cairo.ImageSurface.create_from_png("media/templates/multiitem.png")

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


async def multiitem(ctx, data):
    imgIO   = io.BytesIO()
    image   = cairo.ImageSurface(cairo.FORMAT_RGB24, 1536, 1728)
    ct      = cairo.Context(image)
    
    ct.save()
    ct.set_source_surface(base3)
    ct.paint()
    ct.restore()


    def drawItem(ct, x, y, item, amount):
        itemProps = objects.inventoryAPI.properties(item)
        if   itemProps.rarity == 1: ct.set_source_rgb(0.13, 0.54, 0.10)
        elif itemProps.rarity == 2: ct.set_source_rgb(0.18, 0.42, 0.90)
        elif itemProps.rarity == 3: ct.set_source_rgb(0.58, 0.18, 0.90)
        elif itemProps.rarity == 4: ct.set_source_rgb(0.90, 0.50, 0.18)
        else                      : ct.set_source_rgb(0.71, 0.71, 0.71)

        ct.rectangle(x, y, 320, 320)
        ct.fill()
        ct.stroke()
        
        itemImg = cairo.ImageSurface.create_from_png(f"media/templates/items/item_{str(item).zfill(3)}.png")
        ct.save()
        ct.translate(x + 16, y + 16)
        ct.set_source_surface(itemImg)
        ct.paint()
        ct.restore()
        ct.stroke()

        ct.set_source_rgb(1, 1, 1)
        ct.move_to(x + 160, y + 240)
        putText(ct,
                text="x",
                size=56,
                width=64,
                height=128,
                font="Heavitas")
        ct.stroke()
        ct.move_to(x + 224, y + 224)
        putText(ct,
                text=str(amount),
                size=72,
                width=128,
                height=128,
                font="Heavitas")
        ct.stroke()
        ct.move_to(x, y + 336)
        ct.set_source_rgb(0.90, 0.72, 0.24)
        putText(ct,
                text=itemProps.name,
                size=30,
                width=320,
                height=96,
                align="CENTER",
                font="Heavitas")
        ct.stroke()

    l = len(data)
    for i,(item,amount) in enumerate(data.items()):
        n, m = divmod(i, 4)
        w    = 3 if (l - n * 4) > 4 else (l - n * 4 - 1)
        x    = 12 * 64 - (((w % 4) + 1) * (10 * 16) + (w % 4) * 16) + m * ((20 * 16) + 32)
        y    = 368 + n * 7 * 64
        drawItem(ct, x, y, item, amount)
    
    ct.stroke()
    out = io.BytesIO()
    image.write_to_png(imgIO)
    imgIO.seek(0)
    img = imgIO.read()

    from src.imageSend import send_image
    await send_image(ctx, image=img)


