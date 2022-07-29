import ctypes
import pathlib
# import struct
# import array

class c:
    
    matrMul = None
    matrSum = None
    math_f  = None
    tape_f  = None
    c_db    = None
    words   = None

    
    def init_c(): 
        global matrMul, matrSum, math_f, tape_f, c_db, words

        path = str(pathlib.Path(__file__).parent.resolve())
        path = path[:(len(path) - 6)] + "c/"
        
        # Matrix multiplication
        matrMul = ctypes.cdll.LoadLibrary(f"{path}matrMul.so")
        matrMul.main.argtypes  = (ctypes.c_char_p, )
        matrMul.main.restype   = ctypes.c_char_p

        # Matrix addition
        matrAdd = ctypes.cdll.LoadLibrary(f"{path}matrAdd.so")
        matrAdd.main.argtypes  = (ctypes.c_char_p, )
        matrAdd.main.restype   = ctypes.c_char_p

        # Math resolver
        math_f  = ctypes.cdll.LoadLibrary(f"{path}math_f.so")
        math_f.main.argtypes  = (
                                        ctypes.c_int,
                                        ctypes.c_int,
                                        ctypes.c_char_p
                                     )
        math_f.main.restype   = ctypes.c_float

        # Math "tape" mode
        tape_f  = ctypes.cdll.LoadLibrary(f"{path}tape.so")
        tape_f.main.argtypes  = (ctypes.c_char_p, )
        tape_f.main.restype   = ctypes.c_char_p

        # database interactions
        c_db  = ctypes.cdll.LoadLibrary(f"{path}database.so")
        c_db.main.argtypes  = (
                                        ctypes.c_int,
                                        ctypes.c_char_p,
                                        ctypes.c_char_p
                                    )
        c_db.main.restype   = ctypes.c_char_p

        # get a random word
        words  = ctypes.cdll.LoadLibrary(f"{path}words.so")
        words.main.argtypes  = (ctypes.c_int, )
        words.main.restype   = ctypes.c_char_p

        print("C code libraries initialized")

    init_c()

    def matrix(msg):
        msg = msg[9:]
        c_in = msg.encode('ascii')

        if   msg.find('-MUL') == 0  :       result = matrMul.main(c_in)
        elif msg.find('-ADD') == 0  :       result = matrAdd.main(c_in)
        else                        :       return "Ingrese una matriz"

        result = result.decode('ascii')
        print(result)
        print(len(result))
        return result

    def math(msg):
        if    msg.find("{") != -1:
            return str(c.tape(msg.upper()))

        msg     = msg.split(" ")
        msg     = msg[1:]
        c_in    = ""

        if len(msg) < 2 : return subCommands.error(2400)

        for i in msg[1:]:
            try: f = float(i)
            except: return subCommands.error(2401)
            c_in  += f"{f}_"

        l      = len(msg) - 1;
        c_in   = c_in.encode("ascii")
        result = ""


        if      msg[0] == "ADD" :        result = math_f.main( 0, l, c_in)
        elif    msg[0] == "SUB" :        result = math_f.main( 1, l, c_in)
        elif    msg[0] == "MUL" :        result = math_f.main( 2, l, c_in)
        elif    msg[0] == "DIV" :        result = math_f.main( 3, l, c_in)
        elif    msg[0] == "POW" :        result = math_f.main( 4, l, c_in)
        elif    msg[0] == "LOG" :        result = math_f.main( 5, l, c_in)
        elif    msg[0] == "SQR" :        result = math_f.main( 6, l, c_in)
        elif    msg[0] == "SIN" :        result = math_f.main( 7, l, c_in)
        elif    msg[0] == "COS" :        result = math_f.main( 8, l, c_in)
        elif    msg[0] == "TAN" :        result = math_f.main( 9, l, c_in)
        elif    msg[0] == "INV" :        result = math_f.main(10, l, c_in)
        else:                            result = f"El argumento '{msg[0]}' no corresponde a un comando válido."


        return str(result)

    def tape(msg):
        msg = msg.encode('ascii')
        return tape_f.main(msg).decode('ascii')

    def database(mode, uid, *, name="none"):
        uid     = uid.encode("utf-8")
        name    = name.encode("utf-8")
        result  = c_db.main(mode, uid, name);
        result  = result.decode("utf-8")
        return result

    def get_word(mode):
        print(mode)
        result = words.main(mode)
        result = result.decode("utf-8")
        print(result)
        return result.upper()

#class f:

