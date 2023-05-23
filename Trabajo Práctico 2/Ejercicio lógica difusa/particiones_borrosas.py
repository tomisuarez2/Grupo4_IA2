from scipy import constants
import numpy as np
from funcion import funcion_triangular

pi = constants.pi

#---------------------------------------------
# Conjuntos borrosos para todas las variables.
#---------------------------------------------

terminos = ["NP","Z","PP"] # Nombres de los conjuntos borrosos, valores que puede tomar la variable lingüistica.

#=====================================================
# Dominio variables lingüisticas de entrada y salidas.
#=====================================================

dominio_posicion = [[-10*pi/180,0], # Considero 10° como el ángulo máximo que se podría mover, de ahí saco el dominio en radianes.
                    [-5*pi/180,5*pi/180],
                    [0,10*pi/180]] 

dominio_velocidad = [[-20*pi/180,0], # Movimiento (+) a derecha y (-) a izquierda (en rad/s). Multiplico 10° entre por dos para sacar los extremos del dominio.
                     [-10*pi/180,10*pi/180],
                     [0,20*pi/180]] 

dom_frzas = [[-8.0,0.0], # Considero que la fuerza máxima es de 8N. (-) si se aplica a izquierda y (+) si es a derecha.
             [-4.0,4.0],
             [0.0,8.0]] 

#=============================================
# Rango de cada conjunto borroso de la fuerza.
#=============================================

funcion_pertencia_fuerza = {} # Diccionario que posteriormente almacenará la función de pertenencia de cada conjunto de la fuerza.
rango_conjunto_fuerza = {} # Diccionario que posteriormente guardará el dominio de cada conjunto borroso de la fuerza.

rango_total = np.arange(dom_frzas[0][0], dom_frzas[-1][1]+0.1, 0.1) # Todos los valores dentro del domino de la fuerza, con incrementos de 0.1. Se hace hasta el extremo mas 0.1 para que incluya al extremo.
rango_total_fuerza = [] # Igual que antes pero redondeado.
for elemento in rango_total:
    rango_total_fuerza.append(round(elemento,1))

for i in range(len(terminos)):
    pertenencia_fuerza = [] # Lista para guardar la función de pertencia de cada conjunto.
    rango = [] # Lista que guarda el rango de la variable lingüistica en cada conjunto.
    ancho = dom_frzas[i][1] - dom_frzas[i][0] # Es el mismo ancho para todos los conjuntos de la fuerza.
    centro = dom_frzas[i][0] + ancho/2 # Varía segun que triángulo sea.
    for xx in rango_total_fuerza: # Rango de la fuerza.
        if (xx <= centro + ancho/2) and (xx >= centro - ancho/2): # Verifico que el valor este dentro del conjunto borroso.
            pertenencia_fuerza.append(round(funcion_triangular(centro,ancho,xx),4)) # Redondeo para evitar errores númericos.
            rango.append(xx)
    funcion_pertencia_fuerza[terminos[i]] = pertenencia_fuerza # Obtengo un diccionario con la siguiente forma {"NP":valor funcion, "Z":valor funcion, "PP":valor funcion}
    rango_conjunto_fuerza[terminos[i]] = rango # Obtengo un diccionario con la siguiente forma {"NP":rango del conjunto, "Z":rango del conjunto, "PP":rango del conjunto}