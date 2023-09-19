import pygame
from pygame.locals import *

from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 200
height = 200

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rayTracer = Raytracer(screen)
rayTracer.rtClearColor(0.2, 0.3, 0.4)
rayTracer.rtColor(1, 1, 1)

# Cuerpo del muñeco
rayTracer.scene.append(Sphere(position = (0, 1.7, -7), radius = 0.8, material = snow()))
rayTracer.scene.append(Sphere(position = (0, 0.2, -7), radius = 1, material = snow()))
rayTracer.scene.append(Sphere(position = (0, -1.5, -7), radius = 1.2, material = snow()))

# Cara del muñeco
rayTracer.scene.append(Sphere(position = (0, 1.2, -5), radius = 0.15, material=  carrot()))
rayTracer.scene.append(Sphere(position = (0.09, 0.9, -5), radius = 0.05, material=  stone()))
rayTracer.scene.append(Sphere(position = (-0.09, 0.9, -5), radius = 0.05, material=  stone()))
rayTracer.scene.append(Sphere(position = (0.25, 1.0, -5), radius = 0.05, material=  stone()))
rayTracer.scene.append(Sphere(position = (-0.25, 1.0, -5), radius = 0.05, material=  stone()))
rayTracer.scene.append(Sphere(position = (0.25, 1.4, -5), radius = 0.1, material=  plastic()))
rayTracer.scene.append(Sphere(position = (-0.25, 1.4, -5), radius = 0.1, material=  plastic()))
rayTracer.scene.append(Sphere(position = (0.209, 1.13, -4), radius = 0.05, material=  stone()))
rayTracer.scene.append(Sphere(position = (-0.209, 1.13, -4), radius = 0.05, material=  stone()))

#Botones del muñeco
rayTracer.scene.append(Sphere(position = (0, 0.3, -5), radius = 0.15, material=  stone()))
rayTracer.scene.append(Sphere(position = (0, -0.4, -5), radius = 0.15, material=  stone()))
rayTracer.scene.append(Sphere(position = (0, -1.1, -5), radius = 0.2, material=  stone()))


rayTracer.lights.append(AmbientLight(intensity=0.7))
rayTracer.lights.append(DirectionalLight(direction=(1, -1, 1), intensity=0.3))
rayTracer.lights.append(PointLight(position=(1, 0.5, -5), intensity=0.07, color=(1, 1, 1)))
#rayTracer.lights.append(PointLight(position=(1, -1, -7), intensity=1, color=(1, 1, 1)))

isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    rayTracer.rtClear()
    rayTracer.rtRender()
    pygame.display.flip()

pygame.quit()
