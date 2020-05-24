# coding=utf-8
import matplotlib.pyplot as plot
import math
import random as rn
import sys
import scipy.stats as stats
import numpy as np

def generar_normal_estandar(x):
    return math.exp(-(x ** 2) / 2) / (math.sqrt(2 * math.pi))

def generar_exponencial(x):
    return math.exp(-x)

def generar_inversa_exponencial(x):
    return -(math.log(x))

def generar_random_array_estandar_aceptados():

    cantidad = 100000

    c = 2*(generar_normal_estandar(1))/generar_exponencial(1) # Derivando fX(x)/fY(y) e igualando a 0 se obtiene x = 1

    numeros = []
    for i in range(cantidad):
        a = generar_inversa_exponencial(rn.random())
        prob_aceptar = generar_normal_estandar(a)/(c * generar_exponencial(a))

        r1 = rn.random()

        if r1 <= prob_aceptar:

            r2 = rn.random()

            if r2 < 0.5:
                numeros.append(a)
            else:
                numeros.append(-a)

    return numeros


def main():
    print("TP 1 - Ejercicio 4")

    print("Aplicando el algoritmo de Aceptación y rechazo se pide:")
    print("a) Generar 100.000 números aleatorios con distribución Normal de media 25 y desvío estándar 2")
    print("b) Realizar un histograma de frecuencias relativas con todos los valores obtenidos")
    print("c) Comparar, en el mismo gráfico, el histograma realizado en el punto anterior con la función de densidad de probabilidad brindada por el lenguaje elegido (para esta última distribución utilizar un gráfico de línea).")
    print("d) Calcular la media y la varianza de la distribución obtenida y compararlos con los valores teóricos")

    random_array_no_estandar = list(map(lambda x: (x * 2) + 25, generar_random_array_estandar_aceptados())) # Por el Teorema Central del Límite

    plot.subplot(121)
    plot.hist(random_array_no_estandar, bins=100)
    plot.title('Histograma')

    plot.subplot(122)
    x = np.linspace(stats.norm.ppf(0.01, 25, 2), stats.norm.ppf(0.99, 25, 2), 100)
    fdp_normal = stats.norm.pdf(x, 25, 2)
    plot.plot(x, fdp_normal)
    plot.title('Función de Densidad de Probabilidad')

    plot.savefig(sys.path[0] + "/E04-histograma.png")
    print("El gráfico se guardó en {0}/E04-histograma.png".format(sys.path[0]))

    media_obtenida = np.mean(random_array_no_estandar)
    desvio_obtenido = np.std(random_array_no_estandar)
    print("Media obtenida: ", media_obtenida, "; Media teorica: ", 25)
    print("Desvio obtenido: ", desvio_obtenido, "; Desvio teorico: ", 2)


if __name__ == "__main__":
    main()