import Ejercicio01 as generador
import Ejercicio02 as lanzador
import numpy as np
import sys
from scipy.stats import chi2

CANT_LANZAMIENTOS = 10000
SIGNIFICANCIA_CHI2 = 0.01

PROBABILIDADES = {2:1/36,
                  3:2/36,
                  4:3/36,
                  5:4/36,
                  6:5/36,
                  7:6/36,
                  8:5/36,
                  9:4/36,
                  10:3/36,
                  11:2/36,
                  12:1/36,}

def simularLanzamientos():
    print("Genero %d pares de lanzamientos".format(CANT_LANZAMIENTOS))
    generadorUnitario = generador.GCL(unitario=True)

    resultados = np.array([])
    for i in range(0, CANT_LANZAMIENTOS):
        dado1 = lanzador.lanzarDado(generadorUnitario)
        dado2 = lanzador.lanzarDado(generadorUnitario)
        resultados = np.append(resultados, dado1 + dado2)

    resultadosUnicos, frecuencias = np.unique(resultados, return_counts=True)
    return dict(zip(resultadosUnicos, frecuencias))

def testChi2 (frecuencias):
    D2 = 0
    for valor, cant_observada in frecuencias.items():
        f_observada = cant_observada
        f_esperada = probabilidadEsperada(valor) * CANT_LANZAMIENTOS
        #Descomentar para testing visual (?)
        #print("PARA EL VALOR ", valor, " OBSERVE ", f_observada, " ESPERABA OBSERVAR ", f_esperada, " EN CANT DE SIMULACIONES ", CANT_LANZAMIENTOS)
        D2i = np.power(f_observada - f_esperada,2) / f_esperada
        D2 += D2i
    limiteSuperior = chi2.ppf(1 - SIGNIFICANCIA_CHI2, df=len(frecuencias) - 1)
    print("Estadistico: {:.2f} ".format(D2))
    print("Limite Superior: {:.2f} ".format(limiteSuperior))

    if D2 <= limiteSuperior:
        print("El test acepta la hipotesis nula. La distribución se comporta como la suma del lanzamiento de 2 dados")
    else:
        print("El test rechaza la hipótesis nula. La distribución no se comporta como la suma del lanzamiento de 2 dados")

def probabilidadEsperada(valor):
    return PROBABILIDADES[valor]

def main():
    print("TP 1 - Ejercicio 06")
    print("Realizar un test Chi2 a la distribución empírica implementada en el Ej 2, y analizar el resultado indicando si la distribución puede o no ser aceptada.")

    frecuenciasObservadas = simularLanzamientos()
    #print(frecuenciasObservadas)
    testChi2(frecuenciasObservadas)

if __name__ == "__main__":
    main()