'''
 * Nombre: rt.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 29.09.2023
 '''

from math import tan, pi, atan2, acos
import pygame
from materials import *
from lights import *

MAX_RECURSION_DEPTH = 3

class Raytracer(object):
    def __init__(self, screen):
        self.vpX = 0
        self.vpY = 0
        self.vpWidth = 0
        self.vpHeight = 0
        self.nearPlane = 0
        self.topEdge = 0
        self.rightEdge = 0
        self.clearColor = None
        self.currentColor = None

        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.scene = []
        self.lights = []

        self.cameraPosition = [0, 0, 0]

        self.rtViewPort(0, 0, self.width, self.height)
        self.rtProjection()

        self.rtClearColor(0, 0, 0)
        self.rtColor(1, 1, 1)
        self.rtClear()

        self.environmentMap = None

    def rtViewPort(self, x, y, width, height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height

    def rtProjection(self, fov=60, near=0.1):
        aspectRatio = self.vpWidth / self.vpHeight
        self.nearPlane = near
        self.topEdge = near * tan(fov * pi / 360)
        self.rightEdge = self.topEdge * aspectRatio

    def rtClearColor(self, r, g, b):
        self.clearColor = (r * 255, g * 255, b * 255)

    def rtColor(self, r, g, b):
        self.currentColor = (r * 255, g * 255, b * 255)

    def rtClear(self):
        self.screen.fill(self.clearColor)

    def rtPoint(self, x, y, color=None):
        y = self.width - y
        if (0 <= x < self.width) and (0 <= y < self.height):
            if color is None:
                color = self.currentColor
            else:
                color = (color[0] * 255, color[1] * 255, color[2] * 255)

            self.screen.set_at((x, y), color)

    def rtCastRay(self, origin, direction, sceneObject=None, recursionDepth=0):
        if recursionDepth > MAX_RECURSION_DEPTH:
            return None

        depth = float("inf")
        hit = None

        for obj in self.scene:
            if obj is not sceneObject:
                intercept = obj.intersect(origin, direction)
                if intercept is not None:
                    if intercept.distance < depth:
                        depth = intercept.distance
                        hit = intercept

        return hit

    def rtRayColor(self, intercept, rayDirection, recursionDepth=0):
        if intercept is None:
            if self.environmentMap is not None:
                x = (atan2(rayDirection[2], rayDirection[0]) / (2 * pi)) + 0.5
                y = acos(rayDirection[1]) / pi
                x = int(x * self.environmentMap.get_width())
                y = int(y * self.environmentMap.get_height())
                color = self.environmentMap.get_at((x, y))
                return [color[i] / 255 for i in range(3)]
            else:
                color = self.clearColor
                return [color[i] / 255 for i in range(3)]

        surfaceColor = intercept.obj.material.diffuse
        if intercept.obj.material.texture and intercept.textureCoordinates:
            x = int(intercept.textureCoordinates[0] * intercept.obj.material.texture.get_width() - 1)
            y = int(intercept.textureCoordinates[1] * intercept.obj.material.texture.get_height() - 1)
            if y >= intercept.obj.material.texture.get_height() or x >= intercept.obj.material.texture.get_width() or x < 0 or y < 0:
                color = [0,0,0]
            else:
                color = intercept.obj.material.texture.get_at((x, y))

            textureColor = [i / 255 for i in color]
            surfaceColor = [surfaceColor[i] * textureColor[i] for i in range(3)]


        ambientLightColor = [0, 0, 0]
        diffuseLightColor = [0, 0, 0]
        specularLightColor = [0, 0, 0]
        reflectColor = [0, 0, 0]
        refractColor = [0, 0, 0]

        if intercept.obj.material.type == OPAQUE:
            for light in self.lights:
                if light.type == "AMBIENT":
                    color = light.getColor()
                    ambientLightColor = [ambientLightColor[i] + color[i] for i in range(3)]
                else:
                    shadowDirection = None
                    if light.type == "DIRECTIONAL":
                        shadowDirection = [i * -1 for i in light.direction]
                    if light.type == "POINT":
                        lightDirection = ml.twoVecSubstraction(light.position, intercept.point)
                        shadowDirection = ml.vecNorm(lightDirection)

                    shadowIntersect = self.rtCastRay(intercept.point, shadowDirection, intercept.obj)

                    if shadowIntersect is None:
                        diffColor = light.getDiffuseColor(intercept)
                        diffuseLightColor = [diffuseLightColor[i] + diffColor[i] for i in range(3)]

                        specColor = light.getSpecularColor(intercept, self.cameraPosition)
                        specularLightColor = [specularLightColor[i] + specColor[i] for i in range(3)]
        elif intercept.obj.material.type == REFLECTIVE:

            factor = -1
            negativeRayDirection = [elemento * factor for elemento in rayDirection]

            reflectRay = reflect(intercept.normal, negativeRayDirection)
            reflectIntercept = self.rtCastRay(intercept.point, reflectRay, intercept.obj, recursionDepth + 1)
            reflectColor = self.rtRayColor(reflectIntercept, reflectRay, recursionDepth + 1)

            for light in self.lights:
                if light.type != "AMBIENT":
                    shadowDirection = None
                    if light.type == "DIRECTIONAL":
                        shadowDirection = [i * -1 for i in light.direction]
                    if light.type == "POINT":
                        lightDirection = ml.twoVecSubstraction(light.position, intercept.point)
                        shadowDirection = ml.vecNorm(lightDirection)

                    shadowIntersect = self.rtCastRay(intercept.point, shadowDirection, intercept.obj)

                    if shadowIntersect is None:
                        specColor = light.getSpecularColor(intercept, self.cameraPosition)
                        specularLightColor = [specularLightColor[i] + specColor[i] for i in range(3)]
        elif intercept.obj.material.type == TRANSPARENT:
            isOutside = ml.twoVecDot(rayDirection, intercept.normal) < 0
            factor = 0.001
            bias = [elemento * factor for elemento in intercept.normal]
            
            factor = -1
            negativeRayDirection = [elemento * factor for elemento in rayDirection]
            reflectRay = reflect(intercept.normal, negativeRayDirection)
            reflectOrigin = ml.twoVecSum(intercept.point, bias) if isOutside else ml.twoVecSubstraction(intercept.point, bias)
            reflectIntercept = self.rtCastRay(reflectOrigin, reflectRay, None, recursionDepth + 1)
            reflectColor = self.rtRayColor(reflectIntercept, reflectRay, recursionDepth + 1)

            for light in self.lights:
                if light.type != "AMBIENT":
                    shadowDirection = None
                    if light.type == "DIRECTIONAL":
                        shadowDirection = [i * -1 for i in light.direction]
                    if light.type == "POINT":
                        lightDirection = ml.twoVecSubstraction(light.position, intercept.point)
                        shadowDirection = ml.vecNorm(lightDirection)

                    shadowIntersect = self.rtCastRay(intercept.point, shadowDirection, intercept.obj)

                    if shadowIntersect is None:
                        specColor = light.getSpecularColor(intercept, self.cameraPosition)
                        specularLightColor = [specularLightColor[i] + specColor[i] for i in range(3)]

            if not totalInternalReflection(intercept.normal, rayDirection, 1.0, intercept.obj.material.ior):
                refractRay = refract(intercept.normal, rayDirection, 1.0, intercept.obj.material.ior)
                refractOrigin = ml.twoVecSubstraction(intercept.point, bias) if isOutside else ml.twoVecSum(intercept.point, bias)
                refractIntercept = self.rtCastRay(refractOrigin, refractRay, None, recursionDepth + 1)
                refractColor = self.rtRayColor(refractIntercept, refractRay, recursionDepth + 1)

                kr, kt = fresnel(intercept.normal, rayDirection, 1.0, intercept.obj.material.ior)
                reflectColor = ml.valVecMultiply(kr, reflectColor)
                refractColor = ml.valVecMultiply(kt, refractColor)

        lightColor = [ambientLightColor[i] + diffuseLightColor[i] +
                      specularLightColor[i] + reflectColor[i] + refractColor[i]
                      for i in range(3)]
        finalColor = [surfaceColor[i] * lightColor[i] for i in range(3)]
        finalColor = [min(1, i) for i in finalColor]
        return finalColor

    def rtRender(self):
        for x in range(self.vpX, self.vpX + self.vpWidth + 1):
            for y in range(self.vpY, self.vpY + self.vpHeight + 1):
                if (0 <= x < self.width) and (0 <= y < self.height):
                    pX = 2 * ((x + 0.5 - self.vpX) / self.vpWidth) - 1
                    pY = 2 * ((y + 0.5 - self.vpY) / self.vpHeight) - 1

                    pX *= self.rightEdge
                    pY *= self.topEdge

                    direction = (pX, pY, -self.nearPlane)
                    direction = ml.vecNorm(direction)

                    intercept = self.rtCastRay(self.cameraPosition, direction)
                    finalColor = self.rtRayColor(intercept, direction)

                    if finalColor is not None:
                        self.rtPoint(x, y, finalColor)
                    pygame.display.flip()
