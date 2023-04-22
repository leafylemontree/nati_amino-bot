import io

class Help:
    DEFAULT = "\n[cb]Mari Mari\n[c]\u25e6 \u2756 \u25e6 \u2741 \u25e6 \u2756 \u25e6 \u2741 \u25e6 \u2756 \u25e6 \u2741 \u25e6 \u2756 \u25e6\n\n[ci]Hola, soy Nati, una bella usuaria creada por Leafy. Cualquier problema dirigirse con \u00e9l (enlace en la biograf\u00eda)\n\n[bc]Comandos:\n[c]\u2501\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u22b9\u22b1\u2719\u22b0\u22b9\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2501\n\n[c]--nano, --sigueme, --biblia, --horoscopo, --matrix, --cutes, --math, --blogs, --info, --help, --nombre, --say, --normas, --platypus, --dados, --doxx, --letra, --def, --article, --tweet, --sus, --soporte, --centro, --news, --join, --imgMatrix.\n\n[cb]Otros Mensajes:\n[c]\u2501\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u22b9\u22b1\u2719\u22b0\u22b9\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2501\n\n[c]plebeyos, la nave, kiwilatigo, ojos (\ud83d\udc40), uwu, doxxea a, :v, @everyone, @staff. \n\n\n[cb]Moderaci\u00f3n:\n[c]\u2501\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u22b9\u22b1\u2719\u22b0\u22b9\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2501\n\n[c]--setlog, --ban, --unban, --view, --config, --stats, --stats2, --deepanalyze, chatanalyze, --admin."

    def __init__(self):
        self.ALL = []
        pass

    def register(self, title, description, command=None, example=None, prefix='--'):
        helpText = HelpTextBase(title, description, command, example, prefix)
        setattr(self, helpText.title.upper().replace('-', ''), helpText)
        self.ALL.append(helpText)
        return
    
    def gen(self):
        return tuple(map(lambda helpText: helpText.title, self.ALL))


class HelpTextBase:
    def __init__(self, title, description, commands=None, example=None, prefix='--'):
        self.title          = title
        self.description    = description
        self.commands       = commands
        self.example        = example
        self.prefix         = prefix

    def __str__(self):
        nl  = '\n'
        nlc = '\n[c]'

        text = io.StringIo()
        text.write(f"""
[cbu]{self.prefix}{self.title}
[c]\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550.\u2665.\u2550

[c]{description.replace(nl, nlc)}""")
        
        if self.commands:
            text.write('\n\n[cb]Comandos:')
            text.write('\n\n'.join([f'[cu]{prefix}{title} {com[0]}\n[c]{com[1]}' for com in self.commands ]))

        if self.example:
            text.write('\n\n[cb]Ejemplos:')
            text.write('\n\n'.join([f'[cu]{prefix}{title} {exm}' for exm in self.example ]))
        
        s = text.getvalue()
        text.close()
        return s

helpInfo = Help()

