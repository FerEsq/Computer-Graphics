'''
 * Nombre: main.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode, pygame, OpenGL
 * Historial: Finalizado el 26.10.2023
              Modificado el 01.11.2023
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

#Model loading
obj = Obj("models/koala.obj")
objData = []

for face in obj.faces:
    if len(face) == 3:
        for vertexInfo in face:
            vertexID, texcoordID, normalID = vertexInfo
            vertex = obj.vertices[vertexID - 1]
            normals = obj.normals[normalID - 1]
            uv = obj.texcoords[texcoordID - 1]
            uv = [uv[0], uv[1]]
            objData.extend(vertex + uv + normals)
    elif len(face) == 4:
        for i in [0, 1, 2]:
            vertexInfo = face[i]
            vertexID, texcoordID, normalID = vertexInfo
            vertex = obj.vertices[vertexID - 1]
            normals = obj.normals[normalID - 1]
            uv = obj.texcoords[texcoordID - 1]
            uv = [uv[0], uv[1]]
            objData.extend(vertex + uv + normals)
        for i in [0, 2, 3]:
            vertexInfo = face[i]
            vertexID, texcoordID, normalID = vertexInfo
            vertex = obj.vertices[vertexID - 1]
            normals = obj.normals[normalID - 1]
            uv = obj.texcoords[texcoordID - 1]
            uv = [uv[0], uv[1]]
            objData.extend(vertex + uv + normals)


model = Model(objData)
model.loadTexture("textures/koala.bmp")
model.position.z = -6
model.position.y = 0
model.scale = glm.vec3(0.01, 0.01, 0.01)
renderer.scene.append(model)

isRunning = True
while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    renderer.elapsedTime += deltaTime
    keys = pygame.key.get_pressed()

    if keys[K_RIGHT]:
        renderer.clearColor[0] += deltaTime
    if keys[K_LEFT]:
        renderer.clearColor[0] -= deltaTime
    if keys[K_UP]:
        renderer.clearColor[1] += deltaTime
    if keys[K_DOWN]:
        renderer.clearColor[1] -= deltaTime
    if keys[K_SPACE]:
        renderer.clearColor[2] += deltaTime
    if keys[K_LSHIFT]:
        renderer.clearColor[2] -= deltaTime

    if keys[K_d]:
        model.rotation.y += deltaTime * 50
    if keys[K_a]:
        model.rotation.y -= deltaTime * 50
    if keys[K_w]:
        model.rotation.x += deltaTime * 50
    if keys[K_s]:
        model.rotation.x -= deltaTime * 50


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    renderer.render()
    pygame.display.flip()

pygame.quit()