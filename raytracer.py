'''
 * Nombre: raytracer.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 29.09.2023
              Modificado el 12.10.2023
 '''

import pygame

from figures import *
from lights import *
from rt import *
from materials import *

width = 50
height = 50

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rayTracer = Raytracer(screen)
rayTracer.environmentMap = pygame.image.load("maps/map2.jpg")
rayTracer.rtClearColor(0.25, 0.25, 0.25)
rayTracer.rtColor(1, 1, 1)

# Transparentes
rayTracer.scene.append(
    Pyramid(position=(1.5, 0, -5), size=(1.7, 1.7, 1.7), material=diamond())
)

# Reflectivas
rayTracer.scene.append(
    Pyramid(position=(-0.3, -0.1, -5), size=(1.4, 1.5, 1.4), material=soapy())
)

# Opacas
rayTracer.scene.append(
    Pyramid(position=(-2, -0.4, -5), size=(1, 1, 1), material=pink())
)

rayTracer.lights.append(
    AmbientLight(intensity=0.7)
)

rayTracer.rtClear()
rayTracer.rtRender()

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
'''
rect = pygame. Rect(0, 0, width, height)
sub = screen.subsurface(rect)
pygame.image.save(sub, "scene.jpg")
'''
pygame.quit()
