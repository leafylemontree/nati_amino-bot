from random import random
from src import utils

@utils.userTracker("sus")
async def sus(ctx):
        sus = ["sus", "amogus", "sussy", "sugoma", "amogusgus", "usa", "aaaaa", "amomomogusgus", "asmolgus", "abiggus", "abominatiogus", "what if?", "oh no", "oh yeah!"]
        return sus[int(random() * len(sus))]
