from __future__ import annotations
from src import objects
from src.database import db

async def getLeaderboard(ctx):
    response = await ctx.client.request("GET", f"https://service.narvii.com/api/v1/g/s-{ctx.client.ndc_id}/community/leaderboard?rankingType=2&start=0&size=100", full_url=True)

    users = tuple(map(lambda user: objects.LeaderboardUserProfile(**user), response['userProfileList']))

    msg = ""
    for rank, user in enumerate(users):
        msg += f"{rank+1}\t{user.activeTime/60:.2f}\t{user.nickname}\n"
        db.cursor.execute(f'INSERT INTO Rep VALUES ("{user.uid}", {ctx.msg.ndcId}, {user.activeTime}, NOW());')

    await ctx.send(msg[:2000])
    return
