import mariadb
import datetime, time
import matplotlib.pyplot as plt
import cairo
from aiofile import AIOFile
from src.database import db
import ctypes
import math

def getNext(data):
    path = 'src/subcommands/_math/c/'
    predict = ctypes.cdll.LoadLibrary(f'{path}predic.so')
    predict.predict.argtypes = (ctypes.c_char_p, ctypes.c_int,)
    predict.predict.restype  = ctypes.c_float
    ls = data[-16:]

    bytedata = b''
    for value in ls:
        bt = value.to_bytes(4, byteorder="little", signed=True)
        bytedata += bt
    pr = predict.predict(bytedata, len(ls))
    print(pr)
    return abs(pr/math.factorial(10))


async def botstats2(ctx):
    msg = ctx.msg.content.upper().split(" ")
    if   len(msg) == 1: msg.append("-G")
    msg.pop(0)
    if   len(msg) == 1: msg.append("48")
    
    if msg[0] == "-C":
        db.cursor.execute(f"SELECT * FROM Reports WHERE comId={ctx.msg.ndcId}")
    else:
        db.cursor.execute(f"SELECT * FROM Reports")

    hours = 0
    if   msg[1] == "2"  :   hours = 2
    elif msg[1] == "24" :  hours = 24
    elif msg[1] == "48" :  hours = 48
    elif msg[1] == "96" :  hours = 96
    else                : hours = 120
    days = int(hours/24)
    crdate = datetime.datetime.now()
    update = datetime.timedelta(hours=hours)
    
    a = db.cursor.fetchall()
    reportLength = len(a)
    data = []
    labels = []
    rtype = [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
                ]

    for i in range(hours * 4):
        data.append(0)
        labels.append(days*24 - (i//4))
    for registry in a:
        dt = registry[3]
        if (crdate - dt) > update: continue
        secs =  time.mktime(crdate.timetuple()) - time.mktime(dt.timetuple())
        data[-int(secs) // 1200] += 1
        if registry[4]:     rtype[0] += 1
        if registry[5]:     rtype[1] += 1
        if registry[6]:     rtype[2] += 1
        if registry[7]:     rtype[3] += 1
        if registry[8]:     rtype[4] += 1
        if registry[9]:     rtype[5] += 1
        if registry[10]:    rtype[6] += 1
        if registry[11]:    rtype[7] += 1
        if registry[12]:    rtype[8] += 1
        if registry[13]:    rtype[9] += 1
        if registry[14]:    rtype[10] += 1
   
    derivative = []
    fx  = 0
    fxh = 0
    h = 1
    labels3 = []
    for n,value in enumerate(data):
        fxh += value
        if n%4 == 3:
            derivative.append((fxh - fx)/h)
            labels3.append(n//4)
            fx  = fxh
            fxh = 0

    derivative.reverse()

    plt.bar(labels, data, label="Nº de reportes")
    plt.xlabel("Tiempo (horas)")
    plt.ylabel("Reportes")
    plt.title("Reportes obtenidos a tiempo real")
    plt.legend()
    plt.savefig("media/botstats2/graph1.png")
    plt.cla()
    plt.clf()

    plt.plot(labels3, derivative, color='red', label="Derivada")
    plt.xlabel("Tiempo (horas)")
    plt.ylabel("Tasa de cambio")
    plt.title("Derivada reportes a tiempo real")
    plt.legend()
    plt.savefig("media/botstats2/graph3.png")
    plt.cla()
    plt.clf()
    
    labels2=['Nick reconocidos', 'Palabras clave', 'Nick sexuales', 'Telegram', 'Amino', 'Amino', 'Twitter', 'Glitch', 'Longitud', 'Crash', 'Fantasma']
    plt.pie(rtype, labels=labels2, autopct="%1.1f%%i")
    plt.title("Tipo de reportes")
    plt.legend()
    plt.savefig("media/botstats2/graph2.png")
    plt.cla()
    plt.clf()


    sl = []
    a = 0
    print(data)
    for i,d in enumerate(data):
        a += d
        if i%4 == 3:
            sl.append(a)
            a = 0
    media = 0
    for d in sl: media += d
    media = int(media/len(sl))

    moda = max(set(sl), key=sl.count)

    sl.sort()
    l = len(sl)
    if l%2  : mediana = int((sl[(l-1)//2] + sl[(l+1)/2])//2)
    else    : mediana = sl[int(l/2)]

    nxhour = getNext(data)

    w,h = 1024,1280
    im = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
    cr = cairo.Context(im)

    template = cairo.ImageSurface.create_from_png("media/botstats2/botstats2.png")
    cr.save()
    cr.translate(0, 0)
    cr.set_source_surface(template)
    cr.paint()
    cr.restore()

    cr.set_source_rgb(0.09, 0.09, 0.29)
    cr.select_font_face("Lemon Juice", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

    cr.set_source_rgb(0.6, 0.6, 0.79)
    cr.select_font_face("Heavitas", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

    cr.set_font_size(64)
    cr.move_to(w-240, h-80)
    cr.show_text(str(round(nxhour, 2)))
    cr.set_font_size(64)
    cr.move_to(80, 524)
    cr.show_text(str(reportLength))
    cr.stroke()
    cr.set_font_size(40)
    cr.move_to(164, 192)
    cr.show_text(str(min(sl)))
    cr.stroke()
    cr.move_to(164, 288)
    cr.show_text(str(max(sl)))
    cr.stroke()
    
    cr.set_font_size(40)
    cr.move_to(164, h-148)
    cr.show_text(str(media))
    cr.stroke()
    cr.move_to(164, h-60)
    cr.show_text(str(moda))
    cr.stroke()
    cr.move_to(452, h-148)
    cr.show_text(str(mediana))
    cr.stroke()
    cr.move_to(452, h-60)
    cr.show_text(str(max(sl) - min(sl)))
    cr.stroke()
            
    graph1 = cairo.ImageSurface.create_from_png("media/botstats2/graph1.png")
    cr.save()
    cr.translate(336, 48)
    cr.scale(1, 1)
    cr.set_source_surface(graph1)
    cr.paint()
    cr.restore()
    
    graph2 = cairo.ImageSurface.create_from_png("media/botstats2/graph2.png")
    cr.save()
    cr.translate(576, 672)
    cr.scale(0.6, 0.6)
    cr.set_source_surface(graph2)
    cr.paint()
    cr.restore()
    
    graph3 = cairo.ImageSurface.create_from_png("media/botstats2/graph3.png")
    cr.save()
    cr.translate(48, 672)
    cr.scale(0.6, 0.6)
    cr.set_source_surface(graph3)
    cr.paint()
    cr.restore()
    
    cr.stroke()
    im.write_to_png("media/botstats2/stats2out.png")  # Output to PNG
    
    async with AIOFile("media/botstats2/stats2out.png", 'rb') as file:
            img = await file.read()
            from src.imageSend import send_image
            await send_image(ctx, img)
    return


