import Ejercicio01 as generador
import numpy as np
import mpmath as mp
import numpy.ma as M  
from scipy import interpolate
import matplotlib.pyplot as plot
from scipy.interpolate import interp1d
import sys



def obtenerValorAcumulada(x):
    if (x <= -np.pi/2 ):
        return 0
    if (x > np.pi/2):
        return 1
    a = (13 * x)/ (12 * (np.pi))
    b = (x ** 3) / (3 * (np.pi ** 3))

    y = 1/2 + a - b

    return  y

def obtenerValorDensidad(x):
    if(np.isclose(x,-np.pi/2,atol=0.01,rtol=0.01) or np.isclose(x,np.pi/2,atol=0.01,rtol=0.01)):
        return np.nan
    if(x < -np.pi/2 or x > np.pi/2):
        return 0
    else:
        return (13/12*np.pi)-1/np.power(np.pi,3)*x*x

def construirFuncionDensidad():
    x = np.arange(-5, 5, 0.01)
    y = np.array([])

    for i in x:
        y = np.append(y, obtenerValorDensidad(i))

    return (x, y)

def construirFuncionAcumulada():
    # Para construir la funcion de probabilidad acumulada voy a integrar
    # por cada trozo de la funcion. Formalmente hablando, en cada trozo
    # se integra con los limites de -infinito a x
    x = np.arange(-5, 5, 0.01)
    y = np.array([])

    for i in x:
        y = np.append(y, obtenerValorAcumulada(i))

    return (x, y)

def main():
    print("TP 1 - Ejercicio 3")
    print("a) Graficar la función de densidad de probabilidad")
    x,y = construirFuncionDensidad()

    plot.title('Funcion densidad')
    plot.plot(x, y)
    plot.savefig(sys.path[0] + f"/E03-funcion-densidad.png")

    # Utilizo estas funciones porque al guardar en distintos archivos, el plot sigue con
    # el mismo gráfico que antes.
    plot.clf()
    plot.cla()
    plot.close()
    print(f"La función de densisas se guardó en {sys.path[0]}/E03-funcion-densidad.png")

    print("b) Calcular y graficar la función de probabilidad acumulada y su inversa.")
    x,y = construirFuncionAcumulada()

    plot.title('Funcion probabilidad acumulada')
    plot.plot(x, y, color="#FF4500") 
    plot.savefig(sys.path[0] + f"/E03-funcion-acumulada.png")
    plot.clf()
    plot.cla()
    plot.close()
    print(f"La función de probabilidad acumulada se guardó en {sys.path[0]}/E03-funcion-acumulada.png")

    plot.title('Funcion inversa de la funcion probabilidad acumulada')
    plot.plot(y, x)
    plot.savefig(sys.path[0] + f"/E03-funcion-inversa.png")
    plot.clf()
    plot.cla()
    plot.close()
    print(f"La función inversa se guardó en {sys.path[0]}/E03-funcion-inversa.png")

    inversa = interp1d(y, x)
    uniformes = np.random.uniform(0, 1, 100000) 
    random_array_no_estandar = list(map(lambda x: inversa(x), uniformes)) 
    plot.hist(random_array_no_estandar, bins=10)
    plot.title('Histograma')
    plot.savefig(sys.path[0] + f"/E03-histograma-inversa.png")
    print(f"Histograma de la funcion inversa se guardó en {sys.path[0]}/E03-histograma-inversa.png")

if __name__ == "__main__":
    main()