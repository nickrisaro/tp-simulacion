import Ejercicio01 as generador
import numpy as np
import matplotlib.pyplot as plot
import sys

def lanzarDado(generadorUnitario):
    a = 1
    b = 6 + 1
    alpha = b-a
    beta = a
    x = generadorUnitario.generar()
    return int(alpha*x + beta)

def main():
    print("TP 1 - Ejercicio 2")
    print("a) El espacio muestral es [2,12]")
    generadorUnitario = generador.GCL(unitario=True)

    print("b) genero 10000 pares de lanzamientos")
    x = np.array([])
    for i in range(0, 10000):
        dado1 = lanzarDado(generadorUnitario)
        dado2 = lanzarDado(generadorUnitario)
        x =np.append(x, dado1 + dado2)

    print("c) grafico en un histograma las sumas obtenidas")
    plot.hist(x, bins=[2,3,4,5,6,7,8,9,10,11,12,13])
    plot.savefig(sys.path[0] + "/E02-histograma.png")
    print("El histograma se guardó en {0}/E02-histograma.png".format(sys.path[0]))

if __name__ == "__main__":
    main()