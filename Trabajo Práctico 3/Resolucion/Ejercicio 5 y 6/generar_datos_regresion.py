import numpy as np

# Script para la creación de sets de datos.

numero_set = '2'
cantidad_ejemplos = 1000

lineal = False
senoidal = False
funcion_3d = True

if lineal:

    #==============================================
    # Ejemplo para regresión de una función lineal.
    #==============================================

    x = np.linspace(-1, 1, cantidad_ejemplos)

    randomgen = np.random.default_rng() # Generador de números aleatorios de mayor calidad.

    t = 2*x + 0.1*randomgen.standard_normal(size=cantidad_ejemplos)

    x = np.reshape(x, (cantidad_ejemplos, 1)) # Transformamos el array de una dimension en una matriz columna.
    t = np.reshape(t, (cantidad_ejemplos, 1)) 

    np.savez('set_regresion_lineal_n_'+numero_set+'.npz',x,t)

#==================
# Función senoidal.
#==================

if senoidal:

    #================================================
    # Ejemplo para regresión de una función senoidal.
    #================================================

    x = np.linspace(-1, 1, cantidad_ejemplos)

    randomgen = np.random.default_rng() # Generador de números aleatorios de mayor calidad.

    t = 2*np.sin(x) + 0.05*randomgen.standard_normal(size=cantidad_ejemplos)

    x = np.reshape(x, (cantidad_ejemplos, 1)) # Transformamos el array de una dimension en una matriz columna.
    t = np.reshape(t, (cantidad_ejemplos, 1)) 

    np.savez('set_regresion_senoidal_n_'+numero_set+'.npz',x,t)

if funcion_3d:

    #==========================================
    # Ejemplo para regresión de una función 3d.
    #==========================================

    def surface_func_sin(x, y):
        return np.sin(np.sqrt(x**2 + y**2))
    
    def surface_func_cos(x, y):
        return np.cos(np.sqrt(x**2 + y**2)) / (np.sqrt(x**2 + y**2) + 1)

    # Generar los datos de entrenamiento
    valores_en_x = np.random.uniform(-5, 5, (cantidad_ejemplos, 1))
    valores_en_y = np.random.uniform(-5, 5, (cantidad_ejemplos, 1))
    x = np.column_stack((valores_en_x,valores_en_y)) # Juntamos los datos en una matriz de dos columnas.
    t = surface_func_sin(valores_en_x, valores_en_y) + np.random.normal(0, 0.1, (cantidad_ejemplos, 1))

    np.savez('set_regresion_3d_n_'+numero_set+'.npz',x,t)
    