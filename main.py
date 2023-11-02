'''
 * Nombre: main.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode, pygame, OpenGL
 * Historial: Finalizado el 26.10.2023
 '''

import pygame
import glm
from pygame.locals import *

from renderer import Renderer
from model import Model
from shaders import *
from obj import Obj

width = 960
height = 540

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

renderer = Renderer(screen)
renderer.setShader(vertex_shader, fragment_shader)

obj = Obj("models/koala.obj")

modelList = []
modeldata = []

for face in obj.faces:

    for vertexInfo in face:
        vertexID, texcoordID, normalID = vertexInfo

        vertex = obj.vertices[vertexID - 1]
        normal = obj.normals[normalID - 1]

        modeldata.extend(vertex + normal)

    model = Model(modeldata)
    modelList.append(model)

model = Model(modeldata)
model.position.z = -15
model.position.y = 0.5
model.scale = glm.vec3(0.03, 0.03, 0.03)

renderer.scene.append(model)

isRunning = True
while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        renderer.clearColor[0] += deltaTime
    if keys[pygame.K_LEFT]:
        renderer.clearColor[0] -= deltaTime
    if keys[pygame.K_UP]:
        renderer.clearColor[1] += deltaTime
    if keys[pygame.K_DOWN]:
        renderer.clearColor[1] -= deltaTime
    if keys[pygame.K_z]:
        renderer.clearColor[2] += deltaTime
    if keys[pygame.K_x]:
        renderer.clearColor[2] -= deltaTime

    # Handle quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    renderer.render()
    pygame.display.flip()

pygame.quit()