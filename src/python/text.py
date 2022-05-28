import json

msg_text = {
    'nano': '[b]El mejor editor.',
    'plebeyos': '[ci]Ni que esto fuera PAR, ',
    'la_nave': 'Espera un poco, un poquito más para llevarte mi felicidad.',
    'normas': '[cub]Normas\n\n[C]No enviar memes si no son de la grasa o shitpost extremo.\n[C]No hablar de comunismo.\n[C]Si quieren el pack de Leafy, me abren privado.\n\n[cu]En general las de la comunidad, cuales son\n[c]No se permite enviar mensajes repetidos y/o en abundancia (Flood)\n[c]El spam no está permitido, a menos que el organizador diga que se puede\n[c]No se pueden tocar temas subidos de tono, esto incluye desnudos, pornografía, mutilaciones, suicidio, tortura y actividades delictivas.\n[c]Este chat será deshabilitado sin excepción una vez pase un día de inactividad.\n[c]Respetar a los kiwis, ornitorrincos y a cualquier especie que se aparezca. \n\n[bc]Ahora con reglas internas del chat\n[c]Las alianzas con otros chats por el momento están desactivadas, pero sí puede haber promoción de ellos.\n[c]Para solicitar estar en la zona de spam, avisar al organizador por privado, sino su petición será ignorada.\n[c]No se permite el lenguaje soez ni los insultos a otros miembros.\n[c]En momentos de hacer sala de proyección, pueden pedir canciones solamente cuando se permita, que generalmente es siempre.\n[c]Se pide ser paciente con la lista de reproducción de la sala. Si más de la mayoría presentes decide saltar una canción, esto se hará. Si alguien no está presente, no se pondrá su canción a menos que avise que no podrá estar.\n[c]Respetar a todos, excepto si se trata de Mr Facherito, que ni los caníbales lo quieren.\n[c]Aoi Asahina best waifu',
    'grasa': '[cb]¡Papulince detectado! :v',
    'msg_oculto': 'A ver chiquillos, antes que nada vamos a dar las reglas del chat\n\n- Primero, prohibido hablar de Jairo\n- Segundo, prohibido hablar de Niara\n- Tercero, prohibido los insultos\n- Y cuarto, no están permitidos los garabatos ni hablar de comunismo\n\nY si quieren el pack de Leafy, preguntar por interno.',
    'ojos': '\ud83d\udc40',
    'toy_chica': '[ci]Para muchos Toy Chica, para mi Toy Chica es la única animatrónico que lleva ropa, la cual es un short, que para mí la hace ver muy sexy, y los hombres la adoran. A Toy Chica los fans le han hecho muchas fotos en versiones muy sexys, y está claro por qué lo han hecho; es la favorita de muchos hombres. Para los hombres, Toy Chica es considerada la única animatrónico que es muy sexy, y está claro, tiene unas curvas que cualquier hombre quisiera. Se rumorea que Toy Chica es la animatrónico utilizada en ocasiones muy especiales.',
    'hola': '[ci]Hola uwu,',
    'uwu': '[ci]uwu',
    'dados': '[cb]Dados\n[c]◦ ❖ ◦ ❁ ◦ ❖ ◦ ❁ ◦ ❖ ◦ ❁ ◦ ❖ ◦\n\n[c]Genera un número aleatorio según la entrada que haya sido dada.',
    'meth': 'No a las drogas.',
    'math': '[cb]Calculadora:\n[c]◦ ❖ ◦ ❁ ◦ ❖ ◦ ❁ ◦ ❖ ◦ ❁ ◦ ❖ ◦\n\n[C]Este modo le permitirá calcular un número en base a distintos operadores matemáticos.\n\n[c]Puede consultar la sintaxis de este modo al pone lo siguiente:\n\n[c]--math ejemplo',
    'platypus': ['Hola, buenas tardes', 'Sopa'],
    'help': {
            "default" : '[cb]Mari Mari\n[c]◦ ❖ ◦ ❁ ◦ ❖ ◦ ❁ ◦ ❖ ◦ ❁ ◦ ❖ ◦\n\n[ci]Hola, soy una bella usuaria que fue creada por el pendejo de Leafy. Cualquier problema dirigirse con él (enlace en la biografía)\n\n[bc]Comandos:\n[c]━───────⊹⊱✙⊰⊹───────━\n\n[c]--nano, --wordle, --sigueme, --chat, --biblia, --horoscopo, --matrix, --cutes, --copypaste, --math, --blogs, --info, --help, --nombre, --say, --normas, --platypus, --dados, --sus, --doxx.\n\n[cb]Otros Mensajes:\n[c]━───────⊹⊱✙⊰⊹───────━\n\n[c]plebeyos, la nave, kiwilatigo, ojos (\ud83d\udc40), uwu, doxxea a, :v',

            "nano"          : "[cbu]--nano\n[c]═══════════.♥.═\n\n[c]Este comando está hecho a modo de ejemplo de respuesta del bot. Queda acá por motivos históricos.\n\n[c]Trivia: el nano al cual se refiere hace referencia a GNU nano, un editor de texto que suele venir en las instalaciones de Linux por defecto.",
            "wordle"        : "[cbu]--wordle\n[c]═══════════.♥.═\n\n[c]Inicia un juego de Wordle. Wordle es un juego que trata de adivinar una palabra ingresando palabras de la misma longitud, con la gracias que las letras que coinciden en posición son marcadas entre corchetes.\n\n[cb]Comandos:\n\n[c]-init : inicia el juego.\n[c]-info : muestra ayuda de cómo jugarlo.",
            "sigueme"       : "[cbu]--sigueme\n[c]═══════════.♥.═\n\n[c]El bot seguirá su perfil desde ahora.",
            "chat"          : "[cbu]--chat\n[c]═══════════.♥.═\n\n[c]En beta aún. Esta función le permite ingresa texto y esperar que el bot continúe escribiendo.",
            "biblia"        : "[cbu]--biblia\n[c]═══════════.♥.═\n\n[c]Busca y responde con un capítulo de la biblia (edición Reina Valera 1960).\n\n[c]Para buscar un capítulo, debe ingresar el nombre del libro en minúscula (salmos, genesis), y el número del capítulo. Se truncará el mensaje a 2000 caracteres.",
            "horoscopo"     : "[cbu]--horoscopo\n[c]═══════════.♥.═\n\n[c]Lee el horóscopo de hoy con sus poderes de oyente.\n\n[c]Se accede colocando el nombre del signo zodiacal tras el comando, por ejemplo, Aries.\n\n[C]El horóscopo se actualiza a diario.",
            "matrix"        : "[cbu]--matrix\n[c]═══════════.♥.═\n\n[c]Modo para manipular matrices, permite multiplicación y suma de estas.\n\n[cb]Comandos:\n[c]-mul: multiplica dos matrices.\n[c]-add: suma dos matrices.\n\n[C]Las matrices se ingresan de esta manera:\n[c](\n[c]a b\n[C]c d\n[c])\n\n[c]con a, b, c, d  siendo números. Hay soporte para matrices de mayor tamaño aún, por ejemplo 3x3, e incluso rectangulares.",
            "cutes"         : "[cbu]--cutes\n[c]═══════════.♥.═\n\n[c]Envía una imagen tierna que representa a dos usuarios, quien manda el comando y a quien va dirigido.\n\n[Cb]Comandos:\n[c]-hug: abrazo.\n[C]-kiss : beso.\n[c]-pat : acariciar.",
            "copypaste"     : "[cbu]--copypaste\n[c]═══════════.♥.═\n\n[c]Permite almacenar texto en el bot, así como leerlo a posterios.\n\n[cb]Comandos:\n[C]-mk : crea un nuevo texto.\n[c]-ds : habilita o deshabilita un texto.\n[C]-rm : elimina un texto.",
            "math"          : "[cbu]--math\n[c]═══════════.♥.═\n\n[c]Permite hacer operaciones matemáticas, tanto individuales como en modo cinta. El modo cinta es una serie de comandos, ejecutados uno despues de otro que permite cargar funciones más complejas.\n\n[cb]Comandos (modo normal):\n[c]add (número) (número): suma dos números. \n[c]sub (número) (número): resta dos números. \n[c]mul (número) (número): multiplica dos números.\n[c]div (número) (número): divide dos números.\n[c]pow (número) (número): eleva el primer número al segundo.\n\n[c]sqr (número): retorna la raíz cuadrada del número ingresado.\n[C]{ (función)} : entra en modo cinta.\n\n[Cb]Comandos (modo cinta):\n[C]Los mismos del modo normal, con soporte para variables literales.\n\n[c]var (nombre) (número): Permite crear una variable con un nombre y número por defecto.\n\n[c]print (variable): imprime el valor de la variable como resultado.",
            "blogs"         : "[cbu]--blogs\n[c]═══════════.♥.═\n\n[c]Retorna los blogs del usuario, sean los últimos 25 de este, o uno en específico.\n\n[cb]Comandos:\n\n[c]-user -all: entrega los nombres de los últimos 25 blogs del usuario.\n[C]-user (número): entrega información adicional del blog seleccionado.",
            "info"          : "[cbu]--info\n[c]═══════════.♥.═\n\n[c]Entrega información detallada del usuario, como fecha de unión, blogs subidos, comentarios, etc.",
            "plebeyos"      : "[cbu]plebeyos\n[c]═══════════.♥.═\n\n[c]Pequeño mensaje que hace alusión a un grupo.",
            "nave"          : "[cbu]la nave\n[c]═══════════.♥.═\n\n[c]Jose Jose lo hubiera querido así.",
            "help"          : "[cbu]--help\n[c]═══════════.♥.═\n\n[c]Muestra ayuda de los diferentes comandos, así como los existentes hasta el momento-\n\n[cb]Comandos:\n[c](comando): información de ese comando, incluyendo los comandos disponibles.",
            "nombre"        : "[cbu]--nombre\n[c]═══════════.♥.═\n\n[c]Repite el nombre del usuario que llame el comando.",
            "say"           : "[cbu]--say\n[c]═══════════.♥.═\n\n[c]Repite todo lo que se ponga después del comando.",
            "kiwilatigo"    : "[cbu]kiwilatigo\n[c]═══════════.♥.═\n\n[c]No lo toquen o haran enojar a quien lo ejecuta, unu.",
            "normas"        : "[cbu]--normas\n[c]═══════════.♥.═\n\n[cU](Esto tiene sentido en otro chat).\n\n[c]Para cambiarlas a voluntad, consultar con el creador del bot.",
            "ojos"          : "[cbu]ojos\n[c]═══════════.♥.═\n\n[c]No miren a Nati que los mira de vuelta.",
            "uwu"           : "[cbu]uwu\n[c]═══════════.♥.═\n\n[c]uwu.",
            "platypus"      : "[cbu]--platypus\n[c]═══════════.♥.═\n\n[c]Responde cosas que les gusta a los ornitorrincos.",
            "meth"          : "[cbu]--meth\n[c]═══════════.♥.═\n\n[ci]Quizás quizo decir: math.\n[c]\ud83d\udc40",
            "dados"         : "[cbu]--dados\n[c]═══════════.♥.═\n\n[c]Retorna un número entre 1 y el número ingresado, como si se tiraran dados, pero también tiene soportes para número más grandes.\n\n[cb]Comandos:\n[C](número): tope superior del generador de números.",
            "sus"           : "[cbu]--sus\n[c]═══════════.♥.═\n\n[c]amogus, ao ao, amogus aaAAA.",
            "doxx"          : "[cbu]--doxx\n[c]═══════════.♥.═\n\n[c]Este comando permite autodoxxearse, así que, tener precaución con este.\n\n[cu]Nota:\n[c]La IP no es real, se calcula usando el userId.",
            "doxxea"        : "[cbu]--doxxea\n[c]═══════════.♥.═\n\n[c]Este comando no lo usaría ni con mis peores enemigos. Permite doxxear a varios usuarios a la vez, para ellos deben ser mencionados.",
            "boku"          : "[cbu]boku\n[c]═══════════.♥.═\n\n[c]Turbio quien haya escrito esto...",
            "grasa"         : "[cbu]grasa\n[c]═══════════.♥.═\n\n[c]Esto es para todos los grasosos que ponen un  :v salvaje. Si le dan coanfitrión al bot, puede sacar los usuarios del chat."
        }
    }

with open("../json/text.json", "w+") as textfile:
    json.dump(msg_text, textfile)

print(msg_text)
