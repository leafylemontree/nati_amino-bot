from src.antispam.data import AS

async def send_all(ctx):
        if user.uid != "17261eb7-7fcd-4af2-9539-dc69c5bf2c76": return await ctx.send("Usted no está autorizado para ejercer este comando")
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

