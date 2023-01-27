import aiohttp
import asyncio
from bs4 import BeautifulSoup
import random
#import cairo
from aiofile import async_open, AIOFile
import os

import cairocffi        as      cairo 
import pangocffi        as      pango
import pangocairocffi   as      pc
from   .funcs           import  putText
async def getNews(ctx):
    
    link        = ""
    imageLink   = ""
    title       = ""
    subtitle    = ""
    caption     = ""
    article     = []
    
    async with aiohttp.ClientSession() as session:
        async with session.get('http://www.bbc.com/mundo') as response:
            page        = BeautifulSoup(await response.text(), "html.parser")
            newsList    = page.find("ul", class_="e13i2e3d0")
            allNews     = newsList.findChildren(recursive=False)
            news        = allNews[int(random.random() * len(allNews))]
            aTag        = news.find("a")
            link        = str(aTag).split('href="')[1].split('"')[0]
        async with session.get('http://www.bbc.com/' + link) as response:
            page        = BeautifulSoup(await response.text(), 'html.parser')
            imageLink   = str(page.find("img", class_="e1mo64ex0")).split('src="')[1].split('"')[0]
            h1          = str(page.find('h1', class_='e1p3vdyi0')).split(">")[1].split("<")[0]
            t = h1.split(": ")
            title       = t[0].replace('"', "")
            subtitle    = t[1] if len(t) > 1 else ""
            caption     = str(page.find("figcaption", class_="e6i104o0").find("p")).replace("<p>", "").replace("</p>", "")
            print(imageLink)
            fullArticle = page.findAll("div", class_="ebmt73l0")
            for art in fullArticle:
                text = str(art.find("p")).replace("<p>","").replace("</p>","")
                if text == 'None': continue
                if text.find("<span") != -1: continue
                text = text.split('dir="ltr">')
                if len(text) > 1:
                    text = text[1].split("<")[0]
                    article.append(text)
       
        async with session.get(imageLink) as resp:
            async with AIOFile("media/news/dlimage.jpg", "wb+") as img:
                    await img.write(await resp.read())
                    os.system("magick media/news/dlimage.jpg media/news/dlimage.png")

    w = 1024
    h = 768
        
    im      = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
    ct      = cairo.Context(im)
    base    = cairo.ImageSurface.create_from_png("media/news/news.png")
    ct.save()
    ct.set_source_surface(base)
    ct.paint()
    ct.restore()
    
    img = cairo.ImageSurface.create_from_png("media/news/dlimage.png")
    px, py  = img.get_width(), img.get_height()
    ct.save()
    ct.translate(576, 384)
    ct.scale((384/px), (384/px))
    ct.set_source_surface(img)
    ct.paint()
    ct.restore()

    ct.move_to(560, 48)
    ct.set_source_rgb(1, 1, 1)
    putText(ct,
            text=title,
            size=48 if len(title) < 24 else 28, 
            align="LEFT",
            width=412,
            height=64,
            wrap="WCHAR",
            font="HEAVITAS")

    ct.move_to(576, 264)
    ct.set_source_rgb(1, 1, 1)
    putText(ct,
            text=subtitle,
            size=28, 
            align="CENTER",
            width=384,
            height=640,
            wrap="WCHAR",
            font="Lemon Juice")

    ct.set_source_rgb(0.07, 0.04, 0.27)
    ct.move_to(576,(384/px)*py + 408)
    putText(ct,
            text=caption,
            size=22, 
            align="CENTER",
            width=384,
            height=640,
            wrap="WCHAR",
            font="Lemon Juice")
    
    ct.move_to(48,0)
    article = "\n\n".join(article)
    putText(
            ct,
            text=article,
            size=14,
            align="LEFT",
            width=448,
            height=616,
            wrap="WORD",
            font="Evogria")
    
    im.write_to_png("media/news/newsout.png")
    
    async with AIOFile("media/news/newsout.png", 'rb') as file:
            img = await file.read()
            from src.imageSend import send_image
            await send_image(ctx, img)
       
    return
