import cairocffi        as cairo 
from src.database import db
import io
from src.images.funcs import putText
from src import objects
from src.pet import helpers
import edamino
import random
from src.shop.images import multiitem

pet_card        = cairo.ImageSurface.create_from_png("media/templates/pet/stats_card.png")
give_item_card  = cairo.ImageSurface.create_from_png("media/templates/pet/give_item_card.png")

def maximizePet(pet):
    if pet.health       > pet.maxHealth :   pet.health      = pet.maxHealth
    if pet.happiness    > 10000         :   pet.happiness   = 10000
    if pet.energy       > 10000         :   pet.energy      = 10000
    if pet.care         > 10000         :   pet.care        = 10000
    if pet.hunger       > 10000         :   pet.hunger      = 10000
    if pet.thirst       > 10000         :   pet.thirst      = 10000

    if pet.health       < 0             :   pet.health      = 0
    if pet.happiness    < 0             :   pet.happiness   = 0
    if pet.energy       < 0             :   pet.energy      = 0
    if pet.care         < 0             :   pet.care        = 0
    if pet.hunger       < 0             :   pet.hunger      = 0
    if pet.thirst       < 0             :   pet.thirst      = 0
    return

async def info(ctx):

    pet = db.getNatiPetData(ctx.msg.ndcId)
    maximizePet(pet)

    nati_sticker = helpers.getStickerValue(pet)

    imageFile      = io.BytesIO()
    image     = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1024, 1024)
    ct        = cairo.Context(image)
    
    ct.save()
    ct.set_source_surface(pet_card)
    ct.paint()
    ct.restore()

    scale = 1
    nati = cairo.ImageSurface.create_from_png(f"media/templates/pet/stickers/nati_base_{nati_sticker}.png")
    ct.save()
    ct.translate(592, 96)
    ct.scale(scale, scale)
    ct.set_source_surface(nati)
    ct.paint()
    ct.restore()

    ox = 12

    ct.set_source_rgb(0.62, 0.63, 0.70)
    ct.move_to(328+ox, 252)
    putText(ct,
            text=str(pet.ndcId),
            size=24, width=(560-328-24), height=(288-232),
            align='RIGHT', font='Heavitas')
    ct.stroke()

    ct.move_to(328+ox, 324)
    putText(ct,
            text=str(helpers.getLevelFromEXP(pet.exp)),
            size=24, width=(560-328-24), height=(288-232),
            align='RIGHT', font='Heavitas')
    ct.stroke()

    ct.move_to(328+ox, 396)
    putText(ct,
            text=str(pet.exp),
            size=24, width=(560-328-24), height=(288-232),
            align='RIGHT', font='Heavitas')
    ct.stroke()
    
    x = 214
    h = 35
    w = 344
    o = 8

    ct.set_source_rgb(0.78, 0, 0)
    ct.rectangle(x, 462, int(w*(pet.health / pet.maxHealth)), h)
    ct.fill()
    ct.stroke()
    ct.set_source_rgb(1, 1 ,1)
    ct.move_to(x, 462+o)
    putText(ct, text=f"{(pet.health / 100):.2f}", size=18, width=w, height=h, align='CENTER', font='Heavitas')
    ct.stroke()

    ct.set_source_rgb(0.84, 0.82, 0)
    ct.rectangle(x, 510, int(w*(pet.happiness / 10000)), h)
    ct.fill()
    ct.stroke()
    ct.set_source_rgb(1, 1 ,1)
    ct.move_to(x, 510+o)
    putText(ct, text=f"{(pet.happiness / 100):.2f}", size=18, width=w, height=h, align='CENTER', font='Heavitas')
    ct.stroke()

    ct.set_source_rgb(0, 0.78, 0.11)
    ct.rectangle(x, 558, int(w*(pet.energy / 10000)), h)
    ct.fill()
    ct.stroke()
    ct.set_source_rgb(1, 1 ,1)
    ct.move_to(x, 558+o)
    putText(ct, text=f"{(pet.energy / 100):.2f}", size=18, width=w, height=h, align='CENTER', font='Heavitas')
    ct.stroke()

    ct.set_source_rgb(0.86, 0, 0.64)
    ct.rectangle(x, 606, int(w*(pet.care / 10000)), h)
    ct.fill()
    ct.stroke()
    ct.set_source_rgb(1, 1 ,1)
    ct.move_to(x, 606+o)
    putText(ct, text=f"{(pet.care / 100):.2f}", size=18, width=w, height=h, align='CENTER', font='Heavitas')
    ct.stroke()

    ct.set_source_rgb(0.92, 0.62, 0)
    ct.rectangle(x, 654, int(w*(pet.hunger / 10000)), h)
    ct.fill()
    ct.stroke()
    ct.set_source_rgb(1, 1 ,1)
    ct.move_to(x, 654+o)
    putText(ct, text=f"{(pet.hunger / 100):.2f}", size=18, width=w, height=h, align='CENTER', font='Heavitas')
    ct.stroke()

    ct.set_source_rgb(0, 0.48, 0.78)
    ct.rectangle(x, 702, int(w*(pet.thirst / 10000)), h)
    ct.fill()
    ct.stroke()
    ct.set_source_rgb(1, 1 ,1)
    ct.move_to(x, 702+o)
    putText(ct, text=f"{(pet.thirst / 100):.2f}", size=18, width=w, height=h, align='CENTER', font='Heavitas')
    ct.stroke()

    ct.stroke()
    image.write_to_png(imageFile)
    imageFile.seek(0)
    img = imageFile.read()

    from src.imageSend import send_image
    await send_image(ctx, image=img)
    return

