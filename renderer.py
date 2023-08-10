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

modelFile = "models/dice.obj"
textureFile = "textures/dice.bmp"
exitFile = "photoshoots/mediumShot.bmp"

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

# ~~~~~ Medium Shot ~~~~~
rend.glLookAt(camPos = (0,0,0), eyePos= (0,0,-5))

# ~~~~~ Low Angle ~~~~~
#rend.glLookAt(camPos = (0,-3,-2), eyePos= (0,0,-5))

# ~~~~~ High Angle ~~~~~
#rend.glLookAt(camPos = (0,3,-1), eyePos= (0,0,-5))

# ~~~~~ Dutch Angle ~~~~~
#rend.glLookAt(camPos = (-3,-2,-2), eyePos= (0,0,-5))
        
rend.glLoadModel(filename = modelFile,
                 textureName = textureFile,
                 translate = (0,0,-5),
                 rotate = (0, 0, 0),
                 scale = (3,3,3))

rend.glRender()

rend.glFinish(exitFile)
