import numpy as np
import matplotlib.pyplot as plot
import sys

class GCL:

    def __init__(self, a = 1013904223, c = 1664525, m = np.power(2, 32), x0 = 1013904223):
        self.a = a
        self.c = c
        self.m = m
        self.x0 = x0
        self.xActual = x0

    def generar(self):
        self.xActual = (self.a*self.xActual + self.c) % self.m
        return self.xActual

def main():
    print("TP 1 - Ejercicio 1")
    padrones = np.array([84623, 95042, 95099, 95512])
    promedioPadrones = np.average(padrones)

    generador = GCL(x0 = int(promedioPadrones))
    print("a) un Generador Congruencial Lineal de módulo 2^32, multiplicador 1013904223, incremento de 1664525 y semilla {0}".format(int(promedioPadrones)))
    for i in range(0, 10):
        print("{0} - {1}".format(i, generador.generar()))

    generador = GCL(x0 = promedioPadrones, c = 0.1664525, m = 1)
    print("b) para que devuelva números entre 0 y 1 utilizo módulo 1, multiplicador 1013904223, incremento de 0.1664525 y semilla {0}".format(promedioPadrones))
    print("c) Genero 100000 valores con los parámetros de b y los grafico en un histograma")
    x = np.array([])
    for i in range(0, 100000):
        x = np.append(x, generador.generar())

    plot.hist(x)
    plot.savefig(sys.path[0] + "/E01-histograma.png")
    print("El histograma se guardó en {0}/E01-histograma.png".format(sys.path[0]))

if __name__ == "__main__":
    main()