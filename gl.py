'''
 * Nombre: gl.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 16.07.2023 
              Modificado el 14.08.2023
 '''

import struct
import mathLibrary as ml
from math import sin, cos, tan, radians
from obj import Obj
from texture import Texture

POINTS = 0
LINES = 1
TRIANGLES = 2
QUADS = 3

def char(c):
    #1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h', w)

def dword(d):
    #4 bytes
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([ int(b * 255),
                   int(g * 255),
                   int(r * 255) ])

class Model(object):
    def __init__(self, filename, translate=(0,0,0), rotate=(0,0,0), scale=(1,1,1)):
        model = Obj(filename)

        self.faces = model.faces
        self.vertices = model.vertices
        self.texcoords = model.texcoords
        self.normals = model.normals

        self.translate = translate
        self.rotate = rotate
        self.scale = scale

    def LoadTexture(self, textureName):
        self.texture = Texture(textureName)

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

        self.vertexBuffer=[ ]
        self.activeTexture = None

        self.glViewport(0,0,self.width,self.height)
        self.glCameraMatrix()
        self.glProjectionMatrix()

        self.directionalLight = (0,0,-1)
        

    def glAddVertices(self, vertices):
        for vert in vertices:
            self.vertexBuffer.append(vert)

    def glPrimitiveAssembly(self,tVerts, tTexCoords, tNormals):
        primitives = [ ]
        if self.primitiveType == TRIANGLES:
            for i in range(0,len(tVerts), 3):
                
                #Verts
                verts =[]
                verts.append(tVerts[i])
                verts.append(tVerts[i+1])
                verts.append(tVerts[i+2])
                #TexCoords
                texCoords = []
                texCoords.append(tTexCoords[i])
                texCoords.append(tTexCoords[i+1])
                texCoords.append(tTexCoords[i+2])
                #Normals
                normals = []
                normals.append(tNormals[i])
                normals.append(tNormals[i+1])
                normals.append(tNormals[i+2])

                triangle = [verts, texCoords, normals]

                primitives.append(triangle)
        
        return primitives
    
    def glBackgroundTexture(self, filename):
        self.background = Texture(filename)

    def clearBackground(self):
        self.glClear()

        if self.background:
            for x in range(self.vpX, self.vpX+self.vpWidth+1):
                for y in range(self.vpY, self.vpY+self.vpHeight+1):
                    u=(x-self.vpX)/self.vpWidth
                    v=(y-self.vpY)/self.vpHeight
                    texColor = self.background.getColor(u, v)
                    if texColor:
                        self.glPoint(x,y,color(texColor[0],texColor[1],texColor[2]))

    def glClearColor(self, r, g, b):
        self.clearColor = color(r,g,b)

    def glColor(self, r, g, b):
        self.currColor = color(r,g,b)

    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)]
                       for x in range(self.width)]
        
        self.zbuffer = [[float('inf') for y in range(self.height)]
                       for x in range(self.width)]
        
    def glPoint(self, x, y, clr = None):
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y]=clr or self.currColor

    def glTriangle(self, verts, texCoords, normals):
        A= verts[0]
        B= verts[1]
        C= verts[2]
        minX = round(min(A[0], B[0], C[0]))
        maxX = round(max(A[0], B[0], C[0]))
        minY = round(min(A[1], B[1], C[1]))
        maxY = round(max(A[1], B[1], C[1]))

        colorA = (1,0,0)
        colorB = (0,1,0)
        colorC = (0,0,1)

        for x in range(minX, maxX+1):
            for y in range(minY, maxY+1):

                if (0 <= x < self.width) and (0 <= y < self.height):

                    P=(x,y)
                    bCoords=ml.barycentricCoords(A,B,C,P)
                    u,v,w = bCoords

                    if 0<=u<=1 and 0<=v<=1 and 0<=w<=1:

                        z = u * A[2] + v * B[2] + w * C[2]
                        
                        if z < self.zbuffer[x][y]:

                            self.zbuffer[x][y] = z
                            
                            if self.fragmentShader != None:

                                colorP = self.fragmentShader(texture = self.activeTexture,
                                                             texCoords = texCoords,
                                                             normals = normals,
                                                             dLight = self.directionalLight,
                                                             bCoords = bCoords)
                                
                                self.glPoint(x,y,color(colorP[0],colorP[1],colorP[2]))
                            else:
                                self.glPoint(x,y,colorP)


    def glViewport(self, x,y,width,height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height

        self.vpMatrix = [[self.vpWidth/2,0,0,self.vpX + self.vpWidth/2],
                         [0,self.vpHeight/2,0,self.vpY + self.vpHeight/2],
                         [0,0,0.5,0.5],
                         [0,0,0,1]]

    def glCameraMatrix(self, translate=(0,0,0), rotate=(0,0,0)):
        self.camMatrix = self.glModelMatrix(translate, rotate)
        self.viewMatrix = ml.matInverse(self.camMatrix)

    def glLookAt(self, camPos = (0,0,0), eyePos=(0,0,0)):
        forward = ml.vecNorm(ml.twoVecSubstraction(camPos, eyePos))
        right = ml.vecNorm(ml.twoVecCross((0,1,0), forward))
        up = ml.vecNorm(ml.twoVecCross(forward, right))

        self.camMatrix = [[right[0],up[0],forward[0],camPos[0]],
                          [right[1],up[1],forward[1],camPos[1]],
                          [right[2],up[2],forward[2],camPos[2]],
                          [0,0,0,1]]
        
        self.viewMatrix = ml.matInverse(self.camMatrix)

    def glProjectionMatrix(self, fov=60, n=0.1, f=1000):
        aspectRatio = self.vpWidth/self.vpHeight
        t = tan(radians(fov)/2) * n
        r = t * aspectRatio
        self.projectionMatrix = [[n/r,0,0,0],
                                 [0,n/t,0,0],
                                 [0,0,-(f+n)/(f-n),-(2*f*n)/(f-n)],
                                 [0,0,-1,0]]

    def glModelMatrix(self, translate=(0,0,0), rotate=(0,0,0), scale=(1,1,1)):
        
        translateMat = [[1,0,0,translate[0]],
                        [0,1,0,translate[1]],
                        [0,0,1,translate[2]],
                        [0,0,0,1]]
        
        scaleMat = [[scale[0],0,0,0],
                    [0,scale[1],0,0],
                    [0,0,scale[2],0],
                    [0,0,0,1]]
        
        rx = [[1,0,0,0],
            [0,cos(radians(rotate[0])),-sin(radians(rotate[0])),0],
            [0,sin(radians(rotate[0])),cos(radians(rotate[0])),0],
            [0,0,0,1]]
        
        ry = [[cos(radians(rotate[1])),0,sin(radians(rotate[1])),0],
            [0,1,0,0],
            [-sin(radians(rotate[1])),0,cos(radians(rotate[1])),0],
            [0,0,0,1]]
        
        rz = [[cos(radians(rotate[2])),-sin(radians(rotate[2])),0,0],
            [sin(radians(rotate[2])),cos(radians(rotate[2])),0,0],
            [0,0,1,0],
            [0,0,0,1]]
        
        rotationMat = ml.nMatProduct([rx,ry,rz])
        return ml.nMatProduct([translateMat, rotationMat, scaleMat])

    def glLine(self, v0, v1, clr=None):

        x0=int(v0[0])
        x1=int(v1[0])
        y0=int(v0[1])
        y1=int(v1[1])

        #si el punto 0 es igual al punto 1 solo dibujar un punto
        if x0==x1 and y0==y1:
            self.glPoint(x0,y0)
            return
        
        dy = abs(y1-y0)
        dx = abs(x1-x0)

        steep = dy > dx

        # si la linea tiene pendiente > 1 
        # se intercambian las x por y para poder
        # dibujar la linea de manera vertical en vez de horizontal 
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        
        # Si el punto inicial en X es mayor que el punto final en X
        # intercambiamos los puntos para siempre dibujar de
        # izquierda a derecha
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1-y0)
        dx = abs(x1-x0)

        offset=0
        limit=0.5
        m = dy/dx
        y=y0

        for x in range(x0, x1+1):
            if steep:
                #Dibujar de manera vertical
                self.glPoint(y,x, clr or self.currColor)
            else:
                #Dibujar de manera horizontal
                self.glPoint(x,y, clr or self.currColor)

            offset += m

            if offset >= limit:
                if y0<y1:
                    y+=1
                else:
                    y-=1
                
                limit +=1

    def glLoadModel(self, filename, textureName, translate=(0,0,0),rotate=(0,0,0) ,scale=(1,1,1)):

        model = Model(filename,translate,rotate,scale)
        model.LoadTexture(textureName)
       
        self.objects.append(model)

    def glRender(self):
        transformedVerts = []
        texCoords = []
        normals = []

        for model in self.objects:

            self.activeTexture = model.texture
            mMatrix = self.glModelMatrix(model.translate, model.rotate ,model.scale)

            for face in model.faces:
                vertCount = len(face)
                v0=model.vertices[face[0][0] -1]
                v1=model.vertices[face[1][0] -1]
                v2=model.vertices[face[2][0] -1]
                if vertCount == 4:
                    v3=model.vertices[face[3][0] -1]

                if self.vertexShader:
                    v0=self.vertexShader(v0, 
                                         modelMatrix=mMatrix,
                                         viewMatrix=self.viewMatrix,
                                         projectionMatrix=self.projectionMatrix,
                                         vpMatrix=self.vpMatrix)
                    
                    v1=self.vertexShader(v1, 
                                         modelMatrix=mMatrix,
                                         viewMatrix=self.viewMatrix,
                                         projectionMatrix=self.projectionMatrix,
                                         vpMatrix=self.vpMatrix)
                    
                    v2=self.vertexShader(v2, 
                                         modelMatrix=mMatrix,
                                         viewMatrix=self.viewMatrix,
                                         projectionMatrix=self.projectionMatrix,
                                         vpMatrix=self.vpMatrix)
                    if vertCount == 4:
                        v3=self.vertexShader(v3, 
                                         modelMatrix=mMatrix,
                                         viewMatrix=self.viewMatrix,
                                         projectionMatrix=self.projectionMatrix,
                                         vpMatrix=self.vpMatrix)
                
                transformedVerts.append(v0)
                transformedVerts.append(v1)
                transformedVerts.append(v2)

                if vertCount == 4:
                    transformedVerts.append(v0)
                    transformedVerts.append(v2)
                    transformedVerts.append(v3)

                vt0=model.texcoords[face[0][1] -1]
                vt1=model.texcoords[face[1][1] -1]
                vt2=model.texcoords[face[2][1] -1]

                if vertCount == 4:
                    vt3=model.texcoords[face[3][1] -1]

                texCoords.append(vt0)
                texCoords.append(vt1)
                texCoords.append(vt2)

                if vertCount == 4:
                    texCoords.append(vt0)
                    texCoords.append(vt2)
                    texCoords.append(vt3)
                
                #normales del modelo
                vn0=model.normals[face[0][2] -1]
                vn1=model.normals[face[1][2] -1]
                vn2=model.normals[face[2][2] -1]

                if vertCount == 4:
                    vn3=model.normals[face[3][2] -1]

                normals.append(vn0)
                normals.append(vn1)
                normals.append(vn2)

                if vertCount == 4:
                    normals.append(vn0)
                    normals.append(vn2)
                    normals.append(vn3)

        primitives = self.glPrimitiveAssembly(transformedVerts, texCoords, normals)

        for prim in primitives:
            if self.primitiveType == TRIANGLES:
                self.glTriangle(prim[0], prim[1], prim[2])

    def glFinish(self, filename):
        with open(filename, "wb") as file:
            #Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14+40+(self.width*self.height * 3)))
            file.write(dword(0))
            file.write(dword(14+40))

            #InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword((self.width*self.height * 3)))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #ColorTable
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])

            print("\nBMP creado con éxito!")