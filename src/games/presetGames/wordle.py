from .base import BaseInstance
import cairo
from src.images.funcs import *
from aiofile import AIOFile

class Wordle(BaseInstance):

    class data:
        word        = "ARBOL"
        keys        = []
        turn        = 0
        state       = 0
        control     = False
        minPlayers  = 1
        maxPlayers  = 4

    async def screen(self, ctx):
        w = 560
        h = 576

        im = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
        cr = cairo.Context(im)
        
        cr.move_to(0, 0)
        base = cairo.ImageSurface.create_from_png("media/wordle/base.png")
        cr.save()
        cr.set_source_surface(base)
        cr.paint()
        cr.restore()

        name = self.players[self.data.turn][1]
        cr.move_to(160, 48)
        cr.set_source_rgb(1, 1, 1)
        cr.set_font_size(40)
        cr.select_font_face("Georgia", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.show_text(name)
        cr.stroke()

        cr.set_font_size(56)
        cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        for b,y in enumerate(self.data.keys):
            for a,(x,l) in enumerate(zip(y,self.data.word)):
                posX = 48 + a*96
                posY = 80 + b*96
                if x == l:
                    cr.set_source_rgb(0.24, 0.55, 0.12)
                    rounded(cr, posX, posY, 80, 80, 16)
                elif x in self.data.word:
                    cr.set_source_rgb(0.59, 0.58, 0.12)
                    rounded(cr, posX, posY, 80, 80, 16)
                
                cr.fill()
                cr.stroke()
                cr.set_source_rgb(1, 1, 1)
                cr.move_to(posX+18, posY+60)
                cr.show_text(x)
                cr.stroke()

        cr.stroke()
        im.write_to_png("media/wordle/output.png")  # Output to PNG
        async with AIOFile("media/wordle/output.png", 'rb') as file:
            img = await file.read()
            await ctx.send_image(img)
        return None

    async def logic(self, ctx, key):
        key = key.upper()
        if len(key) != len(self.data.word): return await ctx.send("El largo de la palabra no corresponde")

        self.data.keys.append(key)
        await self.screen(ctx)
        self.data.state += 1
        return

    async def win(self):
        if len(self.data.keys) < 6 and self.data.keys[-1] == self.data.word:
            self.data.turn += 1
            self.data.keys = []
            return True
        return False

    async def lose(self):
        if len(self.data.keys) > 5 and self.data.keys[-1] != self.data.word:
            self.data.turn += 1
            self.data.keys = []
            return True
        return False
