'''
 * Nombre: raytracer.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 12.09.2023
 '''

import pygame

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Material:
    def __init__(self, diffuse=(1, 1, 1), spec=1.0, Ks=0.0, ior=1.0, type=OPAQUE, texture=None):
        self.diffuse = diffuse
        self.spec = spec
        self.Ks = Ks
        self.ior = ior
        self.type = type
        self.texture = texture

def pink():
    return Material(diffuse=(0.9, 0.6, 0.7), spec=64, Ks=0.15, type=OPAQUE, texture=pygame.image.load("maps/pink.jpg"))

def purple():
    return Material(diffuse=(0.5, 0.3, 0.7), spec=64, Ks=0.15, type=OPAQUE, texture=pygame.image.load("maps/purple.jpg"))

def blue():
    return Material(diffuse=(0.7, 0.9, 0.9), spec=64, Ks=0.15, type=OPAQUE, texture=pygame.image.load("maps/blue.jpg"))

def greenMirror():
    return Material(diffuse=(0, 1, 0), spec=32, Ks=0.15, type=REFLECTIVE)

def ceiling():
    return Material(diffuse=(0.7, 0.7, 0.7), spec=64, Ks=0.15, type=REFLECTIVE)

def wall():
    return Material(diffuse=(0.1, 0.4, 0.1))

def floor():
    return Material(diffuse=(0.8, 0.9, 0.6))

def glass():
    return Material(diffuse=(0.8, 0.8, 0.8), spec=64, Ks=0.15, ior=1.5, type=TRANSPARENT)

def diamond():
    return Material(diffuse=(1, 1, 1), spec=128, Ks=0.2, ior=2.417, type=TRANSPARENT)

def mirror():
    return Material(diffuse=(0.9, 0.9, 0.9), spec=64, Ks=0.2, type=REFLECTIVE)

def blueMirror():
    return Material(diffuse=(0.2, 0.2, 0.8), spec=32, Ks=0.15, type=REFLECTIVE)

def earth():
    return Material(spec=256, Ks=0.01, texture=pygame.image.load("maps/earth.jpg"))

def studio():
    return Material(spec=256, Ks=0.01, texture=pygame.image.load("maps/studio.jpg"))

def soapy():
    return Material(spec=64, Ks=0.2, type=REFLECTIVE, texture=pygame.image.load("maps/soapy.jpg"))

def electric():
    return Material(spec=64, Ks=0.2, type=REFLECTIVE, texture=pygame.image.load("maps/electric.jpg"))

def brick():
    return Material(diffuse=(1.0, 0.3, 0.2), spec=8, Ks=0.01)

def grass():
    return Material(diffuse=(0.2, 0.8, 0.2), spec=32, Ks=0.1)

def water():
    return Material(diffuse=(0.2, 0.2, 0.8), spec=256, Ks=0.5)

def snow():
    return Material(diffuse=(1.0, 0.9, 0.8), spec=8, Ks=1)

def stone():
    return Material(diffuse=(0.0, 0.0, 0.0), spec=8, Ks=0.01)

def carrot():
    return Material(diffuse=(1.0, 0.2, 0.1), spec=8, Ks=0.01)

def plastic():
    return Material(diffuse=(1.0, 1.0, 1.0), spec=8, Ks=0.01)