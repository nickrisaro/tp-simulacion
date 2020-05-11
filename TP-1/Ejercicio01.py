import numpy as np
import matplotlib.pyplot as plot
import sys

class GCL:

    def __init__(self, unitario = False):
        padrones = np.array([84623, 95042, 95099, 95512])
        self.a = 1013904223
        self.c = 1664525
        self.m = np.power(2, 32)
        self.x0 = int(np.average(padrones))
        self.xActual = self.x0
        if unitario:
            self.m = 1
            self.c = 0.1664525

    def generar(self):
        self.xActual = (self.a*self.xActual + self.c) % self.m
        return self.xActual

def main():
    print("TP 1 - Ejercicio 1")

    generador = GCL()
    print("a) Implementar un Generador Congruencial Lineal de módulo {0}, multiplicador {1}, incremento de {2} y semilla {3}"
            .format(generador.m, generador.a, generador.c, generador.x0))
    for i in range(0, 10):
        print("{0} - {1}".format(i, generador.generar()))

    generador = GCL(unitario = True)
    print("b) para que devuelva números entre 0 y 1 utilizo módulo {0}, multiplicador {1}, incremento de {2} y semilla {3}"
            .format(generador.m, generador.a, generador.c, generador.x0))
    print("c) Genero 100000 valores con los parámetros de b y los grafico en un histograma")
    x = np.array([])
    for i in range(0, 100000):
        x = np.append(x, generador.generar())

    plot.hist(x)
    plot.savefig(sys.path[0] + "/E01-histograma.png")
    print("El histograma se guardó en {0}/E01-histograma.png".format(sys.path[0]))

if __name__ == "__main__":
    main()