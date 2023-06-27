import cairocffi        as cairo 
from src.images.funcs import putText
import io

base    = cairo.ImageSurface.create_from_png("media/templates/palette_base.png")

async def paletteCard(ctx, colors, image):
    predominant = colors[0]
    subcolors   = colors[1:]

    image.seek(0)

    img = cairo.ImageSurface(cairo.FORMAT_RGB24, 1024, 1280)
    ct  = cairo.Context(img)
    file      = io.BytesIO()

    ct.save()
    ct.set_source_surface(base)
    ct.paint()
    ct.restore()

    imgPrev = cairo.ImageSurface.create_from_png(image)
    px, py  = imgPrev.get_width(), imgPrev.get_height()
    ct.save()
    ct.translate(64, 48)
    ct.scale((14*32)/px, (9*32)/py)
    ct.set_source_surface(imgPrev)
    ct.paint()
    ct.restore()
    ct.stroke()

    def printColor(ct, x, y, h, w):
        ct.move_to(x + 8, y + 8)
        ct.rectangle(x+8, y+8, 32*6, 32*2)
        ct.fill()
        ct.stroke()

        ct.set_source_rgb(0.852, 0.625, 0.953)
        ct.move_to(x + 32 * 6.75, y + 8)
        putText(ct, text=str(h), size=36, align="LEFT", width=32*6.5, height=32*1.5, font="Heavitas")
        if w != 0:
            ct.set_source_rgb(0.157, 0.07, 0.391)
            ct.move_to(x + 32 * 9, y + 32 * 1.5)
            putText(ct, text=f"{w:.2%}", size=24, align="RIGHT", width=32*4, height=32*1.5, font="Heavitas")
        return

    ct.set_source_rgb((predominant.r + 1)/256, (predominant.b + 1)/256, (predominant.b + 1)/256)
    printColor(ct, 16.5 * 32, 7 * 32, str(hex(predominant.r * 65536 + predominant.g * 256 + predominant.b))[2:], 0)

    sortedColors = sorted(subcolors, key=lambda x: x.w, reverse=True)
    weight = 0
    for color in sortedColors: weight += color.w
    for i,color in enumerate(sortedColors):
        x = (32 * 2)  + (i // 8) * (14.5 * 32)
        y = (32 * 13) + (i  % 8) * (   8 * 13)
        ct.set_source_rgb((color.r + 1)/256, (color.b + 1)/256, (color.b + 1)/256)
        printColor(ct, x, y, str(hex(color.r * 65536 + color.g * 256 + color.b))[2:], (color.w/weight))
        ct.stroke()

    img.write_to_png(file)
    file.seek(0)
    from src.imageSend import send_image
    await send_image(ctx, image=file.read())


