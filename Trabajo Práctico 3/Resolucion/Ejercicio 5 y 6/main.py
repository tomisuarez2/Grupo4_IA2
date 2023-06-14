from MLP_Regresion import inicializar_pesos, train, regresion, ejecutar_adelante, calcular_RMSE
import numpy as np
import matplotlib.pyplot as plt

salida = 1 # Considero siempre una salida igual a 1 en estos casos.
funcion = 'ReLU' # Defino la función de activación.

#=========================
# Tomamos un set de datos.
#=========================

set_datos = 'set_regresion_lineal_n_1.npz'

datos = np.load(set_datos)
x = datos['arr_0']
t = datos['arr_1']

# Neuronas de entrada.
dimension_x = np.shape(x)
entrada = dimension_x[1] # Busco la cantidad de neuronas de entrada según el ejemplo.

# Dividimos los datos en conjuntos de entrenamiento y prueba.

m = np.size(x, 0) # Cantidad de ejemplos del set.

n1 = int(0.6*m) # Divisor en el número de datos para training.
n2 = int(0.2*m) # Divisor en el número de datos para test y validación.

# Divido el set de datos en training, validación y test.

x_training = x[:n1]
x_validacion = x[n1:(n1+n2)]
x_test = x[(n1+n2):]
t_training = t[:n1]
t_validacion = t[n1:(n1+n2)]
t_test = t[(n1+n2):]


#=============================
# Realizamos el entrenamiento.
#=============================

graficar_datos_training = True

# Graficamos los datos si es necesario.
if graficar_datos_training:
    fig = plt.figure()
    # Corroboro la dimensión de los datos.
    if entrada == 1:
        plt.scatter(x_training, t_training, c='blue') # Para 2d.
    elif entrada == 2:
        ax = fig.add_subplot(111, projection='3d') # Para 3d.
        plt.scatter(x_training[:,0],x_training[:,1], t_training, c='blue') # Para 3d.
    plt.title('Datos de entrenamiento')
    plt.show()
    
# Inicializamos pesos de la red.
NEURONAS_CAPA_OCULTA = 100
pesos_iniciales = inicializar_pesos(n_entrada=entrada, n_capa_2=NEURONAS_CAPA_OCULTA, n_capa_3=salida)

# Entrena.
LEARNING_RATE = 0.5
EPOCHS = 1000
N = 50 # Cada cuantos epochs realizamos la verificación con el set de validación.
tolerancia_validacion = 1
pesos_entrenados, loss_de_entrenamiento = train(x_training, t_training, x_validacion, t_validacion, pesos_iniciales, LEARNING_RATE, EPOCHS, N, tolerancia_validacion, funcion)

#====================================
# Utilizamos el set de datos de test.
#====================================

# Ejecutamos hacia delante.

resultado = regresion(x_test,pesos_entrenados,funcion)

graficar_regresion = True

# Graficamos los datos si es necesario.

if graficar_regresion:
    fig = plt.figure()
    # Corroboro la dimensión de los datos.
    if entrada == 1:
        plt.scatter(x_test, t_test, c='blue', label='Valor target') # Para 2d.
        plt.scatter(x_test, resultado, c='red', label='Valor de regresion') # Para 2d.
    elif entrada == 2:
        ax = fig.add_subplot(111, projection='3d') # Para 3d.
        plt.scatter(x_test[:,0], x_test[:,1], t_test, c='blue', label='Valor target') # Para 3d.
        plt.scatter(x_test[:,0], x_test[:,1], resultado, c='red', label='Valor de regresion') # Para 3d.
    plt.title('Resultados de la regresión')
    plt.legend()
    plt.show()

#====================
# Calculamos el RMSE.
#====================

valor_rmse = calcular_RMSE(resultado,t_test)
valor_rmse = round(valor_rmse,2) # Redondeamos la precisión a dos decimales.

print('El valor RMSE de los resultados predichos es:',valor_rmse,'\n')

#==================================================
# Graficamos los valores de loss del entrenamiento.
#==================================================

plt.figure()
indice = np.where(loss_de_entrenamiento == -1)
if np.size(indice) != 0:
    plt.plot(loss_de_entrenamiento[:int(indice[0])], c='blue', label = 'Training')
else:
    plt.plot(loss_de_entrenamiento, c='blue', label = 'Training')
plt.title('Loss')
plt.xlabel('Epochs')
plt.ylabel('Error')
plt.legend()
plt.grid(True)
plt.show()


