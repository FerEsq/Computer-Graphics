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

width = 500
height = 500

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

#Music and sound effects
mii = pygame.mixer.Sound("media/mii.mp3")
ducky = pygame.mixer.Sound("media/ducky.mp3") 
octopus = pygame.mixer.Sound("media/octopus.mp3") 
diamond = pygame.mixer.Sound("media/diamond.mp3") 
catPlush = pygame.mixer.Sound("media/catPlush.mp3") 

mii.set_volume(0.2)
ducky.set_volume(0.5)
octopus.set_volume(0.5)
diamond.set_volume(0.5)
catPlush.set_volume(0.5)

mii.play(-1)

renderer = Renderer(screen)
renderer.setShader(vertex_shader, fragment_shader)

drag = False
oldPosition = None
catModel = False
actualShader = 0

#Menu printing
def printMenu():
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Welcome to the 3D model viewer! To see this menu again, press M.")
    print("We recommend you volume up your speakers to enjoy the experience!")

    print("\nModels available:")
    print("\t- A cute ducky plush (press 1)")
    print("\t- A cute litle octopus (press 2)")
    print("\t- A shiny diamond (press 3)")
    print("\t- A cute kitty plush (press 4)")
    print("\t\t* If you have the kitty on your screen, press 9 and 0 for a surprise!")

    print("\nShaders available:")
    print("\t- Original shader (press n)")
    print("\t- Party shader (press p)")
    print("\t- Sparkling shader (press s)")
    print("\t- Distorsioned shader (press d)")
    print("\t- Outline shader (press o)")
    print("\t\t* If you have a shader on your screen, press a for se the alternative version!")

    print("\nControls:")
    print("\t- Use the arrow keys to rotate the model")
    print("\t- Use the + and - keys to move the model closer or farther")
    print("\t- Use the mouse wheel to zoom in and out")
    print("\t- Use the mouse to rotate the camera around the model")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

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
model.lookAt = glm.vec3(model.position.x + 0.4, model.position.y + 2 , model.position.z - 2.4)
renderer.scene.append(model)
renderer.target = model.lookAt

#Lighting
renderer.lightIntensity = 0.8
renderer.dirLight = glm.vec3(0.0, 0.0, -1.0)

isRunning = True

movement_sensitive = 0.1
sensX = 1
sensY = 0.1
distance = abs(renderer.cameraPosition.z- model.position.z)
radius = distance
zoomSensitive = 0.5
angle = 0

