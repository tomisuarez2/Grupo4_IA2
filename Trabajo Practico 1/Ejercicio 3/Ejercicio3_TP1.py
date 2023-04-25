import random
import numpy as np
from lectura_datos import  posiciones_originales, lectura_de_ordenes, leer_distancias # Funciones para leer los datos.
from temple_modificado import temple_simulado # Función de temple simulado.

#--------------------
# Función de fitness.
#--------------------

def fitness(individuo, posiciones_estantes, distancias_estantes, ordenes):
    # El individuo es la configuración de los estantes.
    # posicion_estantes es la poscion de los estantes.
    configuracion = dict(zip(individuo, posiciones_estantes)) # Armamos un diccionario con ambas listas.
    sum = 0 # Suma para las casillas totales.
    for orden in ordenes:
        sum = sum + temple_simulado(configuracion, distancias_estantes, orden, 5, 0.001, 1)
    # Pasos totales caminados en todas las ordenes. No es un promedio.
    
    return (-1)*sum # Pasamos el fitness negativo, asi a mayor numero, mejor fitness.

#-----------------------------------------------------
# Función de seleccion de padres - Selección elitista.
#-----------------------------------------------------

def seleccion_elitista(poblacion, fitness_poblacion):
    fitness_population = [ (1/ (-1*f))*1e5  for f in fitness_poblacion] # Invertimos fitness, a menor fitness mejor individuo, por eso invertimos.
    suma_fitness = sum(fitness_population)
    # Normalizamos el fitness invertido dividiéndolo por la suma.
    probabilidad_seleccion = [f / suma_fitness for f in fitness_population] # Calculamos la probabilidad de elección.
    return random.choices(poblacion, k=2, weights=probabilidad_seleccion) # Extraemos dos padres de la población por probabilidad.

#--------------------------------------------
# Función de seleccion de padres - K mejores.
#--------------------------------------------

def seleccion_2_mejores(poblacion, fitness_poblacion):
    population = poblacion.copy() # Copiamos para no pisar.
    fitness_population = fitness_poblacion.copy() # Copiamos para no pisar.
    candidatos = [] # Lista de padres.
    fitness_max1 = fitness_population[0]
    indice_max1 = 0
    # Buscamos el mayor fitness.
    for i in range(len(population)):
        if fitness_population[i] > fitness_max1:
            fitness_max1 = fitness_population[i]
            indice_max1 = i
    candidato1 = population[indice_max1].copy()
    del population[indice_max1]
    del fitness_population[indice_max1]
    fitness_max2 = fitness_population[0]
    indice_max2 = 0
    # Buscamos el segundo mayor fitness.
    for i in range(len(population)):
        if fitness_population[i] > fitness_max2:
            fitness_max2 = fitness_population[i]
            indice_max2 = i
    candidato2 = population[indice_max2].copy()
    # Agregamos los padres a la lista.
    candidatos.append(candidato1)
    candidatos.append(candidato2)
    
    return candidatos # Retornamos los mejores individuos.

#---------------------------------------
# Función de Crossover - Cruce de orden.
#---------------------------------------

