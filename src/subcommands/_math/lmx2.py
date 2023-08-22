import ctypes
from PIL import Image
import io
from src.images import paletteCard
from src import utils

libmx2 = ctypes.cdll.LoadLibrary("./src/subcommands/_math/eigen/main.so")

def prepareImage(image):
    d = 8

    img = Image.open(image).convert("L")
    im2 = img.resize((d, d))

    v = im2.split()[0].tobytes()
    w = im2.width
    h = im2.height
    print(h,w, v)

    libmx2.eigen_image.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_char_p,)
    libmx2.eigen_image.restype  =  ctypes.c_char_p
    s = libmx2.eigen_image(w, h, v)
    return s

def splitImage(image):
    img     = Image.open(image).convert("RGB")
    w       = img.width
    h       = img.height
    r,g,b   = img.split()
    r       = r.tobytes()
    g       = g.tobytes()
    b       = b.tobytes()
    libmx2.image_tree.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,)
    libmx2.image_tree.restype  =  ctypes.c_char_p
    s = libmx2.image_tree(w, h, r, g, b)
    return s

@utils.userTracker("valores-propios")
async def imageEigenvalues(ctx):
    im = None
    if ctx.msg.extensions.replyMessage is None: return await ctx.send("Debe usar este comando respondiendo a una imagen")
    else: im = ctx.msg.extensions.replyMessage.mediaValue
    
    response    = await ctx.client.session.request(method='GET', url=im)
    image       = io.BytesIO(await response.read())
    image.seek(0)
    
    s = prepareImage(image)
    if s is None: return await ctx.send("Ha ocurrido un error, :c.")
    await ctx.send(s.decode('utf-8'))

class Color:
    r:  int
    g:  int
    b:  int
    w:  float

    def __init__(self, s):
        s = s.split("\t")
        if s == ['']: return
        if len(s) > 1: self.w = float(s[1])
        else         : self.w = 1
        self.r = int(s[0][:2], 16)
        self.g = int(s[0][2:4], 16)
        self.b = int(s[0][4:], 16)
        return

    def __repr__(self):
        return f"""
Hex: {hex(self.r * 65536 + self.g*256 + self.b)}
r  : {self.r}
g  : {self.g}
b  : {self.b}
weight: {self.w}
"""


@utils.userTracker("paleta")
async def imagePalette(ctx):
    im = None
    if ctx.msg.extensions.replyMessage is None: return await ctx.send("Debe usar este comando respondiendo a una imagen")
    else: im = ctx.msg.extensions.replyMessage.mediaValue
    
    response    = await ctx.client.session.request(method='GET', url=im)
    image       = io.BytesIO(await response.read())
    image.seek(0)

    s           = splitImage(image)
    s           = s.decode("utf-8")
    s           = s.split("\n")
    palette     = [Color(t) for t in s[:-1]]

    result      = io.BytesIO()
    image.seek(0)
    temp = Image.open(image)
    temp.save(result, format="PNG")
    result.seek(0)
    await paletteCard(ctx, palette, result)
    return 

