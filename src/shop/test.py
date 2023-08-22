from src.challenges.rewards import donateAC
import random
from src.database import db
from src          import utils

@utils.userTracker("testdonation")
async def testDonation(ctx):
    amount = 2 + random.randint(0, 4)
    try:
        #db.setUserReward(ctx.msg.author.uid, ctx.msg.ndcId, dtype=0, amount=amount)
        #await ctx.send(f"Se han añadido {amount} AC como recompensa. Reclamelas usando --reclamar-recompensa (link de un blog donde donar).")
        await donateAC(ctx, ctx.msg.author.uid, amount)
    except Exception as e:
        await ctx.send(f"Ha ocurrido un error:\n{e}")
    return

