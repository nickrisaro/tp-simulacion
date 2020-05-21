# coding=utf-8
import matplotlib.pyplot as plot
import math
import random as rn
import sys

def generar_normal_estandar(x):
    return math.exp(-(x ** 2) / (2)) / (math.sqrt(2 * math.pi))

def generar_exponencial(x):
    return math.exp(-x)

def generar_random_array(cantidad):
    array = []
    for i in range (0, cantidad):
        array.append(rn.random())
    return array

def generar_random_array_estandar_aceptados():

    cantidad = 100000

    c = 2*(generar_normal_estandar(1))/generar_exponencial(1) # Derivando fX(x)/fY(y) e igualando a 0 se obtiene x = 1

    print(c)

    array_nums = generar_random_array(cantidad)
    array_probs = list(map(lambda x: generar_normal_estandar(x)/(c*generar_exponencial(x)), array_nums))

    numeros = []
    for i in range(0, cantidad):
        r1 = rn.random()

        if r1 < array_probs[i]:

            r2 = rn.random()

            if r2 < 0.5:
                numeros.append(array_nums[i])
            else:
                numeros.append(-array_nums[i])

    return numeros


def main():
    print("TP 1 - Ejercicio 4")

    print("Aplicando el algoritmo de Aceptación y rechazo se pide:")
    print("a) Generar 100.000 números aleatorios con distribución Normal de media 25 y desvío estándar 2")

    random_array_no_estandar = list(map(lambda x: (x * 2) + 25, generar_random_array_estandar_aceptados())) # Por el Teorema Central del Límite

    print("b) Realizar un histograma de frecuencias relativas con todos los valores obtenidos")

    plot.hist(random_array_no_estandar, bins=100)
    plot.savefig(sys.path[0] + "/E04-histograma.png")
    print("El histograma se guardó en {0}/E04-histograma.png".format(sys.path[0]))


if __name__ == "__main__":
    main()