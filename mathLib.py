from math import isclose

def barycentricCoords(A, B, C, P):
    # Se saca el �rea de los subtri�ngulos y del tri�ngulo
    # mayor usando el Shoelace Theorem, una f�rmula que permite
    # sacar el �rea de un pol�gono de cualquier cantidad de v�rtices.

    areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
                  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

    areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

    areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

    areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

    # Si el �rea del tri�ngulo es 0, retornar nada para
    # prevenir divisi�n por 0.
    if areaABC == 0:
        return None

    # Determinar las coordenadas baric�ntricas dividiendo el 
    # �rea de cada subtri�ngulo por el �rea del tri�ngulo mayor.
    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC

    # Si cada coordenada est� entre 0 a 1 y la suma de las tres
    # es igual a 1, entonces son v�lidas.
    if 0<=u<=1 and 0<=v<=1 and 0<=w<=1 and isclose(u+v+w, 1.0):
        return (u, v, w)
    else:
        return None

#Multiplicación de dos matrices de 4*4
def multi4x4matrix(matrix1, matrix2):
    resultado = [
        [0.0,0.0,0.0,0.0],
        [0.0,0.0,0.0,0.0],
        [0.0,0.0,0.0,0.0],
        [0.0,0.0,0.0,0.0]]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                resultado[i][j] += matrix1[i][k] * matrix2[k][j]
    return resultado

#Multiplicación de una matriz con un vector 
def multimatrixvec(matrix, vect):
    resultado = [0.0, 0.0, 0.0, 0.0]

    for i in range(4):
        for j in range(4):
            resultado[i] += matrix[i][j] * vect[j]

    return resultado

#Producto cruz de dos vectores
def cross_product(vector_a, vector_b):
    if len(vector_a) != 3 or len(vector_b) != 3:
        raise ValueError("Los vectores tienen que ser de tres elementos")
    
    result = [0, 0, 0]
    
    result[0] = vector_a[1] * vector_b[2] - vector_a[2] * vector_b[1]
    result[1] = vector_a[2] * vector_b[0] - vector_a[0] * vector_b[2]
    result[2] = vector_a[0] * vector_b[1] - vector_a[1] * vector_b[0]
    
    return result

#Producto punto de dos vectores
def dot_product(vector_a, vector_b):
    if len(vector_a) != len(vector_b):
        raise ValueError("Los vectores tienen que ser del mismo tamaño")
    
    result = 0
    for i in range(len(vector_a)):
        result += vector_a[i] * vector_b[i]
    
    return result

#Transpuesta de una matriz
def transpose_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    transposed = [[0 for _ in range(rows)] for _ in range(cols)]
    
    for i in range(rows):
        for j in range(cols):
            transposed[j][i] = matrix[i][j]
    
    return transposed

def matrix_minor(matrix, row, col):
    return [row[:col] + row[col+1:] for row in (matrix[:row] + matrix[row+1:])]

#Determinante de una matriz
def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    
    det = 0
    for col in range(len(matrix)):
        det += ((-1) ** col) * matrix[0][col] * determinant(matrix_minor(matrix, 0, col))
    
    return det

#Matriz inverza
def matrix_inverse(matrix):
    det = determinant(matrix)
    if det == 0:
        raise ValueError("El determinante es 0, no se puede calcular la inversa.")
    
    rows = len(matrix)
    cols = len(matrix[0])
    adjugate = [[0 for _ in range(rows)] for _ in range(cols)]
    
    for i in range(rows):
        for j in range(cols):
            minor = matrix_minor(matrix, i, j)
            cofactor = ((-1) ** (i + j)) * determinant(minor)
            adjugate[j][i] = cofactor / det
    
    return adjugate

#Maagnitud de un vector
def vector_magnitude(vector):
    return sum(component ** 2 for component in vector) ** 0.5

#Normalización de un vector
def normalize_vector(vector):
    magnitude = vector_magnitude(vector)
    normalized = [component / magnitude for component in vector]
    return normalized

#Resta de dos vectores
def vector_subtraction(vector_a, vector_b):
    if len(vector_a) != len(vector_b):
        raise ValueError("Los vectores tienen que ser del mismo tamaño")
    
    result = [a - b for a, b in zip(vector_a, vector_b)]
    return result

def vector_addition(vector_a, vector_b):
    if len(vector_a) != len(vector_b):
        raise ValueError("Los vectores tienen que ser del mismo tamaño")
    
    result = [a + b for a, b in zip(vector_a, vector_b)]
    return result

def reflect(incident, normal):
    dot_product_result = 2 * dot_product(incident, normal)
    reflected = [incident[i] - dot_product_result * normal[i] for i in range(len(incident))]
    return reflected

def interpolate_colors(color1, color2, t):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = int((1 - t) * r1 + t * r2)
    g = int((1 - t) * g1 + t * g2)
    b = int((1 - t) * b1 + t * b2)
    return r, g, b

def scalar_multiply(scalar, vector):
    result = [scalar * component for component in vector]
    return result

def reflect_vector(vector, normal):
    dotProduct = 2.0 * dot_product(vector, normal)
    reflection = vector_subtraction(vector, scalar_multiply(dotProduct, normal))
    return reflection