printMenu()
while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    renderer.elapsedTime += deltaTime
    keys = pygame.key.get_pressed()

    renderer.cameraPosition.x = math.sin(math.radians(angle)) * radius + model.position.x
    renderer.cameraPosition.z = math.cos(math.radians(angle)) * radius + model.position.z

    if keys[K_RIGHT]:
        model.rotation.y += deltaTime * 50
    if keys[K_LEFT]:
        model.rotation.y -= deltaTime * 50
    if keys[K_UP]:
        if (model.rotation.x <= 45):
            model.rotation.x += deltaTime * 50
    if keys[K_DOWN]:
        if (model.rotation.x >= -100):
            model.rotation.x -= deltaTime * 50
    if keys[K_PLUS]:
        if (model.position.z <= 0):
            model.position.z += 0.1
    if keys[K_MINUS]:
        if (model.position.z >= -10):
            model.position.z -= 0.1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            if event.key == pygame.K_m:
                printMenu()
            if event.key == pygame.K_n:
                print("Original shader")
                renderer.setShader(vertex_shader, fragment_shader)

            if event.key == pygame.K_p:
                print("Party shader")
                actualShader = 1
                renderer.setShader(vertex_shader, party_fragment_shader)

            if event.key == pygame.K_s:
                print("Sparkling shader")
                actualShader = 2
                renderer.setShader(vertex_shader, sparkling_fragment_shader)

            if event.key == pygame.K_d:
                print("Distorsioned shader")
                actualShader = 3
                renderer.setShader(vertex_shader, distorsioned_fragment_shader)

            if event.key == pygame.K_o:
                print("Outline shader")
                actualShader = 4
                renderer.setShader(vertex_shader, outline_fragment_shader)

            if event.key == pygame.K_a:
                if (actualShader == 1):
                    print("Party alternative shader")
                    renderer.setShader(vertex_shader, party_fragment_shader_alternative)
                if (actualShader == 2):
                    print("Sparkling alternative shader")
                    renderer.setShader(vertex_shader, sparkling_fragment_shader_alternative)
                if (actualShader == 3):
                    print("Distorsioned alternative shader")
                    renderer.setShader(vertex_shader, distorsioned_fragment_shader_alternative)
                if (actualShader == 4):
                    print("Outline alternative shader")
                    renderer.setShader(vertex_shader, outline_fragment_shader_alternative)

            if event.key == pygame.K_1:
                octopus.stop()
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
                model.lookAt = glm.vec3(model.position.x + 0.4, model.position.y + 2 , model.position.z - 2.4)
                renderer.target = model.lookAt
                renderer.scene.append(model)
                
            if event.key == pygame.K_2:
                catModel = False
                print("A cute litle octopus has enter the scene!")
                octopus.play()
                renderer.scene.clear()
                obj = Obj("models/octopus.obj")
                objData = loadModel(obj)
                model = Model(objData)
                model.loadTexture("textures/octopus.bmp")
                model.loadNoiseTexture("textures/purple.jpg")
                model.rotation.y = 180
                model.scale = glm.vec3(0.30, 0.30, 0.30)
                model.lookAt = glm.vec3(model.position.x, model.position.y, model.position.z)
                renderer.target = model.lookAt
                renderer.scene.append(model)

            if event.key == pygame.K_3:
                octopus.stop()
                catModel = False
                print("A shiny diamond has enter the scene!")
                diamond.play()
                renderer.scene.clear()
                obj = Obj("models/diamond.obj")
                objData = loadModel(obj)
                model = Model(objData)
                model.loadTexture("textures/diamond.bmp")
                model.loadNoiseTexture("textures/purple.jpg")
                model.rotation.x = -90
                model.scale = glm.vec3(0.8,0.8,0.8)
                model.lookAt = glm.vec3(model.position.x, model.position.y, model.position.z)
                renderer.target = model.lookAt
                renderer.scene.append(model)

            if event.key == pygame.K_4:
                octopus.stop()
                catModel = True
                print("A cute kitty plush has enter the scene!")
                catPlush.play()
                renderer.scene.clear()
                obj = Obj("models/catPlush.obj")
                objData = loadModel(obj)
                model = Model(objData)
                model.loadTexture("textures/catPlushCalico.bmp")
                model.loadNoiseTexture("textures/purple.jpg")
                model.scale = glm.vec3(3.5, 3.5, 3.5)
                model.lookAt = glm.vec3(model.position.x, model.position.y + 0.6, model.position.z)
                renderer.target = model.lookAt
                renderer.scene.append(model)
            if (catModel == True):
                if event.key == pygame.K_9:
                    catPlush.play()
                    model.loadTexture("textures/catPlushGray.bmp")
                if event.key == pygame.K_0:
                    catPlush.play()
                    model.loadTexture("textures/catPlushOrange.bmp")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                drag = True
                oldPosition = pygame.mouse.get_pos()

            elif event.button == 4:
                if radius > distance * 0.5:
                    radius -= zoomSensitive             

            elif event.button == 5:
                if radius < distance * 1.5:
                    radius += zoomSensitive

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  
                drag = False

        elif event.type == pygame.MOUSEMOTION:
            if drag:
                new_position = pygame.mouse.get_pos()
                deltax = new_position[0] - oldPosition[0]
                deltay = new_position[1] - oldPosition[1]
                angle += deltax * -sensX

                if angle > 360:
                    angle = 0

                if distance > renderer.cameraPosition.y + deltay * -sensY and distance * -1.5 < renderer.cameraPosition.y + deltay * -sensY:
                    renderer.cameraPosition.y += deltay * -sensY

                oldPosition = new_position
            

    renderer.updateViewMatrix()
    renderer.render()
    pygame.display.flip()

pygame.quit()