'''
 * Nombre: shaders.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 16.07.2023 
              Modificado el 07.08.2023
 '''

from mathLibrary import vecMatProduct

def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    vpMatrix = kwargs["vpMatrix"]

    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]

    vt = vpMatrix * projectionMatrix * viewMatrix * modelMatrix @ vt

    vt = vt.tolist()[0]

    vt = [vt[0]/vt[3],
          vt[1]/vt[3],
          vt[2]/vt[3]]

    return vt

def fragmentShader(**kwargs):
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]

    if texture != None:
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (1,1,1)

    return color