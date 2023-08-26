import numpy as np
import mathLib as ml

def vertexShader(vertex, **kwargs):  
    # El Vertex Shader se lleva a cabo por cada v�rtice

    modelMatrix = kwargs["modelMatrix"]
    viewMatrix= kwargs["viewMatrix"]
    projectionMatrix= kwargs["projectionMatrix"]
    vpMatrix= kwargs["vpMatrix"]

    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]

    vt1= ml.multi4x4matrix(vpMatrix, projectionMatrix)
    vt2= ml.multi4x4matrix(vt1, viewMatrix)
    vt3= ml.multi4x4matrix(vt2, modelMatrix)
    vt = ml.multimatrixvec(vt3, vt)

    vt = [vt[0]/vt[3],
          vt[1]/vt[3],
          vt[2]/vt[3]]

    return vt

def fragmentShader(**kwargs):
    # El Fragment Shader se lleva a cabo por cada pixel
    # que se renderizar� en la pantalla.

    texture= kwargs["texture"]
    tA, tB, tC= kwargs["texCoords"]
    u, v, w= kwargs["bCoords"]

    b= 1.0
    g= 1.0
    r= 1.0

    if texture != None:
        tU= u * tA[0] + v * tB[0] + w * tC[0]
        tV= u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    return r, g, b

def flatShader(**kwargs):
    dLight = kwargs["dLight"]
    nA, nB, nC= kwargs["normals"]
    texture= kwargs["texture"]
    tA, tB, tC= kwargs["texCoords"]
    u, v, w= kwargs["bCoords"]

    b= 1.0
    g= 1.0
    r= 1.0

    if texture != None:
        tU= u * tA[0] + v * tB[0] + w * tC[0]
        tV= u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal= [u * nA[0] + v * nB[0] + w * nC[0],
             u * nA[1] + v * nB[1] + w * nC[1],
             u * nA[2] + v * nB[2] + w * nC[2]]

    dLightNeg=(-dLight[0], -dLight[1], -dLight[2])
    intensity= ml.dot_product(normal, dLightNeg)
    
    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b

    else:
        return [0,0,0]
    
def gouradShader(**kwargs):
    texture= kwargs["texture"]
    tA, tB, tC= kwargs["texCoords"]
    nA, nB, nC= kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w= kwargs["bCoords"]
    modelMatrix= kwargs["modelMatrix"]

    b= 1.0
    g= 1.0
    r= 1.0

    if texture != None:
        tU= u * tA[0] + v * tB[0] + w * tC[0]
        tV= u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal= [u * nA[0] + v * nB[0] + w * nC[0],
             u * nA[1] + v * nB[1] + w * nC[1],
             u * nA[2] + v * nB[2] + w * nC[2],
             0]
    
    normal= ml.multimatrixvec(modelMatrix, normal)
    normal=[normal[0], normal[1], normal[2]]
    normal= ml.normalize_vector(normal)
    
    dLightNeg=(-dLight[0], -dLight[1], -dLight[2])
    dLightNeg= ml.normalize_vector(dLightNeg)
    intensity= ml.dot_product(normal, dLightNeg)
    
    b *= intensity
    g *= intensity
    r *= intensity

    b = min(b, 1.0)
    g = min(g, 1.0)
    r = min(r, 1.0)

    if intensity > 0:
        return r, g, b

    else:
        return [0,0,0]
    
def toonShader(**kwargs):
    texture= kwargs["texture"]
    tA, tB, tC= kwargs["texCoords"]
    nA, nB, nC= kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w= kwargs["bCoords"]

    b= 1.0
    g= 1.0
    r= 1.0

    if texture != None:
        tU= u * tA[0] + v * tB[0] + w * tC[0]
        tV= u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal= [u * nA[0] + v * nB[0] + w * nC[0],
            u * nA[1] + v * nB[1] + w * nC[1],
            u * nA[2] + v * nB[2] + w * nC[2]]
    
    dLight= (-dLight[0], -dLight[1], -dLight[2])
    intensity= ml.dot_product(normal, dLight)

    if intensity <= 0.25:
        intensity= 0.2

    elif intensity <=0.5:
        intensity= 0.45

    elif intensity <=0.75:
        intensity=0.7

    elif intensity<=1.0:
        intensity= 0.95
    
    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b

    else:
        return [0,0,0]
    
