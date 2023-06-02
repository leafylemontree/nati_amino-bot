from src    import utils
import io
import cairocffi        as cairo 
from src.images.funcs import putText
import edamino

rank_card   = cairo.ImageSurface.create_from_png("media/templates/rank_card.png")

async def triggerLevelUp(ctx, level, communityChallenge, userId=None):
    level     = level + 1 
    prevLevel = (level - 1) if level >= 1                           else None
    nextLevel = (level + 1) if level <= communityChallenge.levels    else None
    if userId is None: userId = ctx.msg.author.uid
    user      = await ctx.client.get_user_info(userId)
    nickname  = user.nickname
    profile   = await utils.getImageBytes(ctx, user.icon)

    file      = io.BytesIO()
    image     = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1024, 512)
    ct        = cairo.Context(image)

    pfp       = cairo.ImageSurface.create_from_png(profile)
    px,py     = pfp.get_width(), pfp.get_height()
    scale     = 512/py
    ct.save()
    ct.translate(0, 0)
    ct.scale(1, scale)
    ct.set_source_surface(pfp)
    ct.paint()
    ct.restore()

    ct.save()
    ct.translate(0, 0)
    ct.set_source_surface(rank_card)
    ct.paint()
    ct.restore()

    ct.stroke()
    ct.set_source_rgba(0.843, 0.741, 0.396, 1)
    ct.move_to(640, 240)
    putText(ct, text=level, size=72, width=156, height=180, align='CENTER', font='Heavitas')
    ct.stroke()
    ct.move_to(418, 420)
    putText(ct, text=nickname, size=28, width=564, height=400, align='CENTER', font='Heavitas')
    ct.stroke()

    if prevLevel: 
        ct.set_source_rgba(0.843, 0.741, 0.396, 0.691)
        ct.move_to(448, 256)
        putText(ct, text=str(prevLevel), size=48, width=540, height=180, align='LEFT', font='Heavitas')
        ct.stroke()

    if nextLevel: 
        ct.set_source_rgba(0.843, 0.741, 0.396, 0.344)
        ct.move_to(448, 256)
        putText(ct, text=str(nextLevel), size=48, width=540, height=180, align='RIGHT', font='Heavitas')
        ct.stroke()

    image.write_to_png(file)
    file.seek(0)
    linkSnippet = edamino.api.LinkSnippet(
                link=f'ndc://x{ctx.msg.ndcId}/user-profile/{user.uid}',
                media_upload_value=file.read(),
            )
    

    await ctx.client.send_message(message=f"¡Enhorabuena! Has subido de nivel", chat_id=ctx.msg.threadId ,link_snippets_list=[linkSnippet])
    return


