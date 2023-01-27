import ctypes
from aiofile import async_open, AIOFile
from src import utils
from PIL import Image as PImage
import struct
import os

path = 'src/subcommands/_math/c/'

async def imgMatrix(ctx):
    imgDs = ctypes.cdll.LoadLibrary(f'{path}imgMatrix.so')
    im    = None
    if ctx.msg.extensions.replyMessage is None: return await ctx.send("Debe usar este comando respondiendo a una imagen")
    else: im = ctx.msg.extensions.replyMessage.mediaValue
    print(im)
    await utils.downloadImage(im) 

    img     = PImage.open('media/dl.jpg')
    w       = img.width
    h       = img.height
    r,g,b   = img.split()
    r       = r.tobytes()
    g       = g.tobytes()
    b       = b.tobytes()
    
    try:
        m = ctx.msg.content.split('\n)')[0].split('(\n')[-1]
    except Exception:
        return await ctx.send("""Ha habido un error ingresando la matriz.

Las matrices deben ingresarse de esta manera:
(
0 1 0
1 4 1
0 1 0
)""")
    
    nor_ = 0
    if ctx.msg.content.upper().find("-NORMALIZE") != -1 : nor_ = 1 

    class Matrix:
    
        def __new__(self, st):
            print(st)
            r = st.replace("\n", " ").split(" ")
            l = b''
            for i in r:
                l += bytearray(struct.pack('f', float(i)))
            self.w   = len(st.split("\n"))
            self.h   = int(len(l)/4) // self.w
            self.raw = l

            if (self.w * self.h) != int(len(self.raw)/4): return None
            return self

    mat = Matrix(m)
    print(mat.w, mat.h, mat.raw)

    imgDs.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int,)
    imgDs.restype  = ctypes.c_char_p
    a = imgDs.arrayRead(r, b, g, len(r), w, h, mat.raw, mat.w, mat.h, nor_)
    
    os.system(f"convert -size {w}x{h} -depth 8 rgb:imgout.raw media/res.png")
    async with AIOFile("media/res.png", 'rb') as file:
                img = await file.read()
                from src.imageSend import send_image
                await send_image(ctx, img)

    return
