from src.objects import ba
from random import random
from aiofile import AIOFile
import asyncio

jokes = [
            "No todas las Nati son iguales, algunas de las dos puede molestarse con facilidad",
            'Nati significa "Nuevo bot de Amino, Tecnológicamente Inferior"',
            "Ante fallas con el bot, acudir con el dueño, si no, corran por sus vidas",
            "Todas las naciones de Amino estuvieron en regla, hasta que la nación de las Nati atacó, y cuando más se necesitaba a Leafy, este desapareció",
            "No le intenten dar sentido a los nombres de los comandos, por lo general se ponen una vez provicionalmente, y luego se quedan así",
            "Nati posee modos ocultos. Puede verlos si accede al Github del bot",
            "Nati no ataca a Luna, Drev y Mari, sin embargo, Venti sí parece ser atacado por ella, por lo que, efectivamente, bot misándrica",
            "Las opiniones vertidas en las noticias son de uso exclusivo de quien las ha creado, y no representa la manera de pensar ni del bot ni del dueño",
            "Neko kawaii busca ama felina que le haga compañía. Si usted desea, ponga el comando --soytunekitaonishan, y le mandaremos al psicólogo",
            "Limonero Frondoso pudo haber sido un Manzano Frondoso",
            "Nati los espía, cuidado",
            "No se confíen de los espejismos, podrían ser efímeros",
            "Hay una escena (perdida) en la que estaban Nati y Mari en las escaleras. Una día Nati tomó el violín de Mari, y por consiguiente esta se enojó con ella, y Nati sin pensarlo empujó a Mari con la mala suerte que este cayera de cabeza, muriendo en el acto. Nati entonces escapó de la casa y fue donde Venti para que le ayudara a esconder el cuerpo",
            "Lo anterior era una referencia a Omori, ha",
            "Nati puede o no estar conectada con servicios legales de fuerza y seguridad ciudadana. Todo lo que digan puede o no recibir la policía",
            "Dependiendo de la instancia, tendrán perfiles diferentes. La 1 tiene a Najimi, mientras que la 2 a Yashiro. La versión dev tiene a Vueroeruko, ¿podrá adivinar la tercera?",
            "Nati es un ser malvado.\n    --Kyubey",
            "Intenten adivinar el sexo de quien ha creado el bot. Spoiler, ese no es",
            "L muere al final de Death Note",
            "Maria, abre la ventana",
            "Esperabas que esto fuera un dato curioso, pero era yo, una broma reciclada",
            "La mitad de los datos o son falsos, o son el creador haciendo el pelmazo",
        ]

async def instance(ctx):
    if int(random() * 20) == 0:
        async with AIOFile(f'media/enojo.jpg', 'rb') as file:
                 await ctx.send("/c enoja")
                 await asyncio.sleep(1)
                 img = await file.read()
                 from src.imageSend import send_image
                 await send_image(ctx, img)
                 return

    wallet = await ctx.client.get_wallet_info()
    await ctx.send(f"Esta instancia de Nati es la número: {ba.instance + 1}\nPosee: {wallet.totalCoins} AC\n\nDato:\n{jokes[int(random() * len(jokes))]}")
