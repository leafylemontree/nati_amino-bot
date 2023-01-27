import cairo
from aiofile import AIOFile
from .funcs import *
import time
from src import objects

async def stats(ctx):
        time_passed = time.time() - objects.botStats.time
        
        days = int(time_passed // 86400)
        hours= int(time_passed // 3600 )%24
        mins = int(time_passed // 60   )%60
        secs = int(time_passed %  60)
        fmt_t= f"{days}:{hours:02d}:{mins:02d}:{secs:02d}"
        
        w = 640
        h = 480
        ux, uy = w/40, h/30

        sf = cairo.ImageSurface(cairo.FORMAT_RGB24, w,h)
        cr = cairo.Context(sf)

        cr.set_source_rgb(0.25, 0.36, 0.56)
        rounded(cr, 8, 8, w-16, h-16, 8)
        cr.fill()
        
        cr.set_source_rgb(0.15, 0.29, 0.48)
        cr.move_to(5*ux, h-8)
        cr.line_to(14*ux, h-8)
        cr.line_to(32*ux, 8)
        cr.line_to(23*ux, 8)
        cr.close_path()
        cr.fill()

        cr.set_source_rgb(0.15, 0.14, 0.37)
        rounded(cr, 8, 8, w-16, h-16, 8)
        cr.stroke()
        
        cr.set_source_rgb(0.36, 0.61, 0.76)
        rounded(cr, 2*ux, 2*uy, w, 3*uy, 8)
        cr.fill()
        cr.stroke()
        
        cr.set_source_rgb(0.21, 0.45, 0.74)
        rounded(cr, 2*ux, 7*uy, 14*ux, 12*uy, 16)
        rounded(cr, 18*ux, 7*uy, 20*ux, 8*uy, 16)
        rounded(cr, 18*ux, 17*uy, 20*ux, 11*uy, 16)
        cr.fill()
        cr.stroke()

        cr.set_line_width(4)
        cr.set_source_rgb(0.19, 0.31, 0.47)
        rounded(cr, 2*ux, 7*uy, 14*ux, 12*uy, 16)
        rounded(cr, 18*ux, 7*uy, 20*ux, 8*uy, 16)
        rounded(cr, 18*ux, 17*uy, 20*ux, 11*uy, 16)
        cr.stroke()

        x0, y0 = 3.5*ux, 10*uy 
        labels = ["Activo por:", "Reinicios:", "Espera estimada:"]
        data   = [fmt_t, objects.botStats.reset, "15"]
        for i,(j,k) in enumerate(zip(labels, data)):
            cr.set_source_rgb(0.54, 0.75, 0.96)
            cr.set_font_size(24)
            cr.select_font_face("Georgia", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            cr.move_to(x0, y0 + i*3*uy)
            cr.show_text(str(j))
            cr.set_source_rgb(0.06, 0.06, 0.33)
            cr.set_font_size(28)
            cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.move_to(x0, y0 + i*3*uy + uy*1.75)
            cr.show_text(str(k))
        
        x0, y0 = 19.5*ux, 9.5*uy 
        labels = ["Usuarios:", "Mensajes:"]
        data   = [objects.botStats.users, objects.botStats.messages]
        for i,(j,k) in enumerate(zip(labels, data)):
            cr.set_source_rgb(0.54, 0.75, 0.96)
            cr.set_font_size(24)
            cr.select_font_face("Georgia", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            cr.move_to(x0, y0 + i*3*uy)
            cr.show_text(str(j))
            cr.set_source_rgb(0.06, 0.06, 0.33)
            cr.set_font_size(28)
            cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.move_to(x0, y0 + i*3*uy + uy*1.5)
            cr.show_text(str(k))


        x0, y0 = 19.5*ux, 19.5*uy 
        labels = ["Perfiles reconocidos:", "Mensajees de spam:", "Mensajes extraños"]
        data   = [objects.botStats.sus_names, objects.botStats.spam_msg, objects.botStats.strange]
        for i,(j,k) in enumerate(zip(labels, data)):
            cr.set_source_rgb(0.54, 0.75, 0.96)
            cr.set_font_size(24)
            cr.select_font_face("Georgia", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            cr.move_to(x0, y0 + i*3*uy)
            cr.show_text(str(j))
            cr.set_source_rgb(0.06, 0.06, 0.33)
            cr.set_font_size(28)
            cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.move_to(x0, y0 + i*3*uy + uy*1.5)
            cr.show_text(str(k))
        
        cr.set_source_rgb(0.23, 0.36, 0.64)
        cr.rectangle(4*ux, 6.5*uy, 10*ux, 2*uy)
        cr.rectangle(26*ux, 6.5*uy, 10*ux, 2*uy)
        cr.rectangle(26*ux, 16.5*uy, 10*ux, 2*uy)
        cr.fill()
        cr.stroke()
        cr.set_line_width(2)
        cr.set_source_rgb(0.06, 0.06, 0.33)
        cr.rectangle(4*ux, 6.5*uy, 10*ux, 2*uy)
        cr.rectangle(26*ux, 6.5*uy, 10*ux, 2*uy)
        cr.rectangle(26*ux, 16.5*uy, 10*ux, 2*uy)
        cr.stroke()

        cr.set_source_rgb(0.5, 0.7, 0.89)
        cr.set_font_size(24)
        cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.move_to(4.5*ux, 8*uy )
        cr.show_text("Tiempo")
        cr.move_to(26.5*ux, 8*uy )
        cr.show_text("Analizado")
        cr.move_to(26.5*ux, 18*uy )
        cr.show_text("Detectado")

        cr.set_font_size(52)
        cr.move_to(3*ux, 4.5*uy )
        cr.show_text("Estadísticas")
        cr.stroke()
        
        
        cr.set_source_rgb(0.05, 0.13, 0.21)
        cr.set_font_size(36)
        cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.move_to(2.5*ux, 23*uy )
        cr.show_text("Naturaleza")
        cr.move_to(2.5*ux, 25*uy )
        cr.show_text("Muerta")
        cr.set_font_size(20)
        cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.move_to(2.5*ux, 27*uy)
        cr.show_text("Los datos están tomados")
        cr.move_to(2.5*ux, 28.25*uy)
        cr.show_text("desde el 5/08/2022")

        sf.write_to_png("media/stats.png")
        async with AIOFile("media/stats.png", 'rb') as file:
            img = await file.read()
            from src.imageSend import send_image
            await send_image(ctx, img)
        return

