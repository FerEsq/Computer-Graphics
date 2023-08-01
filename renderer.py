'''
 * Nombre: renderer.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 16.07.2023 
              Modificado el 31.07.2023
 '''

from gl import Renderer, V2, V3, color
import shaders

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("Bienvenido al renderizador de archivos .obj")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

width = 3800
height = 3800
modelFile = "dog.obj"
textureFile = "texture.bmp"
exitFile = "output.bmp"

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

rend.glLoadModel(filename = modelFile, 
                 textureName = textureFile, 
                 translate=(width/4, height/1.5, 0), 
                 scale=(1200,1200,1200), 
                 rotate=(0,0,0))

rend.glLoadModel(filename = modelFile, 
                 textureName = textureFile, 
                 translate=(width-(width/4), height/1.5, 0), 
                 scale=(1200,1200,1200),  
                 rotate=(0,90,0))

rend.glLoadModel(filename = modelFile, 
                 textureName = textureFile, 
                 translate=(width/4, height/16, 0), 
                 scale=(1200,1200,1200), 
                 rotate=(0,180,0))

rend.glLoadModel(filename = modelFile, 
                 textureName = textureFile, 
                 translate=(width-(width/4), height/16, 0), 
                 scale=(1200,1200,1200), 
                 rotate=(0,270,0))

rend.glRender()

rend.glFinish(exitFile)
