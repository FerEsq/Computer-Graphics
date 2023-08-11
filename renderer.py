'''
 * Nombre: renderer.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 16.07.2023 
              Modificado el 09.08.2023
 '''

from gl import Renderer
import shaders

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("Bienvenido al renderizador de archivos .obj")
print("La cara frontal del dado es la que tiene el 3")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

width = 1080
height = 720

modelFile = "models/model.obj"
textureFile = "textures/model.bmp"
exitFile = "shaders/model2.bmp"

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.flatShader

#rend.glLookAt(camPos = (-3,-2,-2), eyePos= (0,0,-5))
        
rend.glLoadModel(filename = modelFile,
                 textureName = textureFile,
                 translate = (0,0,-5),
                 rotate = (0, 0, 0),
                 scale = (2,2,2))

rend.glRender()

rend.glFinish(exitFile)
