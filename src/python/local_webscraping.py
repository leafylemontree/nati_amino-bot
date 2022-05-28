import requests
from bs4 import BeautifulSoup

DEEP_AI_API_KEY = "1815b770-ab06-40c2-9481-4934e7de0c4c"

class web_tools:
    def generateText(msg):
        global DEEP_AI_API_KEY

        response = requests.post(
                "https://api.deepai.org/api/text-generator",
                data    = {'text': msg},
                headers = {'api-key': "1815b770-ab06-40c2-9481-4934e7de0c4c"}
        )
        text = response.json()
        return text['output']
    def bible(msg):
        msg = msg.split(" ")
        libro     = ""
        capitulo  = -1
        versículo = -1

        if len(msg) < 3: return "Los argumentos no son los suficientes"
        elif len(msg) == 3:
            libro = msg[1]
            try: capitulo = int(msg[2])
            except: return "El argumento 2 no es un número"

        elif len(msg) == 4:
            libro = msg[1]
            try: capitulo = int(msg[2])
            except: return "El argumento 2 no es un número"

            try: versiculo= int(msg[3])
            except: return "El argumento 3 no es un número"

        url = f"https://www.bibliaenlinea.org/{libro}-{capitulo}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        text    = str(soup.find("h1", class_="post-title"))
        title   = web_tools.utils.getText(text, '</h1')

        text     = str(soup.find("div", class_="post-entry"))
        parr     = web_tools.utils.getText(text, '<div class="lazysocialbuttons"')
        return f"[cb]{title}\n\n{parr}"[:2000]
    def horoscopo(msg):
        msg = msg.split(" ")
        if len(msg) < 2 : return "Horóscopo de hoy. Si deseas saber sobre tu signo, ponlo después del comando, así:\n\n--horoscopo cancer"
        msg[1] = msg[1].lower()
        names = ["aries", "tauro", "geminis", "géminis", "cancer", "cáncer", "leo", "virgo", "libra", "escorpio", "sagitario", "capricornio", "acuario", "piscis"]

        if msg[1] not in names : return f'El parámetro ingresado "{msg[1]}" no es válido.'
        if   msg[1] == 'geminis': msg[1] = 'Géminis'
        elif msg[1] == 'cancer' : msg[1] = 'Cáncer'

        msg[1] = (msg[1][:1].upper()) + msg[1][1:]
        url = "https://www.clarin.com/horoscopo/"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        text = str(soup.find("div", id=f"data-{msg[1]}"))
        text = web_tools.utils.getText(text, "</div")
        return f"[CB]{msg[1]}\n\n{text}"
    def birthChart(msg):
        data = {
                    "nombre"    : "",
                    "dia"       : "",
                    "mes"       : "",
                    "ano"       : "",
                    "hora"      : "",
                    "minutos"   : "",
                    "pais"      : "100",
                    "geoloc"    : "2",
                    "V5"        : ""
        }

        msg = msg.upper().split("\n");
        print(msg)
        msg = msg[1:]



        for i in msg:
            j = i.split(' ')
            value = None
            label = None

            for k in j:
                if ((k in ['NOMBRE', 'HORA', 'FECHA']) & (label is None)) : label = k
                elif ((k != '=') & (label is not None)) : value = k

            print(label, value)
            if   label == "NOMBRE"  : data['nombre'] = value
            elif label == "HORA"    :
                value = value.split(":")
                data['hora']    = value[0]
                data['minutos'] = value[1]
            elif label == "FECHA"   :
                value = value.split("/")
                data['dia'] = value[0]
                data['mes'] = value[1]
                data['ano'] = value[2]

        print(data)
        page = requests.post("https://www.losarcanos.com/carta-astral-resu-m.php", data)
        soup = BeautifulSoup(page.content, "html.parser")
        text = str(soup.find("div", class_="arcanoastro1"))

        print(text)

        with open("out.txt", "w") as textFile:
            textFile.write(str(soup))

        return False;
    def lyrics(msg):
        rep  = ""
        msg  = msg[8:]
        url  = f"https://www.musica.com/letras.asp?t2={msg}"

        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        text = soup.find("table", class_="rst")
        text = text.find("table")
        text = text.find("tr").findChildren()
        if len(text) == 0: return "No se ha encontrado la letra :c."
        text = text[0]
        text = str(text.find("a"))
        url  = text.split('"')[1]

        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        text = soup.find("div", id="letra").findChildren()

        # for i in range(20):
        for i in text:
            r = web_tools.utils.getLabel(i)
            if r != "": rep += f"{r}\n\n"

        return rep[:2000]
    def definition(msg):
        msg = msg.split(" ")
        if len(msg) < 2: return "Coloque una palabra de la que gusta saber su significado.\n\nEjemplo: --def naturaleza"

        msg = msg[1].lower()
        url = "https://www.wordreference.com/definicion/" + msg
        page = requests.get(url)
        if page == 500: return "No se encuentra esta palabra"
        soup = BeautifulSoup(page.content, "html.parser")
        text = soup.find("ol", class_="entry").findChildren()

        reply = f"[cb]{msg}:\n\n"
        print(text)

        for a, i in enumerate(text):
            reply += f"{web_tools.utils.getText(str(i), '<br/')}\n"

        # print(soup)
        # print(reply)

        return reply[:2000]

    class utils:
        def getText(text, comp):
            parr = ""
            active = 1
            dom = ""
            for i in text:
                if i == "<":         active = 0
                elif i == ">":       active = 2

                if dom == comp:      break

                if active == 0:      dom += i
                elif active == 1:    parr += i
                elif active == 2:
                    active -= 1
                    dom = ""

            return parr
        def getLabel(text):
            rep  = ""
            text = str(text)
            text = text.split("<")
            text.pop(0)
            for i in text:
                i = i.split(">")
                if   ((i[0] == 'p'  ) & (i[1] != ""))  : rep += i[1]
                elif ((i[0] == 'br/') & (i[1] != ""))  : rep += f"\n{i[1]}"
            # print(text)
            return rep
