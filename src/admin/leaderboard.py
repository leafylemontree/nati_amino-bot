from __future__ import annotations
from typing import List, Dict, Optional, Any, Tuple
from pydantic import BaseModel
from src.database import db

class LeaderboardUserProfile(BaseModel):
    status:                     Optional[int]
    isNicknameVerified:         Any
    activeTime:                 Optional[int]
    uid:                        Optional[str]
    level:                      Optional[int]
    followingStatus:            Optional[int]
    accountMembershipStatus:    Optional[int]
    isGlobal:                   Any
    membershipStatus:           Optional[int]
    reputation:                 Optional[int]
    role:                       Optional[int]
    ndcId:                      Optional[int]
    membersCount:               Optional[int]
    nickname:                   Optional[str]
    icon:                       Optional[str]


async def getLeaderboard(ctx):
    response = await ctx.client.request("GET", f"https://service.narvii.com/api/v1/g/s-{ctx.client.ndc_id}/community/leaderboard?rankingType=2&start=0&size=100", full_url=True)

    users = tuple(map(lambda user: LeaderboardUserProfile(**user), response['userProfileList']))

    msg = ""
    for rank, user in enumerate(users):
        msg += f"{rank+1}\t{user.activeTime/60:.2f}\t{user.nickname}\n"
        db.cursor.execute(f'INSERT INTO Rep VALUES ("{user.uid}", {ctx.msg.ndcId}, {user.activeTime}, NOW());')

    await ctx.send(msg[:2000])
    return
