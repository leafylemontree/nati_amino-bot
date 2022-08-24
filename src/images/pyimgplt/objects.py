from dataclasses import dataclass
import ctypes

class Objects:

    @dataclass
    class Color:
        r       : int 
        g       : int
        b       : int
        a       : int       =  255


    class c_Image(ctypes.Structure):

        _fields_ = [
                 ('name',   ctypes.c_char_p),
                 ('width',  ctypes.c_int),
                 ('height', ctypes.c_int),
                 ('data',   ctypes.c_char_p)
            ]

    class c_Color(ctypes.Structure):

        _fields_ = [
                 ('r',   ctypes.c_ubyte),
                 ('g',   ctypes.c_ubyte),
                 ('b',   ctypes.c_ubyte),
                 ('a',   ctypes.c_ubyte)
            ]

def Exchange(func):
    def py_to_c(self, args):
        c_img = Objects.c_Image(
                    self.name.encode("utf-8"),
                    self.width,
                    self.height,
                    data=self.data
                )

        args = list(args) 
        la  = len(args)

        col1  = None
        col2  = None

        if la > 0:
            if isinstance(args[0], Objects.Color):
                col1 = Objects.c_Color(
                            args[0].r,
                            args[0].g,
                            args[0].b,
                            args[0].a
                        )
        if la > 1:
            if isinstance(args[1], Objects.Color):
                col2 = Objects.c_Color(
                            args[0].r,
                            args[0].g,
                            args[0].b,
                            args[0].a
                        )
        
        fc_args = [c_img]
        if col1:
            fc_args.append(col1)
            args.pop(0)
        if col2:
            fc_args.append(col2)
            args.pop(0)
        fc_args.extend(args)
        
        return (*fc_args,)
    
    def c_to_py(self, ret):
        self.name   = ret.name.decode("utf-8")
        self.width  = ret.width
        self.height = ret.height
        self.data   = ret.data
    
    def wrapper(self, *args, **kwargs):
        args = py_to_c(self, args)
        ret  = func(*args)
        c_to_py(self, ret)
        return 
    return wrapper
