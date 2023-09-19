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
rayTracer.rtClearColor(0.3, 0.3, 0.3)
rayTracer.rtColor(1, 1, 1)


rayTracer.scene.append(Sphere(position=(1, 1, -5), radius=0.5, material=grass()))
rayTracer.scene.append(Sphere(position=(0, 0, -7), radius=2, material=brick()))
rayTracer.scene.append(Sphere(position=(-1, 0, -4), radius=0.3, material=water()))

rayTracer.lights.append(AmbientLight(intensity=0))
rayTracer.lights.append(DirectionalLight(direction=(-1, -1, -1), intensity=0.3))
rayTracer.lights.append(PointLight(position=(2.5, 5, -5), intensity=0.07, color=(1, 1, 1)))

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
