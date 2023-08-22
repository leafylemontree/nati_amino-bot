from src            import  utils
from src.database   import  db

@utils.userTracker("confesion")
async def addConfession(ctx):
    msg = ctx.msg.content.split(" ")
    if len(msg) < 2:
        await ctx.send("Debe ingresar el texto de la confesión tras el comando de la siguiente manera:\n\n--confesion Me gustan las uvas")
        return

    msg = " ".join(msg[1:])
    db.newConfession(ctx.msg.ndcId, ctx.msg.author.uid, msg)
    await ctx.send("Confesión guardada exitósamente, u.u.")
    return

@utils.userTracker("confesiones", isStaff=True)
async def confessionList(ctx):
    globalFlag = False
    if ctx.msg.content.lower().find("-global") != -1: globalFlag = True

    confessions = db.retrieveConfessions(ctx.msg.ndcId, globalFlag)
    msg = f"Estas son las confesiones {'globales' if globalFlag is True else 'esta comunidad'}:\n\n"
    for i,confession in enumerate(confessions):
        msg += f"{i+1}.\n------------------\n{confession.content}\n\n"

    index = 0
    while len(msg) > 1999:
        m = msg[:1999]
        msg = msg[:1999]
        await ctx.send(m)

    if msg != "": await ctx.send(msg)
    return

