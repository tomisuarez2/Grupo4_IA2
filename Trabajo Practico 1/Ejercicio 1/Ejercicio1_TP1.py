import turtle

#----------------------------------------
# Estantes comienzo y fin del recorrido.
#----------------------------------------

inicio = 'P1'
final = 'P144'

#--------------------------------------------
# Listas para guardar las distintas casillas.
#--------------------------------------------

lugar_paredes = []         # Lista que almacena la posición de las paredes.
lugar_estantes = {}        # Diccionario que almacena la posición de los estantes.
pasillo = []               # Lista que almacena las casillas del pasillo, es decir, aquellas que carecen de obstaculos. Son transitables.
entre_estantes = []        # Lista que almacena el espacio entre estantes, transitar por acá es más ineficaz. Es transitable.
visitado = []              # Lista para casillas visitadas.
frontera = []              # Lista que guarda los estados frontera del estado inicial.
costo_total = []           # Lista que guarda las funciones de costo de las casillas.
solucion = {}              # Diccionario que guarda el camino solución.

#-----------------------------------
# Definimos la ventana para dibujar.
#-----------------------------------

ventana = turtle.Screen()         # Instanciamos un objeto ventana para dibujar.
ventana.bgcolor("black")          # Definimos el color de fondo de la ventana.
ventana.title("Almacen")          # Título de la ventana.
ventana.setup(800, 700, 350, -40) # Tamaño y ubicación de la ventana en pixeles.

#-----------------------------------------------------------
# Instanciamos los cursores y definimos sus caracteristicas.
#-----------------------------------------------------------

# Cursor para paredes del almacén.
paredes = turtle.Turtle()
paredes.shape('square') 
paredes.color('white')  
paredes.penup()         
paredes.speed('fastest')
paredes.hideturtle()

# Cursor para los estantes del almacén.
estantes = turtle.Turtle()
estantes.shape('square')
estantes.color('gray')
estantes.penup()
estantes.speed('fastest')
estantes.hideturtle()

# Cursor para el estante de comienzo.
rojo = turtle.Turtle()
rojo.shape('circle') 
rojo.color('red')  
rojo.penup()         
rojo.speed('fastest')
rojo.hideturtle()

# Cursor para el estante de fin.
azul = turtle.Turtle()
azul.shape('circle') 
azul.color('blue')  
azul.penup()         
azul.speed('fastest')
azul.hideturtle()

# Cursor para el camino.
camino = turtle.Turtle()
camino.shape('square') 
camino.color('yellow')  
camino.penup()         
camino.speed('fastest')
camino.hideturtle()

# Cursor para las casillas visitadas.
verde = turtle.Turtle()
verde.shape('square') 
verde.color('green')  
verde.penup()         
verde.speed('fastest')
verde.hideturtle()

#------------------------------------------
# Grilla que refleja la forma del almacen.
#------------------------------------------

grilla_almacen = [      
    '++++++++++++++++++++++++++++',
    '+                          +',
    '+                          +',
    '+  aaooddooggoojjoommooqq  +',  
    '+  aaooddooggoojjoommooqq  +',  
    '+  aaooddooggoojjoommooqq  +',  
    '+  aaooddooggoojjoommooqq  +',  
    '+                          +',           
    '+                          +',
    '+  bbooeeoohhookkoonnoorr  +',
    '+  bbooeeoohhookkoonnoorr  +',
    '+  bbooeeoohhookkoonnoorr  +',
    '+  bbooeeoohhookkoonnoorr  +',
    '+                          +',
    '+                          +',
    '+  ccooffooiioollooppooss  +',
    '+  ccooffooiioollooppooss  +',
    '+  ccooffooiioollooppooss  +',
    '+  ccooffooiioollooppooss  +',
    '+                          +',
    '+                          +',
    '++++++++++++++++++++++++++++',
]

#----------------------------------------------------
# Función que crea el almacen a partir de la grilla.
#----------------------------------------------------

# Parámetros de graficación.
distancia_cuadrados = 24 # Distancia entre los cuadrados del problema.
desplazamiento_en_x = 300 # Desplazamiento del gráfico hacia la izquierda.
desplazamiento_en_y = 300 # Desplazamiento del gráfico hacia la derecha.

# Bloques de almacenes.
bloques = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','p','q','r','s']