def redShader(**kwargs):
    texture= kwargs["texture"]
    tA, tB, tC= kwargs["texCoords"]
    nA, nB, nC= kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w= kwargs["bCoords"]

    b= 1.0
    g= 1.0
    r= 1.0

    if texture != None:
        tU= u * tA[0] + v * tB[0] + w * tC[0]
        tV= u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal= [u * nA[0] + v * nB[0] + w * nC[0],
             u * nA[1] + v * nB[1] + w * nC[1],
             u * nA[2] + v * nB[2] + w * nC[2]]
    
    dLight= (-dLight[0], -dLight[1], -dLight[2])
    intensity= ml.dot_product(normal, dLight)
    
    b *= intensity
    g *= intensity
    r *= intensity

    red= (1,0,0)

    b *= red[2]
    g *= red[1]
    r *= red[0]

    if intensity > 0:
        return r, g, b

    else:
        return [0,0,0]

def emissionShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    u, v, w= kwargs["bCoords"]

    b = 0.0
    g = 0.0
    r = 0.0

    if texture is not None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b += textureColor[2]
        g += textureColor[1]
        r += textureColor[0]

    # Simulate emission by adding a constant value
    emission_color = [0.2, 0.4, 0.8]  # Emission color
    b += emission_color[2]
    g += emission_color[1]
    r += emission_color[0]

    b = min(b, 1.0)
    g = min(g, 1.0)
    r = min(r, 1.0)

    return r, g, b

def celShader(**kwargs):
    nA, nB, nC = kwargs["normals"]
    dLight = kwargs["dLight"]
    bCoords = kwargs["bCoords"]

    # Calcular la intensidad del brillo especular
    specularIntensity = ml.dot_product(nA, dLight)

    # Definir el número de divisiones para los tonos de sombra y luz
    numDivisions = 150

    # Calcular el rango de intensidad para cada división
    intensityRange = 1.0 / numDivisions

    # Calcular el valor de intensidad en función de la división
    intensityLevel = int(specularIntensity / intensityRange)

    # Asignar colores planos para tonos de sombra y luz
    shadowColor = (1, 0.502, 1)
    lightColor = (0.85, 0.0, 0.147)

    # Seleccionar el color correspondiente según el nivel de intensidad
    if intensityLevel % 2 == 0:
        color = shadowColor
    else:
        color = lightColor

    return color

def snakeShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w = kwargs["bCoords"]
    modelMatrix = kwargs["modelMatrix"]

    b = 1.0
    g = 1.0
    r = 1.0

    # Define las coordenadas del punto actual
    x, y = u, v

    # Define el umbral para la detección de líneas diagonales
    threshold = 0.3

    # Verifica si el punto está en una línea diagonal
    if abs(x - y) < threshold:
        return 0, 0, 0  # Devuelve color transparente

    if texture is not None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]

        textureColor = texture.getColor(tU, tV)
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2],
              0]

    normal = ml.multimatrixvec(modelMatrix, normal)
    normal = [normal[0], normal[1], normal[2]]
    normal= ml.normalize_vector(normal)

    dLightNeg = (-dLight[0], -dLight[1], -dLight[2])
    dLightNeg= ml.normalize_vector(dLightNeg)
    intensity = ml.dot_product(normal, dLightNeg)

    gradient_intensity = (u + v) / 2

    b *= intensity * gradient_intensity
    g *= intensity * gradient_intensity
    r *= intensity * gradient_intensity

    b = min(b, 1.0)
    g = min(g, 1.0)
    r = min(r, 1.0)

    if intensity > 0:
        return r, g, b
    else:
        return [0, 0, 0]
