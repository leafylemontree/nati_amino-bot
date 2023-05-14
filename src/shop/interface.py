from src.database import db
from src          import objects
from .images      import inventoryNewItemCard

async def inventory(ctx):

    inventory = await db.getUserInventory(ctx.msg.author.uid)
    user      = db.getUserData(ctx.msg.author)

    msg = f"""
[cb]Inventario
[c]----------------

[c]Usuario: {ctx.msg.author.nickname}
[c]Alias: {user.alias}
[c]Puntos: {user.points}
[c]Inventario: {inventory.length}/10

[c]Objetos:
"""    
    for i,element in enumerate(inventory.data):    msg += f"  {i+1}. {element.amount}x {objects.inventoryAPI.name(element.objectId)}\n"

    await ctx.send(msg[:1999])
    return

async def add_item(ctx, mode='ADD', verbose=True, objectId=None, amount=None, use_text=False):
    msg         = ctx.msg.content.split(" ")

    if use_text:
        if len(msg) < 3: return await ctx.send("Debe añadir la id del objeto y la cantidad")

        try                 :    objectId = int(msg[1])
        except ValueError   :    return await ctx.send("La id del objeto es inválida")

        try                 :    amount = int(msg[2])
        except ValueError   :    return await ctx.send("La cantidad es inválida")

    inventory = await db.getUserInventory(ctx.msg.author.uid)

    if   mode == 'ADD':
        
        index = None
        for i,element in enumerate(inventory.data):
            if element.objectId == objectId: index = i
        objectProps = objects.inventoryAPI.properties(inventory.data[index].objectId) if index is not None else None

        if index is not None and objectProps.limit < (inventory.data[index].amount + amount) and objectProps.limit != -1: return await ctx.send(f"¡Se ha alcanzado el máximo de {objectProps.name} en el invetario de {ctx.msg.author.nickname}!")

        response = inventory.add(objectId, amount)

        if verbose:
            
            linkSnippet = await inventoryNewItemCard(ctx, objectId, amount)

            if response: return await ctx.send(f"¡Se ha alcanzado el máximo de items en el inventario de {ctx.msg.author.nickname}!")

            c_type = 'Añadido'
            if amount < 0: c_type = 'Quitado'
            await ctx.client.send_message(
                    message=f"[ci]{c_type} {amount} {objects.inventoryAPI.name(objectId)} al\ninventario de {ctx.msg.author.nickname}",
                    chat_id=ctx.msg.threadId,
                    link_snippets_list=[linkSnippet])

    elif mode == 'DEL':
        inventory.remove(objectId)
        if verbose: await ctx.send(f"[c]Removido {objects.inventoryAPI.name(objectId)} del inventario de {ctx.msg.author.nickname}")

    await db.setUserInventory(inventory)
    return


async def giveRandomItem(ctx):
    objectId = objects.inventoryAPI.getRandomItem()
    await add_item(ctx, objectId=objectId, amount=1)
    return

async def clearInventory(ctx):
    inventory = await db.getUserInventory(ctx.msg.author.uid)
    inventory.clear()
    await db.setUserInventory(inventory)
    await ctx.send("Inventario limpiado")
    return


