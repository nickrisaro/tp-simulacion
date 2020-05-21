import Ejercicio01 as generador
import numpy as np
import mpmath as mp
import matplotlib.pyplot as plot
import sys

def plotFunction(x, y, tipo, lbl, legend, labelColor):
    # Umbral para aplicar la máscara
    threshold = 1

    # Aplico una máscara
    y_values = np.ma.array(y)
    y_masked_values = np.ma.masked_where(y_values < threshold , y_values)

    plot.plot(x, y_masked_values, '-r', label='f1(x)')
    plot.title(f'Gráfico de la función {tipo}')
    plot.xlabel('x', color=labelColor)
    plot.ylabel('y', color=labelColor)
    plot.legend(loc=legend)
    plot.grid()
    plot.savefig(sys.path[0] + f"/E03-funcion-{tipo}.png")
    print(f"La función {tipo} se guardó en {sys.path[0]}/E03-funcion-{tipo}.png")

def construirFuncionDensidad():
    x = []
    y = []    	

    for i in np.arange(-10, 10, 0.01):
        x.append(i)
        if (i>= -mp.pi/2 and i<= mp.pi/2):
            a = 13.0/(12.0 * mp.pi)
            b = ((i ** 2)/(mp.pi ** 3))
            y.append(a - b)
        else:
            y.append(0)

    pos = np.where(np.abs(np.diff(y)) >= mp.pi/2)[0]

    x[pos] = np.nan
    y[pos] = np.nan

    plotFunction(x, y, 'densidad','f1(x)','upper right','#1C2833')

def construirFuncionAcumulada():
    # Para construir la funcion de probabilidad acumulada voy a integrar
    # por cada trozo de la funcion. Formalmente hablando, en cada trozo
    # se integra con los limites de -infinito a x
    x = []
    y = []      

    # Utilizo este rango de valores porque si es mucho más grande, la parábola que se genera se termina
    # viendo como una linea recta vertical
    for i in np.arange(-10, 10, 0.01):
        x.append(i)
        if (i>= -mp.pi/2 and i<= mp.pi/2):
            a = 8 * (i ** 3) - (26 * (mp.pi ** 4)* i)
            b = 13 * (mp.pi ** 5) + (mp.pi ** 3)
            y.append((a - b) / (24 * mp.pi ** 3))
        else:
            y.append(0)
    plotFunction(x, y,'distribucion','F1(x)','upper left','#1C2833')



def main():
    print("TP 1 - Ejercicio 3")
    print("a) Graficar la función de densidad de probabilidad")
    construirFuncionDensidad()

    print("b) Calcular y graficar la función de probabilidad acumulada y su inversa.")
    construirFuncionAcumulada()


if __name__ == "__main__":
    main()