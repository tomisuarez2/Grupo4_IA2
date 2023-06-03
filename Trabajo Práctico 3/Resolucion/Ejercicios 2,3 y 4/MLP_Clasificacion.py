import numpy as np
import matplotlib.pyplot as plt

# Generador basado en ejemplo del curso CS231 de Stanford: 
# CS231n Convolutional Neural Networks for Visual Recognition
# (https://cs231n.github.io/neural-networks-case-study/)


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


def ejecutar_adelante(x, pesos):

    # Función para proporcionar entradas y permitir que estas entradas vayan propagandose hacia delante hasta
    # propocionar una salida.

    # Se proporciona el valor de las entradas y los pesos.

    # Funcion de entrada (a.k.a. "regla de propagacion") para la primera capa oculta.
    z = x.dot(pesos["w1"]) + pesos["b1"] # -> Z = X.W1 + B1

    # Funcion de activacion ReLU para la capa oculta (h -> "hidden").
    h = np.maximum(0, z) # -> Toma el máximo entre 0 y cada elemento de Z.

    # Salida de la red (funcion de activacion lineal). Esto incluye la salida de todas
    # las neuronas y para todos los ejemplos proporcionados.
    y = h.dot(pesos["w2"]) + pesos["b2"] # -> Y = H.W2 + B2
    # Se adopta como función g la función identidad.

    return {"z": z, "h": h, "y": y}
    # Recordemos que en el entrenamiento no se clasifica. Es decir, no se predice la clase.


def clasificar(x, pesos):

    # Corremos la red "hacia adelante".
    resultados_feed_forward = ejecutar_adelante(x, pesos)
    # La función anterior retorna un diccionario con 'z', 'h' e 'y'.
    
    # Buscamos la(s) clase(s) con scores mas altos (en caso de que haya mas de una con 
    # el mismo score estas podrian ser varias). Dado que se puede ejecutar en batch (x 
    # podria contener varios ejemplos), buscamos los maximos a lo largo del axis=1 
    # (es decir, por filas).
    max_scores = np.argmax(resultados_feed_forward["y"], axis=1)
    # Recordar que en 'y' cada fila representa los ejemplos y cada columna la salida.

    # Tomamos el primero de los maximos (podria usarse otro criterio, como ser eleccion aleatoria).
    # Nuevamente, dado que max_scores puede contener varios renglones (uno por cada ejemplo),
    # retornamos la primera columna.

    return max_scores

# x: n entradas para cada uno de los m ejemplos(nxm).
# -> Recordemos que cada una de las filas representa un ejemplo de entrenamiento y cada columna
#    representa cada una de las entradas.

# t: salida correcta (target) para cada uno de los m ejemplos (m x 1).
# -> Cada fila de este vector representa la clase correspondiente al ejemplo en cuestión.
# -> El valor que tenemos en cada fila es el índice de la neurona de salida que representa la clase correcta.

# pesos: pesos (W y b)