def crossover_cruce_de_orden(padre1, padre2): # Crossover por orden.
    # Generamos dos puntos de corte aleatorios.
    cut1 = random.randint(0, len(padre1)-1)
    cut2 = random.randint(0, len(padre2)-1)
    # Nos aseguramos de que los puntos de corte sean distintos.
    while cut2 == cut1:
        cut2 = random.randint(0, len(padre1)-1)
    # Nos aseguramos de que cut1 es menor que cut2.
    if cut1 > cut2:
        cut1, cut2 = cut2, cut1
    # Inicializamos los hijos con valores nulos.
    hijo1 = [None]*len(padre1)
    hijo2 = [None]*len(padre2)
    # Copiamos los elementos de los padres entre los puntos de cruce.
    hijo1[cut1:cut2+1] = padre1[cut1:cut2+1]
    hijo2[cut1:cut2+1] = padre2[cut1:cut2+1]
    # Copiamos los valores restantes a partir del segundo corte, en orden, evitando duplicar valores.
    index1 = cut2
    index2 = cut2
    while None in hijo1: # Mientras exista un valor no asignado en hijo1.
        if hijo1[index1] is not None: # Si el valor en hijo 1 es no None.
            ind = padre2.index(hijo1[index1]) # Busco el valor final del segmento en el padre contrario.
            ind_posterior = (ind + 1) % len(padre2)
            while padre2[ind_posterior] in hijo1: # Si el valor ya esta en hijo, avanzo de posición.
                ind_posterior = (ind_posterior + 1) % len(padre2)
            else:
                hijo1[(index1 + 1) % len(padre2)] = padre2[ind_posterior] # Agrego.
        index1 = (index1 + 1) % len(padre2) # Comando para que sea ciclico el indexado.
    while None in hijo2: # Mientras exista un valor no asignado en hijo2.
        if hijo2[index2] is not None: # Si el valor en hijo 2 es no None.
            ind = padre1.index(hijo2[index2]) # Busco el valor final del segmento en el padre contrario.
            ind_posterior = (ind + 1) % len(padre1)
            while padre1[ind_posterior] in hijo2: # Si el valor ya esta en hijo, avanzo de posición.
                ind_posterior = (ind_posterior + 1) % len(padre1)
            else:
                hijo2[(index2 + 1) % len(padre1)] = padre1[ind_posterior] # Agrego.
        index2 = (index2 + 1) % len(padre1) # Comando para que sea ciclico el indexado.
    # Devolvemos los hijos generados.
    return hijo1, hijo2

#-----------------
# Crossover - PMX.
#-----------------

def crossover_cruce_PMX(padre1, padre2):
    # Generamos dos puntos de corte aleatorios.
    cut1 = random.randint(0, len(padre1)-1)
    cut2 = random.randint(0, len(padre2)-1)
    # Nos aseguramos de que los puntos de corte sean distintos.
    while cut2 == cut1:
        cut2 = random.randint(0, len(padre1)-1)
    # Nos aseguramos de que cut1 es menor que cut2.
    if cut1 > cut2:
        cut1, cut2 = cut2, cut1
    # Creamos una copia de los padres.
    hijo1 = padre1.copy()
    hijo2 = padre2.copy()
    # Generamos los segmentos de los padres que serán intercambiados.
    segmento1 = padre1[cut1:cut2+1]
    segmento2 = padre2[cut1:cut2+1]
    # Realizamos el intercambio de los segmentos en los hijos.
    hijo1[cut1:cut2+1] = segmento2
    hijo2[cut1:cut2+1] = segmento1
    # Realizamos la asignación de los elementos que no están en los segmentos.
    for i in range(len(hijo1)):
        if i < cut1 or i > cut2:
            while hijo1[i] in segmento2:
                index = segmento2.index(hijo1[i])
                hijo1[i] = segmento1[index]
            while hijo2[i] in segmento1:
                index = segmento1.index(hijo2[i])
                hijo2[i] = segmento2[index]
    # Devolvemos los hijos generados.
    return hijo1, hijo2

#---------------------------------
# Función de mutación - Inserción.
#---------------------------------

def mutacion(individuo): # Función de mutación (intercambio aleatorio de 2 genes).
    elementos = random.sample(individuo, 2) # Tomamos dos elementos aleatorios.
    indice1 = individuo.index(elementos[0]) # Buscamos sus indices.
    indice2 = individuo.index(elementos[1])
    aux = individuo
    individuo[indice1], individuo[indice2] = aux[indice2], aux[indice1] # Intercambiamos.
    return individuo

#-----------------------------
# Configuración del algoritmo.
#-----------------------------

TAMANO_POBLACION = 10
GENERACIONES = 10
PROBABILIDAD_MUTACION = 0.3
poblacion = [] # Lista vacia que almacenará la población.

#==================
# Bloque principal.
#==================

#---------------
# Toma de datos.
#---------------

