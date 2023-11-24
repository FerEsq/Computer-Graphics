'''
 * Nombre: main.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode, pygame, OpenGL
 * Historial: Finalizado el 26.10.2023
              Modificado el 08.11.2023
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

#Model loading function
def loadModel(objF):
    objDataF = []
    for face in objF.faces:
        if len(face) == 3:
            for vertexInfo in face:
                vertexID, texcoordID, normalID = vertexInfo
                vertex = objF.vertices[vertexID - 1]
                normals = objF.normals[normalID - 1]
                uv = objF.texcoords[texcoordID - 1]
                uv = [uv[0], uv[1]]
                objDataF.extend(vertex + uv + normals)
        elif len(face) == 4:
            for i in [0, 1, 2]:
                vertexInfo = face[i]
                vertexID, texcoordID, normalID = vertexInfo
                vertex = objF.vertices[vertexID - 1]
                normals = objF.normals[normalID - 1]
                uv = objF.texcoords[texcoordID - 1]
                uv = [uv[0], uv[1]]
                objDataF.extend(vertex + uv + normals)
            for i in [0, 2, 3]:
                vertexInfo = face[i]
                vertexID, texcoordID, normalID = vertexInfo
                vertex = objF.vertices[vertexID - 1]
                normals = objF.normals[normalID - 1]
                uv = objF.texcoords[texcoordID - 1]
                uv = [uv[0], uv[1]]
                objDataF.extend(vertex + uv + normals)
    return objDataF

#Model loading
obj = Obj("models/ducky.obj")
objData = loadModel(obj)
model = Model(objData)
model.loadTexture("textures/ducky.bmp")
model.loadNoiseTexture("textures/purple.jpg")

#Model position
model.position.z = -2.4
model.position.y = -2
model.position.x = -0.3
model.rotation.y = 120
model.scale = glm.vec3(1.20, 1.20, 1.20)
renderer.scene.append(model)

#Lighting
renderer.lightIntensity = 0.8
renderer.dirLight = glm.vec3(0.0, 0.0, -1.0)

isRunning = True
while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    renderer.elapsedTime += deltaTime
    keys = pygame.key.get_pressed()

    if keys[K_SPACE]:
        renderer.clearColor[2] += deltaTime
    if keys[K_LSHIFT]:
        renderer.clearColor[2] -= deltaTime

    if keys[K_RIGHT]:
        model.rotation.y += deltaTime * 50
    if keys[K_LEFT]:
        model.rotation.y -= deltaTime * 50
    if keys[K_UP]:
        model.rotation.x += deltaTime * 50
    if keys[K_DOWN]:
        model.rotation.x -= deltaTime * 50

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            if event.key == pygame.K_n:
                print("Original shader")
                renderer.setShader(vertex_shader, fragment_shader)
            if event.key == pygame.K_p:
                print("Party shader")
                renderer.setShader(vertex_shader, party_fragment_shader)
            if event.key == pygame.K_s:
                print("Sparkling shader")
                renderer.setShader(vertex_shader, sparkling_fragment_shader)
            if event.key == pygame.K_d:
                print("Distorsioned shader")
                renderer.setShader(vertex_shader, distorsioned_fragment_shader)
            if event.key == pygame.K_o:
                print("Outline shader")
                renderer.setShader(vertex_shader, outline_fragment_shader)

            if event.key == pygame.K_1:
                print("A cute ducky plush has enter the scene!")
                renderer.scene.clear()
                obj = Obj("models/ducky.obj")
                objData = loadModel(obj)
                model = Model(objData)
                model.loadTexture("textures/ducky.bmp")
                model.loadNoiseTexture("textures/purple.jpg")
                model.position.z = -2.4
                model.position.y = -2
                model.position.x = -0.3
                model.rotation.y = 120
                model.scale = glm.vec3(1.20, 1.20, 1.20)
                renderer.scene.append(model)
                
            if event.key == pygame.K_2:
                print("A cute little octopus has enter the scene!")
                renderer.scene.clear()
                obj = Obj("models/octopus.obj")
                objData = loadModel(obj)
                model = Model(objData)
                model.loadTexture("textures/octopus.bmp")
                model.loadNoiseTexture("textures/purple.jpg")
                model.position.z = -10
                model.position.y = 0
                model.position.x = -0.3
                model.rotation.y = 180
                model.scale = glm.vec3(1.20,1.20,1.20)
                renderer.scene.append(model)

            if event.key == pygame.K_3:
                print("A watermelon has enter the scene!")
                renderer.scene.clear()
                obj = Obj("models/diamond.obj")
                objData = loadModel(obj)
                model = Model(objData)
                model.loadTexture("textures/diamond.bmp")
                model.loadNoiseTexture("textures/purple.jpg")
                model.position.z = -3.5
                model.position.y = 0
                model.position.x = 0
                model.rotation.x = -90
                model.scale = glm.vec3(1.20,1.20,1.20)
                renderer.scene.append(model)

            if event.key == pygame.K_4:
                print("A cute kitty plush has enter the scene!")
                renderer.scene.clear()
                obj = Obj("models/catPlush.obj")
                objData = loadModel(obj)
                model = Model(objData)
                model.loadTexture("textures/catPlushCalico.bmp")
                model.loadNoiseTexture("textures/purple.jpg")
                model.position.z = -1
                model.position.y = -0.3
                model.position.x = 0
                model.rotation.y = 0
                model.scale = glm.vec3(1.5, 1.5, 1.5)
                renderer.scene.append(model)

    renderer.render()
    pygame.display.flip()

pygame.quit()