async def initPet(ctx):
    pet = db.initNatiPet(ctx.msg.ndcId)
    return await ctx.send("Mascota creada")


async def giveItem(ctx):
    msg = ctx.msg.content.split(" ")
    if len(msg) < 2:    return await ctx.send("Debe ingresar el item que quiere darle a Nati. Consulte el inventario con --inventario e ingrese el número de la posición que sale a la izquierda.")

    item = -1
    try:
        item = int(msg[1])
        item -= 1
        if(item < 0): return await ctx.send("No existe un item en esta posición en tu inventario.")
    except ValueError:
        return await ctx.send("El valor ingresado como parámetro no es un número")

    pet = db.getNatiPetData(ctx.msg.ndcId)
    if pet.happiness    > 10000     :   pet.happiness   = 10000
    if pet.energy       > 10000     :   pet.energy      = 10000
    if pet.care         > 10000     :   pet.care        = 10000
    if pet.hunger       > 10000     :   pet.hunger      = 10000
    if pet.thirst       > 10000     :   pet.thirst      = 10000

    inventory   = await db.getUserInventory(ctx.msg.author.uid)
    if(item > inventory.length) : return await ctx.send("No existe un item con esta posición en tu inventario.")
    itemId      = inventory.data[item].objectId
    itemData = objects.inventoryAPI.properties(itemId)
    if itemData.usable is False:    return await ctx.send(f"Lo siento, pero {itemData.name} no puede ser utilizado, :c.")

    inventory.add(itemId, -1)
    await db.setUserInventory(inventory)

    data = {
        "exp"       : helpers.getEXPGain(itemData),
        "health"    : itemData.health,
        "happiness" : itemData.happiness,
        "energy"    : itemData.energy,
        "care"      : itemData.care,
        "hunger"    : itemData.hunger,
        "thirst"    : itemData.thirst,
        "effects"   : itemData.effects 
    }

    pet2 = db.updateMultipleNatiPet(ctx.msg.ndcId, data)
    if pet2.happiness    > 10000     :   pet2.happiness   = 10000
    if pet2.energy       > 10000     :   pet2.energy      = 10000
    if pet2.care         > 10000     :   pet2.care        = 10000
    if pet2.hunger       > 10000     :   pet2.hunger      = 10000
    if pet2.thirst       > 10000     :   pet2.thirst      = 10000

    imageFile = io.BytesIO()
    image     = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1024, 768)
    ct        = cairo.Context(image)
    
    ct.save()
    ct.set_source_surface(give_item_card)
    ct.paint()
    ct.restore()
    ct.stroke()
    
    itemImage = cairo.ImageSurface.create_from_png(f"media/templates/items/item_{str(itemId).zfill(3)}.png")
    ct.save()
    ct.translate(120, 288)
    ct.set_source_surface(itemImage)
    ct.paint()
    ct.restore()
    ct.stroke()

    ct.set_source_rgb(0.46, 0.49, 0.63)
    ct.move_to(48, 120)
    putText(ct, text=itemData.name, size=28, width=416, height=80, align='CENTER', font='Heavitas')

    def writeDesc(ct, y, old, change, new, minV=0, maxV=10000, x1=560, x2=976, scale=100):
        size    =  24
        width   = 112
        h       = 4

        ct.rectangle(x1+16, y+46, int(((new - minV)/ (maxV - minV)) * (x2-16 - x1-16)), h)
        ct.fill()
        ct.stroke()

        ct.move_to(((x2+x1-width)//2), y+8)
        if      change > 0:
            ct.set_source_rgb(0, 0.78, 0.11)
            change = f"+{(change/scale):.1f}"
        elif    change < 0:
            ct.set_source_rgb(0.78, 0, 0)
            change = f"{(change/scale):.1f}"
        else              :
            ct.set_source_rgb(0.46, 0.49, 0.63)
            change = f"{(change/scale):.1f}"

        putText(ct, text=change, size=size, width=width, height=48, align='CENTER', font='Heavitas')

        ct.set_source_rgb(0.46, 0.49, 0.63)
        ct.move_to(x1, y+8)
        putText(ct, text=f"{(old/scale):.1f}", size=size, width=width, height=48, align='LEFT', font='Heavitas')
        ct.stroke()
        ct.move_to(x2-width, y+8)
        putText(ct, text=f"{(new/scale):.1f}", size=size, width=width, height=48, align='RIGHT', font='Heavitas')
        ct.stroke()
        return

    ct.set_source_rgb(0.78, 0, 0)
    writeDesc(ct,  96, pet.health, itemData.health, pet2.health, maxV=pet2.maxHealth)
    ct.set_source_rgb(0.84, 0.82, 0)
    writeDesc(ct, 192, pet.happiness, itemData.happiness, pet2.happiness)
    ct.set_source_rgb(0, 0.78, 0.11)
    writeDesc(ct, 288, pet.energy, itemData.energy, pet2.energy)
    ct.set_source_rgb(0.86, 0, 0.64)
    writeDesc(ct, 384, pet.care, itemData.care, pet2.care)
    ct.set_source_rgb(0.91, 0.62, 0)
    writeDesc(ct, 480, pet.hunger, itemData.hunger, pet2.hunger)
    ct.set_source_rgb(0, 0.48, 0.78)
    writeDesc(ct, 576, pet.thirst, itemData.thirst, pet2.thirst)

    level   = helpers.getLevelFromEXP(pet2.exp)
    lowExp  = helpers.getExpBaseFromLevel(level)
    nextExp = helpers.getExpBaseFromLevel(level+1)

    ct.set_source_rgb(0.47, 0.21, 0.85)
    writeDesc(ct, 672, pet.exp, data['exp'], pet2.exp, x1=48, x2=976, minV=lowExp, maxV=nextExp, scale=1)

    ct.stroke()
    image.write_to_png(imageFile)
    imageFile.seek(0)
    img = imageFile.read()
    linkSnippet = edamino.api.LinkSnippet(
                link=f'ndc://x{ctx.msg.ndcId}/user-profile/{ctx.msg.author.uid}',
                media_upload_value=img,
            )

    await ctx.client.send_message(message=f"[ci]¡Dado 1x {itemData.name} a Nati!", chat_id=ctx.msg.threadId ,link_snippets_list=[linkSnippet])

    lv1 = helpers.getLevelFromEXP(pet.exp)
    lv2 = helpers.getLevelFromEXP(pet2.exp)
    if(lv2 > lv1):
        await ctx.send(f"¡Felicidades! Nati ha sudo al nivel {lv2} u.u.")
    return


def parseNumbers(msg):
    nums  = []
    words = msg.split(" ")
    for word in words:
        try:    nums.append(int(word))
        except ValueError: pass
    return nums

def lootGenerator(loot):
    rarity = 0
    lower  = 0
    upper  = 0

    items  = []
    for key,value in loot.items():
        if      key == "common"     : rarity = 0
        elif    key == "casual"     : rarity = 1
        elif    key == "rare"       : rarity = 2
        elif    key == "strange"    : rarity = 3
        elif    key == "legendary"  : rarity = 4
        else                        : rarity = -1
        print("Loot:", key, rarity, value)

        lower  = value["min"]
        upper  = value["max"]

        amount = lower + round(random.random() * (upper - lower))
        item   = None
        for a in range(amount):
            if rarity != -1 : item   = objects.inventoryAPI.getItemByRarity(rarity)
            else            : item   = objects.inventoryAPI.getRandomItem()
            if item is not None: items.append(item) 
    return items

async def updateInventoryLoot(ctx, inventory, items, LOOTBOX_ID, test=False):
    data = {}
    for item in items:
        if item not in tuple(data.keys()): data[item]  = 1
        else                             : data[item] += 1


    for item,amount in data.items():
        inventory.add(item, amount)

    inventory.add(LOOTBOX_ID, -1)
    if test is False:           await db.setUserInventory(inventory)
    await multiitem(ctx, data)
    return

async def open_lootBox_small(ctx, inventory, test=False):
    LOOTBOX_ID = 31
    if test is False:
        if inventory.exists(LOOTBOX_ID) < 1: return await ctx.send("NO posee esta caja, de alguna manera.")

    loot = {
        "casual": {
                "min": 1,
                "max": 2
            },
        "random": {
                "min": 0,
                "max": 2
            }
    }

    items = lootGenerator(loot)
    await updateInventoryLoot(ctx, inventory, items, LOOTBOX_ID, test=test)
    return


async def open_lootBox_medium(ctx, inventory, test=False):
    LOOTBOX_ID = 32
    if test is False:
        if inventory.exists(LOOTBOX_ID) < 1: return await ctx.send("NO posee esta caja, de alguna manera.")

    loot = {
        "rare": {
                "min": 1,
                "max": 2
            },
        "casual": {
                "min": 0,
                "max": 2
            },
        "random": {
                "min": 0,
                "max": 2
            }
    }

    items = lootGenerator(loot)
    await updateInventoryLoot(ctx, inventory, items, LOOTBOX_ID, test=test)
    return

async def open_lootBox_large(ctx, inventory, test=False):
    LOOTBOX_ID = 33
    if test is False:
        if inventory.exists(LOOTBOX_ID) < 1: return await ctx.send("NO posee esta caja, de alguna manera.")

    loot = {
        "strange": {
                "min": 1,
                "max": 2
            },
        "rare": {
                "min": 0,
                "max": 2
            },
        "casual": {
                "min": 0,
                "max": 3 
            },
        "random": {
                "min": 0,
                "max": 2
            }
    }

    items = lootGenerator(loot)
    await updateInventoryLoot(ctx, inventory, items, LOOTBOX_ID, test=test)
    return

async def useItem(ctx):
    nums = parseNumbers(ctx.msg.content)
    if len(nums) == 0:    return await ctx.send("Debe ingresar el item que quiere utilizar. Consulte el inventario con --inventario e ingrese el número de la posición que sale a la izquierda.")
    item = nums[0] - 1
    if item < 0: return await ctx.send("Han ingresado una posición inválida.")

    pet = db.getNatiPetData(ctx.msg.ndcId)
    inventory   = await db.getUserInventory(ctx.msg.author.uid)

    if(item > inventory.length) : return await ctx.send("No existe un item con esta posición en tu inventario.")
    itemId      = inventory.data[item].objectId
    itemData = objects.inventoryAPI.properties(itemId)

    if   itemData.effects == 0   :   await giveItem(ctx)
    elif itemData.effects == 1   :   pass
    elif itemData.effects == 301 :   await open_lootBox_small(ctx, inventory)
    elif itemData.effects == 302 :   await open_lootBox_medium(ctx, inventory)
    elif itemData.effects == 303 :   await open_lootBox_large(ctx, inventory)

    return



async def testBox(ctx):
    nums    = parseNumbers(ctx.msg.content)
    num     = 1
    if nums != []: num = nums[0]
    inventory   = await db.getUserInventory(ctx.msg.author.uid)

    if   num == 1:    await open_lootBox_small(ctx, inventory, test=True)
    elif num == 2:    await open_lootBox_medium(ctx, inventory, test=True)
    elif num == 3:    await open_lootBox_large(ctx, inventory, test=True)
    return
