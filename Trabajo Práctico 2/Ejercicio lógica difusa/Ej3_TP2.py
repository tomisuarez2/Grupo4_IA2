from Borrosificador import borrosificador
from particiones_borrosas import *
from Respuesta_sistema import respuesta_sistema, calculo_aceleracion
from controlador import controlador_difuso
import matplotlib.pyplot as plt

#================
# Base de reglas.
#================

reglas = {"NP":{"NP":"NP","Z":"NP","PP":"Z"},  # Reglas aplicadas a modo de diccionario, de modo que siendo primer
          "Z":{"NP":"NP","Z":"Z","PP":"PP"},   # elemento la velocidad y el segundo la posición, se obtiene el 
          "PP":{"NP":"Z","Z":"PP","PP":"PP"}}  # consecuente de la regla. Ej: reglas['Z']['Z'] = 'Z'.

#=======================================
# Defino posición y velocidad iniciales.
#=======================================

posicion_inicial = 2.5*pi/180 
velocidad_inicial = 0
fuerza_inicial = 0
aceleracion_inicial = calculo_aceleracion(posicion_inicial, velocidad_inicial, fuerza_inicial)
dt = 0.001 # Incremento de tiempo.
num_iter = 0 # Contador de iteraciones.

historia_posicion = [] # Lista para graficar la posición.
historia_posicion.append(posicion_inicial)
historia_velocidad = [] # Lista para graficar la velocidad.
historia_velocidad.append(velocidad_inicial)
historia_aceleracion = [] # Lista para graficar la aceleración.
historia_aceleracion.append(aceleracion_inicial)
historia_fuerza = [] # Lista para graficar la fuerza aplicada.
historia_fuerza.append(fuerza_inicial)
tiempo = [] # Lista para el tiempo.
tiempo.append(0.0) # Tiempo inicial.

#--------------------------------------------------------
# Renombrado de variables para entrar en bucle iterativo.
#--------------------------------------------------------

posicion = posicion_inicial
velocidad = velocidad_inicial
aceleracion = aceleracion_inicial

#========================================
# Iteraciones hasta lograr el equilibrio.
#========================================

flag = 1 # Flag para seguir iterando.
num_iter_max = 1000000 # Numero máximo de iteraciones.

while flag == 1:

    #-------------------------
    # Contador de iteraciones.
    #-------------------------

    num_iter += 1

    #-----------------
    # Borrosificación.
    #-----------------

    pert_posicion = borrosificador(posicion, dominio_posicion)
    pert_velocidad = borrosificador(velocidad, dominio_velocidad)

    #-------------------------------------
    # Motor de inferencia y desfusicación.
    #-------------------------------------

    fuerza = controlador_difuso(pert_posicion, pert_velocidad, funcion_pertencia_fuerza, rango_conjunto_fuerza, dom_frzas, reglas)

    #-----------------------------
    # Actualización de magnitudes.
    #-----------------------------

    acel_nueva, vel_nueva, pos_nueva = respuesta_sistema(posicion, velocidad, fuerza, dt)
    posicion = pos_nueva
    velocidad = vel_nueva
    aceleracion = acel_nueva

    #--------------------------------------
    # Guardado de magnitudes para graficar.
    #--------------------------------------

    historia_posicion.append(posicion)
    historia_velocidad.append(velocidad)
    historia_aceleracion.append(aceleracion)
    historia_fuerza.append(fuerza)
    tiempo.append(num_iter*dt)

    #-----------------------
    # Condiciones de parada.
    #-----------------------

    if (abs(posicion) < 1e-5) and (abs(velocidad) < 1e-5) and (abs(aceleracion) < 1e-5): # Si llegamos al equilibrio, dejamos de iterar.
        flag = 0

    if num_iter == num_iter_max: # Si llegamos al número máximo de iteraciones, dejamos de iterar.
        flag = 0

#==========================
# Estadísticas del control.
#==========================

print("Se llego al equilibrio en el instante: ", num_iter*dt)

#=======================
# Ploteo de resultados.
#=======================

plt.figure(1)
plt.plot(tiempo, historia_posicion)
plt.grid(True)
plt.xlabel('Tiempo [s]')
plt.ylabel('Posición angular [rad]')
plt.title('Gráfica de la posición angular vs tiempo')
plt.show()

plt.figure(2)
plt.plot(tiempo, historia_velocidad)
plt.grid(True)
plt.xlabel('Tiempo [s]')
plt.ylabel('Velocidad angular [rad/s]')
plt.title('Gráfica de la velocidad angular vs tiempo')
plt.show()

plt.figure(3)
plt.plot(tiempo, historia_aceleracion)
plt.grid(True)
plt.xlabel('Tiempo [s]')
plt.ylabel('Aceleración angular [rad/s^2]')
plt.title('Gráfica de la aceleración angular vs tiempo')
plt.show()

plt.figure(4)
plt.plot(tiempo, historia_fuerza)
plt.grid(True)
plt.xlabel('Tiempo [s]')
plt.ylabel('Fuerza del carro [N]')
plt.title('Gráfica de la fuerza aplicada vs tiempo')
plt.show()