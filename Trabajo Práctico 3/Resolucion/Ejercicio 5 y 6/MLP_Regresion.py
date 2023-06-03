import numpy as np
import matplotlib.pyplot as plt

def calcular_RMSE(resultado,target):
    # Calculamos el error cuadrático medio (MSE) entre el resultado y el target.
    mse = np.mean((resultado-target)**2)
    # Calculamos la raiz del error cuadrático medio.
    rmse = np.sqrt(mse)
    return rmse

def sigmoide(x):
    """
    Función de activación sigmoide.
    """
    return 1 / (1 + np.exp(-x))

def inicializar_pesos(n_entrada, n_capa_2, n_capa_3):

    # Inicializamos pesos sinápticos, w1 y w1, pero también los sesgos b1 y b2.

    randomgen = np.random.default_rng() # Instanciamos una clase generadora de números aleatorios.

    # Incializamos pesos sináputicos y sesgos a partir de una distribución de probabilidad estándar.
    # Los escalamos porque son muy grandes.

    w1 = 0.1 * randomgen.standard_normal((n_entrada, n_capa_2))
    b1 = 0.1 * randomgen.standard_normal((1, n_capa_2))

    w2 = 0.1 * randomgen.standard_normal((n_capa_2, n_capa_3))
    b2 = 0.1 * randomgen.standard_normal((1,n_capa_3))

    # Devolvemos diccionarios con los pesos sinápticos y los sesgos.
    return {"w1": w1, "b1": b1, "w2": w2, "b2": b2}

def ejecutar_adelante(x, pesos, funcion_de_activacion):

    # Función para proporcionar entradas y permitir que estas entradas vayan propagandose hacia delante hasta
    # propocionar una salida.

    # Se proporciona el valor de las entradas y los pesos.
    
    # Funcion de entrada (a.k.a. "regla de propagacion") para la primera capa oculta.
    z = x.dot(pesos["w1"]) + pesos["b1"] # -> Z = X.W1 + B1
 
    # Funcion de activacion ReLU para la capa oculta (h -> "hidden").
    if funcion_de_activacion == 'ReLU':
        h = np.maximum(0, z) # -> Toma el máximo entre 0 y cada elemento de Z.
    elif funcion_de_activacion == 'Sigmoide':
        h = sigmoide(z) # Función de activación sigmoide.

    # Salida de la red (funcion de activacion lineal). Esto incluye la salida de todas
    # las neuronas y para todos los ejemplos proporcionados.
    y = h.dot(pesos["w2"]) + pesos["b2"] # -> Y = H.W2 + B2
    # Se adopta como función g la función identidad.

    return {"z": z, "h": h, "y": y}
    # Recordemos que en el entrenamiento no se clasifica. Es decir, no se predice la clase.

def regresion(x, pesos, funcion_de_activacion):

    # Corremos la red "hacia adelante".
    resultados_feed_forward = ejecutar_adelante(x, pesos, funcion_de_activacion)
    # La función anterior retorna un diccionario con 'z', 'h' e 'y'.
    
    # Retornamos la salida.

    return resultados_feed_forward['y']

# x: n entradas para cada uno de los m ejemplos(nxm).
# -> Recordemos que cada una de las filas representa un ejemplo de entrenamiento y cada columna
#    representa cada una de las entradas.

# t: salida correcta (target) para cada uno de los m ejemplos (m x 1).
# -> Cada fila de este vector representa la clase correspondiente al ejemplo en cuestión.
# -> El valor que tenemos en cada fila es el índice de la neurona de salida que representa la clase correcta.

# pesos: pesos (W y b)

