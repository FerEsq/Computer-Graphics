'''
 * Nombre: renderer.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 16.07.2023 
 '''

from gl import Renderer, V2, V3, color
import shaders

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("Bienvenido al renderizador de archivos .obj")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

width = 1500
height = 1500
modelFile = "bb8.obj"
textureFile = "texture.bmp"
exitFile = "output.bmp"

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

rend.glLoadModel(filename = modelFile, 
                 textureName = textureFile, 
                 translate=(width-(width/4), height/32, 0), 
                 scale=(23,23,23), 
                 rotate=(-90,0,90))

rend.glRender()

rend.glFinish(exitFile)