def train(x, t, x_val, t_val, pesos, learning_rate, epochs, N, tolerancia):

    #====================================
    # Carga de los datos para validación.
    #====================================
    
    x_validacion = x_val
    t_validacion = t_val

    #==========================
    # Función de entrenamiento.
    #==========================

    # Cantidad de filas del conjunto de entrenamiento (i.e. cantidad de ejemplos).
    m = np.size(x, 0) 

    # Creamos un array para guardar los valores de loss de los datos de entrenamiento.
    loss_entrenamiento = np.zeros(epochs) 
    
    for i in range(epochs): # Ejecutamos el algoritmo de entranamiento por cada epoch.

        # Ejecucion de la red hacia adelante.
        resultados_feed_forward = ejecutar_adelante(x, pesos)
        y = resultados_feed_forward["y"]
        h = resultados_feed_forward["h"]
        z = resultados_feed_forward["z"]

        #------------------------------------------------------------
        # Calculos necesarios para el ajuste de los pesos sinápticos.
        #------------------------------------------------------------

        # LOSS

        # Utilizamos como función de pérdida la función Softmax.

        # a. Exponencial de todos los scores.
        exp_scores = np.exp(y)

        # b. Suma de todos los exponenciales de los scores, fila por fila (ejemplo por ejemplo).
        #    Mantenemos las dimensiones (indicamos a NumPy que mantenga la segunda dimension del
        #    arreglo, aunque sea una sola columna, para permitir el broadcast correcto en operaciones
        #    subsiguientes)
        sum_exp_scores = np.sum(exp_scores, axis=1, keepdims=True) # Hacemos la sumatoria fila por fila.

        # c. "Probabilidades": normalizacion de las exponenciales del score de cada clase (dividiendo por 
        #    la suma de exponenciales de todos los scores), fila por fila.
        p = exp_scores / sum_exp_scores

        # d. Calculo de la funcion de perdida global. Solo se usa la probabilidad de la clase correcta, 
        #    que tomamos del array t ("target").
        loss = (1 / m) * np.sum( -np.log( p[range(m), t] ))

        # Guardamos en el vector de loss.
        loss_entrenamiento[i] = loss

        #============================================
        # Parada temprana con conjunto de validación. 
        #============================================

        if (i % N == 0 and i > N): # Cada N epochs realizamos la validación.
            loss_validacion = verificar_loss(x_validacion,t_validacion,pesos) # Buscamos el loss de validación.
            if (loss_entrenamiento[i-1] - loss_validacion) < -1*tolerancia: # Si el loss de validación es mayor.
                print(loss_entrenamiento[i-1] - loss_validacion)
                print('Se detiene el entrenamiento, comienza a aumentar el valor de loss.\n')
                loss_entrenamiento[i] = -1 # Esto es para saber hasta donde graficar.
                break # Detengo el entrenamiento para evitar Overfitting.

        # Extraemos los pesos a variables locales.
        w1 = pesos["w1"]
        b1 = pesos["b1"]
        w2 = pesos["w2"]
        b2 = pesos["b2"]

        # Ajustamos los pesos: Backpropagation
        dL_dy = p                # Para todas las salidas, L' = p (la probabilidad)...
        dL_dy[range(m), t] -= 1  # ... excepto para la clase correcta.
        dL_dy /= m

        dL_dw2 = h.T.dot(dL_dy)                         # Ajuste para w2.
        dL_db2 = np.sum(dL_dy, axis=0, keepdims=True)   # Ajuste para b2.

        dL_dh = dL_dy.dot(w2.T)
        
        dL_dz = dL_dh       # El calculo dL/dz = dL/dh * dh/dz. La funcion "h" es la funcion de activacion de la capa oculta,
        dL_dz[z <= 0] = 0   # para la que usamos ReLU. La derivada de la funcion ReLU: 1(z > 0) (0 en otro caso).

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

def verificar_loss(x_validacion,t_validacion,pesos):

    # Cantidad de filas del conjunto de validación (i.e. cantidad de ejemplos).
    mv = np.size(t_validacion)

    # Ejecucion de la red hacia adelante.
    resultados_feed_forward = ejecutar_adelante(x_validacion, pesos)
    y = resultados_feed_forward["y"]
   
    # LOSS

    # Utilizamos como función de pérdida la función Softmax.

    # a. Exponencial de todos los scores.
    exp_scores = np.exp(y)

    # b. Suma de todos los exponenciales de los scores, fila por fila (ejemplo por ejemplo).
    #    Mantenemos las dimensiones (indicamos a NumPy que mantenga la segunda dimension del
    #    arreglo, aunque sea una sola columna, para permitir el broadcast correcto en operaciones
    #    subsiguientes)
    sum_exp_scores = np.sum(exp_scores, axis=1, keepdims=True) # Hacemos la sumatoria fila por fila.

    # c. "Probabilidades": normalizacion de las exponenciales del score de cada clase (dividiendo por 
    #    la suma de exponenciales de todos los scores), fila por fila.
    p = exp_scores / sum_exp_scores

    # d. Calculo de la funcion de perdida global. Solo se usa la probabilidad de la clase correcta, 
    #    que tomamos del array t ("target").
    loss_validacion = (1 / mv) * np.sum( -np.log( p[range(mv), t_validacion] ))

    return loss_validacion




