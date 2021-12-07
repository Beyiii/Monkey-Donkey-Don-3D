# Con este codigo el monito es capás de trepar plataformas cuyas posiciones están dado
# por un archivo csv

import glfw
import OpenGL.GL.shaders
import lighting_shaders as ls

from Escenografia import *


# Clase que almacena el control de la aplicación (control aplication)
class Controller:
    def __init__(self):        
        self.monitoRotaA = False
        self.direccionA = False
        
        self.monitoRotaD = False
        self.direccionD = False
        
        self.monitoAvanza = False

        self.upOn = False

        self.camaraB = False
        self.camaraN = False
        self.camaraM = False
        
        self.monitoX = 0
        self.monitoY = 0
        self.monitoZ = 0.04

# Controlador global como comunicación con la función de devolución de llamada (callback function)
controller = Controller()

# Función que sirve para colocar el funcionamiento de las teclas a ocupar
def on_key(window, key, scancode, action, mods):

    global controller

    if action == glfw.PRESS:

        if key == glfw.KEY_A:
            controller.monitoRotaA = True
            controller.direccionA = True

        elif key == glfw.KEY_D:
            controller.monitoRotaD = True
            controller.direccionD = True

        elif key == glfw.KEY_W:
            controller.monitoAvanza = True

        elif key == glfw.KEY_SPACE:
            controller.upOn = True

        elif key == glfw.KEY_B:
            controller.camaraB = True
            controller.camaraN = False
            controller.camaraM = False

        elif key == glfw.KEY_N:
            controller.camaraN = True
            controller.camaraB = False
            controller.camaraM = False

        elif key == glfw.KEY_M:
            controller.camaraM = True
            controller.camaraB = False
            controller.camaraN = False

        elif key == glfw.KEY_ESCAPE:
            glfw.terminate()
            sys.exit()
            
        else:
            print('Unknown key')
            
    elif (action ==glfw.RELEASE):
        if key == glfw.KEY_W:
            controller.monitoAvanza = False


# Funciones para poder leer los objetos 
def readFaceVertex(faceDescription):

    aux = faceDescription.split('/')

    assert len(aux[0]), "Vertex index has not been defined."

    faceVertex = [int(aux[0]), None, None]

    assert len(aux) == 3, "Only faces where its vertices require 3 indices are defined."

    if len(aux[1]) != 0:
        faceVertex[1] = int(aux[1])

    if len(aux[2]) != 0:
        faceVertex[2] = int(aux[2])

    return faceVertex



def readOBJ(filename, color):

    vertices = []
    normals = []
    textCoords= []
    faces = []

    with open(filename, 'r') as file:
        for line in file.readlines():
            aux = line.strip().split(' ')
            
            if aux[0] == 'v':
                vertices += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'vn':
                normals += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'vt':
                assert len(aux[1:]) == 2, "Texture coordinates with different than 2 dimensions are not supported"
                textCoords += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'f':
                N = len(aux)                
                faces += [[readFaceVertex(faceVertex) for faceVertex in aux[1:4]]]
                for i in range(3, N-1):
                    faces += [[readFaceVertex(faceVertex) for faceVertex in [aux[i], aux[i+1], aux[1]]]]

        vertexData = []
        indices = []
        index = 0

        # Per previous construction, each face is a triangle
        for face in faces:

            # Checking each of the triangle vertices
            for i in range(0,3):
                vertex = vertices[face[i][0]-1]
                normal = normals[face[i][2]-1]

                vertexData += [
                    vertex[0], vertex[1], vertex[2],
                    color[0], color[1], color[2],
                    normal[0], normal[1], normal[2]
                ]

            # Connecting the 3 vertices to create a triangle
            indices += [index, index + 1, index + 2]
            index += 3        

        return bs.Shape(vertexData, indices)

# Funciones para que el monito pueda chocar con y escalar las plataformas

