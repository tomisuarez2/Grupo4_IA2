import math
import random

#-------------------------
# Función temple simulado.
#-------------------------

def temple_simulado(configuracion, distancias, orden_inicial, temperatura_inicial, enfriamiento, n_iteraciones):

    """ Temple simulado """

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
    # Ubicacion del primer elemento.
    # No entramos a los estantes. Quedamos frente a los estantes. 
    if list(configuracion.keys()).index(orden_mejor[0]) % 2 == 0: # Compruebo si el indice es par. 
        X1, Y1 = configuracion[orden_mejor[0]][0] - 1, configuracion[orden_mejor[0]][1]
    else: # Si no, es impar.
        X1, Y1 = configuracion[orden_mejor[0]][0] + 1, configuracion[orden_mejor[0]][1]
    # Distancia de la bahía al primer elemento.
    numero_de_casillas_mejor = numero_de_casillas_mejor + distancias[0,0, X1, Y1]

    for i in range(len(orden_mejor)-1):
        # Buscamos los puntos inciales y finales.
        # No entramos a los estantes. Quedamos frente a los estantes. 
        if list(configuracion.keys()).index(orden_mejor[i]) % 2 == 0: # Compruebo si el indice es par. 
            comienzoX, comienzoY = configuracion[orden_mejor[i]][0] - 1, configuracion[orden_mejor[i]][1]
        else: # Si no, es impar.
            comienzoX, comienzoY = configuracion[orden_mejor[i]][0] + 1, configuracion[orden_mejor[i]][1]
        if list(configuracion.keys()).index(orden_mejor[i+1]) % 2 == 0: # Compruebo si es par. 
            finalX, finalY = configuracion[orden_mejor[i+1]][0] - 1, configuracion[orden_mejor[i+1]][1]
        else: # Si no, es impar.
            finalX, finalY = configuracion[orden_mejor[i+1]][0] + 1, configuracion[orden_mejor[i+1]][1]
       
        numero_de_casillas_mejor = numero_de_casillas_mejor + distancias[comienzoX, comienzoY, finalX, finalY]
        
    # Distancia del último elemento a la bahía.
    # No entramos a los estantes. Quedamos frente a los estantes. 
    if list(configuracion.keys()).index(orden_mejor[-1]) % 2 == 0: # Compruebo si es par. 
        Xf, Yf = configuracion[orden_mejor[-1]][0] - 1, configuracion[orden_mejor[-1]][1]
    else: # Si no, es impar.
        Xf, Yf = configuracion[orden_mejor[-1]][0] + 1, configuracion[orden_mejor[-1]][1]
    # Distancia de la bahía al primer elemento.
    numero_de_casillas_mejor = numero_de_casillas_mejor + distancias[0,0, Xf, Yf]

    #---------------------------------------------
    # Iteración hasta que la temperatura sea baja.
    #---------------------------------------------

    while (temperatura_actual > 1e-10): # Iteramos hasta que la temperatura sea casi cero.
        for _ in range(n_iteraciones): # Numero de iteraciones por temperatura.

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
            # Ubicacion del primer elemento.
            # No entramos a los estantes. Quedamos frente a los estantes. 
            if list(configuracion.keys()).index(orden_vecino[0]) % 2 == 0: # Compruebo si es par. 
                X1, Y1 = configuracion[orden_vecino[0]][0] - 1, configuracion[orden_vecino[0]][1]
            else: # Si no, es impar.
                X1, Y1 = configuracion[orden_vecino[0]][0] + 1, configuracion[orden_vecino[0]][1]
            # Distancia de la bahía al primer elemento.
            numero_de_casillas_vecino = numero_de_casillas_vecino + distancias[0,0, X1, Y1]

            for i in range(len(orden_vecino)-1):
                # Buscamos los puntos inciales y finales.
                # No entramos a los estantes. Quedamos frente a los estantes. 
                if list(configuracion.keys()).index(orden_vecino[i]) % 2 == 0: # Compruebo si es par. 
                    comienzoX, comienzoY = configuracion[orden_vecino[i]][0] - 1, configuracion[orden_vecino[i]][1]
                else: # Si no, es impar.
                    comienzoX, comienzoY = configuracion[orden_vecino[i]][0] + 1, configuracion[orden_vecino[i]][1]
                if list(configuracion.keys()).index(orden_vecino[i+1]) % 2 == 0: # Compruebo si es par. 
                    finalX, finalY = configuracion[orden_vecino[i+1]][0] - 1, configuracion[orden_vecino[i+1]][1]
                else: # Si no, es impar.
                    finalX, finalY = configuracion[orden_vecino[i+1]][0] + 1, configuracion[orden_vecino[i+1]][1]
        
                numero_de_casillas_vecino = numero_de_casillas_vecino + distancias[comienzoX, comienzoY, finalX, finalY]
            
            # Distancia del último elemento a la bahía.
            # No entramos a los estantes. Quedamos frente a los estantes. 
            if list(configuracion.keys()).index(orden_vecino[-1]) % 2 == 0: # Compruebo si es par. 
                Xf, Yf = configuracion[orden_vecino[-1]][0] - 1, configuracion[orden_vecino[-1]][1]
            else: # Si no, es impar.
                Xf, Yf = configuracion[orden_vecino[-1]][0] + 1, configuracion[orden_vecino[-1]][1]
            # Distancia de la bahía al primer elemento.
            numero_de_casillas_vecino = numero_de_casillas_vecino + distancias[0,0, Xf, Yf]

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

        temperatura_actual -= enfriamiento  # Enfriamiento lineal

    return numero_de_casillas_mejor