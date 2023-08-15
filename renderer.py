'''
 * Nombre: renderer.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 16.07.2023 
              Modificado el 14.08.2023
 '''

from gl import Renderer
import shaders

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("Bienvenido al renderizador de archivos .obj")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

width = 1080
height = 720

modelFile = "models/koala.obj"
textureFile = "textures/koala.bmp"
exitFile = "shaders/shader3.bmp"

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.outlineShader

#difused -> dLight = (0,0,-1)
#satured -> dLight = (0,0,1)
#outline -> dLight = (0,0,-1)
        
rend.glLoadModel(filename = modelFile,
                 textureName = textureFile,
                 translate = (0,0,-3.5),
                 rotate = (0, 0, 0),
                 scale = (0.006,0.006,0.006))

rend.glRender()

rend.glFinish(exitFile)
