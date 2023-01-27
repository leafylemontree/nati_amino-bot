import ctypes

path = 'src/subcommands/_math/c/'

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

def mathfc(msg):
        if    msg.find("{") != -1:
            return str(tape(msg.upper()))

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

