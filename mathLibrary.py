'''
 * Nombre: matrix.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 16.07.2023 
              Modificado el 31.07.2023
 '''

def nMatProduct(matArray):
    result = [[1,0,0,0],
             [0,1,0,0],
             [0,0,1,0],
             [0,0,0,1]]
    
    for mat in matArray:
        result = twoMatProduct(result, mat)
    
    return result

def twoMatProduct(A, B):
    result = [[0,0,0,0],
           [0,0,0,0],
           [0,0,0,0],
           [0,0,0,0]]
    
    for x in range(4):
        for y in range(4):
            for i in range(4):
                result[x][y] += A[x][i] * B[i][y]
                
    return result

def vecMatProduct(M, V):
    result = [0 for _ in range(len(M))]
    
    for i in range(len(M)):
        for j in range(len(V)):
            result[i] += M[i][j] * V[j]
    
    return result

def getBarycentricCoordinates(A, B, C, P):
    pcbArea = (B[1] - C[1]) * (P[0] - C[0]) + (C[0] - B[0]) * (P[1] - C[1])
    acpArea = (C[1] - A[1]) * (P[0] - C[0]) + (A[0] - C[0]) * (P[1] - C[1])
    abcArea = (B[1] - C[1]) * (A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1])
    
    try:
        u = pcbArea / abcArea
        v = acpArea / abcArea
        w = 1 - u - v
        return u, v, w
    except:
        return -1,-1,-1
