from src.antispam.data import AS
from src.utils.decorators import leafId

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

