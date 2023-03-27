import time
from src import utils

async def notice(ctx, userId, title='Example', content='Testing', penaltyType=0, adminOpNote=None, noticeType=0):
    if not adminOpNote: adminOpNote = {}

    data = {
        "uid": userId,
        "title": title,
        "content": content,
        "attachedObject": {
            "objectId": userId,
            "objectType": 0
                    },
        "penaltyType": penaltyType,
        "adminOpNote": adminOpNote,
        "noticeType": noticeType,
        "timestamp": int(time.time() * 1000)
        }

    response = await ctx.client.request("POST", "notice", json=data)
    return

@utils.isStaff
async def giveNotice(ctx):
    msg = ctx.msg.content.split(" ")

    num = -1
    if len(msg) > 1:
        try                 :   num = int(msg[1])
        except ValueError   :   num = 0

    content = 'testing'
    if len(msg) > 2: content = " ".join(msg[2:])
    await notice(ctx, userId=ctx.msg.author.uid, title='Example', content=content, penaltyType=0, noticeType=num)
    return
