'''
 * Nombre: lights.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 29.09.2023
 '''

import mathLibrary as ml
from math import acos, asin, sin, cos

def reflect(normal, direction):
    reflectValue = [2 * ml.twoVecDot(normal, direction) * n - d for n, d in zip(normal, direction)]
    return ml.vecNorm(reflectValue)

def totalInternalReflection(incident, normal, n1, n2):
    c1 = ml.twoVecDot(normal, incident)

    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    if n1 < n2:
        return False

    theta1 = acos(c1)
    thetaCritical = asin(n2 / n1)

    return theta1 >= thetaCritical


def refract(normal, incident, n1, n2):
    c1 = ml.twoVecDot(normal, incident)

    if c1 < 0:
        c1 = -c1
    else:
        factor = -1
        normal = [elemento * factor for elemento in normal]
        n1, n2 = n2, n1

    n = n1 / n2

    p1 = incident + [elemento * c1 for elemento in normal]
    p2 = 1 - n ** 2 * (1 - c1 ** 2)

    sp1 = [elemento * n for elemento in p1]
    sp2 = p2 ** 0.5
    sp3 = [elemento * sp2 for elemento in normal]
    
    t = ml.twoVecSubstraction(sp1, sp3)
    return ml.vecNorm(t)


def fresnel(normal, incident, n1, n2):
    c1 = ml.twoVecDot(normal, incident)

    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    s2 = (n1 * (1 - c1 ** 2) ** 0.5) / n2
    c2 = (1 - s2 ** 2) ** 0.5

    f1 = ((n2 * c1 - n1 * c2) / (n2 * c1 + n1 * c2)) ** 2
    f2 = ((n1 * c2 - n2 * c1) / (n1 * c2 + n2 * c1)) ** 2

    kr = (f1 + f2) / 2
    kt = 1 - kr

    return kr, kt


class Light:
    def __init__(self, intensity=1, color=(1, 1, 1), lightType="LIGHT"):
        self.intensity = intensity
        self.color = color
        self.type = lightType

    def getColor(self):
        return [self.color[0] * self.intensity,
                self.color[1] * self.intensity,
                self.color[2] * self.intensity]

    def getDiffuseColor(self, intercept):
        return None

    def getSpecularColor(self, intercept, viewPosition):
        return None

class AmbientLight(Light):
    def __init__(self, intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "AMBIENT")

class DirectionalLight(Light):
    def __init__(self, direction=(0, 1, 0), intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "DIRECTIONAL")
        self.direction = ml.vecNorm(direction)

    def getDiffuseColor(self, intercept):
        direction = [i * -1 for i in self.direction]

        intensity = ml.twoVecDot(intercept.normal, direction) * self.intensity
        intensity = max(0, min(1, intensity))
        intensity *= 1 - intercept.obj.material.Ks

        return [i * intensity for i in self.color]

    def getSpecularColor(self, intercept, viewPosition):
        direction = [i * -1 for i in self.direction]

        reflectDirection = reflect(intercept.normal, direction)

        viewDirection = ml.twoVecSubstraction(viewPosition, intercept.point)
        viewDirection = ml.vecNorm(viewDirection)

        intensity = max(0, min(1, ml.twoVecDot(reflectDirection, viewDirection))) ** intercept.obj.material.spec
        intensity *= self.intensity
        intensity *= intercept.obj.material.Ks

        return [i * intensity for i in self.color]

class PointLight(Light):
    def __init__(self, position=(0, 0, 0), intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "POINT")
        self.position = position

    def getDiffuseColor(self, intercept):
        direction = ml.twoVecSubstraction(self.position, intercept.point)
        radius = ml.vecNormSimple(direction)
        direction = direction / radius

        intensity = ml.twoVecDot(intercept.normal, direction) * self.intensity
        intensity *= 1 - intercept.obj.material.Ks

        if radius != 0:
            intensity /= radius ** 2
        intensity = max(0, min(1, intensity))

        return [i * intensity for i in self.color]

    def getSpecularColor(self, intercept, viewPosition):
        direction = ml.twoVecSubstraction(self.position, intercept.point)
        radius = ml.vecNormSimple(direction)
        direction = direction / radius

        reflectDirection = reflect(intercept.normal, direction)

        viewDirection = ml.twoVecSubstraction(viewPosition, intercept.point)
        viewDirection = ml.vecNorm(viewDirection)

        intensity = max(0, min(1, ml.twoVecDot(reflectDirection, viewDirection))) ** intercept.obj.material.spec
        intensity *= self.intensity
        intensity *= intercept.obj.material.Ks

        if radius != 0:
            intensity /= radius ** 2
        intensity = max(0, min(1, intensity))

        return [i * intensity for i in self.color]
