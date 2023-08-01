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

def twoMatProduct(A, B):
    rA = len(A) #Filas de A
    cA = len(A[0]) #Columnas de A
    rB = len(B) #Filas de B
    cB = len(B[0]) #Columnas de B

    result = [[0 for row in range(cB)] for col in range(rA)]

    for s in range(rA):
        for j in range(cB):
            for k in range(cA):
                result[s][j] += A[s][k] * B[k][j]

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
