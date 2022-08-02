def CrossOp(M1, M2):
    matrix = []
    for i in range(len(M1)):
        matrix.append([])
        for j in range(len(M2[0])):
            matrix[i].append(0)

    for i in range(len(M1)):
        for j in range(len(M2[0])):
            for k in range(len(M1[0])):
                matrix[i][j] += M1[i][k] * M2[k][j]
    return matrix


def IdentityOp(a):
    matrix = []
    for i in range(0, a):
        matrix.append([])
        for j in range(0, a):
            if (i == j):
                matrix[i].append(1)
            else:
                matrix[i].append(0)
    return matrix

def MV(M, V):
    matriz = []
    for fila in M:
        res = 0
        for col in range(len(fila)):
            res += (fila[col]*V[col])
        matriz.append(res)
    return matriz