# True si el monito choca con la plataforma que está arriba (da igual si es 1 o x)
def colision(x, y, z, a=A, b=B, c=C):
    n = len(A)
    for i in range(n):
        if A[i] - 2.5 <= x <= A[i] + 2.5 and B[i] - 1.5 <= y <= B[i] + 1.5 and C[i] > z >= C[i] - 3.0:
            return True

# True si el monito está sobre una plataforma        
def enPlataforma(x, y, z, a=unoA, b=unoB, c=unoC):
    n = len(a)
    for i in range(n):
        if a[i] - 2.5 <= x <= a[i] + 2.5 and b[i] - 1.5 <= y <= b[i] + 1.5 and c[i] + 0.27 < z <= c[i] + 0.36:
            return True

# Para modificar el Z del monito
def MonitoZ(z, c=unoC):
    n = len(c)
    for i in range(n):
        if c[i] + 0.27 < z <= c[i] + 0.36:
            z = c[i]+ 0.29
            return z

# Plataformas
plataformas = PlataformaCreator()

def Desaparecer(x, y, z, a=equisA, b=equisB, c=equisC):
    n = len(a)
    for i in range(n):
        if a[i] - 2.5 <= x <= a[i] + 2.5 and b[i] - 1.5 <= y <= b[i] + 1.5 and c[i] + 0.32 < z <= c[i] + 0.36:
            print('TOCA PLATAFORMA X')
            plataformas.eliminar(a[i],b[i],c[i])
            
