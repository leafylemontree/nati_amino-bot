import ctypes
from .objects import Objects

imgfc = ctypes.cdll.LoadLibrary("src/images/pyimgplt/img_plotter.so")

class Render:
    
    def add(img1, img2, imgO, o, x, y, c):
        """
            img1 = input bottom
            img2 = input top
            imgO = output

            o    = opacity
            x    = offset x
            y    = offset y
            c    = copy everything from img1
        """
        
        imgfc.render_add.argtypes = (
                    ctypes.POINTER(type(img1)),
                    ctypes.POINTER(type(img2)),
                    ctypes.POINTER(type(imgO)),
                    ctypes.c_float,
                    ctypes.c_int,
                    ctypes.c_int,
                    ctypes.c_int
                )
        imgfc.render_add.restype  = ctypes.c_int
        r = imgfc.render_add(
                    ctypes.byref(img1),
                    ctypes.byref(img2),
                    ctypes.byref(imgO),
                    o, x, y, c
                )
        return r

    def sub(img1, img2, imgO, o, x, y, c):
        """
            img1 = input bottom
            img2 = input top
            imgO = output

            o    = opacity
            x    = offset x
            y    = offset y
            c    = copy everything from img1
        """
        
        imgfc.render_add.argtypes = (
                    ctypes.POINTER(type(img1)),
                    ctypes.POINTER(type(img2)),
                    ctypes.POINTER(type(imgO)),
                    ctypes.c_float,
                    ctypes.c_int,
                    ctypes.c_int,
                    ctypes.c_int
                )
        imgfc.render_add.restype  = ctypes.c_int
        r = imgfc.render_add(
                    ctypes.byref(img1),
                    ctypes.byref(img2),
                    ctypes.byref(imgO),
                    o, x, y, c
                )
        return r

    def average(img1, img2, imgO, o, x, y, c):
        """
            img1 = input bottom
            img2 = input top
            imgO = output

            o    = opacity
            x    = offset x
            y    = offset y
            c    = copy everything from img1
        """
        
        imgfc.render_add.argtypes = (
                    ctypes.POINTER(type(img1)),
                    ctypes.POINTER(type(img2)),
                    ctypes.POINTER(type(imgO)),
                    ctypes.c_float,
                    ctypes.c_int,
                    ctypes.c_int,
                    ctypes.c_int
                )
        imgfc.render_add.restype  = ctypes.c_int
        r = imgfc.render_add(
                    ctypes.byref(img1),
                    ctypes.byref(img2),
                    ctypes.byref(imgO),
                    o, x, y, c
                )
        return r

    def normal(img1, img2, imgO, o, x, y, c):
        """
            img1 = input bottom
            img2 = input top
            imgO = output

            o    = opacity
            x    = offset x
            y    = offset y
            c    = copy everything from img1
        """
        
        imgfc.render_normal.argtypes = (
                    ctypes.POINTER(type(img1)),
                    ctypes.POINTER(type(img2)),
                    ctypes.POINTER(type(imgO)),
                    ctypes.c_float,
                    ctypes.c_int,
                    ctypes.c_int,
                    ctypes.c_int
                )
        imgfc.render_normal.restype  = ctypes.c_int
        r = imgfc.render_normal(
                    ctypes.byref(img1),
                    ctypes.byref(img2),
                    ctypes.byref(imgO),
                    o, x, y, c
                )
        return r
