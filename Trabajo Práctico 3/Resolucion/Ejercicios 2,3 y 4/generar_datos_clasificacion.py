#=====================================================
# Script para generar los datos de las clasifiaciones.
#=====================================================

# Script que se utilizará para la creación de sets de datos, tanto para entrenamiento, como validación o test.

"""
Basado en la función provista por el profesor, los sets de datos se guardan para ser utilizados posteriormente.
Se debe especificar numero de clases, cantidad de ejemplos, el numero de set y los factores de angulo y amplitud.
"""

import numpy as np

numero_set = '6'

cantidad_ejemplos = 100
cantidad_clases = 5

FACTOR_ANGULO = 0.5
AMPLITUD_ALEATORIEDAD = 0.6

# Calculamos la cantidad de puntos por cada clase, asumiendo la misma cantidad para cada 
# una (clases balanceadas).

n = int(cantidad_ejemplos / cantidad_clases)

# Entradas: 2 columnas (x1 y x2).
x = np.zeros((cantidad_ejemplos, 2))
# Salida deseada ("target"): 1 columna que contendra la clase correspondiente (codificada como un entero).
t = np.zeros(cantidad_ejemplos, dtype="uint8")  # 1 columna: la clase correspondiente (t -> "target").

randomgen = np.random.default_rng() # Generador de números aleatorios de mayor calidad.

# Por cada clase (que va de 0 a cantidad_clases)...
for clase in range(cantidad_clases):
    # Tomando la ecuación parametrica del circulo (x = r * cos(t), y = r * sin(t)), generamos 
    # radios distribuidos uniformemente entre 0 y 1 para la clase actual, y agregamos un poco de
    # aleatoriedad.
    radios = np.linspace(0, 1, n) + AMPLITUD_ALEATORIEDAD * randomgen.standard_normal(size=n)

    # ... y angulos distribuidos tambien uniformemente, con un desfasaje por cada clase.
    angulos = np.linspace(clase * np.pi * FACTOR_ANGULO, (clase + 1) * np.pi * FACTOR_ANGULO, n)

    # Generamos un rango con los subindices de cada punto de esta clase. Este rango se va
    # desplazando para cada clase: para la primera clase los indices estan en [0, n-1], para
    # la segunda clase estan en [n, (2 * n) - 1], etc.
    indices = range(clase * n, (clase + 1) * n)

    # Generamos las "entradas", los valores de las variables independientes. Las variables:
    # radios, angulos e indices tienen n elementos cada una, por lo que le estamos agregando
    # tambien n elementos a la variable x (que incorpora ambas entradas, x1 y x2).
    x1 = radios * np.sin(angulos)
    x2 = radios * np.cos(angulos)
    x[indices] = np.c_[x1, x2] # Concatena los vectores argumentos en una matriz de dos columnas, una por cada vector.

    # Guardamos el valor de la clase que le vamos a asociar a las entradas x1 y x2 que acabamos
    # de generar.

    t[indices] = clase

#---------------------------------------
# Guardamos los sets de datos generados.
#---------------------------------------

np.savez('set_n_'+numero_set+'.npz',x,t)

    