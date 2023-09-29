'''
 * Nombre: figures.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 29.09.2023
 '''

import numpy as np
from math import tan, pi, atan2, acos

class Shape:
    def __init__(self, position, material):
        self.position = position
        self.material = material

    def intersect(self, origin, direction):
        return None

    def normal(self, point):
        raise NotImplementedError()
    
class Intercept:
    def __init__(self, distance, point, normal, obj, textureCoordinates):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.obj = obj
        self.textureCoordinates = textureCoordinates

class Sphere(Shape):
    def __init__(self, position, radius, material):
        super().__init__(position, material)
        self.radius = radius

    def intersect(self, origin, direction):
        L = np.subtract(self.position, origin)
        lengthL = np.linalg.norm(L)
        tca = np.dot(L, direction)
        d = (lengthL ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1

        if t0 < 0:
            return None

        point = np.add(origin, np.multiply(t0, direction))
        normal = np.subtract(point, self.position)
        normal = normal / np.linalg.norm(normal)

        u = 0.5 + (atan2(normal[2], normal[0]) / (2 * pi))
        v = (acos(normal[1]) / pi)

        return Intercept(distance=t0,
                         point=point,
                         normal=normal,
                         obj=self,
                         textureCoordinates=(u, v))
