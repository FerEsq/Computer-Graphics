'''
 * Nombre: rt.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 20.09.2023
 '''

from math import pi, tan
import mathLibrary as ml

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

    def rtCastRay(self, origin, direction, sceneObject=None):
        depth = float("inf")
        hit = None

        for obj in self.scene:
            if obj is not sceneObject:
                intercept = obj.ray_intersect(origin, direction)
                if intercept is not None:
                    if intercept.distance < depth:
                        depth = intercept.distance
                        hit = intercept

        return hit

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
                    if intercept is not None:
                        surfaceColor = intercept.obj.material.diffuse
                        ambientLightColor = [0, 0, 0]
                        diffuseLightColor = [0, 0, 0]
                        specularLightColor = [0, 0, 0]

                        for light in self.lights:
                            if light.ligthType == "Ambient":
                                color = light.getColor()
                                ambientLightColor = [ambientLightColor[i] + color[i] for i in range(3)]
                            else:
                                shadowDirection = None
                                if light.ligthType == "Directional":
                                    shadowDirection = [i * -1 for i in light.direction]
                                if light.ligthType == "Point":
                                    lightDirection = ml.twoVecSubstraction(light.position, intercept.point)
                                    shadowDirection = ml.vecNorm(lightDirection)

                                shadowIntersect = self.rtCastRay(intercept.point, shadowDirection, intercept.obj)

                                if shadowIntersect is None:
                                    diffColor = light.getDiffuseColor(intercept)
                                    diffuseLightColor = [diffuseLightColor[i] + diffColor[i] for i in range(3)]

                                    specColor = light.getSpecularColor(intercept, self.cameraPosition)
                                    specularLightColor = [specularLightColor[i] + specColor[i] for i in range(3)]

                        lightColor = [ambientLightColor[i] + diffuseLightColor[i] + specularLightColor[i]
                                      for i in range(3)]

                        finalColor = [surfaceColor[i] * lightColor[i] for i in range(3)]
                        finalColor = [min(1, i) for i in finalColor]

                        self.rtPoint(x, y, finalColor)