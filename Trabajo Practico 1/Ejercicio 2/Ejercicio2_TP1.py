import math
import random
import numpy as np
import matplotlib.pyplot as plt

def lectura_de_datos(): # Función para obtención de ordenes y las distancias.

    #------------------------
    # Lectura de las ordenes.
    #------------------------

    ordenes = [] # Lista para guardar las ordenes.
    ordenes_todas = [] # Lista que guarda todas las lineas del .txt.
    with open("orders.txt", "r") as archivo: # Abrimos el archivo de ordenes.
        for linea in archivo: # Leemos las líneas.
            linea_aux = linea.strip() # Quitamos espacios en blanco.
            if linea_aux != '': # Si nos es una linea vacía la agregamos a la lista.
                ordenes_todas.append(linea_aux) # Quedan todas las lineas en una lista.
    orden = 'Order'
    for i in range(1,100,1): # Guardamos cada orden en una linea distinta.
        orden_i = orden + ' ' + str(i)
        orden_f = orden + ' ' + str(i+1)
        indice1 = ordenes_todas.index(orden_i)
        indice2 = ordenes_todas.index(orden_f)
        ordenes.append(ordenes_todas[indice1+1:indice2])
    ordenes.append(ordenes_todas[indice2+1:]) # Agregamos la ultima orden.

    #--------------------------- 
    # Lectura de las distancias.
    #---------------------------

    distancias = np.zeros((145, 145)) # Creamos una matriz de 145x145 elementos para las distancias. Hay 144 estantes.
    with open("distancias.txt", "r") as archivo: # Abrimos el archivo de distancias.
        for linea in archivo: # Leemos las líneas.
            linea_aux = linea.strip() # Quitamos espacios en blanco.
            indice_coma = linea_aux.index(',') # Buscamos indice de la coma.
            indice_igual = linea_aux.index('=') # Buscamos indice del igual.
            incio = int(linea_aux[:indice_coma])
            fin = int(linea_aux[indice_coma+1:indice_igual])
            distancia = int(linea_aux[indice_igual+1:])
            # Agregamos los elementos a la matriz.
            distancias[incio, fin] = distancia

    return ordenes, distancias
    
    
def temple_simulado(distancias, orden_inicial, temperatura_inicial, enfriamiento, lineal_logaritmica):

    """ Temple simulado """

    historial_casillas = [] # Lista para el historial de casillas.
    iteraciones = []        # Lista para el historial de iteraciones.

    #-------------------------
    # Inicializamos variables.
    #-------------------------

    orden_mejor = [] # Lista que indica el orden en que se deben visitar las estanterias.
    orden_mejor = orden_inicial
    temperatura_actual = temperatura_inicial

    #-------------------------------------------------------------------
    # Cálculo de la cantidad de casillas recorridas en el orden inicial.
    #-------------------------------------------------------------------

    numero_de_casillas_mejor = 0
    # Distancia de la bahía al primer elemento.
    numero_de_casillas_mejor = numero_de_casillas_mejor + distancias[0, int(orden_mejor[0][1:])]
    for i in range(len(orden_mejor)-1):
        numero_de_casillas_mejor = numero_de_casillas_mejor + distancias[int(orden_mejor[i][1:]),int(orden_mejor[i+1][1:])]
    # Distancia del último elemento a la bahía.
    numero_de_casillas_mejor = numero_de_casillas_mejor + distancias[0, int(orden_mejor[-1][1:])]

    #---------------------------------------------
    # Iteración hasta que la temperatura sea baja.
    #---------------------------------------------

    j = 0 # Contador de iteraciones.
    while (temperatura_actual > 1e-10): # Iteramos hasta que la temperatura sea casi cero.
        
        j += 1
        historial_casillas.append(numero_de_casillas_mejor)
        iteraciones.append(j)

        #-----------------------------------------
        # Generamos un vecino de forma aleatoria.
        #-----------------------------------------
                
        orden_vecino = orden_mejor
        elementos = random.sample(orden_mejor, 2) # Seleccionar dos elementos de la lista de forma aleatoria.

        indice_1 = orden_mejor.index(elementos[0]) # Obtener los índices de los elementos seleccionados.
        indice_2 = orden_mejor.index(elementos[1])

        orden_vecino[indice_1], orden_vecino[indice_2] = orden_mejor[indice_2], orden_mejor[indice_1]

        #-------------------------------------------------------------------------
        # Calculo de la diferencia de casillas entre orden_mejor (actual) y vecino.
        #-------------------------------------------------------------------------

        numero_de_casillas_vecino = 0
        # Distancia de la bahía al primer elemento.
        numero_de_casillas_vecino = numero_de_casillas_vecino + distancias[0, int(orden_vecino[0][1:])]
        for i in range(len(orden_vecino)-1):
            numero_de_casillas_vecino = numero_de_casillas_vecino + distancias[int(orden_vecino[i][1:]),int(orden_vecino[i+1][1:])]
        # Distancia del último elemento a la bahía.
        numero_de_casillas_vecino = numero_de_casillas_vecino + distancias[0, int(orden_vecino[-1][1:])]

        diferencia = numero_de_casillas_vecino - numero_de_casillas_mejor

        #----------------------------
        # Actualizacion de variables.
        #----------------------------

        if diferencia < 0: # Si la solución vecina es mejor, actualizar la mejor solución.
            orden_mejor = orden_vecino
            numero_de_casillas_mejor = numero_de_casillas_vecino
        else: # Si la solución vecina es peor, aceptarla con una cierta probabilidad.
            probabilidad_aceptacion = math.exp(-diferencia / temperatura_actual)
            if random.uniform(0, 1) < probabilidad_aceptacion:
                orden_mejor = orden_vecino
                numero_de_casillas_mejor = numero_de_casillas_vecino

        #--------------------------
        # Enfriamos la temperatura.
        #--------------------------

        if lineal_logaritmica == 1:
            temperatura_actual -= enfriamiento  # Enfriamiento lineal
        elif lineal_logaritmica == 0:
            temperatura_actual /= 2             # Enfriamiento exponencial.

    return iteraciones, historial_casillas, orden_mejor, numero_de_casillas_mejor

#------------------
# Bloque principal.
#------------------

ordenes_, distancias_ = lectura_de_datos()
tamano_orden = 10
orden = ordenes_[6][:(tamano_orden-1)]
numero_iteraciones, historial, orden_mejor, numero_casillas_mejor = temple_simulado(distancias_, orden, 5, 0.001, 1)
print('='*100)
print('La orden mas eficiente es: ')
print(orden_mejor)
print('\n')
print('El numero de casillas recorridas es: ')
print(numero_casillas_mejor)
print('\n')
print('Cantidad de itaraciones realizadas: ')
print(len(numero_iteraciones))
print('\n')
print('='*100)

#print(historial)
fig, ax = plt.subplots()
ax.scatter(numero_iteraciones, historial)
ax.grid()
plt.xlabel('Numero de iteración')
plt.ylabel('Casillas totales recorridas por configuración')
plt.title('Resultados')
plt.show()