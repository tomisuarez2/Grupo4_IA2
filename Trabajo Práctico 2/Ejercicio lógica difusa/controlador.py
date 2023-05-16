import numpy as np

def controlador_difuso(pert_posicion, pert_velocidad, fcn_pert_frza, rango_conj_frza, dom_frzas, reglas):

    valores_minimos = [] # Lista para almacenar los valores cada antecedente.
    consecuentes = [] # Lista para guardar todos los consecuentes a tener en cuenta.

    #--------------------------------------------------
    # Cálculo del valor de pertenencia del antecedente.
    #--------------------------------------------------

    for p in pert_posicion: # Toma valores como 'NP', 'Z' y 'PP'.
        for v in pert_velocidad: # Toma valores como 'NP', 'Z' y 'PP'.
            valor_min = min([pert_posicion[p], pert_velocidad[v]]) # Cálculo de antecedente por conjunción.
            valores_minimos.append(valor_min) # Añadimos a la lista de valores de antecedentes.
            consecuentes.append(reglas[p][v]) # Guardo los consecuentes de las reglas.

    #---------------------------------------------------------------------------------------------------------
    # Reglas cuyo consecuente se refiere al mismo conjunto borroso de la misma variable lingüística de salida.
    #---------------------------------------------------------------------------------------------------------

    consecuente_NP = []
    consecuente_Z = []  # Listas para los consecuentes iguales.
    consecuente_PP = []

    indices_NP = buscar_indices('NP',consecuentes)
    indices_Z = buscar_indices('Z',consecuentes)  # Buscamos los indices que correspondan a cada consecuente igual.
    indices_PP = buscar_indices('PP',consecuentes)

    for ind in indices_NP:
        consecuente_NP.append(valores_minimos[ind])
    for ind in indices_Z:
        consecuente_Z.append(valores_minimos[ind]) # Agregamos los valores a las listas correspondientes, podrían suceder que no existan antecedentes para los consecuentes.
    for ind in indices_PP:
        consecuente_PP.append(valores_minimos[ind])

    if len(consecuente_NP) != 0:        # Tomamos el valor máximo del consecuente solo si este existe.
        valor_NP = max(consecuente_NP)  
    else:
        valor_NP = 0 # Si no existe el consecuente, lo definimos como 0 para no interferir en los posteriores cálculos.

    if len(consecuente_Z) != 0:         # Tomamos el valor máximo del consecuente solo si este existe.
        valor_Z = max(consecuente_Z)
    else:
        valor_Z = 0 # Si no existe el consecuente, lo definimos como 0 para no interferir en los posteriores cálculos.

    if len(consecuente_PP) != 0:        # Tomamos el valor máximo del consecuente solo si este existe.
        valor_PP = max(consecuente_PP)
    else:
        valor_PP = 0 # Si no existe el consecuente, lo definimos como 0 para no interferir en los posteriores cálculos.

    #----------------------------------------------
    # Truncado de los conjuntos borrosos de salida.
    #----------------------------------------------

    salida_NP = truncacion(fcn_pert_frza['NP'],valor_NP)
    salida_Z = truncacion(fcn_pert_frza['Z'],valor_Z) # Truncado de conjuntos borrosos de salida.
    salida_PP = truncacion(fcn_pert_frza['PP'],valor_PP)

    dic_NP = {}
    dic_Z = {} # Diccionarios que almacenarán el valor de pertenencia de un valor del conjunto luego del truncado.
    dic_PP = {}

    for i in range(len(salida_NP)): # Llenamos los diccionarios.
        dic_NP[rango_conj_frza['NP'][i]] = salida_NP[i]
        dic_Z[rango_conj_frza['Z'][i]] = salida_Z[i]
        dic_PP[rango_conj_frza['PP'][i]] = salida_PP[i]

    #---------------------------------------------
    # Combinación de conjuntos borrosos de sálida.
    #---------------------------------------------

    # Esta combinación se hace con el fin de una hipotetica aplicación de un desborrosificador por centro de gravedad.
    # Hacemos ombinación de conjuntos borrosos de salida mediante t-conorma max().

    conjunto_salida = [] # Conjunto de sálidas.
    rango_total = np.arange(-8.0, 9.0, 0.1) # Es porque el rango de la fuerza va de -8 a 8, con un incremento de 0.1.

    # Uno todos las funciones de pertenencia en un solo conjunto de salida, cuando hay superposición elijo el mayor valor.
    for x in rango_total:
        x = round(x,1) # Redondeo para evitar errores númericos.
        if (x in rango_conj_frza['NP']) and (x not in rango_conj_frza['Z']):
            conjunto_salida.append([x,dic_NP[x]])
        elif (x in rango_conj_frza['NP']) and (x in rango_conj_frza['Z']):
            conjunto_salida.append([x,max(dic_NP[x],dic_Z[x])])
        elif (x in rango_conj_frza['Z']) and (x in rango_conj_frza['PP']):
            conjunto_salida.append([x,max(dic_Z[x],dic_PP[x])])
        elif (x in rango_conj_frza['PP']) and (x not in rango_conj_frza['Z']):
            conjunto_salida.append([x,dic_PP[x]])

    #--------------------
    # Desborrosificación.
    #--------------------

    f_nitido = desborrosificador_media_centros(dom_frzas, valor_NP, valor_Z, valor_PP)     

    return f_nitido


