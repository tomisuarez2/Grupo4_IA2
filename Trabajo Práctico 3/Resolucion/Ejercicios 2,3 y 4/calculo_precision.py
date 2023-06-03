#======================================================
# Script para calcular la precisión de la clasifiación.
#======================================================

def calcular_precision(clasificacion,target):
    sum = 0 # Cantidad de ejemplos clasificados correctamente.
    for i in range(len(clasificacion)): # Buscamos en los resultados de la clasificación.
        if clasificacion[i] == target[i]: # Buscamos cuales han sido clasificados correctamente.
            sum += 1                        # Si se clasifiacaron correctamente, sumamos uno.
    precision = sum/len(clasificacion)*100 # Precisión porcentual = n° de clasificaciones correctas/n° total de clasificaciones.
    return precision