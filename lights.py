import numpy as np

class Light(object):
  def __init__(self, intensity = 1, color = (1,1,1), ligthType = "None"):
    self.intensity = intensity
    self.color = color
    self.ligthType = ligthType

  def getColor(self):
        return [self.color[0] * self.intensity,
                self.color[1] * self.intensity,
                self.color[2] * self.intensity]

  def getDiffuseColor(self, intercept):
      return None

  def getSpecularColor(self, intercept, viewPosition):
      return None

class AmbientLight(Light):
  def __init__(self, intensity = 1, color = (1,1,1)):
    super().__init__(intensity, color, "Ambient")

def reflect(normal, direction):
    reflectValue = (2 * np.dot(normal, direction) * normal - direction)
    return reflectValue / np.linalg.norm(reflectValue)

class DirectionalLight(Light):
    def __init__(self, direction=(0, 1, 0), intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "Directional")
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
        super().__init__(intensity, color, "Point")
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