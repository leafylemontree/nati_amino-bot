from src import utils
import cairo
from aiofile import AIOFile

@utils.checkFor(m=1, M=24, notcount=1, copy=1)
async def plot(ctx, msg):
    
    constants = []
    for i in msg: constants.append(float(i))
    l = len(msg)-1
    for a,i in enumerate(constants): print(a,l-a,i)

    sf = cairo.ImageSurface(cairo.FORMAT_RGB24, 512,512)
    cr = cairo.Context(sf)
    cr.set_source_rgb(1, 1, 1)
    cr.rectangle(0, 0, 512, 512)
    cr.fill()
    cr.stroke()
    cr.set_source_rgb(0.7, 0.7, 0.7)
    cr.move_to(0, 255)
    cr.line_to(511, 255)
    cr.stroke()
    cr.move_to(255, 0)
    cr.line_to(255, 511)
    cr.stroke()

    cr.set_source_rgb(0.75, 0.16, 0.2)
    accumulator = 511
    cr.set_line_width(4)

    for x in range(512):
        cr.move_to(x, 255-accumulator)
        accumulator = 0
        for n,c in enumerate(constants):
            accumulator += (c * (((x-255)/16) ** (l-n)))
        print(x, accumulator)
        accumulator *=  16
        accumulator  =  256 if accumulator >  256 else accumulator
        accumulator  = -256 if accumulator < -256 else accumulator
        cr.line_to(x, 255-accumulator)
        cr.stroke()
    
    sf.write_to_png("media/graph.png")
    async with AIOFile("media/graph.png", 'rb') as file:
        img = await file.read()
        from src.imageSend import send_image
        await send_image(ctx, img)
    return

