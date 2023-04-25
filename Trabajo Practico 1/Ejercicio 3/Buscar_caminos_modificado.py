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

#-----------------------------------------------------------------
# Función para calcular la heurística como distancia de Manhattan.
#-----------------------------------------------------------------

def calcular_heuristica(x,y): 
    global finalX, finalY
    return abs(finalX - x) + abs(finalY - y)

#---------------------------------------------
# Función para definir el costo de movimiento.
#---------------------------------------------

def calcular_costo(x, y): # x, y hacen referencia a pixeles.
    global pasillo, entre_estantes
    if (x, y) in pasillo: # Si el punto en cuestión esta en el pasillo.
        costo = 1
    elif (x, y) in entre_estantes: # Si el punto en cuestión está en el lugar entre estantes.
        costo = 3
    return costo

#--------------------
# Busqueda de camino.
#--------------------

def buscar(comienzo_x, comienzo_y, final_x, final_y):
    global lugar_paredes, lugar_estantes, pasillo, entre_estantes, visitado, frontera, costo_total, solucion
    x, y = comienzo_x, comienzo_y # Definimos el punto de comienzo.
    frontera.append((x, y))  # Añadimos la posición inicial x,y a la lista de casillas de frontera
    costo_total.append(calcular_heuristica(x,y) + calcular_costo(x,y)) # Calculamos el costo total de la casilla.
    solucion[x, y] = x, y  # Añadimos la posición inicial x,y al diccionario de soluciones
    while len(frontera) > 0:
        casilla_actual = (x, y)
        if (((x - 1, y) in (pasillo)) or ((x - 1, y) in entre_estantes)) and (x - 1, y) not in visitado:  # Revisa a la izquierda.
            celda_izquierda = (x - 1, y)
            solucion[celda_izquierda] = x, y  # Al reconstruir el camino de solución, [celda_izquierda] es la celda anterior. x,y es la celda actual.
            frontera.append(celda_izquierda)
            costo_total.append(calcular_heuristica(x - 1, y) + calcular_costo(x - 1, y))
        if (((x + 1, y) in (pasillo)) or ((x + 1, y) in entre_estantes)) and (x + 1, y) not in visitado:  # Revisa a la derecha.
            celda_derecha = (x + 1, y)
            solucion[celda_derecha] = x, y
            frontera.append(celda_derecha)
            costo_total.append(calcular_heuristica(x + 1, y) + calcular_costo(x + 1, y))
        if (((x, y - 1) in (pasillo)) or ((x, y - 1) in entre_estantes)) and (x, y - 1) not in visitado:  # Revisa abajo.
            celda_abajo = (x, y - 1)
            solucion[celda_abajo] = x, y
            frontera.append(celda_abajo)
            costo_total.append(calcular_heuristica(x, y - 1) + calcular_costo(x, y - 1))
        if (((x, y + 1) in (pasillo)) or ((x, y + 1) in entre_estantes)) and (x, y + 1) not in visitado:  # Revisa arriba.
            celda_arriba = (x, y + 1)
            solucion[celda_arriba] = x, y
            frontera.append(celda_arriba)
            costo_total.append(calcular_heuristica(x, y + 1) + calcular_costo(x, y + 1))
        costo_total, frontera = (list(t) for t in zip(*sorted(zip(costo_total, frontera), reverse = True)))
        x, y = frontera.pop()  # Remueve el último elemento de la lista de casillas de frontera, el de menor costo total.
        costo_total.pop()
        visitado.append(casilla_actual)
        if (x, y) == (final_x, final_y):
            break

    # Armamos una lista para entregar la solución limpia, sin estados repetidos.
    solucion_limpia = [] 
    x, y = final_x, final_y
    while (x, y) != (comienzo_x, comienzo_y):
        if (x, y) in solucion_limpia:
            pass
        else:
            solucion_limpia.append([x, y])
        x, y = solucion[x, y]
    solucion_limpia.append([comienzo_x, comienzo_y]) # Arego el inicio

    # Calculamos las casillas caminadas.
    casillas_caminadas = len(solucion_limpia)

    return casillas_caminadas


#------------------------------------------
# Grilla que refleja la forma del almacen.
#------------------------------------------

