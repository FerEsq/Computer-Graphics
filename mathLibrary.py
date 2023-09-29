'''
 * Nombre: mathLibrary.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 16.07.2023 
              Modificado el 29.09.2023
 '''

from math import isclose, sqrt

def nMatProduct(matArray):
    result = [[1,0,0,0],
              [0,1,0,0],
              [0,0,1,0],
              [0,0,0,1]]
    
    for mat in matArray:
        result = twoMatProduct(result, mat)
    
    return result

def twoMatProduct(A, B):
    result = [[0 for row in range(4)] for col in range(4)]
    
    for x in range(4):
        for y in range(4):
            for i in range(4):
                result[x][y] += A[x][i] * B[i][y]
                
    return result

def vecMatProduct(M, V):
    result = [0 for row in range(len(M))]
    
    for i in range(len(M)):
        for j in range(len(V)):
            result[i] += M[i][j] * V[j]
    
    return result

def barycentricCoords(A, B, C, P):
    areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
                  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

    areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

    areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

    areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))
    if areaABC == 0:
        return -1,-1,-1

    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC

    if 0<=u<=1 and 0<=v<=1 and 0<=w<=1 and isclose(u+v+w, 1.0):
        return u, v, w
    else:
        return -1,-1,-1

def twoVecSubstraction(V1, V2): #Replace for: np.subtract(V1, V2)
    result = [x - y for x, y in zip(V1, V2)]
    return result

def vecNorm(V): #Replace for: V / np.linalg.norm(V)
    norm = sqrt(sum([x * x for x in V]))
    result = [x / norm for x in V]
    return result

def vecNormSimple(V): #Replace for: np.linalg.norm(V)
    result = sqrt(sum([x * x for x in V]))
    return result

def twoVecCross(V1, V2):
    if len(V1) != len(V2):
        print("Los vectores deben tener la misma cantidad de componentes")
    
    x1, y1, z1 = V1
    x2, y2, z2 = V2
    
    rx = y1 * z2 - z1 * y2
    ry = z1 * x2 - x1 * z2
    rz = x1 * y2 - y1 * x2

    result = (rx, ry, rz)
    return result

def matInverse(M): #Replace for: np.linalg.inv(M)
    n = len(M)
    result = [[1,0,0,0],
              [0,1,0,0],
              [0,0,1,0],
              [0,0,0,1]]
    
    for i in range(n):
        pivot = M[i][i]
        for j in range(n):
            M[i][j] /= pivot
            result[i][j] /= pivot

        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(n):
                    M[k][j] -= factor * M[i][j]
                    result[k][j] -= factor * result[i][j]
    
    return result

def twoVecDot(V1, V2): #Replace for: np.dot(V1, V2)
    if len(V1) != 3 or len(V2) != 3:
        raise ValueError("Los vectores deben tener tres componentes cada uno.")
    
    result = sum(component1 * component2 for component1, component2 in zip(V1, V2))
    
    return result

def twoVecSum(V1, V2): #Replace for: np.add(V1, V2)
    if len(V1) != len(V2):
        raise ValueError("Los vectores deben tener la misma longitud")
    
    result = [x + y for x, y in zip(V1, V2)]
    return result

def twoVecMultiply(V1, V2): #Replace for: np.multiply(V1, V2)    
    result = [x * y for x, y in zip(V1, V2)]
    return result

def valVecMultiply(val, V): #Replace for: np.multiply(val, V2)
    result = [x * val for x in V]
    return result