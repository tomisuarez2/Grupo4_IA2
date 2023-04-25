import ast
import numpy as np

#-----------------------------------------------------
# Función para leer la distancia entre las posiciones.
#-----------------------------------------------------

def leer_distancias():
    distancias = np.zeros((145, 145, 145, 145)) # Creamos una matriz de 145x145 elementos para las distancias. Hay 144 estantes.
    with open("distancias_modificado.txt", "r") as archivo: # Abrimos el archivo de distancias.
        for linea in archivo: # Leemos las líneas.
            linea_aux = linea.strip() # Quitamos espacios en blanco.
            indice_coma_1 = linea_aux.index(',') # Buscamos indice de la primer coma.
            incioX = int(linea_aux[:indice_coma_1])
            corte1 = linea_aux[indice_coma_1+1:]  # Cortamos la cadena desde la primer coma.
            indice_coma_2 = corte1.index(',') # Buscamos indice de la segunda coma.
            incioY = int(corte1[:indice_coma_2])
            corte2 = corte1[indice_coma_2+1:]  # Cortamos la cadena desde la segunda coma.
            indice_coma_3 = corte2.index(',') # Buscamos indice de la tercer coma.
            finalX = int(corte2[:indice_coma_3])
            corte3 = corte2[indice_coma_3+1:]  # Cortamos la cadena desde la tercer coma.
            indice_igual = corte3.index('=') # Buscamos indice del igual.
            finalY = int(corte3[:indice_igual])
            distancia = int(corte3[indice_igual+1:])
            # Agregamos los elementos a la matriz.
            distancias[incioX, incioY, finalX, finalY] = distancia

    return distancias

    
#------------------------------------------------------------------------
# Función para leer diccionario con la posición original de los estantes.
#------------------------------------------------------------------------

def posiciones_originales():
    with open('configuracion_predeterminada_estantes.txt', "r") as archivo:
        diccionario_str = archivo.read()
        diccionario = ast.literal_eval(diccionario_str)
        return diccionario
    
#-------------------------------
# Función de lectura de ordenes.
#-------------------------------

def lectura_de_ordenes(tamano_maximo_orden): # Función para obtención de ordenes.

    """ Argumento: Longitud máxima de las ordenes. Si el argumento es -1 se deja la longitud original. """

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

        if tamano_maximo_orden > 0:
            ordenes.append(ordenes_todas[(indice1+1):(indice1+1) + tamano_maximo_orden]) # si limitamos el tamaño de la orden.
        elif tamano_maximo_orden == -1:
            ordenes.append(ordenes_todas[indice1+1:indice2])

    # Agregamos la última orden.
    if tamano_maximo_orden > 0:
        ordenes.append(ordenes_todas[(indice2+1):(indice2+1) + tamano_maximo_orden]) 
    elif tamano_maximo_orden == -1:
        ordenes.append(ordenes_todas[indice2+1:])

    return ordenes