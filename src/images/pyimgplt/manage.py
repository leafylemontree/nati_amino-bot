import ctypes
from .objects import Objects, Exchange
from dataclasses import dataclass
from .draw import Draw
from .render import Render
from random import random
import os
import time

imgfc = ctypes.cdll.LoadLibrary("src/images/pyimgplt/img_plotter.so")


class Image(ctypes.Structure):
    
    _fields_ = [
                 ('name',   ctypes.c_char_p),
                 ('width',  ctypes.c_int),
                 ('height', ctypes.c_int),
                 ('data',   ctypes.c_char_p),

            ]

    def __init__(self, name, width, height):
        self.name   = name.encode("utf-8")
        self.width  = width
        self.height = height
        self.data   = None 
        self.draw   = Draw
        self.render = Render 
        self.effect = None

    def generate(self, color):
        imgfc.generateBlank.argtypes = (ctypes.POINTER(Image), ctypes.POINTER(Objects.c_Color),)
        imgfc.generateBlank.restype = ctypes.c_int
        r = imgfc.generateBlank(ctypes.byref(self), ctypes.byref(color))
        return r
    
    def write(self):
        imgfc.imageWrite.argtypes = (ctypes.POINTER(Image),)
        imgfc.imageWrite.restype = ctypes.c_int
        r = imgfc.imageWrite(ctypes.byref(self))
        os.system(f"convert -size {self.width}x{self.height} -depth 8 rgba:{self.name.decode('utf-8')}.raw result.png")
        return r

    def subSampler(self, sub):
        imgfc.subSampler.argtypes = (ctypes.POINTER(Image), ctypes.c_int)
        imgfc.subSampler.restype = ctypes.c_int
        r = imgfc.subSampler(ctypes.byref(self), sub)
        return r

    def free(self):
        imgfc._free.argtypes = (ctypes.POINTER(Image),)
        imgfc._free.restype = ctypes.c_int
        r = imgfc._free(ctypes.byref(self))
        return r

