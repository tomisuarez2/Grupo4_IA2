from MLP_Clasificacion import inicializar_pesos, train, clasificar
from calculo_precision import calcular_precision
import numpy as np
import matplotlib.pyplot as plt

# Se usan los sets 1,2 y 3 para ejemplos con 3 clases, los sets 4,5 y 6 para ejemplos de 3 clases.
# Los sets se corresponden con entrenamiento, test y validación respectivamente.
# Recordar cambiar el número de clases en cada ejemplo.

numero_clases = 3 

#=============================
# Realizamos el entrenamiento.
#=============================

# Tomamos un set de datos para entrenar.

set_entrenamiento = '1'

datos_training = np.load('set_n_'+set_entrenamiento+'.npz')
x_training = datos_training['arr_0']
t_training = datos_training['arr_1']

graficar_datos_training = True

# Graficamos los datos si es necesario.
if graficar_datos_training:
    # Parametro: "c": color (un color distinto para cada clase en t).
    plt.figure()
    plt.scatter(x_training[:, 0], x_training[:, 1], c=t_training)
    plt.title('Datos de entrenamiento')
    plt.show()
    
# Inicializamos pesos de la red.
NEURONAS_CAPA_OCULTA = 100
NEURONAS_ENTRADA = 2
pesos_iniciales = inicializar_pesos(n_entrada=NEURONAS_ENTRADA, n_capa_2=NEURONAS_CAPA_OCULTA, n_capa_3=numero_clases)

#====================================
# Carga de los datos para validación.
#====================================

set_validacion = '3'

datos_validacion = np.load('set_n_'+set_validacion+'.npz')
x_validacion = datos_validacion['arr_0']
t_validacion = datos_validacion['arr_1']

# Entrena.
LEARNING_RATE=1
EPOCHS=10000
N = 200 # Cada cuantos epochs realizamos la verificación con el set de validación.
tolerancia_validacion = 1e-1
pesos_entrenados, loss_de_entrenamiento = train(x_training, t_training, x_validacion, t_validacion, pesos_iniciales, LEARNING_RATE, EPOCHS, N, tolerancia_validacion)

#======================================
# Clasificamos el set de datos de test.
#======================================

# Tomamos un set de datos para realizar el test, en este caso el set n°2.

set_test = '2'

datos_test = np.load('set_n_'+set_test+'.npz')
x_test = datos_test['arr_0']
t_test = datos_test['arr_1']

graficar_datos_test = True

# Graficamos los datos si es necesario.
if graficar_datos_test:
    # Parametro: "c": color (un color distinto para cada clase en t).
    plt.figure()
    plt.scatter(x_test[:, 0], x_test[:, 1], c=t_test)
    plt.title('Datos de test')
    plt.show()

# Clasificamos.
resultado_clasificacion = clasificar(x_test,pesos_entrenados)

#=========================
# Calculamos la precisión.
#=========================

precision = calcular_precision(resultado_clasificacion,t_test)
precision = round(precision,2) # Redondeamos la precisión a dos decimales.

print('La precisión porcentual calculada es del',precision,'%.\n')

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


