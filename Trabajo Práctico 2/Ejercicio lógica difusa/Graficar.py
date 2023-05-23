import matplotlib.pyplot as plt
import numpy as np
from scipy import constants
from funcion import funcion_triangular
from particiones_borrosas import *

pi=constants.pi

#ancho=dom_frzas[0][1]-dom_frzas[0][0]
#ancho=dominio_posicion[0][1]-dominio_posicion[0][0]
ancho=dominio_velocidad[0][1]-dominio_velocidad[0][0]
a=dominio_velocidad[0][0]
b=dominio_velocidad[2][1]
#a = dom_frzas[0][0]
#b = dom_frzas[2][1]
#a=dominio_posicion[0][0]
#b=dominio_posicion[2][1]
centro=[]
for i in range(3):
    centro.append(dominio_velocidad[i][0]+ancho/2)
x=np.linspace(a,b,1000)
y1=np.array([funcion_triangular(centro[0],ancho,t) for t in x])
y2=np.array([funcion_triangular(centro[1],ancho,t) for t in x])
y3=np.array([funcion_triangular(centro[2],ancho,t) for t in x])
plt.ylim(0,1.1)
plt.plot(x,y1,color='green')
plt.plot(x,y2,color='green')
plt.plot(x,y3,color='green')
plt.ylabel('Pertenencia')
plt.xlabel('Velocidad (rad/s)')
plt.show()