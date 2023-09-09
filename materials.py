class Material:
    def __init__(self, diffuse=(1, 1, 1), albedo=(1, 0, 0), spec=1.0):
        self.diffuse = diffuse
        self.albedo = albedo
        self.spec = spec

def brick():
    return Material(diffuse=(1, 0.3, 0.2), albedo=(0.2, 0.8, 0.0), spec=8)

def grass():
    return Material(diffuse=(0.2, 0.8, 0.2), albedo=(0.2, 0.8, 0.0), spec=32)

def water():
    return Material(diffuse=(0.2, 0.2, 0.8), albedo=(0.2, 0.8, 0.0), spec=256)