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
print("Las medidas recomendadas son: \n- Ancho: 3500 \n- Altura: 3500")
print("Archivo de entrada: 'kirby.obj'")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

width = 3500
height = 3500
inputFile = "kirby.obj"
exitFile = "salida.bmp"

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

rend.glLoadModel(inputFile, 
                 translate=(-width*6.47, height/6, 0), 
                 scale=(5000,5000,5000))

rend.glRender()

rend.glFinish(exitFile)