# Acá se pone las caracteristicas de la ventana, el nombre, los elementos que habrán, entre otras cosas
if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 650

    window = glfw.create_window(width, height, "Monkey Donkey Don!", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Conexión de la función callback 'on_key' para manejar eventos de teclado
    glfw.set_key_callback(window, on_key)

    # Shaders
    pipeline = ls.SimpleGouraudShaderProgram()
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()
    pipeline_texture = es.SimpleTextureModelViewProjectionShaderProgram()

    # Decir a OpenGL que use nuestro progama de sombreado
    glUseProgram(pipeline.shaderProgram)

    # Configurar el color de la pantalla
    glClearColor(0.419, 0.694, 1.0, 1.0)

    # Para darle la profundidad. Activa lo 3D
    glEnable(GL_DEPTH_TEST)

    # Creando shapes en la memoria de la GPU
    gpuPared = es.toGPUShape(bs.createTextureCube("Fondo.png"), GL_REPEAT, GL_NEAREST)
    gpuPiso = es.toGPUShape(bs.createTextureCube("Pasto.png"), GL_REPEAT, GL_NEAREST)
    gpuMonito = es.toGPUShape(shape = readOBJ("Mono.obj", (0.808,0.769,0.8)))
    gpuMonitoDie = es.toGPUShape(shape = readOBJ("Mono.obj", (1,0,0)))
    gpuHeart = es.toGPUShape(shape = readOBJ("Corazon.obj", (1,0,0)))
    gpuLava = es.toGPUShape(bs.createTextureCube("Lava.png"), GL_REPEAT, GL_NEAREST)

    gpuGameOver = es.toGPUShape(shape = readOBJ("GameOver.obj", (0.808,0.769,0.8)))
    gpuWin = es.toGPUShape(shape = readOBJ("Win.obj", (0.808,0.769,0.8)))
    gpuBanana = es.toGPUShape(shape = readOBJ("BananaChiquita.obj", (0.980,0.776,0.192)))
    
    # Roquitas
    roquitas = RoquitaCreator()

    # CREAR PLATAFORMAS
    plataformas.create_plataforma()

    # BANANA
    banana = Banana()
    
    # Funciones para poder girar la camara alrededor del monito 
    t0 = glfw.get_time()
    camera_theta = -3*np.pi/4
    camera_phi = -3*np.pi/4

    # Funciones por el momento para el movimiento de la camara
    cameraX = 0
    cameraY = 8
    cameraZ = 3

    # camara at
    atX = 0
    atY = 0
    atZ = 1
    
    # camara up
    upX = 0
    upY = 0
    upZ = 1   

    # Rotación en Z de monito por el momento
    MonitoRotation = np.pi

    # Rotación en X de monito por el momento
    MonitoRotationX = np.pi/2
    
    # Rotación en Y de monito por el momento
    MonitoRotationY = 0

    # Booleanos
    bajada = False
    bajadaPlat = False
    sobrePlataforma = False
    lavaOn = False
    perder = False
    subida = True
    gameover = False
    win = False
    ganar = False
    saltarWin = False

    # Variables para animaciones finales
    contarSubida = 0
    contarDieWin = 0

    # Variables para cuando el monito salta
    contarSalto = 0
    vidas = 3

    # Dirección del monito (c/r a él mismo)
    # 1 = norte 
    # 2 = noreste
    # 3 = este
    # 4 = sureste
    # 5 = sur
    # 6 = suroeste
    # 7 = oeste
    # 8 = noroeste
    
    direccion = 1

    # En este ciclo se coloca lo que harán las figuras
    while not glfw.window_should_close(window):
        # Usa GLFW para verificar eventos de entrada/ esto va para todo
        glfw.poll_events()

        
        # Obtener la diferencia de los tiempos de la iteración anterior
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1
                
        # Para el movimiento de la camara
#---------------------------------------- Camara ------------------------------------
        if controller.camaraB == True:
            atX = controller.monitoX 
            atY = controller.monitoY
            atZ = controller.monitoZ 

            cameraX = controller.monitoX
            cameraZ = 5 + controller.monitoZ

            if controller.monitoY <= 2:
                cameraY = 22 + controller.monitoY

            else:
                cameraY
                
        if controller.camaraN == True:
            atX = controller.monitoX 
            atY = controller.monitoY
            atZ = controller.monitoZ 

            cameraZ = 14 + controller.monitoZ

            if controller.monitoX <= 9.8:
                cameraX = 14 + controller.monitoX

            elif controller.monitoY > 9.8:
                cameraX     
        
            elif controller.monitoY <= 7.7:
                cameraY = 14 + controller.monitoY

            elif controller.monitoY > 7.7:
                cameraY
    

        if controller.camaraM == True:
            atX = controller.monitoX 
            atY = controller.monitoY
            atZ = controller.monitoZ 

            cameraZ = 14 + controller.monitoZ
       

            if controller.monitoX >= -9.8:
                cameraX = -14 + controller.monitoX

            elif controller.monitoY < -9.8:
                cameraX     
        
            elif controller.monitoY <= 7.7:
                cameraY = 14 + controller.monitoY

            elif controller.monitoY > 7.7:
                cameraY

#---------------------------------------- Camara ------------------------------------

        viewPos = np.array([cameraX, cameraY, cameraZ])
        
        view = tr.lookAt(
            viewPos,
            np.array([atX,atY,atZ]),
            np.array([upX,upY,upZ])
        )


        # Funciones booleanas
        colition = colision(controller.monitoX, controller.monitoY, controller.monitoZ)         # False
        enPlat = enPlataforma(controller.monitoX, controller.monitoY, controller.monitoZ)  # False

        # Funcion para modificar Z del monito
        monitoZ = MonitoZ(controller.monitoZ)

        # Funcion para eliminar plataformas
        Desaparecer(controller.monitoX, controller.monitoY, controller.monitoZ)


        # Rotación en Z y direccion del monito
        
        if controller.monitoRotaA and not controller.upOn:
            MonitoRotation += np.pi/4
            controller.monitoRotaA = False
            if direccion != 0:
                direccion -= 1
                controller.direccionD = False
            if direccion == 0:
                direccion = 8
                controller.direccionD = False
            
        if controller.monitoRotaD and not controller.upOn:
            MonitoRotation -= np.pi/4
            controller.monitoRotaD = False
    
            if direccion != 9:
                direccion += 1
                controller.direccionD = False
            if direccion == 9:
                direccion = 1
                controller.direccionD = False     

        # Para que el monito AVANCE
        
        if controller.monitoAvanza and not controller.upOn:

            if direccion == 1:
                if controller.monitoY < 23:
                    controller.monitoY += 0.04
                    
                else:
                    controller.monitoY
                    
            if direccion == 2:    
                if controller.monitoY < 23 and controller.monitoX < 23:
                    controller.monitoY += 0.04
                    controller.monitoX += 0.04
                    
                else:
                    controller.monitoY
                    controller.monitoX

            if direccion == 3:
                if controller.monitoX < 23:
                    controller.monitoX += 0.04
                    
                else:
                    controller.monitoX
                
            if direccion == 4:
                if controller.monitoY > -23 and controller.monitoX < 23:
                    controller.monitoY -= 0.04
                    controller.monitoX += 0.04
                    
                else:
                    controller.monitoY
                    controller.monitoX

            if direccion == 5:
                if controller.monitoY > -23:
                    controller.monitoY -= 0.04
                    
                else:
                    controller.monitoY

            if direccion == 6:
                if controller.monitoY > -23 and controller.monitoX > -23:
                    controller.monitoY -= 0.04
                    controller.monitoX -= 0.04
                    
                else:
                    controller.monitoY
                    controller.monitoX

            if direccion == 7:
                if controller.monitoX > -23:
                    controller.monitoX -= 0.04
                    
                else:
                    controller.monitoX

            if direccion == 8:
                if controller.monitoY < 23 and controller.monitoX > -23:
                    controller.monitoY += 0.04
                    controller.monitoX -= 0.04
                    
                else:
                    controller.monitoY
                    controller.monitoX

        # Para que el monito SALTE PARABOLICAMENTE en el PISO
        
        if controller.upOn and not sobrePlataforma:
            if bajada == False:
                controller.monitoZ += 0.04

            if bajada == True:
                controller.monitoZ -= 0.04

            if controller.monitoZ >= 6 or colition == True:
                bajada = True

            if bajada == True and enPlat == True:
               sobrePlataforma = True 
               bajada = False
               controller.monitoZ = monitoZ
               controller.upOn = False

            if controller.monitoZ <= 0.04:
                controller.monitoZ = 0.04
                bajada = False
                controller.upOn = False
                
            if direccion == 1:
                if controller.monitoY < 23:
                    controller.monitoY += 0.03
                    
                else:
                    controller.monitoY
                    
            if direccion == 2:    
                if controller.monitoY < 23 and controller.monitoX < 23:
                    controller.monitoY += 0.03
                    controller.monitoX += 0.03
                    
                else:
                    controller.monitoY
                    controller.monitoX

            if direccion == 3:
                if controller.monitoX < 23:
                    controller.monitoX += 0.03
                    
                else:
                    controller.monitoX
                

            if direccion == 4:
                if controller.monitoY > -23 and controller.monitoX < 23:
                    controller.monitoY -= 0.03
                    controller.monitoX += 0.03
                    
                else:
                    controller.monitoY
                    controller.monitoX

            if direccion == 5:
                if controller.monitoY > -23:
                    controller.monitoY -= 0.03
                    
                else:
                    controller.monitoY

            if direccion == 6:
                if controller.monitoY > -23 and controller.monitoX > -23:
                    controller.monitoY -= 0.03
                    controller.monitoX -= 0.03
                    
                else:
                    controller.monitoY
                    controller.monitoX

            if direccion == 7:
                if controller.monitoX > -23:
                    controller.monitoX -= 0.03
                    
                else:
                    controller.monitoX

            if direccion == 8:
                if controller.monitoY < 23 and controller.monitoX > -23:
                    controller.monitoY += 0.03
                    controller.monitoX -= 0.03
                    
                else:
                    controller.monitoY
                    controller.monitoX

        # SALTO AL GANAR

        if saltarWin:
            controller.upOn = False
            controller.monitoAvanza = False
            
            if bajadaPlat == False:
                contarSalto += 1
                controller.monitoZ += 0.04

            if bajadaPlat == True:
                contarSalto = 0
                controller.monitoZ -= 0.04

            if contarSalto == 50 or colition == True:
                bajadaPlat = True

            if bajadaPlat == True and enPlat == True:
               bajadaPlat = False
               controller.monitoZ = monitoZ
               controller.upOn = False

            if controller.monitoZ <= 0.04:
                controller.monitoZ = 0.04
                bajadaPlat = False
                controller.upOn = False

            if enPlat is not True and contarSalto == 0 and sobrePlataforma == True:
                bajadaPlat = True


        # Para que el monito SALTE PARABOLICAMENTE en las PLATAFORMAS
        
        if controller.upOn and sobrePlataforma:
            if bajadaPlat == False:
                contarSalto += 1
                controller.monitoZ += 0.04

            if bajadaPlat == True:
                contarSalto = 0
                controller.monitoZ -= 0.04

            if contarSalto == 149 or colition == True:
                bajadaPlat = True

            if bajadaPlat == True and enPlat == True:
               bajadaPlat = False
               controller.monitoZ = monitoZ
               controller.upOn = False

            if controller.monitoZ <= 0.04:
                controller.monitoZ = 0.04
                bajadaPlat = False
                controller.upOn = False

            if enPlat is not True and contarSalto == 0 and sobrePlataforma == True:
                bajadaPlat = True
                
            if direccion == 1:
                if controller.monitoY < 23:
                    controller.monitoY += 0.025
                    
                else:
                    controller.monitoY
                    
            if direccion == 2:    
                if controller.monitoY < 23 and controller.monitoX < 23:
                    controller.monitoY += 0.025
                    controller.monitoX += 0.025
                    
                else:
                    controller.monitoY
                    controller.monitoX

            if direccion == 3:
                if controller.monitoX < 23:
                    controller.monitoX += 0.025
                    
                else:
                    controller.monitoX
                

            if direccion == 4:
                if controller.monitoY > -23 and controller.monitoX < 23:
                    controller.monitoY -= 0.025
                    controller.monitoX += 0.025
                    
                else:
                    controller.monitoY
                    controller.monitoX

            if direccion == 5:
                if controller.monitoY > -23:
                    controller.monitoY -= 0.025
                    
                else:
                    controller.monitoY

            if direccion == 6:
                if controller.monitoY > -23 and controller.monitoX > -23:
                    controller.monitoY -= 0.025
                    controller.monitoX -= 0.025
                    
                else:
                    controller.monitoY
                    controller.monitoX

            if direccion == 7:
                if controller.monitoX > -23:
                    controller.monitoX -= 0.025
                    
                else:
                    controller.monitoX

            if direccion == 8:
                if controller.monitoY < 23 and controller.monitoX > -23:
                    controller.monitoY += 0.025
                    controller.monitoX -= 0.025
                    
                else:
                    controller.monitoY
                    controller.monitoX

        # Bajada de una plataforma
        
        elif enPlat is not True and contarSalto == 0 and sobrePlataforma == True:
            controller.upOn = True
            bajadaPlat = True
            if controller.monitoZ == 0.04:
                controller.upOn = False
                sobrePlataforma = False                
            
        # Configurar las proyecciones
        projection = tr.perspective(60, float(width)/float(height), 0.1, 100)
   
        # Limpia la pantalla tanto en color como en profundidad
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Dibujar las shapes
        # Luz del objeto (creo)
        glUseProgram(pipeline.shaderProgram) # para usar este pipeline en el monito
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)


        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 0, 0, 10)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 80)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.01)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.1)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        # Proyección del obj
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        # Objeto (monito)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, 
            tr.matmul([
            tr.translate(controller.monitoX, controller.monitoY, controller.monitoZ),    
            tr.uniformScale(0.35),
            tr.rotationZ(MonitoRotation),
            tr.rotationX(MonitoRotationX),
            tr.rotationY(MonitoRotationY)])
        )

        if perder == True:
            pipeline.drawShape(gpuMonitoDie)

        if perder == False and gameover == False and ganar == False:
            pipeline.drawShape(gpuMonito)

    
