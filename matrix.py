'''
 * Nombre: matrix.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 16.07.2023 
 '''

def multiplication(A, B):
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
