from src import utils
from dataclasses import dataclass
import asyncio

@dataclass
class Post:
    type:           int
    title:          str
    content:        str
    mediaList:      list
    icon:           str
    keywords:       list
    extensions:     dict
    backgroundI:    str
    backgroundC:    str

class MediaList:
    type:           int
    url:            str
    label:          str
    code:           str

    def __init__(self, data):
        try: self.type   = data[0]
        except: self.type = None
        try: self.url   = data[1]
        except: self.url = ""
        try: self.label   = data[2]
        except: self.label = None
        try: self.code   = data[3]
        except: self.code = None
        return

async def generateMediaList(ctx, mediaList):
    newMediaList = []
    for media in mediaList:
        ml = MediaList(media)
        rawImage = await utils.getImageBytes(ctx, ml.url, noconvert=True)
        imageURL = await ctx.client.upload_media(data=rawImage, content_type="image/gif" if ml.url.find("gif") != -1 else "image/jpg")
        newMediaList.append([ml.type, imageURL, ml.label, ml.code])
        await asyncio.sleep(1)
    return newMediaList


async def parseBlog(ctx, objectId, postndcId):
    ctx.client.set_ndc(postndcId)
    blog = await ctx.client.get_blog_info(blog_id=objectId)

    print(blog)

    title       = blog.title
    content     = blog.content
    mediaList   = await generateMediaList(ctx, blog.mediaList)
    keywords    = blog.keywords
    extensions  = {
        "style": {}
    }
    if hasattr(blog.extensions.style, "backgroundColor"):       extensions["style"]["backgroundColor"]      = blog.extensions.style.backgroundColor
    if hasattr(blog.extensions.style, "backgroundMediaList"):   extensions["style"]["backgroundMediaList"]  = blog.extensions.style.backgroundMediaList

    ctx.client.set_ndc(ctx.msg.ndcId)
    return Post(1, title, content, mediaList, None, keywords, extensions, None, None)


async def parseWiki(ctx, objectId, postndcId):
    ctx.client.set_ndc(postndcId)
    wiki = await ctx.client.get_wiki_info(wiki_id=objectId)
    print(wiki)

    title       = wiki.label
    content     = wiki.content
    mediaList   = await generateMediaList(ctx, wiki.mediaList)
    icon        = mediaList[0][1]
    keywords    = wiki.keywords
    extensions  = wiki.extensions
    backgroundI = extensions['style']['backgroundMediaList'][0][1] if "backgroundMediaList" in extensions['style'].keys() else None
    backgroundC = extensions['style']['backgroundColor']           if "backgroundColor"     in extensions['style'].keys() else "#000000"
    ctx.client.set_ndc(ctx.msg.ndcId)
    return Post(2, title, content, mediaList, icon, keywords, None, backgroundI, backgroundC)

async def publishWiki(ctx, post):
    return await ctx.client.post_wiki(
                title           = post.title,
                content         = post.content,
                icon            = post.icon,
                image_list_raw  = post.mediaList,
                keywords        = post.keywords,
                backgroundColor = post.backgroundC,
                backgroundImage = post.backgroundI,
                ignoreErrors    = True
            )

async def publishBlog(ctx, post):
    return await ctx.client.post_blog(
                    title           = post.title,
                    content         = post.content,
                    image_list_raw  = post.mediaList,
                    extensions      = post.extensions,
                    ignoreErrors    = True
                )


@utils.isStaff
@utils.userTracker("copiarBlog")
async def copyPost(ctx):
    args = ctx.msg.content.split(" ")
    if len(args) < 2:   return await ctx.send("Debe añadir el enlace de un blog o una wiki tras el comando.")

    link = await ctx.client.get_info_link(args[1])
    if link.linkInfo.objectType not in [1, 2]: return await ctx.send("El link que ingrese debe ser de una wiki.")

    objectId    = link.linkInfo.objectId
    objectType  = link.linkInfo.objectType
    postndcId   = link.linkInfo.ndcId

    if   objectType == 1:
        post = await parseBlog(ctx, objectId, postndcId)
        await publishBlog(ctx, post)
    elif objectType == 2:
        post = await parseWiki(ctx, objectId, postndcId)
        await publishWiki(ctx, post)

    return
