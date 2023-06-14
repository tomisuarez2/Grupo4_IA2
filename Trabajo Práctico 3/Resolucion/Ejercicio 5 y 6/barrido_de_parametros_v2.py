import numpy as np
from MLP_Regresion import iniciar
import numpy as np
import matplotlib.pyplot as plt

#=======================================================
# Función para obtener todas las combinaciones posibles.
#=======================================================

def obtener_combinaciones(list1, list2, list3):
    """
    Esta función genera todas las combinaciones posibles entre las 3 listas y las devuelve.
    """

    # Obtenemos las longitudes de las listas.
    len1 = len(list1)
    len2 = len(list2)
    len3 = len(list3)

    numero_combinaciones = len1 * len2 * len3 # Número total de combinaciones.
    
    # Generamos todas las combinaciones posibles.
    combinaciones = np.array(np.meshgrid(list1, list2, list3)).T.reshape(-1, 3)
    # Crea un arreglo numpy que contiene todas las combinaciones posibles 
    # de los elementos de las tres listas.
    
    # Mezclamos aleatoriamente las combinaciones.
    np.random.shuffle(combinaciones)
    
    # Devolver la combinación aleatoria y la lista actualizada
    return combinaciones, numero_combinaciones

#==============================================================================
# Función para eliminar una combinación de la lista para no volver a repetirla.
#==============================================================================

def eliminar_fila_aleatoria(matriz):

    # Obtenemos el número total de filas en la matriz.
    num_filas = matriz.shape[0]

    # Generamos un índice aleatorio para seleccionar la fila a eliminar.
    indice_aleatorio = np.random.randint(0, num_filas)

    # Fila a eliminar.
    fila = matriz[indice_aleatorio]

    # Eliminamos la fila seleccionada de la matriz.
    nueva_matriz = np.delete(matriz, indice_aleatorio, axis=0)

    return fila, nueva_matriz

#======================================
# Script para el barrido de parámetros.
#======================================

set_de_datos = 'set_regresion_lineal_n_1.npz'

# Definimos los valores de los hiperparámetros a evaluar.

learning_rates = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
neuronas_capa_oculta = [10,60,110,160,210,260,310,360,410,460,510]
funcion_de_activacion = ["ReLU","Sigmoide"]

combinaciones_posibles, num_comb = obtener_combinaciones(learning_rates,neuronas_capa_oculta,funcion_de_activacion)
# Devuelve un array de (num_comb, 3), donde cada fila es una combinacion, mientras que cada columna es el valor
# correspondiente de la lista.

num_comb = int(0.2*num_comb) # Trabajamos con un menor número de combinaciones dado que son 120.

mejor_configuracion = np.zeros([1,3]) # Array de numpy para guardar la mejor configuracion.

print('='*63)
print('-'*20,'Barrido de parametros','-'*20)
print('='*63)
vector_rmse = np.zeros([num_comb,1]) # Vector para guardar los rmse de cada configuracion.
vector_combinaciones ={} # Vector para guardar las configuraciones.
for j in range(num_comb):

    # Tomo una combinacion aleatoria y la elimino de las posibilidades.
    combinacion, combinaciones_posibles = eliminar_fila_aleatoria(combinaciones_posibles)
    vector_combinaciones[j] = combinacion[:]
    # Printeamos la combinación.
    #print('-'*63)
    #print('Learning Rate:',combinacion[0],'||','Capa oculta:',combinacion[1],'||','Activacion:',combinacion[2])
    rmse_configuracion = iniciar(set_de_datos,int(combinacion[1]),float(combinacion[0]),str(combinacion[2]))
    vector_rmse[j] = rmse_configuracion
    #print('RMSE:', rmse_configuracion)
    #print('-'*63)
print("minimo",np.min(vector_rmse))
print("Valores correspondientes", vector_combinaciones[np.argmin(vector_rmse)]) #argmin() devuelve el indice del minimo valor del vector.
print('='*63)


