'''
 * Nombre: main.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode, pygame, OpenGL
 * Historial: Finalizado el 26.10.2023
              Modificado el 04.11.2023
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
obj = Obj("models/ducky.obj")
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
model.loadTexture("textures/ducky.bmp")
model.loadNoiseTexture("textures/purple.jpg")
model.position.z = -2
model.position.y = -2
model.position.x = -0.3
model.rotation.y = 120
model.scale = glm.vec3(1.20, 1.20, 1.20)
renderer.scene.append(model)
renderer.lightIntensity = 1.0
renderer.dirLight = glm.vec3(0.0, 0.0, -1.0)

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
            if event.key == pygame.K_1:
                print("Original")
                renderer.setShader(vertex_shader, fragment_shader)
            if event.key == pygame.K_2:
                print("Gourad")
                renderer.setShader(vertex_shader, gourad_fragment_shader)
            if event.key == pygame.K_3:
                print("Cell")
                renderer.setShader(vertex_shader, cell_fragment_shader)
            if event.key == pygame.K_4:
                print("Multicolor")
                renderer.setShader(vertex_shader, multicolor_fragment_shader)
            if event.key == pygame.K_5:
                print("Party")
                renderer.setShader(vertex_shader, party_fragment_shader)
            if event.key == pygame.K_6:
                print("Sparkling")
                renderer.setShader(vertex_shader, sparkling_fragment_shader)
            if event.key == pygame.K_7:
                print("Distorsioned")
                renderer.setShader(vertex_shader, distorsioned_fragment_shader)

    renderer.render()
    pygame.display.flip()

pygame.quit()