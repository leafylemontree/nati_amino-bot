from src import utils
from random import random
from aiofile import async_open, AIOFile

datos_gatos = [
                """En términos de desarrollo, el primer año de vida de un gato es igual a los primeros 15 años de una vida humana. Después de su segundo año, un gato tiene 25 años equivalentes al de un humano. Y después de los dos años, cada año de vida de un gato equivale a unos 7 años humanos.

                Adicionalmente, los gatos pueden vivir hasta un poco más que los 16 años.""",
                "Los gatos se comunican a través de vocalizaciones y entre ellas la más popular es el maullido. También, cabe mencionar que, junto con el perro, son los animales más populares para escoger como mascota, debido a su adaptabilidad y características.",
                "Tienen una flexibilidad y agilidad impresionante, pueden saltar desde más de 3 metros de altura.",
                "Los gatos pueden rotar sus orejas 180 grados.",
                "Los gatos pueden pasar hasta 14 horas dormidos.",
                "Debido a su naturaleza nocturna, los gatos suelen ser mucho más hiperactivos en la tarde.",
                "La audición del gato promedio es al menos cinco veces más aguda que la de un adulto humano.",
                "En la raza de gato más grande, el macho promedio pesa aproximadamente 9 kilos.",
                "Los gatos domésticos pasan cerca del 70 por ciento del día durmiendo, y 15 por ciento del día acicalándose.",
                "Un gato no puede ver directamente debajo de su nariz.",
                "Tienen uno de los sistemas sensoriales más sofisticados del mundo.",
                "La mayoría de los gatos no tiene pestañas.",
                "Los gatos tienen cinco dedos en cada pata delantera, pero sólo cuatro en la parte posterior. Sin embargo, no es raro que los gatos tengan dedos extra. ¡El gato con la mayor cantidad de dedos conocidos tenía 32, ocho en cada pata!",
                "Algunas personas creen que si sueñas con un gato blanco, te seguirá la buena suerte.",
                "Los maullidos no son un lenguaje innato para gatos, ¡los desarrollaron para comunicarse con los humanos!"
        ]

datos_perros = [
                "Los perros nacen sordos y ciegos.",
                "La nariz de los perros puede llegar a tener hasta 300 millones de receptores olfativos.",
                "Las papilas gustativas de los perros varían de 1,700 a 2,000 versus las casi 10,000 papilas gustativas que tenemos los humanos.",
                "La inteligencia de los canes es similar a la de un niño de 2 años.",
                "Los perros pueden llegar a entender hasta 250 palabras.",
                "Los perros si tienen una percepción del tiempo, y pueden percibir lapsos de tiempo de hasta 4 horas.",
                "Los perros que no han sido castrados, reciben el terminó de perros enteros.",
                "La raza de perros más antigua es el Saluki, se han encontrado vestigios de estos perros en tumbas egipcias.",
                "Existen aproximadamente 600 millones de perros en el mundo, se estima que 400 millones son perros callejeros.",
                "Los perros pueden sentir celos cuando sus dueños están con otros animales o personas.",
                "Los perros no ven en blanco y negro, ven además de estos colores las gamas de grises y colores azules y amarillos.",
                "Los ojos de los perros brillan en la noche, y en las fotos, debido a una telita o membrana que los recubre, se llama Tapetum lucidum, que es lo que les permite ver de noche.",
                "La palabra Collie, de todas las razas de collies, significa negro, y ese nombre viene porque estos perros solían cuidar ovejas de cara negra.",
                "La palabra Terrier, del grupo de razas de perros terrier, significa tierra en latín, y ese nombre fue usado para designar a los perros pequeños que hacían trabajos en la tierra, como cazar ratas o alimañas.",
                "La nariz del perro está húmeda, porque así puede absorber mejor los químicos aromáticos del ambiente.",
                "Los perros pueden contagiarse de los bostezos de sus dueños.",
                "Todos los perros, sin importar su edad, sueñan, aunque debes saber que los perros en edad adulta son los que más sueños tienen.",
                "Los perros duermen encimados para regular su temperatura, y protegerse de ataques."
        ]


async def data(ctx, aw):
    msg = "------------\n"
    if   aw.content[1].upper() == "-GATO" : msg = f"Dato sobre los gatos:\n\n{datos_gatos[int(random() * len(datos_gatos))]}"
    elif aw.content[1].upper() == "-PERRO": msg = f"Dato sobre los perros:\n\n{datos_perros[int(random() * len(datos_perros))]}"
    else : print(aw.content)
    await ctx.send(msg)
    return

async def animalImg(ctx, aw):
    path = "media/animals/"
    if   aw.content[1].upper() == "-GATO" : path = f"{path}cats/{int(random() * 8)}.jpg"
    elif aw.content[1].upper() == "-PERRO": path = f"{path}dogs/{int(random() * 8)}.jpg"

    async with AIOFile(path, 'rb') as file:
            img = await file.read()
            from src.imageSend import send_image
            await send_image(ctx, img)

    return

@utils.waitForMessage(message="-DATO", callback=data)
@utils.waitForMessage(message="-IMAGEN", callback=animalImg)
async def animals(ctx):
    await ctx.send("""
Comando de animalitos (de prueba)

Ingrese uno de los siguientes
-dato
-imagen
""")
    return






