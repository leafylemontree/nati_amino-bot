from src import utils
import cairo
from aiofile import AIOFile
from .funcs import *
import os

@utils.userId
@utils.userTracker("article")
async def wiki(ctx, uid, msg):
        w = 512
        h = 512
        
        user = await ctx.client.get_user_info(user_id=uid)
        text = msg[10:]
        
        await utils.getPfp(user)

        im = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
        cr = cairo.Context(im)

        cr.set_source_rgb(1, 1, 1)
        cr.set_line_width(1)
        cr.rectangle(0, 0, w, h)
        cr.fill()

        cr.set_source_rgb(0.94, 0.94, 0.94)
        cr.move_to(w*0.675, h*0.625)
        cr.arc(w*0.425, h*0.625, w*0.25, 0, math.pi*2)
        cr.fill()

        cr.set_source_rgb(0.94, 0.94, 0.94)
        cr.set_line_width(3)
        cr.move_to(w*0.7, h*0.625)
        cr.arc(w*0.425, h*0.625, w*0.275, 0, math.pi*2)
        cr.stroke()

        t = "N"
        a,b,x,y,m,n = cr.text_extents(t)
        cr.set_source_rgb(1, 1, 1)
        cr.set_font_size(240)
        cr.select_font_face("Times New Roman", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.move_to(w*0.3, h*0.8)
        cr.show_text(t)
        cr.stroke()
        
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(1)
        cr.move_to(w*0.05, h*0.15)
        cr.line_to(w*0.95, h*0.15)
        cr.move_to(w*0.05, h*0.9)
        cr.line_to(w*0.95, h*0.9)
        cr.stroke()

        
        cr.set_source_rgb(0, 0, 0)
        cr.set_font_size(48)
        cr.select_font_face("Georgia", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.move_to(w*0.05, h*0.1)
        cr.show_text(user.nickname.encode('utf-8', 'ignore').decode('utf-8'))
        tx, body, l  = len(text), [], 24
        for i in range((tx // l)+1)   : body.append([])
        for i,j in enumerate(text): body[int(i/l)].append(j)

        cr.set_source_rgb(0, 0, 0)
        cr.set_font_size(24)
        cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        for i,j in enumerate(body):
            cr.move_to(w*0.05, (h*0.225)+(i*0.05*h))
            cr.show_text("".join(j))

        t = "Natipedia, la enciclopedia comunitaria"
        aa,b,x,y,m,n = cr.text_extents(t)
        cr.set_source_rgb(0, 0, 0)
        cr.set_font_size(18)
        cr.select_font_face("Georgia", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.move_to(w-x, h*0.95)
        cr.show_text(t)
        cr.stroke()
        
        cr.set_source_rgb(0.969, 0.97, 0.94)
        cr.set_line_width(1)
        cr.rectangle(w*0.625, h*0.2, w*0.3, h*0.65)
        cr.fill()
        cr.set_source_rgb(0.78, 0.80, 0.82)
        cr.set_line_width(2)
        cr.rectangle(w*0.625, h*0.2, w*0.3, h*0.65)
        cr.stroke()
        
        cr.set_source_rgb(0.4, 0.8, 0.8)
        cr.set_line_width(1)
        cr.rectangle(w*0.65, h*0.225, w*0.25, h*0.25)
        cr.fill()

        labels = ["Nivel", "Rep", "Blogs", "Seguidores", "Siguiendo", "Títulos"]
        data   = [user.level, user.reputation, user.blogsCount, user.membersCount, user.joinedCount, ""]

        cr.set_font_size(10)
        cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        for i,(j,k) in enumerate(zip(labels, data)):
            cr.set_source_rgb(0.04, 0.27, 0.68)
            cr.move_to(w*0.66, (h*0.51)+i*0.035*h)
            cr.show_text(j)
            cr.set_source_rgb(0, 0, 0)
            cr.move_to(w*0.8, (h*0.51)+i*0.035*h)
            cr.show_text(str(k))
        cr.stroke()

        cr.set_source_rgb(1, 1, 1)
        cr.set_line_width(1)
        cr.rectangle(w*0.65, h*0.7, w*0.25, h*0.125)
        cr.fill()
        cr.stroke()

        if user.userProfileExtensions:
            cr.set_font_size(8)
            cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            for i,j in enumerate(user.userProfileExtensions.customTitles[:6]):
                cr.set_source_rgb(0, 0, 0)
                cr.move_to(w*0.66, (h*0.725)+i*0.02*h)
                cr.show_text(j)
                    
        cr.move_to(0, 0)
        pfp = cairo.ImageSurface.create_from_png("media/pfp.png")
        px  = pfp.get_width()
        py  = pfp.get_height()
        cr.save()
        cr.translate(w*0.65, h*0.225)
        cr.scale((w*0.25/px), (h*0.25/py))
        cr.set_source_surface(pfp)
        cr.paint()
        cr.restore()

        cr.stroke()
        im.write_to_png("wiki.png")  # Output to PNG


        async with AIOFile("wiki.png", 'rb') as file:
            img = await file.read()
            from src.imageSend import send_image
            await send_image(ctx, img)
        return