def hacer_almacen(grilla): # Función que crea el almacén.
    global comienzoX, comienzoY, finalX, finalY
    # Variable para contar el número de estantes.
    na, nb, nc, nd, ne, nf, ng, nh, ni, nj, nk, nl, nm, nn, np, nq, nr, ns = 0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136
    for y in range(len(grilla)):  # Para cada fila.
        for x in range(len(grilla[y])):  # Para casilla de la fila.
            casilla = grilla[y][x]
            pixelX = -desplazamiento_en_x + (x * distancia_cuadrados) # El primer número hace referencia al desplazamiento del laberinto en la pantalla. El segundo número hace referencia al tamaño del cuadrado.
            pixelY = desplazamiento_en_y - (y * distancia_cuadrados)
            if casilla == '+':
                paredes.goto(pixelX, pixelY) # Vamos a la casilla en cuestión.
                paredes.stamp() # Dejamos una copia del cursor.
                lugar_paredes.append((pixelX, pixelY))
            if casilla == 'o':
                entre_estantes.append((pixelX, pixelY))
            elif casilla in bloques:
                if casilla == 'a':
                    na = na + 1
                    identificador = 'P' + str(na)
                elif casilla == 'b':
                    nb = nb + 1
                    identificador = 'P' + str(nb)
                elif casilla == 'c':
                    nc = nc + 1
                    identificador = 'P' + str(nc)
                elif casilla == 'd':
                    nd = nd + 1
                    identificador = 'P' + str(nd)
                elif casilla == 'e':
                    ne = ne + 1
                    identificador = 'P' + str(ne)
                elif casilla == 'f':
                    nf = nf + 1
                    identificador = 'P' + str(nf)
                elif casilla == 'g':
                    ng = ng + 1
                    identificador = 'P' + str(ng)
                elif casilla == 'h':
                    nh = nh + 1
                    identificador = 'P' + str(nh)
                elif casilla == 'i':
                    ni = ni + 1
                    identificador = 'P' + str(ni)
                elif casilla == 'j':
                    nj = nj + 1
                    identificador = 'P' + str(nj)
                elif casilla == 'k':
                    nk = nk + 1
                    identificador = 'P' + str(nk)
                elif casilla == 'l':
                    nl = nl + 1
                    identificador = 'P' + str(nl)
                elif casilla == 'm':
                    nm = nm + 1
                    identificador = 'P' + str(nm)
                elif casilla == 'n':
                    nn = nn + 1
                    identificador = 'P' + str(nn)
                elif casilla == 'p':
                    np = np + 1
                    identificador = 'P' + str(np)
                elif casilla == 'q':
                    nq = nq + 1
                    identificador = 'P' + str(nq)
                elif casilla == 'r':
                    nr = nr + 1
                    identificador = 'P' + str(nr)
                elif casilla == 's':
                    ns = ns + 1
                    identificador = 'P' + str(ns)
                estantes.goto(pixelX, pixelY)
                estantes.stamp()
                lugar_estantes[identificador] = (pixelX, pixelY)
                # Buscamos los puntos inciales y finales.
                # No entramos a los estantes. Quedamos frente a los estantes.
                if identificador == inicio:
                    comienzoX, comienzoY = lugar_estantes[inicio] # Salida.
                    rojo.goto(comienzoX, comienzoY)
                    rojo.stamp()
                    if (grilla[y][x - 1] == ' ' or grilla[y][x - 1] == 'o'):
                        comienzoX, comienzoY = comienzoX - distancia_cuadrados, comienzoY
                    else:
                        comienzoX, comienzoY = comienzoX + distancia_cuadrados, comienzoY
                if identificador == final:
                    finalX, finalY = lugar_estantes[final] # Llegada.
                    azul.goto(finalX, finalY)
                    azul.stamp() 
                    if (grilla[y][x - 1] == ' ' or grilla[y][x - 1] == 'o'):
                        finalX, finalY = finalX - distancia_cuadrados, finalY
                    else:
                        finalX, finalY = finalX + distancia_cuadrados, finalY
            elif casilla == ' ':
                pasillo.append((pixelX, pixelY))
   
#-----------------------------------------------------------------
# Función para calcular la heurística como distancia de Manhattan.
#-----------------------------------------------------------------

def calcular_heuristica(x,y): 
    x = round((x + desplazamiento_en_x)/distancia_cuadrados)
    y = round((desplazamiento_en_y - y)/distancia_cuadrados)
    aux_x = round((finalX + desplazamiento_en_x)/distancia_cuadrados)
    aux_y = round((desplazamiento_en_y - finalY)/distancia_cuadrados)
    return abs(aux_x - x) + abs(aux_y - y)

