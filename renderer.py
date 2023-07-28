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

width = int(input("Ingrese el ancho del canvas: "))
height = int(input("Ingrese la altura del canvas: "))
inputFile = input("Ingrese el nombre del archivo de entrada sin su extensión: ") + ".obj"
exitFile = input("Ingrese el nombre del archivo de salida sin su extensión: ") + ".bmp"

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

rend.glLoadModel(inputFile, translate=(-width*6.47, height/6, 0), scale=(5000,5000,5000))

rend.glRender()

rend.glFinish(exitFile)
