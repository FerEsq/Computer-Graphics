'''
 * Nombre: figures.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 20.09.2023
 '''

import mathLibrary as ml
from math import tan, pi, atan2, acos

class Intercept:
  def __init__(self, distance, point, normal, obj, textureCoordinates):
      self.distance = distance
      self.point = point
      self.normal = normal
      self.obj = obj
      self.textureCoordinates = textureCoordinates

class Shape(object):
  def __init__(self, position, material):
    self.position = position
    self.material = material

  def ray_intersect(self, orig, dir):
    return None
  
  def normal(self, point):
        raise NotImplementedError()

class Sphere(Shape):
  def __init__(self, position, radius, material):
    self.radius = radius
    super().__init__(position, material)
  
  def ray_intersect(self, origin, direction):
    L = ml.twoVecSubstraction(self.position, origin)
    lengthL = ml.vecNormSimple(L)
    tca = ml.twoVecDot(L, direction)
    d = (lengthL**2 - tca**2)**0.5

    if d > self.radius:
      return None
    
    thc = (self.radius**2 - d**2)**0.5

    t0 = tca - thc
    t1 = tca + thc

    if t0 < 0:
      t0 = t1
    
    if t0 < 0:
      return None
    
    multi = ml.valVecMultiply(t0, direction)
    #ml.twoVecMultiply(t0, direction)
    P = ml.twoVecSum(origin, multi)
    normal = ml.twoVecSubstraction(P, self.position)
    normal = ml.vecNorm(normal)

    u = 0.5 + (atan2(normal[2], normal[0]) / (2 * pi))
    v = (acos(normal[1]) / pi)

    return Intercept(distance = t0,
                     point = P,
                     normal=normal,
                     obj=self,
                     textureCoordinates=(u, v))
                     