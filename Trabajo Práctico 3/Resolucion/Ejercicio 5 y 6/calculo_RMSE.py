import numpy as np

def calcular_RMSE(resultado,target):
    # Calculamos el error cuadrático medio (MSE) entre el resultado y el target.
    mse = np.mean((resultado-target)**2)
    # Calculamos la raiz del error cuadrático medio.
    rmse = np.sqrt(mse)
    return rmse