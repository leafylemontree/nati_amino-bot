import ctypes
from src import utils

path = "src/subcommands/_math/c/"

# Matrix multiplication
matrMul = ctypes.cdll.LoadLibrary(f"{path}matrMul.so")
matrMul.main.argtypes  = (ctypes.c_char_p, )
matrMul.main.restype   = ctypes.c_char_p

# Matrix addition
matrAdd = ctypes.cdll.LoadLibrary(f"{path}matrAdd.so")
matrAdd.main.argtypes  = (ctypes.c_char_p, )
matrAdd.main.restype   = ctypes.c_char_p

@utils.userTracker("matrix")
async def matrix(ctx, msg):
        msg = msg[9:]
        c_in = msg.encode('ascii')

        if   msg.find('-MUL') == 0  :       result = matrMul.main(c_in)
        elif msg.find('-ADD') == 0  :       result = matrAdd.main(c_in)
        else                        :       return """
Ingrese una matriz A y una B. Recuerde que las matrices se ingresan de esta manera:

(
a b ...
c d ...
... 
y z ...
)
"""

        result = result.decode('ascii')
        print(result)
        print(len(result))
        return result