posiciones_estantes = posiciones_originales()
ordenes = lectura_de_ordenes(5)
ordenes = ordenes[:5] # Solo tomo 10 ordenes.
# Eliminamos producto P0. No se contempla esa numeración.
for orden in ordenes:
    for elemento in orden:
        if elemento == 'P0':
            orden.remove(elemento)

#-----------------------
# Leemos las distancias.
#-----------------------

distancias = leer_distancias()

#------------------------------------
# Inicializamos la población inicial.
#------------------------------------

for i in range(TAMANO_POBLACION):
    lista = list(posiciones_estantes.keys()).copy()
    random.shuffle(lista)
    poblacion.append(lista)

print('Poblacion incial lista')

# Mejor individuo histórico.
mejor_individuo_historico = poblacion[0].copy()
mejor_fitness_historico = fitness(mejor_individuo_historico, list(posiciones_estantes.values()), distancias, ordenes)

#-----------------------
# Ciclo de optimización.
#-----------------------

print('='*100)
print('-'*40,'Algoritmo genético','-'*40)
print('='*100)

for generacion in range(GENERACIONES):
    print('*'*100)
    print('-'*43,'Generacion {}'.format(generacion),'-'*43)
    print('*'*100)
    # Calculo del fitness.
    lista_fitness = [] # Lista para el fitness de los individuos.
    print('(Calculando fitness...)')
    j = 0 # Contador de individuos en el calculo de fitness.
    for individuo in poblacion: # Calculo el fitness de cada individuo.
        j += 1
        fitness_individuo = fitness(individuo, list(posiciones_estantes.values()), distancias, ordenes)
        lista_fitness.append(fitness_individuo)
        print('Calculo fitness individuo {} listo.'.format(j))
        print('Fitness del individuo:', (-1)*fitness_individuo)
    # Seleccionamos los padres.
    padres = [] # Lista para los padres.
    print('(Seleccionando padres...)')
    for _ in range(TAMANO_POBLACION // 2):
        candidatos = seleccion_2_mejores(poblacion, lista_fitness) # Padres seleccionados.
        padres.append(candidatos[0]) # Agregamos los padres elegidos a la lista.
        padres.append(candidatos[1])
    # Cruzamos.
    cruces = [] # Lista para los hijos.
    print('(Realizando cruces...)')
    for i in range(0,len(padres)-1,2):
        hijo1, hijo2 = crossover_cruce_de_orden(padres[i],padres[i+1])
        cruces.append(hijo1)
        cruces.append(hijo2)
    # Mejor individuo de la población.
    fitness_population = [ -f for f in lista_fitness]
    mejor_individuo = poblacion[0]
    fitness_mejor = lista_fitness[0]
    for i in range(len(poblacion)):
        fitness_i = lista_fitness[i]
        if fitness_i > fitness_mejor:
            mejor_individuo = poblacion[i]
            fitness_mejor = fitness_i
    # Comprobamos si es el mejor historico.
    if fitness_mejor > mejor_fitness_historico:
        mejor_fitness_historico = mejor_individuo
        mejor_fitness_historico = fitness_mejor
    # Imprimimos el mejor individuo de la generación
    print('(Resultados)')
    print("Generacion:", generacion) 
    print("Mejor individuo:", mejor_individuo)
    print("Fitness:", (-1)*fitness_mejor)
    # Actualizamos la población a los hijos.
    poblacion.clear() # Vaciamos la lista población.
    poblacion = cruces.copy() # La hacemos igual a la lista de hijos.
    # Mutamos.
    poblacion = [mutacion(i) if random.random() < PROBABILIDAD_MUTACION else i for i in cruces]
    # Limpiamos variables.
    lista_fitness.clear()
    padres.clear()
    cruces.clear()

# Printeamos el mejor individuo historico.
print('='*100)
print('-'*36,'Mejor individuo historico','-'*37)
print('='*100)
print("Mejor individuo historico:", mejor_individuo_historico)
print("Fitness:", (-1)*mejor_fitness_historico)