#-------------------------------------------------------
# Función de pertenencia según borrosificador singleton.
#-------------------------------------------------------

def funcion_triangular(centro,ancho,x):
    altura = 1
    if x >= centro:
        y = altura*(centro + ancho/2 - x)/(ancho/2) 
        return y
    else:
        y = altura*(x - centro + ancho/2)/(ancho/2)
    return y
