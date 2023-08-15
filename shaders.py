'''
 * Nombre: shaders.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 16.07.2023 
              Modificado el 14.08.2023
 '''

import mathLibrary as ml
import numpy as np
from math import sqrt, exp

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
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w = kwargs["bCoords"]

    b = 1.0
    g = 1.0
    r = 1.0

    if texture != None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal = (u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2])
    
    negativedLight = (-dLight[0], -dLight[1], -dLight[2])
    intensity = max(0, ml.twoVecDot(normal, negativedLight))

    color1 = (0.5, 0.0, 1.0) #Color morado
    color2 = (1.0, 0.6, 0.8) #Color rosa
    color3 = (0.6, 0.8, 1.0) #Color celeste

    intensity = min(intensity * 2, 2)

    if intensity <= 1:
        finalColor = [
            (1 - intensity) * color1[channel] + intensity * color2[channel]
            for channel in range(3)
        ]
    else:
        intensity -= 1
        finalColor = [
            (1 - intensity) * color2[channel] + intensity * color3[channel]
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
    
#Función para ajustar valores
def adjust(value, min_value, max_value):
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

    #color = (0.5, 0.0, 1.0) #Color morado
    color = (0.2, 0.6, 0.4) #Color verde

    b = (1.0 - saturation) * b + saturation * color[2]
    g = (1.0 - saturation) * g + saturation * color[1]
    r = (1.0 - saturation) * r + saturation * color[0]

    #Ajustar los valores de color dentro del rango 0 a 1
    r = adjust(r, 0.0, 1.0)
    g = adjust(g, 0.0, 1.0)
    b = adjust(b, 0.0, 1.0)

    return r, g, b

def outlineShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w = kwargs["bCoords"]

    if texture != None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)

    normal = (u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2])
    
    negativedLight = (-dLight[0], -dLight[1], -dLight[2])
    intensity = max(0, ml.twoVecDot(normal, negativedLight))

    outlineColor = (0.3, 0.7, 0.8)  #Color aqua
    interiorColor = textureColor if texture != None else (1.0, 1.0, 1.0)

    threshold = 0.5
    falloff = 0.2 

    mixFactor = exp(-(intensity - threshold) / falloff)

    finalColor = [
        (1 - mixFactor) * interiorColor[channel] + mixFactor * outlineColor[channel]
        for channel in range(3)
    ]

    finalColor = [max(0.0, min(1.0, channel)) for channel in finalColor]

    return finalColor
