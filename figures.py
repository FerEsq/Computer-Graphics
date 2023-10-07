'''
 * Nombre: figures.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 29.09.2023
              Modificado el 06.10.2023
 '''

import mathLibrary as ml
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
        L = ml.twoVecSubstraction(self.position, origin)
        lengthL = ml.vecNormSimple(L)
        tca = ml.twoVecDot(L, direction)
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
        
        point = ml.twoVecSum(origin, ml.valVecMultiply(t0, direction))
        normal = ml.twoVecSubstraction(point, self.position)
        normal = ml.vecNorm(normal)
        
        u = 0.5 + (atan2(normal[2], normal[0]) / (2 * pi))
        v = (acos(normal[1]) / pi)

        return Intercept(distance=t0,
                         point=point,
                         normal=normal,
                         obj=self,
                         textureCoordinates=(u, v))
    
class Plane(Shape):
    def __init__(self, position, normal, material):
        super().__init__(position, material)
        self.normal = ml.vecNorm(normal)

    def intersect(self, origin, direction):
        denominator = ml.twoVecDot(direction, self.normal)

        if abs(denominator) <= 0.0001:
            return None

        t = ml.twoVecDot(ml.twoVecSubstraction(self.position, origin), self.normal) / denominator

        if t < 0:
            return None
        
        point = ml.twoVecSum(origin, ml.valVecMultiply(t, direction))

        return Intercept(distance=t,
                         point=point,
                         normal=self.normal,
                         obj=self,
                         textureCoordinates=None)
    
class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal, material)
        self.radius = radius

    def intersect(self, origin, direction):
        intercept = super().intersect(origin, direction)

        if intercept is None:
            return None

        if ml.vecNormSimple(ml.twoVecSubstraction(intercept.point, self.position)) > self.radius:
            return None

        return Intercept(
            distance=intercept.distance,
            point=intercept.point,
            normal=self.normal,
            obj=self,
            textureCoordinates=None
        )
    
class AABB(Shape):
    def __init__(self, position, size, material):
        super().__init__(position, material)
        self.size = size
        self.planes = []

        leftPlane = Plane(
            ml.twoVecSum(self.position, (-size[0] / 2, 0, 0)),
            (-1, 0, 0),
            self.material
        )
        rightPlane = Plane(
            ml.twoVecSum(self.position, (size[0] / 2, 0, 0)),
            (1, 0, 0),
            self.material
        )
        bottomPlane = Plane(
            ml.twoVecSum(self.position, (0, -size[1] / 2, 0)),
            (0, -1, 0),
            self.material
        )
        topPlane = Plane(
            ml.twoVecSum(self.position, (0, size[1] / 2, 0)),
            (0, 1, 0),
            self.material
        )
        backPlane = Plane(
            ml.twoVecSum(self.position, (0, 0, -size[2] / 2)),
            (0, 0, -1),
            self.material
        )
        frontPlane = Plane(
            ml.twoVecSum(self.position, (0, 0, size[2] / 2)),
            (0, 0, 1),
            self.material
        )

        self.planes.append(leftPlane)
        self.planes.append(rightPlane)
        self.planes.append(bottomPlane)
        self.planes.append(topPlane)
        self.planes.append(backPlane)
        self.planes.append(frontPlane)

        # BOUNDS
        bias = 0.001
        self.boundsMin = [position[i] - (bias + size[i] / 2) for i in range(3)]
        self.boundsMax = [position[i] + (bias + size[i] / 2) for i in range(3)]

    def intersect(self, origin, direction):
        intersect = None
        t = float('inf')
        u = 0
        v = 0

        for plane in self.planes:
            planeIntersect = plane.intersect(origin, direction)
            if planeIntersect is not None:
                planePoint = planeIntersect.point
                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
                            if planeIntersect.distance < t:
                                t = planeIntersect.distance
                                intersect = planeIntersect

                                if abs(plane.normal[0]) > 0:
                                    u = (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)
                                if abs(plane.normal[1]) > 0:
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)
                                if abs(plane.normal[2]) > 0:
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v = (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)

        if intersect is None:
            return None

        return Intercept(
            distance=t,
            point=intersect.point,
            normal=intersect.normal,
            obj=self,
            textureCoordinates=(u, v)
        )
