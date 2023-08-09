'''
 * Nombre: renderer.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 16.07.2023 
              Modificado el 07.08.2023
 '''

from gl import Renderer
import shaders

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("Bienvenido al renderizador de archivos .obj")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

width = 600
height = 600

modelFile = "models/dice.obj"
textureFile = "textures/dice.bmp"
exitFile = "test.bmp"

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

rend.glLookAt(camPos = (-3,-3,-2), eyePos= (0,0,-5))

rend.glLoadModel(filename = modelFile,
                 textureName = textureFile,
                 translate = (0, 0, -5),
                 rotate = (0, 0, 0),
                 scale = (4,4,4))

rend.glRender()

rend.glFinish(exitFile)
