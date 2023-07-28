'''
 * Nombre: gl.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Iniciado el 20.07.2023 
              Finalizado el 26.07.2023
 '''

import struct
from collections import namedtuple

V2 = namedtuple('Point2', ['x', 'y'])

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

class Renderer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.glClearColor(0,0,0)
        self.glClear()
        self.glColor(1,1,1)

    def glClearColor(self, r, g, b):
        self.clearColor = color(r,g,b)

    def glColor(self, r, g, b):
        self.currColor = color(r,g,b)

    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)]
                       for x in range(self.width)]
        
    def glPoint(self, x, y, clr = None):
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y]=clr or self.currColor

    def glTriangle(self, v0, v1, v2, clr = None):
        self.glLine(v0,v1,clr or self.currColor)
        self.glLine(v1,v2,clr or self.currColor)
        self.glLine(v2,v0,clr or self.currColor)

    def glPolygon (self, vArray, clr = None):
        for i in range(len(vArray)):
            if (i != len(vArray)-1):
                self.glLine(vArray[i], vArray[i+1], clr or self.currColor)
            else:
                self.glLine(vArray[i], vArray[0], clr or self.currColor)
    
    # Función creada mediante la asistencia de la IA "chatGPT"
    def glFill(self, vArray, clr = None):
        insideBox = [[vArray[0][0],vArray[0][1]],[vArray[0][0],vArray[0][1]]]
        for v in vArray:
            if v[0] < insideBox[0][0]:
                insideBox[0][0] = v[0]

            elif v[0] > insideBox[1][0]:
                insideBox[1][0] = v[0]

            if v[1] < insideBox[0][1]:
                insideBox[0][1] = v[1]

            elif v[1] > insideBox[1][1]:
                insideBox[1][1] = v[1]
        
        for x in range(insideBox[0][0], insideBox[1][0]):
            for y in range(insideBox[0][1], insideBox[1][1]):
                n = len(vArray)
                insidePoint = False
                j = n - 1

                for i in range(n):
                    xi, yi = vArray[i]
                    xj, yj = vArray[j]
                    if yi < y and yj >= y or yj < y and yi >= y:
                        if xi + (y - yi) / (yj - yi) * (xj - xi) < x:
                            insidePoint = not insidePoint
                    j = i
    
                if insidePoint:
                    self.glPoint(x, y, clr)

    def glLine(self, v0, v1, clr = None):
        x0=int(v0.x)
        x1=int(v1.x)
        y0=int(v0.y)
        y1=int(v1.y)

        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y0)
            return
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1-y0)
        dx = abs(x1-x0)

        offset = 0
        limit = 0.5
        m = dy/dx
        y = y0

        for x in range(x0, x1+1):
            if steep:
                self.glPoint(y,x, clr or self.currColor)
            else:
                self.glPoint(x,y, clr or self.currColor)

            offset += m

            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1

                limit += 1
        
    def glFinish(self, filename):
        with open(filename, "wb") as file:
            #Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height)*3))
            file.write(dword(0))
            file.write(dword(14 + 40))
            
            #Infoheader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword((self.width * self.height)*3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            
            #Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
        
        print("\nBMP creado con éxito!")
