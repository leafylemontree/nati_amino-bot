import ctypes

path = 'src/utils/c/'

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
