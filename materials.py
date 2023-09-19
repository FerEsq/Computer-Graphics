class Material:
    def __init__(self, diffuse=(1, 1, 1), spec=1.0, Ks=0.0):
        self.diffuse = diffuse
        self.spec = spec
        self.Ks = Ks

def brick():
    return Material(diffuse=(1.0, 0.3, 0.2), spec=8, Ks=0.01)

def grass():
    return Material(diffuse=(0.2, 0.8, 0.2), spec=32, Ks=0.1)

def water():
    return Material(diffuse=(0.2, 0.2, 0.8), spec=256, Ks=0.5)

def snow():
    return Material(diffuse=(1.0, 0.9, 0.8), spec=8, Ks=0.01)

def stone():
    return Material(diffuse=(0.0, 0.0, 0.0), spec=8, Ks=0.01)

def carrot():
    return Material(diffuse=(1.0, 0.2, 0.1), spec=8, Ks=0.01)

def plastic():
    return Material(diffuse=(1.0, 1.0, 1.0), spec=8, Ks=0.01)