#---------------------------- game over
            
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, 
            tr.matmul([
            tr.translate(0, 0, 0.5),    
            tr.uniformScale(0.05),
            tr.rotationZ(np.pi),
            tr.rotationX(np.pi)])
        )
        if gameover == True:
            pipeline.drawShape(gpuGameOver)

        # Objeto (monito)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, 
            tr.matmul([
            tr.translate(0, 0, 0.04),    
            tr.uniformScale(0.35),
            tr.rotationZ(np.pi),
            tr.rotationX(np.pi/2)])
        )
        if gameover == True:
            pipeline.drawShape(gpuMonito)

#---------------------------- win
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, 
            tr.matmul([
            tr.translate(0, 0.5, 0.5),    
            tr.uniformScale(0.05),
            tr.rotationZ(np.pi),
            tr.rotationX(np.pi)])
        )
        if ganar == True:
            pipeline.drawShape(gpuWin)

        # Objeto (monito)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, 
            tr.matmul([
            tr.translate(0, 0, 0.04),    
            tr.uniformScale(0.35),
            tr.rotationZ(np.pi),
            tr.rotationX(np.pi/2)])
        )
        if ganar == True:
            pipeline.drawShape(gpuMonito)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE,
            tr.matmul([tr.translate(-1.2, 0, 1),    
            tr.uniformScale(0.5),
            tr.rotationX(np.pi/2)])
        )
        if ganar == True:
            pipeline.drawShape(gpuBanana)        
            

