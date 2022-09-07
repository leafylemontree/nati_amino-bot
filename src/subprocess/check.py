from src.antispam import get_wall_comments, findContent, findNickname

async def checkWall(ctx, user, ndcId):
        commentsCount = user.commentsCount
        print('\tcomments:',commentsCount)
        detected = {}

        for a in range( int(commentsCount // 100) +1):
            comments = await get_wall_comments(ctx, user_id=user.uid, sorting="newest", start=(a*100), size=((a+1)*100))
            for index,comment in enumerate(comments):
                nick_warnings = await findNickname(comment.author.nickname)
                if nick_warnings:
                    if comment.author.uid in detected: detected[comment.author.uid].append(nick_warnings) 
                    else                             : detected[comment.author.uid] = [nick_warnings]
                cont_warnings = await findContent(comment.content, ndcId)
                if cont_warnings:
                    if comment.author.uid in detected: detected[comment.author.uid].append(cont_warnings) 
                    else                             : detected[comment.author.uid] = [cont_warnings]
                print(index, nick_warnings, cont_warnings) 

        return detected

async def checkBio(ctx, user):
        bio          = user.content
        if bio is None: return []
        bio_warnings = await findContent(bio, ctx.client.ndc_id.replace("x", ""))
        print(bio)
        print("warnings:", bio_warnings)
        return bio_warnings

async def checkBlogs(ctx, user):
        return []

