from src.antispam.data import AS
from src.utils.decorators import leafId
from src import utils
import asyncio

async def send_all(ctx):
        if ctx.msg.author.uid != leafId: return await ctx.send("Usted no está autorizado para ejercer este comando")
        msg = ctx.msg.content[10:]
        for comId,chatId in AS.logging_chat.items():
            try:
                ctx.client.set_ndc(int(comId))
                await ctx.client.send_message(message=f"Mensaje enviado por el creador:\n----------\n\n{msg}",
                                    chat_id=chatId,
                                    message_type=0,
                                    ref_id=None,
                                    mentions=None,
                                    embed=None,
                                    link_snippets_list=None,
                                    reply=None )
            except Exception:
                print("failed at:", comId)


@utils.userTracker("enviartodos")
async def sendEveryone(ctx):

    message = ctx.msg.content.split(" ")
    if len(message) < 2: return await ctx.send("Debe poner un mensaje para enviar a los usuarios de la comunidad.")

    message = await utils.formatter(ctx, " ".join(message[1:]))
    await ctx.send(f"[c]Este es el mensaje que va a enviar a los usuarios.\n\n[c]-SI : Confirmar        -NO : Cancelar\n\n{message}")
    
    response = await utils.confirmation(ctx, ctx.msg.threadId, True, ctx.msg.ndcId, staff=True)
    if response is False: return await ctx.send("Envío cancelado")
    await ctx.send("Enviando mensaje...")

    count = 0
    while True:

        users = await ctx.client.get_online_users(start=(count * 100), size=100)
        
        for user in users:

            await ctx.client.start_chat(
                    invitee_ids=[user.uid],
                    chat_type=0,
                    content=message,
                    )

            await asyncio.sleep(3)

        await asyncio.sleep(15)
        count += 1
        if len(users) < 100: break

    await ctx.send("Envío finalizado")