#----------------------------------------------
        # VIDAS QUE LE QUEDAN AL MONITO
        if vidas == 3:
            # Corazón
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, 
                tr.matmul([
                tr.translate(controller.monitoX, controller.monitoY, controller.monitoZ + 3),    
                tr.uniformScale(0.005),
                tr.rotationZ(MonitoRotation),
                tr.rotationX(np.pi/2)])
            )
        
            pipeline.drawShape(gpuHeart)


            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, 
                tr.matmul([
                tr.translate(controller.monitoX + 0.5, controller.monitoY, controller.monitoZ + 3),    
                tr.uniformScale(0.005),
                tr.rotationZ(MonitoRotation),
                tr.rotationX(np.pi/2)])
                )
        
            pipeline.drawShape(gpuHeart)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, 
                tr.matmul([
                tr.translate(controller.monitoX - 0.5, controller.monitoY, controller.monitoZ + 3),    
                tr.uniformScale(0.005),
                tr.rotationZ(MonitoRotation),
                tr.rotationX(np.pi/2)])
            )
         
            pipeline.drawShape(gpuHeart)
        
        elif vidas == 2:            
            # Corazón
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, 
                tr.matmul([
                tr.translate(controller.monitoX, controller.monitoY, controller.monitoZ + 3),    
                tr.uniformScale(0.005),
                tr.rotationZ(MonitoRotation),
                tr.rotationX(np.pi/2)])
            )
        
            pipeline.drawShape(gpuHeart)

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, 
                tr.matmul([
                tr.translate(controller.monitoX + 0.5, controller.monitoY, controller.monitoZ + 3),    
                tr.uniformScale(0.005),
                tr.rotationZ(MonitoRotation),
                tr.rotationX(np.pi/2)])
                )
        
            pipeline.drawShape(gpuHeart)

        elif vidas == 1:
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, 
                tr.matmul([
                tr.translate(controller.monitoX + 0.5, controller.monitoY, controller.monitoZ + 3),    
                tr.uniformScale(0.005),
                tr.rotationZ(MonitoRotation),
                tr.rotationX(np.pi/2)])
                )
        
            pipeline.drawShape(gpuHeart)

        elif vidas == 0:
            perder = True
            
                               
