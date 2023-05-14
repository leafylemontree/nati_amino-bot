from src import objects
import asyncio

STRIKE          = 205
TITLE_CHANGE    = 207
BAN             = 213
UNBAN           = 214
WARNING         = 267


async def moderation_history(ctx, userId=None, blogId=None, itemId=None, quizId=None, fileId=None, threadId=None, size=25):
    objectType  = None
    objectId    = None

    if userId:
        objectType  = 0
        objectId    = userId

    elif blogId or quizId:
        objectType  = 1
        objectId    = blogId if blogId else quizId

    elif wikiId:
        objectType  = 2
        objectId    = wikiId

    elif threadId:
        objectType  = 12
        objectId    = threadId

    elif fileId:
        objectType  = 109
        objectId    = fileId

    response = await ctx.client.request('GET', f'admin/operation?objectId={objectId}&objectType={objectType}&pagingType=t&size={size}')
    return tuple(map(lambda log: objects.AdminLogList(**log), response['adminLogList']))

async def get_user_moderation(ctx, userId, modType='WARN'):
    logs        = []
    pageToken   = None
    size        = 100
    modType     = modType.upper()

    while True:
        pageTokenUrl = f'&pageToken={token}' if pageToken is not None else ''
        response = await ctx.client.request('GET', f'admin/operation?objectId={userId}&objectType=0&pagingType=t&size={size}' + pageTokenUrl)

        adminLogList    = tuple(map(lambda log: objects.AdminLogList(**log), response['adminLogList']))
        pageToken       = response['paging']['nextPageToken']
        logs.extend(adminLogList)
        if len(adminLogList) < size: break
        await asyncio.sleep(3)

    counter = 0
    for log in logs:
        if      modType == 'WARN'   and log.operation == WARNING    : counter += 1
        elif    modType == 'STRIKE' and log.operation == STRIKE     : counter += 1
        elif    modType == 'BAN'    and log.operation == BAN        : counter += 1

    return counter


async def get_history(ctx):
    #adminLogList = await moderation_history(ctx, userId=ctx.msg.author.uid, size=100)
    try:    adminLogList = await moderation_history(ctx, userId="7d470c61-c596-4b1c-a0b6-ffd7c9e581c6", size=100)
    except Exception as e: return await ctx.send(f"El bot no posee cargo de moderación.\nError: {e}")

    warnings    = 0
    strikes     = 0
    bans        = 0

    for log in adminLogList:
        if      log.operation  == WARNING:     warnings    += 1
        elif    log.operation  == STRIKE:      strikes     += 1
        elif    log.operation  == BAN:         bans        += 1

    await ctx.send(f"""
Historial de moderación de {ctx.msg.author.nickname}
------------------------------------------------

Advertencias : {warnings}
Faltas       : {strikes}
Expulsiones  : {bans}
""")
    return