helpInfo.register('nano', 'Este comando est\u00e1 hecho a modo de ejemplo de respuesta del bot. Queda ac\u00e1 por motivos hist\u00f3ricos.\n\nTrivia: el nano al cual se refiere hace referencia a GNU nano, un editor de texto que suele venir en las instalaciones de Linux por defecto.')
helpInfo.register('wordle' ,'Inicia un juego de Wordle. Wordle es un juego que trata de adivinar una palabra ingresando palabras de la misma longitud, con la gracias que las letras que coinciden en posici\u00f3n son marcadas entre corchetes.', command=[['-init', 'inicia el juego.'], ['-info', 'muestra ayuda de c\u00f3mo jugarlo.']])
helpInfo.register('sigueme' ,'El bot seguir\u00e1 su perfil desde ahora.')
helpInfo.register('chat', 'En beta a\u00fan. Esta funci\u00f3n le permite ingresa texto y esperar que el bot contin\u00fae escribiendo.')
helpInfo.register('biblia', 'Busca y responde con un cap\u00edtulo de la biblia (edici\u00f3n Reina Valera 1960).\n\n[c]Para buscar un cap\u00edtulo, debe ingresar el nombre del libro en min\u00fascula (salmos, genesis), y el n\u00famero del cap\u00edtulo. Se truncar\u00e1 el mensaje a 2000 caracteres.', command=[['(libro) (capítulo)', 'Muestra el capítulo y libro seleccionado.']], example=['romanos 8', 'salmos 119', 'jeremias 33'])
helpInfo.register('horoscopo', 'Lee el hor\u00f3scopo de hoy con sus poderes de oyente.\n[c]Se accede colocando el nombre del signo zodiacal tras el comando.\nSe actualiza a diario.', command=[['(signo)', 'Regresa el horóscopo del signo dado']], example=['aries'])
helpInfo.register('matrix', 'Modo para manipular matrices, permite multiplicaci\u00f3n y suma de estas.\nLas matrices se ingresan de esta manera:\n(\na b\nc d\n)\n\ncon a, b, c, d  siendo n\u00fameros enteros. Hay soporte para matrices de mayor tama\u00f1o a\u00fan, por ejemplo 3x3, e incluso rectangulares.', command=[['-mul', 'Multiplica dos matrices.'],['-add','Suma dos matrices.']], example=['-mul (\n0 1\n1 0\n(\n\n(\n1 2\n3 4\n)'])
helpInfo.register('cutes', 'Env\u00eda una imagen tierna que representa a dos usuarios, quien manda el comando y a quien va dirigido.', command=[['hug @usuario', 'abrazo.'], ['kiss @usuario', 'beso.'], ['pat', 'acariciar']])
helpInfo.register('math', 'Permite hacer operaciones matem\u00e1ticas, tanto individuales como en modo cinta. El modo cinta es una serie de comandos, ejecutados uno despues de otro que permite cargar funciones m\u00e1s complejas.\n\n[cb]Comandos (modo normal):\n[c]add (n\u00famero) (n\u00famero): suma dos n\u00fameros. \n[c]sub (n\u00famero) (n\u00famero): resta dos n\u00fameros. \n[c]mul (n\u00famero) (n\u00famero): multiplica dos n\u00fameros.\n[c]div (n\u00famero) (n\u00famero): divide dos n\u00fameros.\n[c]pow (n\u00famero) (n\u00famero): eleva el primer n\u00famero al segundo.\n\n[c]sqr (n\u00famero): retorna la ra\u00edz cuadrada del n\u00famero ingresado.\n[C]{ (funci\u00f3n)} : entra en modo cinta.\n\n[Cb]Comandos (modo cinta):\n[C]Los mismos del modo normal, con soporte para variables literales.\n\n[c]var (nombre) (n\u00famero): Permite crear una variable con un nombre y n\u00famero por defecto.\n\n[c]print (variable): imprime el valor de la variable como resultado.')
helpInfo.register('blogs', 'Retorna los blogs del usuario, sean los \u00faltimos 25 de este, o uno en espec\u00edfico.', command=[['-user -all','entrega los nombres de los \u00faltimos 25 blogs del usuario.'], ['-user número', 'entrega informaci\u00f3n adicional del blog seleccionado.']])
helpInfo.register('info', 'Entrega informaci\u00f3n detallada del usuario, como fecha de uni\u00f3n, blogs subidos, comentarios, etc', example=['@usuario'])
helpInfo.register('plebeyos', 'Peque\u00f1o mensaje que hace alusi\u00f3n a un grupo')
helpInfo.register('la nave', 'Jose Jose lo hubiera querido as\u00ed')
helpInfo.register('help', 'Muestra ayuda de los diferentes comandos, as\u00ed como los existentes hasta el momento.', command=[['(comando)', 'informaci\u00f3n de ese comando, incluyendo los comandos disponibles']])
helpInfo.register('nombre', 'Repite el nombre del usuario que llame el comando')
helpInfo.register('say', 'Repite todo lo que se ponga despu\u00e9s del comando', example=[['hola']])
helpInfo.register('kiwilatigo', 'No lo toquen o haran enojar a quien lo ejecuta, unu')
helpInfo.register('normas', 'Entrega las normas de la comunidad')
helpInfo.register('ojos', 'No miren a Nati que los mira de vuelta')
helpInfo.register('uwu', 'uwu')
helpInfo.register('platypus', 'Responde cosas que les gusta a los ornitorrincos')
helpInfo.register('meth', 'Quiz\u00e1s quizo decir: math.\n[c]\ud83d\udc40')
helpInfo.register('dados', 'Retorna un n\u00famero entre 1 y el n\u00famero ingresado, como si se tiraran dados, pero tambi\u00e9n tiene soportes para n\u00famero m\u00e1s grandes.', command=[[')n\u00famero)', 'tope superior del generador de n\u00fameros']])
helpInfo.register('sus', 'amogus, ao ao, amogus aaAAA')
helpInfo.register('doxx', 'Este comando permite autodoxxearse, as\u00ed que, tener precauci\u00f3n con este.\n\n[cu]Nota:\n[c]La IP no es real, se calcula usando el userId')
helpInfo.register('doxxea', 'Este comando no lo usar\u00eda ni con mis peores enemigos. Permite doxxear a varios usuarios a la vez, para ellos deben ser mencionados', example=['@usuario', '@usuario1, @usuario2...'])
helpInfo.register('letra', 'Devuelve la letra de una canci\u00f3n. Si no encuentra la canción, no entregará nada.', example=['despacito', 'yonaguni Bad Bunny'])
helpInfo.register('def', 'Busca la palabra en Wordreference y entre la definici\u00f3n de esta', example=['naturaleza'])
helpInfo.register('everyone', 'Menciona a todos los usuarios del chat. Solo puede ser usado por el staff', prefix='@')
helpInfo.register('setlog', 'Selecciona este chat para que, si el bot detecta algo anormal, lo informe. Preferible no poner otros bots en el mismo chat')
helpInfo.register('ban', 'Banea al usuario que seleccione, sea por un reporte del bot, una respuesta a un mensaje o una menci\u00f3n en un chat. Debe aladir un motivo por el cual banea al usuario.', command=[['(motivo) @usuario', 'Banea al usuario seleccionado']], example=['hacer spam @usuario'])
helpInfo.register('unban', 'Desbanea al usuario que seleccione, sea por un reporte del bot, una respuesta a un mensaje o una menci\u00f3n en un chat.', command=[['@usuario', 'Desbanea al usuario seleccionado']], example=['@usuario'])
helpInfo.register('config', 'Este modo permite configurar aspectos del bot generales, como por ejemeplo si da bienvenidas, si est\u00e1 activado, o incluso darle un tiempo fuera o poner el chat en modo lento.\nTras el comando, debe poner 1 para activarlo, 0 para desactivarlo', command=[['-check', 'Hace una revisi\u00f3n de los usuarios a la entrada, en busca de comentarios, blogs, biograf\u00eda o foto de perfil en busca de potenciales cosas ilegales. No abusar de esta funci\u00f3n o podr\u00edan haber problemas 403.'], ['-timeout', 'Permite tener un tiempo en el cual el bot no responder\u00e1 a los mensajes durante un determinado tiempo, medido en segundos.'], ['-welcome', 'Establece si el bot da la bienvenida a usuarios nuevos. Por defecto est\u00e1 activado.'], ['-goodbye', 'Por defecto est\u00e1 desactivado. Pone un mensaje cuando los miembros de un chat se van.'], ['-bot', 'Controla si el bot responder\u00e1 a todos los mensajes del chat, o en cambio, no har\u00e1 nada hasta que se vuelva a activar.'], ['-slow', 'Permite que, si un usuario envia un mensaje, deber\u00e1 esperar al menos treinta segundos para volver a interactiuar con el bot.'], ['-staff', 'Solo permite que el bot responda solo al staff.'], ['-1984', 'De activarse, el bot solo reaccionar\u00e1 a comandos de moderaci\u00f3n']])
helpInfo.register('check', 'Revisa el muro del usuario en b\u00fasqueda de comentarios que puedan cerrar la aplicaci\u00f3n, as\u00ed como de spam')
helpInfo.register('staff', 'Llama al staff de la comunidad al chat', prefix='@')
helpInfo.register('soporte', 'Entrega el link del formulario de soporte de Amino')
helpInfo.register('centro', 'Entrega el link del centro de ayuda de Amino')
helpInfo.register('abstract', 'Dibuja tri\u00e1ngulos aleatorios. Puede elegir la cantidad de figuras', command=[['(número)', 'Cantidad de triángulos a dibujar']], example=['16'])
helpInfo.register('view', 'Permite ver los \u00faltimos diez mensajes, tanto qui\u00e9n los ha puesto, como el id de estos')
helpInfo.register('article', 'Crea un art\u00edculo de Wikipedia (llamado Natipedia) con el mensaje, y usando el nick del usuario como t\u00edtulo', command=[['(mensaje)', 'Crea un artículo con ese mensaje']])
helpInfo.register('botstats', 'Da informaci\u00f3n del bot en si mismo, como su tiempo activo, los mensajes que ha analizado, y dem\u00e1s')
helpInfo.register('tweet', 'El comando m\u00e1s funable. Permite crear un tweet con el mensaje puesto', command=[['(mensaje)', 'Genera un tweet con aquel mensaje']])

