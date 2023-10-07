'''
 * Nombre: raytracer.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 29.09.2023
 '''

import pygame

from figures import *
from lights import *
from rt import *
from materials import *

width = 600
height = 600

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rayTracer = Raytracer(screen)
'''
rayTracer.environmentMap = pygame.image.load("maps/map2.jpg")
rayTracer.rtClearColor(0.25, 0.25, 0.25)
'''
rayTracer.rtClearColor(0.1, 0.4, 0.1)
rayTracer.rtColor(1, 1, 1)

rayTracer.scene.append(
    Plane(position=(0, -2, 0), normal=(0, 1, -0.2), material=floor())
)
rayTracer.scene.append(
    Plane(position=(0, 5, 0), normal=(0, 1, 0.2), material=ceiling())
)
rayTracer.scene.append(
    Plane(position=(4, 0, 0), normal=(1, 0, 0.2), material=wall())
)
rayTracer.scene.append(
    Plane(position=(-4, 0, 0), normal=(1, 0, -0.2), material=wall())
)
rayTracer.scene.append(
    Plane(position=(0, 0, 5), normal=(0, 0, 1), material=brick())
)

rayTracer.scene.append(
    Disk(position=(0, 2, -5), normal=(0, 1, -0.1), radius=1, material=mirror())
)
rayTracer.scene.append(
    Disk(position=(0, -2, -5), normal=(0, 1, 0.1), radius=1, material=mirror())
)

rayTracer.scene.append(
    AABB(position=(0, 1.2, -5), size=(1, 1, 1), material=pink())
)
rayTracer.scene.append(
    AABB(position=(0, 0, -5), size=(1, 1, 1), material=purple())
)
rayTracer.scene.append(
    AABB(position=(0, -1.2, -5), size=(1, 1, 1), material=blue())
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

rect = pygame. Rect(0, 0, width, height)
sub = screen.subsurface(rect)
pygame.image.save(sub, "scene.jpg")

pygame.quit()
