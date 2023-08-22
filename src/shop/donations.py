from src import utils
from src import objects
from src.database import db
from dataclasses import dataclass
from src.shop.interface import add_item

class UserTransaction:
    def __init__(self, notificationId, objectId, createdTime, amount=None):
        self.notificationId = notificationId
        self.amount         = amount
        self.objectId       = objectId
        self.createdTime    = createdTime


async def get_wallet_history(ctx, start=0, size=25):
    response = await ctx.client.request("GET", f"wallet/coin/history?start={start}&size={size}")
    return tuple(map(lambda c: objects.CoinHistory(**c), response['coinHistoryList']))

async def get_notifications(ctx, start=0, size=25, pagingToken=None):
    if pagingToken is None: pagingToken = f'&pagingToken={pagingToken}'
    response = await ctx.client.request("GET", f"notification?pagingType=t&start={start}&size={size}{pagingToken}")
    return objects.NotificationList(response)


def registerDonations(userNotifs, userId, ndcId):
    lastNotificationId = db.getLastDonation(userId, ndcId)
    amount = 0
    notificationId = None

    for notif in userNotifs:
        if notif.amount is None                      : continue
        if notif.notificationId == lastNotificationId: break
        if notif.amount <= 0                         : continue
        amount += notif.amount
        if notificationId is None: notificationId = notif.notificationId

    data = db.setLastDonation(userId, notificationId, amount, ndcId)
    return data

async def parseLastDonations(ctx):
    notifications = await get_notifications(ctx, start=0, size=100)
    coinHistory   = await get_wallet_history(ctx, start=0, size=100)
   
    userNotifs = []
    for notif in notifications.notifications:
        if notif.operator.uid != ctx.msg.author.uid: continue
        userNotifs.append(UserTransaction(notif.notificationId, notif.objectId, notif.createdTime))

    for transaction in coinHistory:
        if transaction.extData.objectDeeplinkUrl is None: continue
        objectId = transaction.extData.objectDeeplinkUrl.split("/")[-1]

        for userNotif in userNotifs:
            if userNotif.amount is not None: continue
            userNotif.amount = transaction.originCoins
            break
        
    data = registerDonations(userNotifs, ctx.msg.author.uid, ctx.msg.ndcId)
    return userNotifs


@utils.userTracker("mis-ultimas-donaciones")
async def myLastDonations(ctx):
    userNotifs = await parseLastDonations(ctx)
    msg = f"Estas son las últimas transaccines hechas por {ctx.msg.author.nickname}:\n\n"
    for notif in userNotifs:
        if notif.amount is None: continue
        msg += f"Cantidad: {notif.amount}  - Fecha: {notif.createdTime}\n"
    await ctx.send(msg)
    return

async def buyLootbox(ctx, ins):
    msg = ctx.msg.content.upper().split(" ")
    await parseLastDonations(ctx) 
    userInfo = db.getUserData(ctx.msg.author) 

    itemId = None
    price  = None
    amount = 1

    if msg[0] == "-AC":
        await ctx.send(f"Usted tiene en reserva {userInfo.ACBuffer} AC")
        return False
    elif msg[0] == "-COMPRAR":
        if len(msg) < 2:
            await ctx.send("Debe ingresar el comando con el número de la caja: -comprar 1")
            return False

        if msg[1] == "1":
            itemId = 31
            price  = 50
        elif msg[1] == "2":
            itemId = 32
            price  = 100
        elif msg[1] == "3":
            itemId = 33
            price  = 200
        else:
            await ctx.send("Debe ingresar el comando de la siguiente manera: -comprar 1")
            return False

        if len(msg) > 2:
            try:    amount = int(msg[2])
            except ValueError: pass

        if userInfo.ACBuffer < (price * amount): 
            await ctx.send("La cantidad de AC que ha donado no le alcanza para comprar esta caja. Done más y vuelva a ingresar el comando nuevamente")
            return False

        r = await add_item(ctx, objectId=itemId, amount=amount)
        if r is True:
            db.modifyRecord(60, ctx.msg.author, -(price * amount))
        else: await ctx.send("Ha ocurrido un error dando el item.")
    else:
        ins.data += 1
        if ins.data > 4: return True

    return False

@utils.waitForMessage(message="*", callback=buyLootbox)
async def lootboxes(ctx, ins):
    userInfo = db.getUserData(ctx.msg.author)
    await ctx.send(f"""
Tienda de cajas de recompensas


Nati le permite cambiar AC por una caja donde puede conseguir items aleatorios. Mientras más rara la caja, mayor posibilidad de obtener items más exclusivos, así como tener una mayor cantidad de ellos


Posee: {userInfo.ACBuffer} AC

[u]1. Caja normal:    50 AC
    - 1-2 item de rareza casual (verde)
    - 0-2 items aleatorios

[u]2. Caja rara:      100 AC
    - 1-2 item de rareza poco común (azul)
    - 0-2 items de rareza casual (verde)
    - 0-2 items aleatorios

[u]3. Caja mágica:    200 AC
    - 1-2 item de rareza extraña (morada)
    - 0-2 items de rareza poco común (azul)
    - 0-3 items de rareza casual (verde)
    - 0-2 items aleatorios

Para donar, vaya a un blog subido por Nati y done la cantidad exacta, o más. Nati guardará si ha donado más monedas. Una vez esté listo, ponga -comprar (número). Ejemplo: -comprar 1

Ver cantidad de AC donadas: -ac
""")
    return 0
