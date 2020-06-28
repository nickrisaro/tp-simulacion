import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import sys

# Parámetros de la enfermedad
BETA = 0.27
GAMMA = 0.043

DIAS = 200
PORCENTAJE_CONTAGIO_INICIAL = 0.03
PORCENTAJE_FIN_EPIDEMIA = 0.01
PORCENTAJE_CAMAS_POBLACION = 0.3
PORCENTAJE_POBLACION_EN_CUARENTENA = 0.35

MOSTRAR_GRAFICO = False
TIEMPO = np.linspace(0, DIAS, DIAS)
CAMAS = np.full(DIAS, PORCENTAJE_CAMAS_POBLACION)

def SIR(y, t):
    """
    Esta función será invocada por el método de resolución de ecuaciones diferenciales
    Para cada instante de tiempo t calcula los nuevos valores de S, I y R
    """
    S, I, R = y
    dsdt = -BETA*S*I
    didt = BETA*S*I - GAMMA*I
    drdt = GAMMA*I
    return dsdt, didt, drdt

def simular_sin_cuarentena():
    """
    Realiza una simulación sin cuarentena del modelo SIR
    Toda la población es susceptible de contagiarse
    Retorna todos los valores de S, I y R para cada instante de tiempo
    """
    I = PORCENTAJE_CONTAGIO_INICIAL
    S = 1 - I
    R = 0
    y0 = [S, I, R]

    ret = odeint(SIR, y0, TIEMPO)
    return ret.T

def simular_con_cuarentena():
    """
    Realiza una simulación con cuarentena del modelo SIR
    Un porcentaje de la población no es susceptible de contagiarse
    Retorna todos los valores de S, I y R para cada instante de tiempo
    """
    I = PORCENTAJE_CONTAGIO_INICIAL
    S = 1 - I - PORCENTAJE_POBLACION_EN_CUARENTENA
    R = 0
    y0 = [S, I, R]

    ret = odeint(SIR, y0, TIEMPO)
    return ret.T

def imprimir_informacion(SIR, modelo):
    """
    Calcula e imprime por consola algunos valores relevantes de la simulación
    """
    S, I, R = SIR
    dia_pico_infectados = 0
    maximo_infectados = 0
    dia_fin_enfermedad = 0
    dia_saturacion = 0
    for dia in range (0, len(S)):
        if I[dia] >= maximo_infectados:
            maximo_infectados = I[dia]
            dia_pico_infectados = dia

        if I[dia] < PORCENTAJE_FIN_EPIDEMIA and dia_fin_enfermedad is 0:
            dia_fin_enfermedad = dia

        if I[dia] >= PORCENTAJE_CAMAS_POBLACION and dia_saturacion is 0:
            dia_saturacion = dia

    print("Información del modelo " + modelo)
    print("El pico de la enfermedad fue el día {0} con el {1:.2f}% de la población infectada".format(dia_pico_infectados, maximo_infectados*100))
    print("La epidemia duró {0} días".format(dia_fin_enfermedad))
    if dia_saturacion is not 0:
        print("El sistema de salud se saturó el día", dia_saturacion)
    else:
        print("El sistema de salud no se saturó")

    return SIR

def graficar(SIR, modelo):
    """
    Realiza un gráfico con la evolución de las 3 variables del modelo respecto del tiempo
    """
    S, I, R = SIR
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
    ax.plot(TIEMPO, S*100, 'b', alpha=0.5, lw=2, label='Susceptibles')
    ax.plot(TIEMPO, I*100, 'r', alpha=0.5, lw=2, label='Infectados')
    ax.plot(TIEMPO, R*100, 'g', alpha=0.5, lw=2, label='Recuperados')
    ax.plot(TIEMPO, CAMAS*100, 'black', alpha=0.5, lw=2, label='Capacidad del sistema sanitario')
    ax.set_xlabel('Tiempo / días')
    ax.set_ylabel('% población')
    ax.set_ylim(0,100)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    plt.title(modelo)
    plt.savefig("{0}/E4-{1}.png".format(sys.path[0], modelo))
    print("El gráfico se guardó en {0}/E4-{1}.png".format(sys.path[0], modelo))
    if MOSTRAR_GRAFICO:
        plt.show()

def main():

    print("TP 2 - Ejercicio 4")

    print("Se desea simular la evolución de una epidemia utilizando el modelo S.I.R.")
    print("Se conoce que inicialmente el 3% de la población se encuentra infectada, toda la población es susceptible de")
    print("contagiarse, la tasa de transmisión β=0,27, y la tasa de recuperación γ = 0,043")

    print()
    print("Consideramos que la enfermedad terminó cuando menos del {0}% de la población está infectada".format(PORCENTAJE_FIN_EPIDEMIA*100))
    print()
    print("En el modelo inicial todas las personas circulan libremente y son susceptibles de contagiarse")
    graficar(imprimir_informacion(simular_sin_cuarentena(), "Sin cuarentena"), "Sin cuarentena")

    print()
    print("Luego se aplica una cuarentena al {0}% de la población para disminuir la cantidad de personas que se pueden contagiar".format(PORCENTAJE_POBLACION_EN_CUARENTENA*100))
    graficar(imprimir_informacion(simular_con_cuarentena(), "Con cuarentena"), "Con cuarentena")

if __name__ == "__main__":
    main()