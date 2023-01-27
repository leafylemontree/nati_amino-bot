from multiprocessing import Pool
from aiofile import AIOFile
from .pyimgplt import Image, Objects 
from random import random

def abstractImageProcessing(steps):
        img = Image("test", 512, 512)
        col = Objects.c_Color(255, 255, 255, 255)
        img.generate(col)
        print(f"steps {steps}")
        
        a = [1, 510, 510]
        b = [1, 510, 510]

        try:
            for i in range(steps):
                col = Objects.c_Color(
                int(random()*255),
                int(random()*255),
                int(random()*255),
                255)

                a = [
                    a[1],
                    a[2], 
                1+int(random()*510),
                    ]

                b = [
                    b[1],
                    b[2], 
                1+int(random()*510),
                    ]
            
                img.draw.triangle(img, col, 
                    a[0],
                    b[0],
                    a[1],
                    b[1],
                    a[2],
                    b[2],
                    )
            img.write()
            img.free()
        except Exception:
            pass

async def abstractImage(ctx):
        steps = 64

        msg = ctx.msg.content
        if msg.find(" ") != -1:
            msg = msg.split(" ")[1]
            try:
                steps = int(msg)
            except:
                pass
            if steps > 100000: steps = 100000 
       
        #await abstractImageProcessing(steps)
        with Pool(1) as p: p.map(abstractImageProcessing, [steps])
        
        async with AIOFile(f'result.png', 'rb') as file:
                 img = await file.read()
                 from src.imageSend import send_image
                 await send_image(ctx, img)

        return "result.png"

