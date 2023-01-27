import cairocffi        as cairo 
from src import utils
from aiofile import AIOFile
from .funcs import *
import datetime

@utils.userId
async def tweet(ctx, uid, msg):
        user = await ctx.client.get_user_info(uid)
        await utils.getPfp(user)
        account = user.nickname
        tweetId = "@" + user.nickname.lower().replace(" ", "").encode('utf-8', 'ignore').decode('utf-8')
        text    = msg[8:].encode('utf-8', 'ignore').decode('utf-8')
        datet   = str(datetime.date.today()).split("-")
        timet   = str(datetime.datetime.now()).split(" ")[1].split(":")
        t_time  = [int(timet[0]), timet[1]]
        t_date  = [datet[2], int(datet[1]) - 1, datet[0]]

        w = 512
        h = 200
        l = len(text)
        r = (l // 36) + 1
        h = 250 + r * 30

        im = cairo.ImageSurface(cairo.FORMAT_RGB24, w,h)
        ct = cairo.Context(im)

        ct.set_source_rgb(0.09, 0.13, 0.17)
        ct.rectangle(0,0,w,h)
        ct.fill()
        
        pfp = cairo.ImageSurface.create_from_png("media/pfp.png")
        px, py  = pfp.get_width(), pfp.get_height()
        ct.save()
        ct.translate(32, 32)
        ct.scale((96/px), (96/py))
        ct.set_source_surface(pfp)
        ct.paint()
        ct.restore()
        around(ct, 32, 32, 96, 96)
       
        ct.set_source_rgb(1, 1, 1)
        ct.move_to(144, 48)
        putText(ct,
            text=account,
            size=26, 
            align="LEFT",
            width=768,
            height=128,
            wrap="None",
            font="Arial")


        #ct.set_source_rgb(0, 1, 1)
        #ct.arc(180+x, 70, 14, 0, math.pi*2 )
        #ct.fill()

        ct.set_source_rgb(0.5, 0.5, 0.5)
        ct.set_font_size(24)
        ct.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ct.move_to(144, 108)
        ct.show_text(tweetId)
        ct.stroke()

        tw = cairo.ImageSurface.create_from_png("media/twitter/twitterbase.png")
        ct.save()
        ct.translate(0, h-48)
        ct.set_source_surface(tw)
        ct.paint()
        ct.restore()
       
        tx = text.split(" ")
        ln = 0
        ct.set_source_rgb(1, 1, 1)
        ct.set_font_size(24)
        ct.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ax = 0
        for wo,t in enumerate(tx): 
            a,b,x,y,n,m = ct.text_extents(t)
            if (ax+x+32) > (w-32):
                ax = 0
                ln += 1
            ct.move_to(32+ax, 170+ln*30)
            ct.show_text(t)
            ax += x+ 8

        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        fmt_h = f"{t_time[0]%12}:{t_time[1]} "
        if t_time[0] // 12: fmt_h += "PM"
        else              : fmt_h += "AM"
        fmt_h += f" - {t_date[0]} {month[t_date[1]]} {t_date[2]}"

        
        ct.set_source_rgb(0.4, 0.4, 0.4)
        ct.set_font_size(18)
        ct.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ct.move_to(32, h-64)
        ct.show_text(fmt_h)
        a,b,x,y,n,m = ct.text_extents(fmt_h)
        ct.set_source_rgb(0, 1, 1)
        ct.move_to(56+x, h-64)
        ct.show_text("Twitter for iPhone")

        ct.stroke()
        im.write_to_png("media/twitter/tweet.png")
        async with AIOFile("media/twitter/tweet.png", 'rb') as file:
            img = await file.read()
            from src.imageSend import send_image
            await send_image(ctx, img)
        return
