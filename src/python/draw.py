from dataclasses import dataclass
from objects import Objects, Exchange
import ctypes

imgfc = ctypes.cdll.LoadLibrary("src/c/img_plotter.so")

class Draw:

    def line(self, color, x1, y1, x2, y2):
        imgfc.image_drawLine.argtypes = (ctypes.POINTER(type(self)), ctypes.POINTER(Objects.c_Color), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
        imgfc.image_drawLine.restype = ctypes.c_int
        r = imgfc.image_drawLine(ctypes.byref(self), ctypes.byref(color), x1, y1, x2, y2)
        return r

    def rect(self, color, x1, y1, x2, y2):
        imgfc.image_drawRect.argtypes = (ctypes.POINTER(type(self)), ctypes.POINTER(Objects.c_Color), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
        imgfc.image_drawRect.restype = ctypes.c_int
        r = imgfc.image_drawRect(ctypes.byref(self), ctypes.byref(color), x1, y1, x2, y2)
        return r

    def gradientX(self, col1, col2):
        return r

    def gradientY(self, col1, col2):
        return r

    def triangle(self, color, x1, y1, x2, y2, x3, y3):
        imgfc.image_drawPoly.argtypes = (ctypes.POINTER(type(self)), ctypes.POINTER(Objects.c_Color), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
        imgfc.image_drawPoly.restype = ctypes.c_int
        r = imgfc.image_drawPoly(ctypes.byref(self), ctypes.byref(color), x1, y1, x2, y2, x3, y3)
        return r

    def circle(self, color, x, y, r):
        return r

    def elipse(self, color, x, y, r, e):
        return r
