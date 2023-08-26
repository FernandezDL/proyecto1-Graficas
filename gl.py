import numpy as np
from math import pi, sin, cos, tan
from support import *
from obj import Obj
from texture import Texture
import mathLib as ml

POINTS = 0
LINES = 1
TRIANGLES = 2
QUADS = 3

class Model(object):
    def __init__(self, filename, translate = (0,0,0), rotate = (0,0,0), scale = (1,1,1)):
        model = Obj(filename)

        self.vertices = model.vertices
        self.texcoords = model.texcoords
        self.normals = model.normals
        self.faces = model.faces

        self.translate = translate
        self.rotate = rotate
        self.scale = scale

        self.texture= None
        
        self.SetShaders(None, None)

    def LoadTexture(self, textureName):
        self.texture = Texture(textureName)

    def SetShaders(self, vertexShader, fragmentShader):
        self.vertexShader= vertexShader
        self.fragmentShader= fragmentShader

class Renderer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.glClearColor(0.5,0.5,0.5)
        self.glClear()

        self.glColor(1,1,1)

        self.objects = []

        self.vertexShader = None
        self.fragmentShader = None

        self.primitiveType = TRIANGLES

        self.activeTexture = None

        self.activeModelMatrix= None
        self.forward= (0,0,0)
        self.camPos= (0,0,0)

        self.glViewport(0, 0, self.width, self.height)

        self.glCamMatrix()       
        self.glProjectionMatrix() 

        self.directionalLight = (1,0, -0.5)

    def glBackgroundTexture(self, filename):
        self.background= Texture(filename)

    def glClearBackground(self):
        self.glClear()

        if self.background:
            for x in range(self.vpX, self.vpX + self.vpWidth + 1):
                for y in range(self.vpY, self.vpY + self.vpHeight + 1):
                    u= (x - self.vpX) / self.vpWidth
                    v= (y - self.vpY) / self.vpHeight

                    texColor= self.background.getColor(u, v)

                    if texColor:
                        self.glPoint(x,y, color(texColor[0], texColor[1], texColor[2]))

    def glClearColor(self, r, g, b):
        # Establecer el color de fondo
        self.clearColor = color(r,g,b)

    def glColor(self, r, g, b):
        # Establecer el color default de rederizaci�n.
        self.currColor = color(r,g,b)

    def glClear(self):
        # Se crea la tabla de pixeles del tama�o width*height.
        # Se le asigna a cada pixel el color de fondo.
        self.pixels = [[self.clearColor for y in range(self.height)]
                       for x in range(self.width)]

        # Se crea otra tabla para el Z Buffer. Aqu� se guarda la profundidad
        # de cada pixel, con el valor m�ximo de profundidad inicial.
        self.zbuffer = [[float('inf') for y in range(self.height)]
                       for x in range(self.width)]

    def glPoint(self, x, y, clr = None):
        # Si el valor de X y Y est� dentro del ancho y alto del framebuffer,
        # dibujar el punto en la posici�n (x,y) del FrameBuffer.
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y] = clr or self.currColor

    def glTriangle(self, verts, texCoords, normals):
        # Rederizaci�n de un tri�ngulo usando coordenadas baric�ntricas.
        # Se reciben los vertices A, B y C y las coordenadas de
        # textura vtA, vtB y vtC

        A= verts[0]
        B= verts[1]
        C= verts[2]

        # Bounding box
        minX = round(min(A[0], B[0], C[0]))
        maxX = round(max(A[0], B[0], C[0]))
        minY = round(min(A[1], B[1], C[1]))
        maxY = round(max(A[1], B[1], C[1]))

        # Para cada pixel dentro del bounding box
        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                # Si el pixel est� dentro del FrameBuffer
                if (0 <= x < self.width) and (0 <= y < self.height):

                    P = (x,y)
                    bCoords = ml.barycentricCoords(A, B, C, P)

                    # Si se obtienen coordenadas baric�ntricas v�lidas para este punto
                    if bCoords != None:

                        u, v, w = bCoords

                        # Se calcula el valor Z para este punto usando las coordenadas baric�ntricas
                        z = u * A[2] + v * B[2] + w * C[2]

                        # Si el valor de Z para este punto es menor que el valor guardado en el Z Buffer
                        if z < self.zbuffer[x][y]:
                            
                            # Guardamos este valor de Z en el Z Buffer
                            self.zbuffer[x][y] = z

                            # Si contamos un Fragment Shader, obtener el color de ah�.
                            # Sino, usar el color preestablecido.
                            if self.fragmentShader != None:
                                # Mandar los par�metros necesarios al shader
                                colorP = self.fragmentShader(texture = self.activeTexture,
                                                             texCoords= texCoords,
                                                             normals= normals,
                                                             dLight= self.directionalLight,
                                                             bCoords= bCoords,
                                                             camMatrix= self.camMatrix,
                                                             modelMatrix= self.activeModelMatrix,
                                                             dView= self.forward,
                                                             camPos= self.camPos)

                                self.glPoint(x, y, color(colorP[0], colorP[1], colorP[2]))
                                
                            else:
                                self.glPoint(x, y)

    def glPrimitiveAssembly(self, tVerts, tTexCoords, tnormals):
        # Esta funci�n construye las primitivas de acuerdo con la
        # opci�n de primitiva actual. De momento solo hay para tri�ngulos
        primitives = [ ]

        if self.primitiveType == TRIANGLES:
            for i in range(0, len(tVerts), 3):
                # Un tri�ngulo contar� con las posiciones de sus v�rtices y
                # y sus UVs, seguidos uno tras otro.

                # Verts
                verts=[]

                verts.append( tVerts[i] )
                verts.append( tVerts[i + 1] )
                verts.append( tVerts[i + 2] )

                # TexCoords
                texCoords=[]

                texCoords.append( tTexCoords[i] )
                texCoords.append( tTexCoords[i + 1] )
                texCoords.append( tTexCoords[i + 2] )

                #Normals
                normals=[]

                normals.append(tnormals[i])
                normals.append(tnormals[i + 1])
                normals.append(tnormals[i + 2])

                triangle=[verts, texCoords, normals]

                primitives.append(triangle)

        return primitives

    def glViewport(self, x, y, width, height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height

        self.vpMatrix= [[self.vpWidth/2,0,0, self.vpX + self.vpWidth/2],
                        [0,self.vpHeight/2,0, self.vpY + self.vpHeight/2],
                        [0,0,0.5,0.5],
                        [0,0,0,1]]

    def glCamMatrix(self, translate=(0,0,0), rotate=(0,0,0)):
        self.camMatrix= self.glModelMatrix(translate, rotate)

        self.viewMatrix= ml.matrix_inverse(self.camMatrix)

    def glLookAt(self, camPos= (0,0,0), eyePos=(0,0,0)):
        worldUp= (0,1,0)

        self.camPos= camPos
        self.forward= ml.vector_subtraction(self.camPos, eyePos)
        self.forward= ml.normalize_vector(self.forward)

        right = ml.cross_product(worldUp, self.forward)
        right= ml.normalize_vector(right)

        up = ml.cross_product(self.forward, right)
        up= ml.normalize_vector(up)

        self.camMatrix= [[right[0],up[0],self.forward[0],self.camPos[0]],
                         [right[1],up[1],self.forward[1],self.camPos[1]],
                         [right[2],up[2],self.forward[2],self.camPos[2]],
                         [0,0,0,1]]
        
        self.viewMatrix = ml.matrix_inverse(self.camMatrix)

    def glProjectionMatrix(self, fov=60, n=0.1, f=1000):
        aspectRatio= self.vpWidth/self.vpHeight

        t= tan(((fov * pi)/180) / 2) * n
        r= t * aspectRatio

        self.projectionMatrix= [[n/r,0,0,0],
                                [0,n/t,0,0],
                                [0,0,-(f+n)/(f-n),-2*f*n/(f-n)],
                                [0,0,-1,0]]

    def glModelMatrix(self, translate = (0,0,0), rotate = (0,0,0), scale = (1,1,1)):
        # Matriz de traslaci�n
        translation = [[1,0,0,translate[0]],
                        [0,1,0,translate[1]],
                        [0,0,1,translate[2]],
                        [0,0,0,1]]

        # Matrix de rotaci�n
        rotMat = self.glRotationMatrix(rotate[0], rotate[1], rotate[2])

        # Matriz de escala
        scaleMat = [[scale[0],0,0,0],
                    [0,scale[1],0,0],
                    [0,0,scale[2],0],
                    [0,0,0,1]]
        
        multMatrix= ml.multi4x4matrix(translation, rotMat)
        result= ml.multi4x4matrix(multMatrix, scaleMat)

        # Se multiplican las tres para obtener la matriz del objeto final
        return result

    def glRotationMatrix(self, pitch = 0, yaw = 0, roll = 0):
        # Convertir a radianes
        pitch *= pi/180
        yaw *= pi/180
        roll *= pi/180

        # Creamos la matriz de rotaci�n para cada eje.
        pitchMat = [[1,0,0,0],
                    [0,cos(pitch),-sin(pitch),0],
                    [0,sin(pitch),cos(pitch),0],
                    [0,0,0,1]]

        yawMat = [[cos(yaw),0,sin(yaw),0],
                  [0,1,0,0],
                  [-sin(yaw),0,cos(yaw),0],
                  [0,0,0,1]]

        rollMat = [[cos(roll),-sin(roll),0,0],
                   [sin(roll),cos(roll),0,0],
                   [0,0,1,0],
                   [0,0,0,1]]

        # Se multiplican las tres matrices para obtener la matriz de rotaci�n final
        mulMatrix= ml.multi4x4matrix(pitchMat, yawMat)
        result= ml.multi4x4matrix(mulMatrix, rollMat)
        return result

    def glLine(self, v0, v1, clr = None):
        # Bresenham line algorith
        # y = m*x + b

        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])

        # Si el punto 0 es igual al punto 1, solo dibujar un punto
        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y0)
            return

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        # Si la linea tiene pendiente mayor a 1 o menor a -1
        # intercambiamos las x por las y, y se dibuja la linea
        # de manera vertical en vez de horizontal
        if steep:
            x0, y0 = y0,x0
            x1, y1 = y1,x1

        # Si el punto inicial en X es mayor que el punto final en X,
        # intercambiamos los puntos para siempre dibujar de 
        # izquierda a derecha
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)


        offset = 0
        limit = 0.5
        m = dy/dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                # Dibujar de manera vertical
                self.glPoint(y, x, clr or self.currColor)
            else:
                # Dibujar de manera horizontal
                self.glPoint(x, y, clr or self.currColor)

            offset += m

            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1

                limit += 1

    def glAddModel(self, model):
        # Se agrega el modelo al listado de objetos 
        self.objects.append( model )

    def glRender(self):
        # Esta funci�n est� encargada de renderizar todo a la tabla de pixeles
        transformedVerts = []
        texCoords = []
        normals= []

        # Para cada modelo en nuestro listado de objetos
        for model in self.objects:
            transformedVerts = []
            texCoords = []
            normals= []

            self.vertexShader= model.vertexShader
            self.fragmentShader= model.fragmentShader

            # Establecemos la textura y la matriz del modelo
            self.activeTexture = model.texture
            self.activeModelMatrix = self.glModelMatrix(model.translate, model.rotate, model.scale)

            # Para cada cara del modelo
            for face in model.faces:
                # Revisamos cuantos v�rtices tiene esta cara. Si tiene cuatro
                # v�rtices, hay que crear un segundo tri�ngulo por cara
                vertCount = len(face)

                # Obtenemos los v�rtices de la cara actual.
                v0 = model.vertices[ face[0][0] - 1]
                v1 = model.vertices[ face[1][0] - 1]
                v2 = model.vertices[ face[2][0] - 1]
                if vertCount == 4:
                    v3 = model.vertices[ face[3][0] - 1]

                # Si contamos con un Vertex Shader, se manda cada v�rtice 
                # al mismo para transformarlos. Recordar pasar las matrices
                # necesarias para usarlas dentro del shader.
                if self.vertexShader:
                    v0 = self.vertexShader(v0, 
                                           modelMatrix = self.activeModelMatrix,
                                           viewMatrix= self.viewMatrix,
                                           projectionMatrix= self.projectionMatrix,
                                           vpMatrix= self.vpMatrix)
                    v1 = self.vertexShader(v1, 
                                           modelMatrix = self.activeModelMatrix,
                                           viewMatrix= self.viewMatrix,
                                           projectionMatrix= self.projectionMatrix,
                                           vpMatrix= self.vpMatrix)
                    v2 = self.vertexShader(v2, 
                                           modelMatrix = self.activeModelMatrix,
                                           viewMatrix= self.viewMatrix,
                                           projectionMatrix= self.projectionMatrix,
                                           vpMatrix= self.vpMatrix)
                    if vertCount == 4:
                        v3 = self.vertexShader(v3,
                                               modelMatrix = self.activeModelMatrix,
                                               viewMatrix= self.viewMatrix,
                                               projectionMatrix= self.projectionMatrix,
                                               vpMatrix= self.vpMatrix)
                
                # Agregar cada v�rtice transformado al listado de v�rtices.
                transformedVerts.append(v0)
                transformedVerts.append(v1)
                transformedVerts.append(v2)
                if vertCount == 4:
                    transformedVerts.append(v0)
                    transformedVerts.append(v2)
                    transformedVerts.append(v3)

                # Obtenemos las coordenadas de textura de la cara actual
                vt0 = model.texcoords[face[0][1] - 1]
                vt1 = model.texcoords[face[1][1] - 1]
                vt2 = model.texcoords[face[2][1] - 1]
                if vertCount == 4:
                    vt3 = model.texcoords[face[3][1] - 1]

                # Agregamos las coordenadas de textura al listado de coordenadas de textura.
                texCoords.append(vt0)
                texCoords.append(vt1)
                texCoords.append(vt2)
                if vertCount == 4:
                    texCoords.append(vt0)
                    texCoords.append(vt2)
                    texCoords.append(vt3)

                # Obtenemos las normales de la cara actual
                v0 = model.normals[face[0][2] - 1]
                v1 = model.normals[face[1][2] - 1]
                v2 = model.normals[face[2][2] - 1]
                if vertCount == 4:
                    v3 = model.normals[face[3][2] - 1]

                normals.append(v0)
                normals.append(v1)
                normals.append(v2)
                if vertCount == 4:
                    normals.append(v0)
                    normals.append(v2)
                    normals.append(v3)

            # Creamos las primitivas
            primitives = self.glPrimitiveAssembly(transformedVerts, texCoords, normals)       

            # Para cada primitiva
            for prim in primitives:
                if self.primitiveType ==  TRIANGLES:
                    self.glTriangle(prim[0], prim[1], prim[2])

    def glFinish(self, filename):
        # Esta funci�n crea una textura BMP de 24 bits y la rellena 
        # con la tabla de pixeles. Este ser� nuestro FrameBuffer final.

        with open(filename, "wb") as file:
            # Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])