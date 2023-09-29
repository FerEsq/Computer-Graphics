'''
 * Nombre: lights.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 29.09.2023
 '''

import numpy as np
from math import acos, asin, sin, cos

def reflect(normal, direction):
    reflectValue = (2 * np.dot(normal, direction) * normal - direction)
    return reflectValue / np.linalg.norm(reflectValue)

def totalInternalReflection(incident, normal, n1, n2):
    c1 = np.dot(normal, incident)

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
    c1 = np.dot(normal, incident)

    if c1 < 0:
        c1 = -c1
    else:
        normal = np.array(normal) * -1
        n1, n2 = n2, n1

    n = n1 / n2

    t = n * (incident + c1 * normal) - normal * (1 - n ** 2 * (1 - c1 ** 2)) ** 0.5
    return t / np.linalg.norm(t)


def fresnel(normal, incident, n1, n2):
    c1 = np.dot(normal, incident)

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
        self.direction = direction / np.linalg.norm(direction)

    def getDiffuseColor(self, intercept):
        direction = [i * -1 for i in self.direction]

        intensity = np.dot(intercept.normal, direction) * self.intensity
        intensity = max(0, min(1, intensity))
        intensity *= 1 - intercept.obj.material.Ks

        return [i * intensity for i in self.color]

    def getSpecularColor(self, intercept, viewPosition):
        direction = [i * -1 for i in self.direction]

        reflectDirection = reflect(intercept.normal, direction)

        viewDirection = np.subtract(viewPosition, intercept.point)
        viewDirection = viewDirection / np.linalg.norm(viewDirection)

        intensity = max(0, min(1, np.dot(reflectDirection, viewDirection))) ** intercept.obj.material.spec
        intensity *= self.intensity
        intensity *= intercept.obj.material.Ks

        return [i * intensity for i in self.color]

class PointLight(Light):
    def __init__(self, position=(0, 0, 0), intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "POINT")
        self.position = position

    def getDiffuseColor(self, intercept):
        direction = np.subtract(self.position, intercept.point)
        radius = np.linalg.norm(direction)
        direction = direction / radius

        intensity = np.dot(intercept.normal, direction) * self.intensity
        intensity *= 1 - intercept.obj.material.Ks

        if radius != 0:
            intensity /= radius ** 2
        intensity = max(0, min(1, intensity))

        return [i * intensity for i in self.color]

    def getSpecularColor(self, intercept, viewPosition):
        direction = np.subtract(self.position, intercept.point)
        radius = np.linalg.norm(direction)
        direction = direction / radius

        reflectDirection = reflect(intercept.normal, direction)

        viewDirection = np.subtract(viewPosition, intercept.point)
        viewDirection = viewDirection / np.linalg.norm(viewDirection)

        intensity = max(0, min(1, np.dot(reflectDirection, viewDirection))) ** intercept.obj.material.spec
        intensity *= self.intensity
        intensity *= intercept.obj.material.Ks

        if radius != 0:
            intensity /= radius ** 2
        intensity = max(0, min(1, intensity))

        return [i * intensity for i in self.color]