grilla = [      
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

# Bloques de almacenes.
bloques = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','p','q','r','s']

#-----------------------------
# Función que crea el almacén.
#-----------------------------

# Variable para contar el número de estantes.
na, nb, nc, nd, ne, nf, ng, nh, ni, nj, nk, nl, nm, nn, np, nq, nr, ns = 0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136
for y in range(len(grilla)):  # Para cada fila.
    for x in range(len(grilla[y])):  # Para casilla de la fila.
        casilla = grilla[y][x]
        pixelX = x  
        pixelY = y 
        if casilla == '+':
            lugar_paredes.append((pixelX, pixelY))
        elif casilla == 'o':
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
            lugar_estantes[identificador] = (pixelX, pixelY)
        elif casilla == ' ':
            pasillo.append((pixelX, pixelY))


#---------------------
# Bloque de ejecución.
#---------------------


# Imprimimos en un archivo .txt la configuración inicial de estantes.
with open('configuracion_predeterminada_estantes.txt', 'w') as archivo:
    archivo.write(str(lugar_estantes))

# Creamos el archivo con las distancias.
with open('distancias_modificado.txt', 'w') as archivo:

    # Buscamos y escribimos las distancias.
    # Quitamos la P de las claves, de modo que solo sean números enteros y los ordenamos.
    claves = list(lugar_estantes.keys()) # Armamos una lista con las claves del diccionario.

    for i in range(len(claves)):
        claves[i] = int(claves[i][1:]) # Transformamos las claves de 'string' a 'int' sin la P. 
    claves = sorted(claves) # Ordenamos de menor a mayor.

    for i in range(len(lugar_estantes)):
        for j in range(len(lugar_estantes)):
            if i != j: # Si los elementos son distintos:
                numeroinicio = claves[i] 
                numerofin = claves[j]
                # Buscamos los puntos inciales y finales.
                # No entramos a los estantes. Quedamos frente a los estantes.
                if numeroinicio % 2 == 0: # Compruebo si es par. 
                    comienzoX, comienzoY = lugar_estantes['P'+str(claves[i])][0] + 1, lugar_estantes['P'+str(claves[i])][1]
                else: # Si no, es impar.
                    comienzoX, comienzoY = lugar_estantes['P'+str(claves[i])][0] - 1, lugar_estantes['P'+str(claves[i])][1]
                if numerofin % 2 == 0: # Compruebo si es par. 
                    finalX, finalY = lugar_estantes['P'+str(claves[j])][0] + 1, lugar_estantes['P'+str(claves[j])][1]
                else: # Si no, es impar.
                    finalX, finalY = lugar_estantes['P'+str(claves[j])][0] - 1, lugar_estantes['P'+str(claves[j])][1]
                # Limpiamos variables.
                visitado = []             
                frontera = []           
                costo_total = []          
                solucion = {}
                # Buscamos distancias.              
                distancia = buscar(comienzoX, comienzoY, finalX, finalY)
                # Guardamos en el .txt.
                archivo.write(str(comienzoX) + ',' + str(comienzoY) + ',' + str(finalX) + ',' + str(finalY) + '=' + str(distancia) + '\n')

    # Calculamos la distancia de los estantes a la bahía. El indice 0,0 en la matriz corresponde a la bahía.
    # La bahía se encuentra en la posición (1,8).

    for j in range(len(lugar_estantes)):
        numeroinicio = 0 
        numerofin = claves[j]
        comienzoX, comienzoY = 1, 8
        # Buscamos los puntos inciales y finales.
        # No entramos a los estantes. Quedamos frente a los estantes.
        if numerofin % 2 == 0: # Compruebo si es par. 
            finalX, finalY = lugar_estantes['P'+str(claves[j])][0] + 1, lugar_estantes['P'+str(claves[j])][1]
        else: # Si no, es impar.
            finalX, finalY = lugar_estantes['P'+str(claves[j])][0] - 1, lugar_estantes['P'+str(claves[j])][1]
        # Limpiamos variables.
        visitado = []             
        frontera = []           
        costo_total = []          
        solucion = {}
        # Buscamos distancias.              
        distancia = buscar(comienzoX, comienzoY, finalX, finalY)
        # Guardamos en el .txt.
        archivo.write(str(0) + ',' + str(0) + ',' + str(finalX) + ',' + str(finalY) + '=' + str(distancia) + '\n')









            

           