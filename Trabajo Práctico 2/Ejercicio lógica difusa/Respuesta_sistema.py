import numpy as np
from scipy import constants

#============================================
# Comportamiento del sistema carro - péndulo.
#============================================

M_CARRITO = 2 # Masa del carro
M_PERTIGA = 1 # Masa de la pertiga
L = 1 # Longitud dela pertiga

def respuesta_sistema(theta, v, fuerza, dt):
    
    a = calculo_aceleracion(theta, v, fuerza)
    v = v + a * dt
    theta = theta + v * dt + a * np.power(dt, 2) / 2

    return a, v, theta

def calculo_aceleracion(theta, v, f):

    numerador = constants.g * np.sin(theta) + np.cos(theta) * ((-f - M_PERTIGA * L * np.power(v, 2) * np.sin(theta)) / (M_CARRITO + M_PERTIGA))
    denominador = L * (4/3 - (M_PERTIGA * np.power(np.cos(theta), 2) / (M_CARRITO + M_PERTIGA)))
    
    return numerador / denominador