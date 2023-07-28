'''
 * Nombre: shaders.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 16.07.2023 
 '''

from matrix import multiplication

def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs['modelMatrix']

    transformedVertex = [[vertex[0]], 
                         [vertex[1]], 
                         [vertex[2]], 
                         [1] ]

    transformedVertex = multiplication(modelMatrix, transformedVertex)

    transformedVertex = [transformedVertex[0][0] / transformedVertex[3][0], 
                        transformedVertex[1][0] / transformedVertex[3][0], 
                        transformedVertex[2][0] / transformedVertex[3][0]]

    return transformedVertex

def fragmentShader(**kwargs):
    color = (1,1,1)
    return color