#------------
# Disyunción.
#------------

def maximo(vector1, vector2):
    disyuncion = len(vector1)*[0] # Inicializamos un vector de salida vacío.
    for k in range(len(vector1)):
        if vector1[k] >= vector2[k]:
            disyuncion[k] = vector1[k]
        else:
            disyuncion[k] = vector2[k]
    return disyuncion

#------------
# Conjunción.
#------------

def minimo(vector1,vector2):
    conjuncion = len(vector1)*[0] # Inicializamos un vector de salida vacío.
    for i in range(len(vector1)):
        if vector1[i] <= vector2[i]:
            conjuncion[i] = vector1[i]
        else:
            conjuncion[i] = vector2[i]
    return conjuncion

#------------------------------------------------
# Función de truncado de los conjuntos de salida.
#------------------------------------------------

def truncacion(vector1, valor_min): 
    truncado = len(vector1)*[0] # Inicializamos un vector de salida vacío.
    for k in range(len(vector1)):
        if vector1[k] >= valor_min:
            truncado[k] = valor_min
        else:
            truncado[k] = vector1[k]
    return truncado

#----------------------------------------
# Desborrosificador por media de centros.
#----------------------------------------

def desborrosificador_media_centros(dominio_conj_fuerza, valorNP, valorZ, valorPP): 
    
    # Tomo el valor del centro de cada conjunto borroso y lo multiplico por su grado de pertenencia. 
    # El denominador va a ser la suma de los grados de pertenencia de todos los conjuntos borrosos.
    # Podría suceder que no tengamos valores de pertencia ya que no se encontaron reglas a aplicar, es decir, 
    # no hay consecuentes. En ese caso la fuerza a aplicar es 0, pero asi como se plantea el problema da 
    # error por división por 0 (0/0), con lo cual devolvemos el 0 a mano.

    ancho = dominio_conj_fuerza[0][1] - dominio_conj_fuerza[0][0]
    pesoNP = (dominio_conj_fuerza[0][0] + ancho/2)*valorNP
    pesoZ = (dominio_conj_fuerza[1][0] + ancho/2)*valorZ
    pesoPP = (dominio_conj_fuerza[2][0] + ancho/2)*valorPP
    numerador = pesoNP + pesoZ + pesoPP 
    denominador = valorNP + valorZ + valorPP
    if denominador != 0:
        return numerador/denominador
    else:
        return 0


#----------------------------------------------------
# Función para buscar elementos iguales en una lista.
#----------------------------------------------------

def buscar_indices(elemento, lista):
    return [indice for indice, valor in enumerate(lista) if valor == elemento]
