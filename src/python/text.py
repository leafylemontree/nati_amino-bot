import json

msg_text = {
    'nano': '[b]El mejor editor.',
    'plebeyos': '[ci]Ni que esto fuera PAR, ',
    'la_nave': 'Espera un poco, un poquito más para llevarte mi felicidad.',
    'normas': '[guidelines]',
    'grasa': '[cb]¡Papulince detectado! :v',
    'msg_oculto': '''
A ver chiquillos, antes que nada vamos a dar las reglas del chat
- Primero, prohibido hablar de la grasa 
- Segundo, prohibido hablar de esa app
- Tercero, prohibido los insultos
- Y cuarto, no están permitidos los garabatos ni hablar de comunismo

Y si quieren el pack de Leafy, preguntar por interno.''',
    'ojos': '\ud83d\udc40',
    'toy_chica': '[ci]Para muchos Toy Chica, para mi Toy Chica es la única animatrónico que lleva ropa, la cual es un short, que para mí la hace ver muy sexy, y los hombres la adoran. A Toy Chica los fans le han hecho muchas fotos en versiones muy sexys, y está claro por qué lo han hecho; es la favorita de muchos hombres. Para los hombres, Toy Chica es considerada la única animatrónico que es muy sexy, y está claro, tiene unas curvas que cualquier hombre quisiera. Se rumorea que Toy Chica es la animatrónico utilizada en ocasiones muy especiales.',
    'hola': '[ci]Hola uwu,',
    'uwu': '[ci]uwu',
    'dados': '''[cb]Dados
[c]◦ ❖ ◦ ❁ ◦ ❖ ◦ ❁ ◦ ❖ ◦ ❁ ◦ ❖ ◦

[c]Genera un número aleatorio según la entrada que haya sido dada.''',
    'meth': 'No a las drogas.',
    'math': '''
[cb]Calculadora:
[c]◦ ❖ ◦ ❁ ◦ ❖ ◦ ❁ ◦ ❖ ◦ ❁ ◦ ❖ ◦
[C]Este modo le permitirá calcular un número en base a distintos operadores matemáticos.''',
    'platypus': ['Hola, buenas tardes', 'Sopa'],
    'help': {
            "default" : '''
[cb]Mari Mari
[c]◦ ❖ ◦ ❁ ◦ ❖ ◦ ❁ ◦ ❖ ◦ ❁ ◦ ❖ ◦

[ci]Hola, soy Nati, una bella usuaria creada por Leafy. Cualquier problema dirigirse con él (enlace en la biografía)

[bc]Comandos:
[c]━───────⊹⊱✙⊰⊹───────━

[c]--nano, --wordle, --sigueme, --chat, --biblia, --horoscopo, --matrix, --cutes, --copypaste, --math, --blogs, --info, --help, --nombre, --say, --normas, --platypus, --dados, --doxx, --letra, --def.

[cb]Otros Mensajes:
[c]━───────⊹⊱✙⊰⊹───────━

[c]plebeyos, la nave, kiwilatigo, ojos (\ud83d\udc40), uwu, doxxea a, :v, @everyone. 


[cb]Moderación:
[c]━───────⊹⊱✙⊰⊹───────━

[c]--setlog, --ban, --unban.''',
            "nano"          : """
[cbu]--nano
[c]═══════════.♥.═

[c]Este comando está hecho a modo de ejemplo de respuesta del bot. Queda acá por motivos históricos.

[c]Trivia: el nano al cual se refiere hace referencia a GNU nano, un editor de texto que suele venir en las instalaciones de Linux por defecto.""",
            "wordle"        : """
[cbu]--wordle
[c]═══════════.♥.═

[c]Inicia un juego de Wordle. Wordle es un juego que trata de adivinar una palabra ingresando palabras de la misma longitud, con la gracias que las letras que coinciden en posición son marcadas entre corchetes.

[cb]Comandos:

[c]-init : inicia el juego.
[c]-info : muestra ayuda de cómo jugarlo.""",
            "sigueme"       : """
[cbu]--sigueme
[c]═══════════.♥.═

[c]El bot seguirá su perfil desde ahora.""",
            "chat"          : """
[cbu]--chat
[c]═══════════.♥.═

[c]En beta aún. Esta función le permite ingresa texto y esperar que el bot continúe escribiendo.""",
            "biblia"        : """
[cbu]--biblia
[c]═══════════.♥.═

[c]Busca y responde con un capítulo de la biblia (edición Reina Valera 1960).

[c]Para buscar un capítulo, debe ingresar el nombre del libro en minúscula (salmos, genesis), y el número del capítulo. Se truncará el mensaje a 2000 caracteres.""",
            "horoscopo"     : """
[cbu]--horoscopo
[c]═══════════.♥.═

[c]Lee el horóscopo de hoy con sus poderes de oyente.
[c]Se accede colocando el nombre del signo zodiacal tras el comando, por ejemplo, Aries.

[C]El horóscopo se actualiza a diario.""",
            "matrix"        : """
[cbu]--matrix
[c]═══════════.♥.═

[c]Modo para manipular matrices, permite multiplicación y suma de estas.

[cb]Comandos:
[c]-mul: multiplica dos matrices.
[c]-add: suma dos matrices.

[C]Las matrices se ingresan de esta manera:
[c](
[c]a b
[C]c d
[c])

[c]con a, b, c, d  siendo números. Hay soporte para matrices de mayor tamaño aún, por ejemplo 3x3, e incluso rectangulares.""",
            "cutes"         : """
[cbu]--cutes
[c]═══════════.♥.═

[c]Envía una imagen tierna que representa a dos usuarios, quien manda el comando y a quien va dirigido.

[Cb]Comandos:
[c]-hug: abrazo.
[C]-kiss : beso.
[c]-pat : acariciar.""",
            "copypaste"     : """
[cbu]--copypaste
[c]═══════════.♥.═

[c]Permite almacenar texto en el bot, así como leerlo a posterios.

[cb]Comandos:
[C]-mk : crea un nuevo texto.
[c]-ds : habilita o deshabilita un texto.
[C]-rm : elimina un texto.""",
            "math"          : """
[cbu]--math
[c]═══════════.♥.═

[c]Permite hacer operaciones matemáticas, tanto individuales como en modo cinta. El modo cinta es una serie de comandos, ejecutados uno despues de otro que permite cargar funciones más complejas.

[cb]Comandos (modo normal):
[c]add (número) (número): suma dos números. 
[c]sub (número) (número): resta dos números. 
[c]mul (número) (número): multiplica dos números.
[c]div (número) (número): divide dos números.
[c]pow (número) (número): eleva el primer número al segundo.

[c]sqr (número): retorna la raíz cuadrada del número ingresado.
[C]{ (función)} : entra en modo cinta.

[Cb]Comandos (modo cinta):
[C]Los mismos del modo normal, con soporte para variables literales.

[c]var (nombre) (número): Permite crear una variable con un nombre y número por defecto.

[c]print (variable): imprime el valor de la variable como resultado.""",
            "blogs"         : """
[cbu]--blogs
[c]═══════════.♥.═

[c]Retorna los blogs del usuario, sean los últimos 25 de este, o uno en específico.

[cb]Comandos:
[c]-user -all: entrega los nombres de los últimos 25 blogs del usuario.
[C]-user (número): entrega información adicional del blog seleccionado.""",
            "info"          : """
[cbu]--info
[c]═══════════.♥.═

[c]Entrega información detallada del usuario, como fecha de unión, blogs subidos, comentarios, etc.""",
            "plebeyos"      : """
[cbu]plebeyos
[c]═══════════.♥.═

[c]Pequeño mensaje que hace alusión a un grupo.""",
            "nave"          : """
[cbu]la nave
[c]═══════════.♥.═

[c]Jose Jose lo hubiera querido así.""",
            "help"          : """
[cbu]--help
[c]═══════════.♥.═

[c]Muestra ayuda de los diferentes comandos, así como los existentes hasta el momento-

[cb]Comandos:
[c](comando): información de ese comando, incluyendo los comandos disponibles.""",
            "nombre"        : """
[cbu]--nombre
[c]═══════════.♥.═

[c]Repite el nombre del usuario que llame el comando.""",
            "say"           : """
[cbu]--say
[c]═══════════.♥.═

[c]Repite todo lo que se ponga después del comando.""",
            "kiwilatigo"    : """
[cbu]kiwilatigo
[c]═══════════.♥.═

[c]No lo toquen o haran enojar a quien lo ejecuta, unu.""",
            "normas"        : """
[cbu]--normas
[c]═══════════.♥.═

[cU](Esto tiene sentido en otro chat).

[c]Para cambiarlas a voluntad, consultar con el creador del bot.""",
            "ojos"          : """
[cbu]ojos
[c]═══════════.♥.═

[c]No miren a Nati que los mira de vuelta.""",
            "uwu"           : """
[cbu]uwu
[c]═══════════.♥.═

[c]uwu.""",
            "platypus"      : """
[cbu]--platypus
[c]═══════════.♥.═

[c]Responde cosas que les gusta a los ornitorrincos.""",
            "meth"          : """
[cbu]--meth
[c]═══════════.♥.═

[ci]Quizás quizo decir: math.
[c]\ud83d\udc40""",
            "dados"         : """
[cbu]--dados
[c]═══════════.♥.═

[c]Retorna un número entre 1 y el número ingresado, como si se tiraran dados, pero también tiene soportes para número más grandes.

[cb]Comandos:
[C](número): tope superior del generador de números.""",
            "sus"           : """
[cbu]--sus
[c]═══════════.♥.═

[c]amogus, ao ao, amogus aaAAA.""",
            "doxx"          : """
[cbu]--doxx
[c]═══════════.♥.═

[c]Este comando permite autodoxxearse, así que, tener precaución con este.

[cu]Nota:
[c]La IP no es real, se calcula usando el userId.""",
            "doxxea"        : """
[cbu]--doxxea
[c]═══════════.♥.═

[c]Este comando no lo usaría ni con mis peores enemigos. Permite doxxear a varios usuarios a la vez, para ellos deben ser mencionados.""",
            "boku"          : """
[cbu]boku
[c]═══════════.♥.═

[c]Turbio quien haya escrito esto...""",
            "grasa"         : """
[cbu]grasa
[c]═══════════.♥.═

[c]Esto es para todos los grasosos que ponen un  :v salvaje. Si le dan coanfitrión al bot, puede sacar los usuarios del chat.""",
            "letra"          : """
[cbu]--letra
[c]═══════════.♥.═

[c]Devuelve la letra de una canción.""",
            "def"          : """
[cbu]--def
[c]═══════════.♥.═

[c]Busca la palabra en Wordreference y entre la definición de esta.""",
            "everyone"          : """
[cbu]@everyone
[c]═══════════.♥.═

[c]Menciona a todos los usuarios del chat. Solo puede ser usado por el staff.""",
            "setlog"          : """
[cbu]--setlog
[c]═══════════.♥.═

[c]Selecciona este chat para que, si el bot detecta algo anormal, lo informe. Preferible no poner otros bots en el mismo chat.""",
            "ban"          : """
[cbu]--ban
[c]═══════════.♥.═

[c]Banea al usuario que seleccione, sea por un reporte del bot, una respuesta a un mensaje o una mención en un chat. Debe aladir un motivo por el cual banea al usuario.

[cu]Uso:
[c]--ban Hacer spam @usuarui""",
            "unban"          : """
[cbu]--unban
[c]═══════════.♥.═

[c]Desbanea a un usuario. Debe usarlo mencionando un usuario en um chat, respondiendo a un mensaje de ese usuario o respondiendo a un reporte del bot.

[cu]Uso:
[c]--unban @usuario"""
        },
    'enter' : ["""
[cb]─────── ♡ ───────
[cb]꒱࿐♡ WELCOME˚.*ೃ
[c]Usuario N° """, """
[c]Espero tengas una bonita
[c]estadía aquí en el chat,
[c]no olvides leer las reglas
[c]de la comunidad y la
[c]temática del chat
[c]
[c]Cualquier queja o duda
[c]respecto a la comunidad
[c]comunicarse con los lìderes
[c]o curadores, que resolveràn
[c]tu problema lo más puntual
[c]posible
[c]
[c]°｡ ፝֯֟⋆๑ ૮ ˶ᵔ ᵕ ᵔ˶ ა ⸙❛◌̥◞
[cb]─────── ♡ ───────
[c]:¨·.·¨:
[c]`·."""]
    }

with open("../json/text.json", "w+") as textfile:
    json.dump(msg_text, textfile, indent=4)

print(json.dumps(msg_text, indent=4))