def train(x, t, x_val, t_val, pesos, learning_rate, epochs, N, tolerancia, funcion_de_activacion):

    #====================================
    # Carga de los datos para validación.
    #====================================

    x_validacion = x_val
    t_validacion = t_val

    #==============================================
    # Función de entrenamiento con Backpropagation.
    #==============================================

    # Cantidad de filas del conjunto de entrenamiento (i.e. cantidad de ejemplos).
    m = np.size(x, 0) 

    # Creamos un array para guardar los valores de loss de los datos de entrenamiento.
    loss_entrenamiento = np.zeros(epochs) 
    
    for i in range(epochs): # Ejecutamos el algoritmo de entranamiento por cada epoch.
 
        # Ejecucion de la red hacia adelante.
        resultados_feed_forward = ejecutar_adelante(x, pesos, funcion_de_activacion)
        y = resultados_feed_forward["y"]
        h = resultados_feed_forward["h"]
        z = resultados_feed_forward["z"]

        #------------------------------------------------------------
        # Calculos necesarios para el ajuste de los pesos sinápticos.
        #------------------------------------------------------------

        # LOSS

        # Utilizamos como función de pérdida la función Mean Squared Error (MSE).
        # 't' e 'y' son dos arrays, ambos de tamaño 1xm (creo). Esto significa que ambos tienen una dimensión de longitud 'm'. 
        # (t - y) realiza una resta elemento a elemento entre los arrays 't' e 'y', generando un nuevo array que contiene las diferencias correspondientes.
        # ** 2 aplica el operador de exponenciación elemento a elemento en las diferencias calculadas. Esto eleva cada diferencia al cuadrado.
        # np.mean() calcula la media de los elementos del array resultante de las diferencias al cuadrado. 
        # Como ambos arrays 't' e 'y' tienen la misma dimensión, la función mean() calculará la media de los elementos del array.

        loss = np.mean((y - t)**2)

        # Guardamos en el vector de loss.
        loss_entrenamiento[i] = loss

        #============================================
        # Parada temprana con conjunto de validación. 
        #============================================

        if (i % N == 0 and i > N): # Cada N epochs realizamos la validación.
            loss_validacion = verificar_loss(x_validacion,t_validacion,pesos,funcion_de_activacion)
            if (loss_entrenamiento[i-1] - loss_validacion) < -1*tolerancia:
                print('Se detiene el entrenamiento, comienza a aumentar el valor de loss.\n')
                loss_entrenamiento[i] = -1 # Esto es para saber hasta donde graficar.
                break

        # Extraemos los pesos a variables locales.
        w1 = pesos["w1"]
        b1 = pesos["b1"]
        w2 = pesos["w2"]
        b2 = pesos["b2"]

        # Ajustamos los pesos: Backpropagation

        dL_dy = 2*(y-t)/m        

        dL_dw2 = h.T.dot(dL_dy)                         # Ajuste para w2.
        dL_db2 = np.sum(dL_dy, axis=0, keepdims=True)   # Ajuste para b2.

        dL_dh = dL_dy.dot(w2.T)

        if funcion_de_activacion == 'ReLU': 
            dL_dz = dL_dh       # El calculo dL/dz = dL/dh * dh/dz. La funcion "h" es la funcion de activacion de la capa oculta,
            dL_dz[z <= 0] = 0   # para la que usamos ReLU. La derivada de la funcion ReLU: 1(z > 0) (0 en otro caso).
        elif funcion_de_activacion == 'Sigmoide':
            dh_dz = sigmoide(z)*(1-sigmoide(z)) 
            dL_dz = dL_dh*dh_dz             

        dL_dw1 = x.T.dot(dL_dz)                         # Ajuste para w1.
        dL_db1 = np.sum(dL_dz, axis=0, keepdims=True)   # Ajuste para b1.

        # Aplicamos el ajuste a los pesos.
        w1 += -learning_rate * dL_dw1
        b1 += -learning_rate * dL_db1
        w2 += -learning_rate * dL_dw2
        b2 += -learning_rate * dL_db2

        # Actualizamos la estructura de pesos.
        # Extraemos los pesos a variables locales.
        pesos["w1"] = w1
        pesos["b1"] = b1
        pesos["w2"] = w2
        pesos["b2"] = b2

    # Retornamos los pesos entrenados para la clasifiación y los valores de loss.
    return pesos, loss_entrenamiento 

def verificar_loss(x_validacion,t_validacion,pesos,funcion_de_activacion):

    # Ejecucion de la red hacia adelante.
    resultados_feed_forward = ejecutar_adelante(x_validacion, pesos, funcion_de_activacion)
    y = resultados_feed_forward["y"]

    # LOSS

    # Utilizamos como función de pérdida la función Mean Squared Error (MSE).
    # 't' e 'y' son dos arrays, ambos de tamaño 1xm (creo). Esto significa que ambos tienen una dimensión de longitud 'm'. 
    # (t - y) realiza una resta elemento a elemento entre los arrays 't' e 'y', generando un nuevo array que contiene las diferencias correspondientes.
    # ** 2 aplica el operador de exponenciación elemento a elemento en las diferencias calculadas. Esto eleva cada diferencia al cuadrado.
    # np.mean() calcula la media de los elementos del array resultante de las diferencias al cuadrado. 
    # Como ambos arrays 't' e 'y' tienen la misma dimensión, la función mean() calculará la media de los elementos del array.

    loss_validacion = np.mean((t_validacion-y)**2)

    return loss_validacion

def iniciar(set_de_datos,neuronas_capa_oculta,learning_rate,activacion):

    salida = 1 # Neuronas de salida de la red neuronal.

    #=========================
    # Tomamos un set de datos.
    #=========================

    datos = np.load(set_de_datos)
    x = datos['arr_0']
    t = datos['arr_1']

    # Neurona de entrada.
    dimension_x = np.shape(x)
    entrada = dimension_x[1]

    # Dividimos los datos en conjuntos de entrenamiento y prueba.

    m = np.size(x, 0) # Cantidad de ejemplos del set.

    n1 = int(0.6*m) # Divisor en el número de datos para training.
    n2 = int(0.2*m) # Divisor en el número de datos para test y validación.

    x_training = x[:n1]
    x_validacion = x[n1:(n1+n2)]
    x_test = x[(n1+n2):]
    t_training = t[:n1]
    t_validacion = t[n1:(n1+n2)]
    t_test = t[(n1+n2):]

    #=============================
    # Realizamos el entrenamiento.
    #=============================

    # Inicializamos pesos de la red.
    pesos_iniciales = inicializar_pesos(n_entrada=entrada, n_capa_2=neuronas_capa_oculta, n_capa_3=salida)

    # Entrena.
    EPOCHS = 500
    N = 50 # Cada cuantos epochs realizamos la verificación con el set de validación.
    tolerancia_validacion = 1e-1
    pesos_entrenados, _ = train(x_training, t_training, x_validacion, t_validacion, pesos_iniciales, learning_rate, EPOCHS, N, tolerancia_validacion, activacion)

    #====================================
    # Utilizamos el set de datos de test.
    #====================================

    # Ejecutamos hacia delante.

    resultado = regresion(x_test,pesos_entrenados,activacion)

    #====================
    # Calculamos el RMSE.
    #====================

    valor_rmse = calcular_RMSE(resultado,t_test)
    valor_rmse = round(valor_rmse,2) # Redondeamos la precisión a dos decimales.

    return valor_rmse





