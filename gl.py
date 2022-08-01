import struct
from collections import namedtuple
import numpy as np
import random
import glmath
from math import cos, sin, pi
from obj import Obj

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])


def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))


def word(w):
    # 2 bytes
    return struct.pack('=h', w)


def dword(d):
    # 4 bytes
    return struct.pack('=i', d)


def color(b, g, r):
    return bytes(
        [int(b * 255),
         int(g * 255),
         int(r * 255)]
    )


def baryCoords(A, B, C, P):

    # || PB X PC ||
    areaPBC = (B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)
    areaPAC = (C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)
    areaABC = (B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)

    #PBC / ABC
    u = areaPBC / areaABC

    #PAC / ABC
    v = areaPAC / areaABC

    # 1 - U - V
    w = 1 - u - v
    return u, v, w


class Renderer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.clearColor = color(0, 0, 0)
        self.currColor = color(1, 1, 1)

        self.glViewport(0, 0, self.width, self.height)

        self.glClear()

    def glViewport(self, posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpW = width
        self.vpH = height

    def glClear(self):  # List comprehension: Asigna color a cada posicion
        self.pixels = [[self.clearColor for y in range(
            self.height)] for x in range(self.width)]

        self.zbuffer = [[float('inf') for y in range(
            self.height)] for x in range(self.width)]

    def glClearColor(self, r, g, b):
        self.clearColor = color(r, g, b)

    def glClearViewport(self, clr=None):
        for x in range(self.vpX, self.vpX + self.vpW):
            for y in range(self.vpY, self.vpY + self.vpH):
                self.glPoint(x, y, clr)

    def glColor(self, r, g, b):
        self.currColor = color(r, g, b)

    def glPoint(self, x, y, clr=None):
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y] = clr or self.currColor

    def glPointvp(self, ndcx, ndcy, clr=None):
        x = int((ndcx + 1) * (self.vpW / 2) + self.vpX)
        y = int((ndcy + 1) * (self.vpH / 2) + self.vpY)

        self.glPoint(x, y, clr)

    def glLine(self, v0, v1, clr=None):
        # Bresenham line algorithm
        # y = m * x + b
        x0 = int(v0.x)
        x1 = int(v1.x)
        y0 = int(v0.y)
        y1 = int(v1.y)

        # Si el punto0 es igual al punto 1, dibujar solamente un punto
        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y0, clr)
            return

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        # Si la linea tiene pendiente mayor a 1 o menor a -1
        # intercambio las x por las y, y se dibuja la linea
        # de manera vertical
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # Si el punto inicial X es mayor que el punto final X,
        # intercambio los puntos para siempre dibujar de
        # izquierda a derecha
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        limit = 0.5
        m = dy / dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                # Dibujar de manera vertical
                self.glPoint(y, x, clr)
            else:
                # Dibujar de manera horizontal
                self.glPoint(x, y, clr)

            offset += m

            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1

                limit += 1

    def GenPolygon(self, polygon, clr=None):
        for i in range(len(polygon)):
            self.glLine(polygon[i], polygon[(i + 1) % len(polygon)], clr)

    def glTriangle2(self, A, B, C, clr=None):
        # Baricentric coordenates

        # colorA = (1,0,0)
        # colorB = (0,1,0)
        # colorC = (0,0,1)

        # bounding box
        minX = round(min(A.x, B.x, C.x))
        maxX = round(max(A.x, B.x, C.x))
        minY = round(min(A.y, B.y, C.y))
        maxY = round(max(A.y, B.y, C.y))

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                u, v, w = baryCoords(A, B, C, V2(x, y))

                if 0 <= u <= 1 and 0 <= v <= 1 and 0 <= w <= 1:
                    # colorP = color(
                    #                 colorA[0]*u + colorB[0] * v + colorC[0] * w,
                    #                 colorA[1]*u + colorB[1] * v + colorC[1] * w,
                    #                 colorA[2]*u + colorB[2] * v + colorC[2] * w)

                    # z = A.z * u + B.z * v + C.z * w
                    # if z < self.zbuffer[x][y]:
                    #     self.zbuffer[x][y] = z
                    # newColor = color(z/1000, z-1000, z/1000)
                    self.glPoint(x, y, clr)

    def glTriangle(self, A, B, C, clr=None):

        # ScanLine Algorithm
        if A.y < B.y:
            A, B = B, A
        if A.y < C.y:
            A, C = C, A
        if B.y < C.y:
            B, C = C, B

        self.glLine(A, B, clr)
        self.glLine(B, C, clr)
        self.glLine(C, A, clr)

        def flatBottom(vA, vB, vC):
            try:
                mBA = (vB.x - vA.x) / (vB.y - vA.y)
                mCA = (vC.x - vA.x) / (vC.y - vA.y)
            except:
                pass
            else:
                x0 = vB.x
                x1 = vC.x
                for y in range(int(vB.y), int(vA.y)):
                    self.glLine(V2(x0, y), V2(x1, y), clr)
                    x0 += mBA
                    x1 += mCA

        def flatTop(vA, vB, vC):
            try:
                mCA = (vC.x - vA.x) / (vC.y - vA.y)
                mCB = (vC.x - vB.x) / (vC.y - vB.y)
            except:
                pass
            else:
                x0 = vA.x
                x1 = vB.x
                for y in range(int(vA.y), int(vC.y), -1):
                    self.glLine(V2(x0, y), V2(x1, y), clr)
                    x0 -= mCA
                    x1 -= mCB

        if B.y == C.y:
            # Parte plana abajo
            flatBottom(A, B, C)
        elif A.y == B.y:
            # Parte plana arriba
            flatTop(A, B, C)
        else:
            # Dibujo ambos tipos de triangulos
            # Teorema de intercepto
            D = V2(A.x + ((B.y - A.y) / (C.y - A.y)) * (C.x - A.x), B.y)
            flatBottom(A, B, D)
            flatTop(B, D, C)

    def glFill(self, poligono, clr=None):
        for y in range(self.height):
            for x in range(self.width):
                last = len(poligono) - 1
                check = False

                # Este algoritmo verifica los puntos que no estan dentro del poligono
                for i in range(len(poligono)):
                    if (poligono[i][1] < y and poligono[last][1] >= y) or (poligono[last][1] < y and poligono[i][1] >= y):
                        if poligono[i][0] + (y - poligono[i][1]) / (poligono[last][1] - poligono[i][1]) * (poligono[last][0] - poligono[i][0]) < x:
                            check = not check
                    last = i
                if check:
                    self.glPoint(x, y, clr)

    def glCreateObjectMatrix(self, translate=V3(0, 0, 0), rotate=V3(0, 0, 0), scale=V3(1, 1, 1)):

        translation = ([[1, 0, 0, translate.x],
                        [0, 1, 0, translate.y],
                        [0, 0, 1, translate.z],
                        [0, 0, 0, 1]])

        rotation = glmath.IdentityOp(4)

        scaleMat = ([[scale.x, 0, 0, 0],
                     [0, scale.y, 0, 0],
                     [0, 0, scale.z, 0],
                     [0, 0, 0, 1]])

        product = glmath.CrossOp(glmath.CrossOp(
            translation, rotation), scaleMat)
        return product

    def glTransform(self, vertex, matrix):

        v = V4(vertex[0], vertex[1], vertex[2], 1)
        vt = np.matrix(matrix) @ v
        vt = vt.tolist()[0]
        vf = V3(vt[0] / vt[3],
                vt[1] / vt[3],
                vt[2] / vt[3])

        return vf

    def glLoadModel(self, filename, translate=V3(0, 0, 0), rotate=V3(0, 0, 0), scale=V3(1, 1, 1)):
        model = Obj(filename)
        modelMatrix = self.glCreateObjectMatrix(translate, rotate, scale)

        for face in model.faces:
            vertCount = len(face)

            v0 = model.vertices[face[0][0] - 1]
            v1 = model.vertices[face[1][0] - 1]
            v2 = model.vertices[face[2][0] - 1]

            v0 = self.glTransform(v0, modelMatrix)
            v1 = self.glTransform(v1, modelMatrix)
            v2 = self.glTransform(v2, modelMatrix)

            self.glTriangle2(v0, v1, v2, color(random.random(),
                                               random.random(),
                                               random.random()))

    def glFinish(self, filename):
        with open(filename, "wb") as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            # tama;o del archivo, cantidad de bytes que va a usar en memoria
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            # El byte donde empieza la informacion de pixeles
            file.write(dword(14 + 40))

            # InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))  # Width
            file.write(dword(self.height))  # Height
            file.write(word(1))  # Planes, solo ocupa 2 bytes
            file.write(word(24))  # Bits Per Pixel
            file.write(dword(0))  # Compression
            # Tama;o de la imagen
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
