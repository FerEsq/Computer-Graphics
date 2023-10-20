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

width = 350
height = 350

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rayTracer = Raytracer(screen)
#rayTracer.environmentMap = pygame.image.load("maps/map2.jpg")
rayTracer.rtClearColor(0.5, 0.9, 0.9)
rayTracer.rtColor(1, 1, 1)

rayTracer.scene.append(Sphere(position = (-0.5, -0.3, -4.5), radius = 0.35, material = mirror()))

# Cilindro
rayTracer.scene.append(Cylinder(position=(0, -1, -5), size=(1.2, 0.4), material=pink()))
rayTracer.scene.append(Cylinder(position=(0.7, -0.7, -6), size=(0.4, 0.8), material=pink()))

rayTracer.lights.append(AmbientLight(intensity=0.9))
rayTracer.lights.append(DirectionalLight(direction=(-0.5, -1, 1), intensity=0.7, color=(1, 1, 1)))
rayTracer.lights.append(PointLight(position=(2.5, -1, -5), intensity=1, color=(1, 1, 1)))

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
