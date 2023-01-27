from aiofile import async_open, AIOFile
from src import utils
from src import objects
import cairo

async def lineart(ctx):
        msg = ctx.msg.content.split(" ")
        if len(msg) < 6: return await ctx.send("Debe ingresar un polinomio de rango 5")

        x0 = float(msg[5])/2048
        x1 = float(msg[4])/512
        x2 = float(msg[3])/128
        x3 = float(msg[2])/32
        x4 = float(msg[1])/8

        im = cairo.ImageSurface(cairo.FORMAT_RGB24, w,h)
        ct = cairo.Context(im)

        ct.set_source_rgb(random.random(), random.random(), random.random())
        for i in range(128):
            ct.move_to(256 + 256*math.sin(i*2*math.pi/128), 256 + 256*math.cos(i*2*math.pi/(511 - x4 * i*i*i*i + x3*i*i*i + x2*i*i + x1*i + x0)))
            ct.line_to(256, 256-256*math.cos(x4*i*i*i*i - x3*i*i*i + x2*i*i - x1*i + x0))

        ct.stroke()
        im.write_to_png("media/line.png")
        async with AIOFile("media/line.png", 'rb') as file:
            img = await file.read()
            from src.imageSend import send_image
            await send_image(ctx, img)
        return
