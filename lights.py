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
  def __init__(self, direction = (0,-1,0), intensity = 1, color = (1,1,1)):
    super().__init__(intensity, color, "Directional")
    self.direction = direction

  def getDiffuseColor(self, interecpt):
    dir = [(i * -1) for i in self.direction]

    intensity = np.dot(interecpt.normal, dir) *  self.intensity
    intensity = max(0, min(1, intensity))

    diffuseColor = [(i * intensity) for i in self.color]

    return diffuseColor
  
  def getSpecularColor(self, intercept, viewPosition):
    direction = [i * -1 for i in self.direction]

    reflectDirection = reflect(intercept.normal, direction)

    viewDirection = np.subtract(viewPosition, intercept.point)
    viewDirection = viewDirection / np.linalg.norm(viewDirection)

    intensity = max(0, min(1, np.dot(reflectDirection, viewDirection))) ** intercept.obj.material.spec
    intensity *= self.intensity

    return [i * intensity for i in self.color]