#----------------------------------------------

        # Pared de atrás
        glUseProgram(pipeline_texture.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, 
            tr.matmul([
            tr.translate(0, -24, 17),    
            tr.scale(48, 0, 34)])
        )
        pipeline_texture.drawShape(gpuPared)

        # Pared de adelante
        glUseProgram(pipeline_texture.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, 
            tr.matmul([
            tr.translate(0, 24, 17),    
            tr.scale(48, 0, 34)])
        )
        pipeline_texture.drawShape(gpuPared)

        # Pared de la izquierda
        glUseProgram(pipeline_texture.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, 
            tr.matmul([
            tr.translate(24, 0, 17),    
            tr.scale(0, 48, 34)])
        )
        pipeline_texture.drawShape(gpuPared)
        
        # Pared de la derecha
        glUseProgram(pipeline_texture.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, 
            tr.matmul([
            tr.translate(-24, 0, 17),    
            tr.scale(0, 48, 34)])
        )
        pipeline_texture.drawShape(gpuPared)

        # LAVA
        if lavaOn and ganar == False:
            glUseProgram(pipeline_texture.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, 
                tr.matmul([
                tr.translate(0, 0, 0),    
                tr.scale(48, 48, 0)])
            )
            pipeline_texture.drawShape(gpuLava)

        # PISO
        glUseProgram(pipeline_texture.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, 
            tr.matmul([
            tr.translate(0, 0, 0),    
            tr.scale(48, 48, 0)])
        )
        pipeline_texture.drawShape(gpuPiso)


        # DIBUJAR LAS PLATAFORMAS

        plataformas.draw(pipeline_texture)

        # DIBUJAR ROQUITAS CUANDO ESTÁ SOBRE PLATAFORMAS
        if sobrePlataforma:
            # LAVA
            lavaOn = True            
            
            # CREAR ROQUITAS
            roquitas.create_roquita()    # dentro del loop para que sea aleatorio

            # Velocidad de las roquitas
            roquitas.posJ(5 * dt)

            # Dibujar ROCAS
            roquitas.draw(pipeline_texture)
            
            # Funcion para eliminar bloques (rocas) si pasan por el fondo o si toca al monito
            roquitas.eliminar(controller.monitoX, controller.monitoY, controller.monitoZ, -25)

            # Monito pierde vidas si la roca-bloque lo golpea
            if roquitas.golpe == True:
                vidas -=1
                roquitas.golpe = False
    
        # Banana moviendose
        t = glfw.get_time()
        ty = 0.5 * np.sin(4 * t)

        
        # Banana en la ultima plataforma
        n = len(A)- 1
        banana.z = C[n] + 2 + ty
        banana.x = A[n]
        banana.y = B[n]

        if banana.x - 0.5 < controller.monitoX < banana.x + 0.5 and banana.y - 0.5 < controller.monitoY < banana.y + 0.5 and banana.z - 2 < controller.monitoZ < banana.z + 2 :
            
            controller.camaraB = False
            controller.camaraN = False
            controller.camaraM = False

            win = True
            saltarWin = True            
            contarDieWin += 1    
            if contarDieWin >= 400:
                contarDieWin = 0

                atX = 0
                atY = 0
                atZ = 1
                
                cameraX = 0
                cameraY = 8
                cameraZ = 3
                ganar = True
                
                
        
        # DIBUJAR BANANA
        banana.draw(pipeline, projection, view, win)

        # GAME OVER
        if lavaOn == True and controller.monitoZ == 0.04:
            perder = True
            vidas = 0

        
        if perder == True:
            controller.upOn = False
            controller.camaraB = False
            controller.camaraN = False
            controller.camaraM = False
            
            if subida == True:
                contarSubida += 1
                controller.monitoZ += 0.03

            if subida == False:
                controller.monitoZ -= 0.03
            
            if contarSubida == 100:
                subida = False

            if controller.monitoZ <= -3:
                controller.monitoZ = -3
                contarDieWin += 1 

            if contarDieWin == 200:
                atX = 0
                atY = 0
                atZ = 1
                
                cameraX = 0
                cameraY = 8
                cameraZ = 3
                gameover = True
                


        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
