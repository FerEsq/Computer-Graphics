'''
 * Nombre: shaders.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 16.07.2023 
              Modificado el 11.08.2023
 '''

import mathLibrary as ml
import numpy as np
from math import sqrt

def vertexShader(vertex, **kwargs):  
    # El Vertex Shader se lleva a cabo por cada v�rtice

    modelMatrix = kwargs["modelMatrix"]
    viewMatrix= kwargs["viewMatrix"]
    projectionMatrix= kwargs["projectionMatrix"]
    vpMatrix= kwargs["vpMatrix"]

    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]

    vt1= ml.twoMatProduct(vpMatrix, projectionMatrix)
    vt2= ml.twoMatProduct(vt1, viewMatrix)
    vt3= ml.twoMatProduct(vt2, modelMatrix)
    vt = ml.vecMatProduct(vt3, vt)

    """ vt = vt.tolist()[0] """

    vt = [vt[0]/vt[3],
          vt[1]/vt[3],
          vt[2]/vt[3]]

    return vt

def fragmentShader(**kwargs):
    # El Fragment Shader se lleva a cabo por cada pixel
    # que se renderizará en la pantalla.

    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]

    if texture != None:
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (1,1,1)


    return color

def flatShader(**kwargs):
    dLight = kwargs["dLight"]
    normal= kwargs["triangleNormal"]
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]

    b = 1.0
    g = 1.0
    r = 1.0

    if texture != None:
        textureColor = texture.getColor(texCoords[0], texCoords[1])    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    negativedLight = (-dLight[0], -dLight[1], -dLight[2])
    intensity = ml.twoVecDot(normal, negativedLight)
    
    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b

    else:
        return [0,0,0]
    
def gouradShader(**kwargs):
    texture= kwargs["texture"]
    tA, tB, tC= kwargs["texCoords"]
    nA, nB, nC= kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w= kwargs["bCoords"]

    b = 1.0
    g = 1.0
    r = 1.0

    if texture != None:
        tU= u * tA[0] + v * tB[0] + w * tC[0]
        tV= u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal= (u * nA[0] + v * nB[0] + w * nC[0],
             u * nA[1] + v * nB[1] + w * nC[1],
             u * nA[2] + v * nB[2] + w * nC[2])
    
    negativedLight = (-dLight[0], -dLight[1], -dLight[2])
    intensity = ml.twoVecDot(normal, negativedLight)
    
    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b

    else:
        return (0,0,0)

def difusedShader(**kwargs):
    texture= kwargs["texture"]
    tA, tB, tC= kwargs["texCoords"]
    nA, nB, nC= kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w= kwargs["bCoords"]

    b = 1.0
    g = 1.0
    r = 1.0

    if texture != None:
        tU= u * tA[0] + v * tB[0] + w * tC[0]
        tV= u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal= (u * nA[0] + v * nB[0] + w * nC[0],
             u * nA[1] + v * nB[1] + w * nC[1],
             u * nA[2] + v * nB[2] + w * nC[2])
    
    negativedLight = (-dLight[0], -dLight[1], -dLight[2])
    intensity = ml.twoVecDot(normal, negativedLight)

    intensity = max(0, intensity)

    color1 = [1.0, 0.6, 0.8] #Color rosa
    color2 = [0.6, 0.8, 1.0] #Color celeste

    mixFactor = sqrt(intensity)  

    #Mezclar ambos colores
    finalColor = [
        (1 - mixFactor) * color1[channel] + mixFactor * color2[channel]
        for channel in range(3)
    ]

    return finalColor

def voidShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    u, v, w = kwargs["bCoords"]

    threshold = 0.5 

    if texture is not None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)
        intensity = (textureColor[0] + textureColor[1] + textureColor[2]) / 3
    else:
        intensity = 0.0

    if intensity < threshold:
        return 1, 1, 1  
    else:
        return 0, 0, 0  
    

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def saturatedShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w = kwargs["bCoords"]

    b = 0.0
    g = 0.0
    r = 0.0

    saturation = 0.0

    if texture is not None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]
        textureColor = texture.getColor(tU, tV)
        b += (1.0 - saturation) * textureColor[2]
        g += (1.0 - saturation) * textureColor[1]
        r += (1.0 - saturation) * textureColor[0]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]

    dLight = np.array(dLight)
    intensity = np.dot(normal, -dLight)
    
    if intensity > 0:
        b += (1.0 - saturation) * intensity
        g += (1.0 - saturation) * intensity
        r += (1.0 - saturation) * intensity

    saturation += 3

    color = (0.5, 0.0, 1.0) #Color morado

    b = (1.0 - saturation) * b + saturation * color[2]
    g = (1.0 - saturation) * g + saturation * color[1]
    r = (1.0 - saturation) * r + saturation * color[0]

    # Ajustar los valores de color dentro del rango 0 a 1
    r = clamp(r, 0.0, 1.0)
    g = clamp(g, 0.0, 1.0)
    b = clamp(b, 0.0, 1.0)

    return r, g, b

def pixelArtShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w = kwargs["bCoords"]

    pixel_size = 4  # Tamaño deseado para los píxeles (ajusta según tus necesidades)

    b = 1.0
    g = 1.0
    r = 1.0

    if texture is not None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]

    dLight = np.array(dLight)
    intensity = np.dot(normal, -dLight)

    b *= intensity
    g *= intensity
    r *= intensity

    # Discretizar colores para lograr el efecto de pixel art
    r = round(r * (pixel_size - 1)) / (pixel_size - 1)
    g = round(g * (pixel_size - 1)) / (pixel_size - 1)
    b = round(b * (pixel_size - 1)) / (pixel_size - 1)

    if intensity > 0:
        return r, g, b
    else:
        return [0, 0, 0]