#---------------------------------------------
# Función para definir el costo de movimiento.
#---------------------------------------------

def calcular_costo(x, y): # x, y hacen referencia a pixeles.
    global pasillo, entre_estantes
    if (x, y) in pasillo:
        costo = 1
    elif (x, y) in entre_estantes:
        costo = 3
    return costo
  
#---------------------
# Busqueda de estados.
#---------------------

def buscar(x, y):
    global frontera, costo_total
    frontera.append((x, y))  # Añadimos la posición inicial x,y a la lista de casillas de frontera
    costo_total.append(calcular_heuristica(x,y) + calcular_costo(x,y))
    solucion[x, y] = x, y  # Añadimos la posición inicial x,y al diccionario de soluciones
    while len(frontera) > 0:
        casilla_actual = (x, y)
        if (((x - distancia_cuadrados, y) in (pasillo)) or ((x - distancia_cuadrados, y) in entre_estantes)) and (x - distancia_cuadrados, y) not in visitado:  # Revisa a la izquierda.
            celda_izquierda = (x - distancia_cuadrados, y)
            solucion[celda_izquierda] = x, y  # Al reconstruir el camino de solución, [celda_izquierda] es la celda anterior. x,y es la celda actual.
            frontera.append(celda_izquierda)
            costo_total.append(calcular_heuristica(x - distancia_cuadrados, y) + calcular_costo(x - distancia_cuadrados, y))
        if (((x + distancia_cuadrados, y) in (pasillo)) or ((x + distancia_cuadrados, y) in entre_estantes)) and (x + distancia_cuadrados, y) not in visitado:  # Revisa a la derecha.
            celda_derecha = (x + distancia_cuadrados, y)
            solucion[celda_derecha] = x, y
            frontera.append(celda_derecha)
            costo_total.append(calcular_heuristica(x + distancia_cuadrados, y) + calcular_costo(x + distancia_cuadrados, y))
        if (((x, y  - distancia_cuadrados) in (pasillo)) or ((x, y - distancia_cuadrados) in entre_estantes)) and (x, y - distancia_cuadrados) not in visitado:  # Revisa abajo.
            celda_abajo = (x, y - distancia_cuadrados)
            solucion[celda_abajo] = x, y
            frontera.append(celda_abajo)
            costo_total.append(calcular_heuristica(x, y - distancia_cuadrados) + calcular_costo(x, y - distancia_cuadrados))
        if (((x, y  + distancia_cuadrados) in (pasillo)) or ((x, y + distancia_cuadrados) in entre_estantes)) and (x, y + distancia_cuadrados) not in visitado:  # Revisa arriba.
            celda_arriba = (x, y + distancia_cuadrados)
            solucion[celda_arriba] = x, y
            frontera.append(celda_arriba)
            costo_total.append(calcular_heuristica(x, y + distancia_cuadrados) + calcular_costo(x, y + distancia_cuadrados))
        costo_total, frontera = (list(t) for t in zip(*sorted(zip(costo_total, frontera), reverse = True)))
        x, y = frontera.pop()  # Remueve el último elemento de la lista de casillas de frontera, el de menor costo total.
        costo_total.pop()
        visitado.append(casilla_actual)
        #----------------------------------------------------------------------
        #verde.goto(x, y)   # Descomentar para graficar las casillas visitadas.
        #verde.stamp()
        #----------------------------------------------------------------------
        if (x, y) == (finalX, finalY):
            break

    # Armamos una lista para entregar la solución limpia, sin estados repetidos.
    solucion_limpia = [] 
    x, y = finalX, finalY
    while (x, y) != (comienzoX, comienzoY):
        if (x, y) in solucion_limpia:
            pass
        else:
            solucion_limpia.append([x, y])
        x, y = solucion[x, y]
    solucion_limpia.append([comienzoX, comienzoY]) # Arego el inicio

    # Calculamos las casillas caminadas.
    casillas_caminadas = len(solucion_limpia)

    return solucion_limpia, casillas_caminadas

#---------------------
# Armamos la solución.
#---------------------

def graficar_solucion(solucion_limpia):
    for casilla in solucion_limpia:
        camino.goto(casilla[0], casilla[1])
        camino.stamp()

#------------------
# Bloque principal.
#------------------

hacer_almacen(grilla_almacen)
solucion_, casillas_ = buscar(comienzoX, comienzoY)
graficar_solucion(solucion_)
print('Numero de casillas recorridas: ')
print(casillas_)


ventana.exitonclick()
