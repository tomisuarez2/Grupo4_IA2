from funcion import funcion_triangular

#==========================
# Borrosificador Singleton.
#==========================

def borrosificador(entrada, dominio): # Busco que valor de pertenencia le corresponde al valor de la variable de entrada que le estoy dando.
    
    terminos = ["NP","Z","PP"] # Conjuntos borrosos para cada variable de entrada.
    pertenencias = {} # Diccionario para guardar los valores de pertenencia a cada conjunto de la entrada.

    if (entrada <= dominio[-1][1]) and (entrada >= dominio[0][0]): # Analizo si la entrada esta dentro del dominio.
        for j in range(len(dominio)): # Itero para cada conjunto borroso.
            ancho = dominio[j][1] - dominio[j][0]
            centro = dominio[j][0] + ancho/2
            if (entrada <= centro + ancho/2) and (entrada >= centro - ancho/2): # Verifico si el valor esta dentro del conjunto borroso analizado.
                valor_pertenencia = funcion_triangular(centro, ancho, entrada) # Obtengo el valor de pertenencia para ese valor de entrada.
                pertenencias[terminos[j]] = valor_pertenencia # Al conjunto borroso correspondiente, le asigno el valor de pertenencia.
    else:
        print('Valor de entrada fuera del dominio correspondiente.') # Mensaje de alerta.

    return pertenencias
