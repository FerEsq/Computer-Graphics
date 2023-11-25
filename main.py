'''
 * Nombre: main.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode, pygame, OpenGL
 * Historial: Finalizado el 26.10.2023
              Modificado el 24.11.2023
 '''

import pygame
import glm
import math
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

mii = pygame.mixer.Sound("media/mii.mp3")
ducky = pygame.mixer.Sound("media/ducky.mp3") 
octopus = pygame.mixer.Sound("media/octopus.mp3") 
diamond = pygame.mixer.Sound("media/diamond.mp3") 
catPlush = pygame.mixer.Sound("media/catPlush.mp3") 

mii.set_volume(0.5)
ducky.set_volume(0.8)
octopus.set_volume(0.8)
diamond.set_volume(0.8)
catPlush.set_volume(0.8)

mii.play(-1)

renderer = Renderer(screen)
renderer.setShader(vertex_shader, fragment_shader)

is_dragging = False
old_position = None
catModel = False

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
model.lookAt = glm.vec3(model.position.x, model.position.y + 2 , model.position.z)
renderer.scene.append(model)
renderer.target = model.lookAt

#Lighting
renderer.lightIntensity = 0.8
renderer.dirLight = glm.vec3(0.0, 0.0, -1.0)

isRunning = True

movement_sensitive = 0.1
sens_x = 1
sens_y = 0.1
distance = abs(renderer.cameraPosition.z- model.position.z)
radius = distance
zoom_sensitive = 0.5
angle = 0.0

while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    renderer.elapsedTime += deltaTime
    #keys = pygame.key.get_pressed()

    renderer.cameraPosition.x = math.sin(math.radians(angle)) * radius + model.position.x
    renderer.cameraPosition.z = math.cos(math.radians(angle)) * radius + model.position.z
    
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
                catModel = False
                print("A cute ducky plush has enter the scene!")
                ducky.play()
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
                catModel = False
                print("A cute little octopus has enter the scene!")
                octopus.play()
                renderer.scene.clear()
                obj = Obj("models/octopus.obj")
                objData = loadModel(obj)
                model = Model(objData)
                model.loadTexture("textures/octopus.bmp")
                model.loadNoiseTexture("textures/purple.jpg")
                model.position.z = -1
                model.position.y = 0
                model.position.x = 0
                model.rotation.y = 180
                model.scale = glm.vec3(0.10,0.10,0.10)
                renderer.scene.append(model)

            if event.key == pygame.K_3:
                catModel = False
                print("A shiny diamond has enter the scene!")
                diamond.play()
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
                catModel = True
                print("A cute kitty plush has enter the scene!")
                catPlush.play()
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
            if (catModel == True):
                if event.key == pygame.K_8:
                    catPlush.play()
                    model.loadTexture("textures/catPlushCalico.bmp")
                if event.key == pygame.K_9:
                    catPlush.play()
                    model.loadTexture("textures/catPlushGray.bmp")
                if event.key == pygame.K_0:
                    catPlush.play()
                    model.loadTexture("textures/catPlushOrange.bmp")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                is_dragging = True
                old_position = pygame.mouse.get_pos()

            elif event.button == 4:
                if radius > distance * 0.5:
                    radius -= zoom_sensitive             

            elif event.button == 5:
                if radius < distance * 1.5:
                    radius += zoom_sensitive

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  
                is_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if is_dragging:
                new_position = pygame.mouse.get_pos()
                deltax = new_position[0] - old_position[0]
                deltay = new_position[1] - old_position[1]
                angle += deltax * -sens_x

                if angle > 360:
                    angle = 0

                if distance > renderer.cameraPosition.y + deltay * -sens_y and distance * -1.5 < renderer.cameraPosition.y + deltay * -sens_y:
                    renderer.cameraPosition.y += deltay * -sens_y

                old_position = new_position
            

    renderer.updateViewMatrix()
    renderer.render()
    pygame.display.flip()

pygame.quit()