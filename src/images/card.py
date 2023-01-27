import cairo
import qrcode
from aiofile import AIOFile

async def card(ctx):
    print("cards")
    text = ctx.msg.content
    text = text.split('\n')
    text.pop(0)
    print(text)
    
    w = 1004
    h = 590
    im = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
    cr = cairo.Context(im)

    name        = text.pop(0)
    alias       = text.pop(0)
    title       = text.pop(0)
    time        = text.pop(0)
    price       = text.pop(0)
    subjects    = text.pop(0)
    fraud       = text.pop(0)

    cr.move_to(0, 0)
    pfp = cairo.ImageSurface.create_from_png("media/cardtemplate1.png")
    cr.save()
    cr.set_source_surface(pfp)
    cr.paint()
    cr.restore()

    cr.move_to(42, 144)
    cr.set_source_rgb(0.2, 0.26, 0.32)
    cr.set_font_size(70)
    cr.select_font_face("Breathing Personal Use", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.show_text(f'{name} {f"({alias})" if alias else ""}')
    cr.stroke()

    cr.move_to(44, 216)
    cr.set_font_size(44)
    cr.select_font_face("TimeBurner", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.show_text(title)
    cr.stroke()
    cr.set_font_size(32)
    cr.select_font_face("TimeBurner", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    
    cr.move_to(44, 298)
    cr.show_text(f"HORARIO: {time}")
    cr.stroke()
    cr.move_to(44, 336)
    cr.show_text(f'PRECIO: {price}')
    cr.stroke()
    cr.move_to(44, 374)
    cr.show_text(f'MATERIAS: {subjects}')
    cr.stroke()
    cr.move_to(44, 412)
    cr.show_text(f'VERIFICACIÓN DE 0 FRAUDES: {fraud}')
    cr.stroke()

    qr = qrcode.make(f'ndc://user-profile/{ctx.msg.author.uid}')
    qr.save('media/qrout.png')

    
    cr.move_to(0, 0)
    qr = cairo.ImageSurface.create_from_png("media/qrout.png")
    cr.save()
    cr.translate(254, 434)
    cr.scale(0.36, 0.36)
    cr.set_source_surface(qr)
    cr.paint()
    cr.restore()

    cr.stroke()
    im.write_to_png("media/card.png")  # Output to PNG
    
    async with AIOFile(f'media/card.png', 'rb') as file:
                img = await file.read()
                from src.imageSend import send_image
                await send_image(ctx, img)

