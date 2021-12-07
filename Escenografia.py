import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es
import numpy as np
import sys
import csv

import random
from OpenGL.GL import *
from obj_reader import *

# FUNCIONES PARA LAS PLATAFORMAS

# Archivo csv y funciones con el
v = sys.argv[1] # Esto es para llamarlo por cmd

def listaD(v):   # es lo mismo que la lista c anterior 
    with open(v) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        d = []
        for row in csv_reader:
            for i in row:
                if i != "x":
                    j = int(i)
                else:
                    j = i
                d.append(j)

    return d

D = listaD(v) # lista que contiene cual plataforma se dibuja (1), cual no(0) y cual desaparece (x)

def rows(v):
    with open(v) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
    return line_count * 5

r = rows(v) #retorna el numero de filas * 5

def listaA(r):
    rows = r
    a = []
    x = [-14, -7, 0, 7, 14]
    while not rows==0:
        a.append(x[0])
        a.append(x[1])
        a.append(x[2])
        a.append(x[3])
        a.append(x[4])
        rows -=5
    return a

listaA = listaA(r) # lista que contiene la posicion en x de las plataformas

def listaB(r):
    rows = r               
    b = []
    y = [3, -3, 3, -3, 3]
    while not rows==0:
        b.append(y[0])
        b.append(y[1])
        b.append(y[2])
        b.append(y[3])
        b.append(y[4])
        rows -= 5
    return b

listaB = listaB(r) # lista que contiene la posicion en y de las plataformas

def listaC(r):
    rows = r                  
    c = []
    z = 5
    while not rows==0:
        c.append(z)
        c.append(z)
        c.append(z)
        c.append(z)
        c.append(z)
        rows -= 5
        z += 5
    return c

listaC = listaC(r) # lista que contiene la posicion en Z de las plataformas

def listaABCD(d,lista): # Funcion que sirve para dibujar solo las plataformas que corresponden
    L = []
    n = len(d)
    for i in range(n):
        if d[i] != 0:
            L.append(lista[i])
    return L   

A = listaABCD(D,listaA)   
B = listaABCD(D,listaB)
C = listaABCD(D,listaC)

def listaUNO(d,lista): # Funcion que sirve para saber las plataformas que se pueden escalar
    L = []
    n = len(d)
    for i in range(n):
        if d[i] == 1:
            L.append(lista[i])
    return L

unoA = listaUNO(D,listaA)
unoB = listaUNO(D,listaB)
unoC = listaUNO(D,listaC)

    
def listaEQUIS(d,lista): # Funcion que sirve para saber las plataformas que desapareceran si se tocan
    L = []
    n = len(d)
    for i in range(n):
        if d[i] == "x":
            L.append(lista[i])
    return L 

equisA = listaEQUIS(D,listaA)
equisB = listaEQUIS(D,listaB)
equisC = listaEQUIS(D,listaC)



#CLASES
        
class Plataforma(object):

    def __init__(self, posX=0.0, posY=0.0, posZ=0.0):
        gpuPlataforma = es.toGPUShape(bs.createTextureCube("Bloque.png"), GL_REPEAT, GL_NEAREST)
      
        plataforma = sg.SceneGraphNode('plataforma')
        plataforma.transform = tr.scale(5, 3, 0.5)
        plataforma.childs += [gpuPlataforma]

        plataforma_tr = sg.SceneGraphNode('plataformaTR')
        plataforma_tr.childs += [plataforma]

        self.pos_x = posX  
        self.pos_y = posY
        self.pos_z = posZ
        self.model = plataforma_tr

    def draw(self, pipeline):
        self.model.transform = tr.translate(self.pos_x, self.pos_y, self.pos_z)
        sg.drawSceneGraphNode(self.model, pipeline, "model")


class PlataformaCreator(object):
    def __init__(self):
        self.plataformas = []

    def create_plataforma(self, a=A, b=B, c=C):
        n = len(a)
        for i in range(n):
            self.plataformas.append(Plataforma(A[i],B[i],C[i]))

    def draw(self, pipeline):
        for k in self.plataformas:
            k.draw(pipeline)

    def eliminar(self, a, b, c):
        for k in self.plataformas:  # Recorro todas las plataformas
            if k.pos_x == a and  k.pos_y == b and k.pos_z == c:
                self.plataformas.remove(k)

class Roquita(object):
    def __init__(self):
        gpuRoquita = es.toGPUShape(bs.createTextureCube("Bloque2.png"), GL_REPEAT, GL_NEAREST)
        
        roquita = sg.SceneGraphNode('roquita')
        roquita.transform = tr.uniformScale(0.8)
        roquita.childs += [gpuRoquita]

        roquita_tr = sg.SceneGraphNode('roquitaTR')
        roquita_tr.childs += [roquita]

        self.pos_x = random.choice([-14, -7, 0, 7, 14])  
        self.pos_y = 20
        self.pos_z = random.choice([6, 12, 18, 24, 30])
        self.model = roquita_tr
        
    def draw(self, pipeline):
        self.model.transform = tr.translate(self.pos_x, self.pos_y, self.pos_z)
        sg.drawSceneGraphNode(self.model, pipeline, "model")

    def posJ(self, j):
        self.pos_y -= j   

class RoquitaCreator(object):
    def __init__(self):
        self.roquita = []
        self.golpe = False

    def create_roquita(self):
        if len(self.roquita) >= 10:  # No puede haber un máximo de 10 roquitas en pantalla
            return
        if random.random() < 0.01:
            self.roquita.append(Roquita())

    def posJ(self, j):
        for k in self.roquita:
            k.posJ(j)

    def draw(self, pipeline):
        for k in self.roquita:
            k.draw(pipeline)
    
    def eliminar(self, a ,b ,c , fondo):      
        for k in self.roquita:  # Recorro todas las roquitas
            if (a - 0.7 <= k.pos_x <= a + 0.7 and k.pos_y <= b and c-1 < k.pos_z < c + 1):
                self.roquita.remove(k)
                self.golpe = True

            if k.pos_y <= fondo:
                self.roquita.remove(k)
                
class Banana(object):
    def __init__(self):
        gpuBanana = es.toGPUShape(shape = readOBJ("BananaChiquita.obj", (0.980,0.776,0.192)))
        self.x = 0.0 
        self.y = 0.0
        self.z = 0.0
        self.banana = gpuBanana

    def draw(self, pipeline, projection, view, win):
        glUseProgram(pipeline.shaderProgram)
        bananaTransformer = tr.matmul([tr.translate(self.x, self.y, self.z),    
            tr.uniformScale(0.5),
            tr.rotationX(np.pi/2)])
        
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, bananaTransformer)
        if win == False:
            pipeline.drawShape(self.banana)


    

        
        

    
        
        

        

    
    
    
