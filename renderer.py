'''
 * Nombre: renderer.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 26.07.2023
              Modificado el 27.08.2023
 '''

from gl import Renderer
import shaders

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("Bienvenido al renderizador de archivos .obj")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

width = 1080
height = 720

modelFile = "models/table.obj"
textureFile = "textures/table.bmp"
exitFile = "scene/scene.bmp"

rend = Renderer(width, height)

rend.glClearColor(0.5,0.5,0.5)
rend.glBackgroundTexture('./backgrounds/living.bmp')
rend.clearBackground()
rend.vertexShader = shaders.vertexShader

# ----- Render del sillón -----
rend.fragmentShader = shaders.difusedShader
rend.glDirectionalLight((0,0,-1))
rend.glLoadModel(filename = "models/chair.obj",
                 textureName = "textures/chair.bmp",
                 translate = (-1.5,-1.5,-4),
                 rotate = (0, 30, 0),
                 scale = (0.6,0.6,0.6))
rend.glRender()

# ----- Render de la mesa -----
rend.fragmentShader = shaders.saturatedShader
rend.glDirectionalLight((0,1,1))
rend.glLoadModel(filename = "models/table.obj",
                 textureName = "textures/table.bmp",
                 translate = (0.3,-1.5,-3),
                 rotate = (0, 0, 0),
                 scale = (0.01,0.01,0.01))
rend.glRender()

# ----- Render de la planta -----
rend.fragmentShader = shaders.outlineShader
rend.glDirectionalLight((0,0,-1))
rend.glLoadModel(filename = "models/plant.obj",
                 textureName = "textures/plant.bmp",
                 translate = (0.3,-1.0,-3),
                 rotate = (0, 0, 0),
                 scale = (0.015,0.015,0.015))
rend.glRender()

# ----- Render del patito -----
rend.fragmentShader = shaders.toonShader
rend.glDirectionalLight((0,0,1))
rend.glLoadModel(filename = "models/ducky.obj",
                 textureName = "textures/ducky.bmp",
                 translate = (-1.7,-1.7,-4),
                 rotate = (0, 145, 0),
                 scale = (0.6,0.6,0.6))
rend.glRender()


rend.glFinish(exitFile)