class ES_ES_TEXT:
    NANO        = "[b]El mejor editor."
    PLEBEYOS    = "[ci]Ni que esto fuera PAR, "
    LA_NAVE     = "Espera un poco, un poquito m\u00e1s para llevarte mi felicidad."
    NORMAS      = "Lee las normas o te pego >:c\n[guidelines]"
    GRASA       = "[cb]\u00a1Papulince detectado! :v"
    OCULTO      = "\nA ver chiquillos, antes que nada vamos a dar las reglas del chat\n- Primero, prohibido hablar de la grasa \n- Segundo, prohibido hablar de esa app\n- Tercero, prohibido los insultos\n- Y cuarto, no est\u00e1n permitidos los garabatos ni hablar de comunismo\n\nY si quieren el pack de Leafy, preguntar por interno."
    EYES        = "\ud83d\udc40"
    TOY_CHICA   = "[ci]Para muchos Toy Chica, para mi Toy Chica es la \u00fanica animatr\u00f3nico que lleva ropa, la cual es un short, que para m\u00ed la hace ver muy sexy, y los hombres la adoran. A Toy Chica los fans le han hecho muchas fotos en versiones muy sexys, y est\u00e1 claro por qu\u00e9 lo han hecho; es la favorita de muchos hombres. Para los hombres, Toy Chica es considerada la \u00fanica animatr\u00f3nico que es muy sexy, y est\u00e1 claro, tiene unas curvas que cualquier hombre quisiera. Se rumorea que Toy Chica es la animatr\u00f3nico utilizada en ocasiones muy especiales."
    HOLA        = "[ci]Hola uwu,"
    UWU         = "[ci]uwu"
    DADOS       = "[cb]Dados\n[c]\u25e6 \u2756 \u25e6 \u2741 \u25e6 \u2756 \u25e6 \u2741 \u25e6 \u2756 \u25e6 \u2741 \u25e6 \u2756 \u25e6\n\n[c]Genera un n\u00famero aleatorio seg\u00fan la entrada que haya sido dada."
    METH        = "No a las drogas."
    MATH        = "\n[cb]Calculadora:\n[c]\u25e6 \u2756 \u25e6 \u2741 \u25e6 \u2756 \u25e6 \u2741 \u25e6 \u2756 \u25e6 \u2741 \u25e6 \u2756 \u25e6\n[C]Este modo le permitir\u00e1 calcular un n\u00famero en base a distintos operadores matem\u00e1ticos."
    PLATYPUS    = ["Hola, buenas tardes", "Sopa"]
    
    CHAT_ENTER = "\n[cb]\u2500\u2500\u2500\u2500\u2500\u2500\u2500 \u2661 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\n[cb]\ua4b1\u0fd0\u2661 WELCOME\u02da.*\u0cc3\n[c]Usuario N\u00b0(CHAT.UNIDOS)\n[c]Espero tengas una bonita\n[c]estad\u00eda aqu\u00ed en el chat,\n[c]no olvides leer las reglas\n[c]de la comunidad y la\n[c]tem\u00e1tica del chat\n[c]\n[c]Cualquier queja o duda\n[c]respecto a la comunidad\n[c]comunicarse con los l\u00ecderes\n[c]o curadores, que resolver\u00e0n\n[c]tu problema lo m\u00e1s puntual\n[c]posible\n[c]\n[c]\u00b0\uff61 \u135d\u05af\u059f\u22c6\u0e51 \u0aee \u02f6\u1d54 \u1d55 \u1d54\u02f6 \u10d0 \u2e19\u275b\u25cc\u0325\u25de\n[cb]\u2500\u2500\u2500\u2500\u2500\u2500\u2500 \u2661 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\n[c]:\u00a8\u00b7.\u00b7\u00a8:\n[c]`\u00b7."


class Text(ES_ES_TEXT):
   pass


def helpFunctioni(name, textClass):

    title       = None
    description = None
    commands    = None
    example     = None

    if not hasattr(name.upper(), Text.Help):
        if textClass is None: raise Exception('Help text not set!')

        
