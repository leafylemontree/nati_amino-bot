from src.database import db
from src import utils
import edamino

@utils.userTracker("crearRPItem", isStaff=True)
async def createRPItem(ctx):
    args = ctx.msg.content.split("\n")
    if len(args) < 5: return await ctx.send("""
Para añadir un item, debe hacerlo de esta forma:

--crearRPItem
nombre
nivel
precio
descripción""") 

    ndcId   = ctx.msg.ndcId
    name    = args[1]
    level   = args[2]
    price   = args[3]
    desc    = "\n".join(args[4:])

    try:
        db.newRoleplayItem(ndcId, name, level, price, desc)
        await ctx.send("¡Nuevo item añadido! Revise la id con --RPItems")
    except:
        await ctx.send("Ha habido un error. Asegure que el valor para nivel y precio sea un número.")

@utils.userTracker("RPItems")
async def retrieveRPItems(ctx):
    items   = db.getRoleplayItems(ctx.msg.ndcId)
    com     = ctx.msg.content.upper().split(" ")
    if len(com) < 2:
        msg = "Estos son los items de roleplay en esta comunidad:\n\n"
        for i,item in enumerate(items):
            msg += f"{item.itemId}. {item.name}\n"
            if len(msg) > 1900:
                await ctx.send(msg)
                msg = ""
        if msg != "": await ctx.send(msg)
        return

    else:
        itemId =  None
        try: itemId = int(com[1])
        except ValueError: return await ctx.send("La id de item ingresado es inválida.")
        item = list(filter(lambda x: x.itemId == itemId, items))
        if item == []:
            return await ctx.send("No hay un item con esta id, :c.")
        else:
            item = item[0]
            return await ctx.send(f"""
Información del item:
--------------------
Id: {item.itemId}
ndcId: {item.ndcId}
nombre: {item.name}
nivel: {item.level}
precio: {item.price}
descripción: {item.description}
""")

async def editError(ctx):
    await ctx.send("""Debe poner el comando de la siguiente forma:

--editarRPItem (id del item) (categoría)
(valor)

Recuerde que la id es un número""")

@utils.userTracker("editarRPItem", isStaff=True)
async def editRPItem(ctx):
    com  = ctx.msg.content.lower().split(" ")
    val  = ctx.msg.content.split("\n")
    if len(com) < 3: return await editError(ctx)
    if len(val) < 2: return await editError(ctx)
    
    ndcId   = ctx.msg.ndcId
    itemId  = None
    column  = "name" if com[2].find("nombre") != -1 else "level" if com[2].find("nivel") != -1 else "price" if com[2].find("precio") != -1 else "description" if com[2].find("descrici") != -1 else "none"
    value   = val[1]
    try:    itemId = int(com[1])
    except ValueError:  return await editError(ctx)

    try:
        db.editRoleplayItem(ndcId, itemId, column, value)
        await ctx.send("Item editado.")
    except Exception as e:
        await ctx.send("Hubo un error modificando el valor. Una columna que debe ser un número ha recibido un valor erróneo")
        return

@utils.userTracker("removerRPItem", isStaff=True)
async def removeRPItem(ctx):
    com     = ctx.msg.content.split(" ")
    if len(com) < 2: return await ctx.send("Debe colocar la id del item tras el comando. Ejemplo: --removerRPItem (id)")
    ndcId   = ctx.msg.ndcId
    itemId  = None
    try:    itemId = int(com[1])
    except ValueError: return await ctx.send("La id ingresada no es válida")
    db.delRoleplayItem(ndcId, itemId)
    await ctx.send("¡Item eliminado!")

@utils.userTracker("RPInventario")
@utils.userId
async def RPInventory(ctx, userId, msg):
    user    = await ctx.client.get_user_info(userId)
    items   = db.getRoleplayInventory(ctx.msg.ndcId, user.uid)
    msg = f"[c]Este es el inventario de {user.nickname}:\n\n"
    for i,item in enumerate(items):
        itemData = db.getRoleplayItem(ctx.msg.ndcId, item.itemId)
        msg += f"[c]{i+1} {itemData.name} x{item.quantity}\n"
        if len(msg) > 1900:
            await ctx.send(msg)
            msg = ""
    if msg != "": await ctx.send(msg)
    return

@utils.userTracker("RPañadirItem", isStaff=True)
@utils.userId
async def addRPItem(ctx, userId, msg):
    com  = ctx.msg.content.upper().split(" ")
    if len(com) < 3: return await ctx.send("Para añadir un item, debe hacerlo de la siguiente manera: --RPAñadirItem (id del item) (cantidad). Si va a hacer @ a alguien o a poner el link del perfl, va al final separado por un espacio.")

    ndcId    = ctx.msg.ndcId
    itemId   = None
    quantity = None
    try: itemId = int(com[1])
    except ValueError: return await ctx.send("El valor ingresado para la id debe ser un número")
    try:
        quantity = int(com[2])
    except ValueError: return await ctx.send("El valor ingresado para la cantidad debe ser un número")

    db.addRoleplayItem(ndcId, userId, itemId, quantity)
    await ctx.send("Items añadidos al inventario.")
    return

@utils.userTracker("RPquitarItem", isStaff=True)
@utils.userId
async def delRPItem(ctx, userId, msg):
    com  = ctx.msg.content.upper().split(" ")
    if len(com) < 3: return await ctx.send("Para quitar un item, debe hacerlo de la siguiente manera: --RPQuitarItem (id del item) (cantidad). Si va a hacer @ a alguien o a poner el link del perfl, va al final separado por un espacio.")

    ndcId    = ctx.msg.ndcId
    itemId   = None
    quantity = None
    try: itemId = int(com[1])
    except ValueError: return await ctx.send("El valor ingresado para la id debe ser un número")
    try:
        quantity = int(com[2])
    except ValueError: return await ctx.send("El valor ingresado para la cantidad debe ser un número")

    db.removeRoleplayItem(ndcId, userId, itemId, quantity)
    await ctx.send("Items quitados del inventario.")
    return

@utils.userTracker("RPEditarNota")
@utils.userId
async def editRPnote(ctx, userId, msg):
    com     = ctx.msg.content.split(" ")
    user    = await ctx.client.get_user_info(userId)
    if len(com) < 2: return await ctx.send("Debe adjuntar una nota tras el comando. Si desea colocar el link de alguien o hacer @, se pone al final con un espacio de separación.")
    r = db.editRoleplayNote(ctx.msg.ndcId, userId, " ".join(msg.split(" ")[1:]))
    if r is True:
        await ctx.send(f"Ha sido añadida una nota a {user.nickname}.")
    else:
        await ctx.send(f"Se ha modificado la nota de {user.nickname}.")
    return

@utils.userTracker("RPVerNota")
@utils.userId
async def viewRPnote(ctx, userId, msg):
    roleplayNote = db.getRoleplayNote(ctx.msg.ndcId, userId)
    user         = await ctx.client.get_user_info(userId)
    if roleplayNote is None: return await ctx.send(f"{user.nickname} no tiene una nota agregada.")

    embed = edamino.api.Embed(
                title="Nota de usuario",
                object_type=0,
                object_id=user.uid,
                content=user.nickname
            )

    await ctx.send(roleplayNote.content, embed=embed)
    return
