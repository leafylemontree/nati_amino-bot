from src import objects

async def warningInfo(ctx):
    warnings = [f"     - {key}: {value}" for key,value in objects.AntiSpam.msg_desc.items()]
    nl = '\n'
    return await ctx.send(f"""
[cb]Códigos de advertencia
[c]﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́﹏̈́ ༅˻˳˯ₑ❛░⃟ ⃟°˟̫· · · ·

[c]Nati está atenta en todo momento a los chats de la comunidad, para ofrecer respuesta a tiempo real frente a amenazas como spam a diferentes redes sociales, links de usuarios que hayan sido baneados con anterioridad, o ciertas anomalías que puedan tener los mensajes que sean propias de bots.

[c]Para que funcione de mejor manera, se recomienda activar el canal de reportes con el comando --setlog, debe ejecutarlo en el chat que quiera dejar para recibir las advertencias de Nati.

[c]

{nl.join(warnings)}
""")
