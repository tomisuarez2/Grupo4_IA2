import random
from lectura_datos import configuracion, posiciones_originales, lectura_de_ordenes # Funciones para leer los datos.

pasillos, entre_estantes = configuracion()
posiciones_estantes = posiciones_originales()
lista = list(posiciones_estantes.keys()).copy()
random.shuffle(lista)
configuracion = dict(zip(lista, list(posiciones_estantes.values()))) # Armamos un diccionario con ambas listas.
#print(calcular_distancias(configuracion, pasillos, entre_estantes))

print(lista)