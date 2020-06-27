import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

DIAS = 200
POBALCION_TOTAL = 1000
PORCENTAJE_CONTAGIO_INICIAL = 0.03
BETA = 0.27
GAMMA = 0.043
PORCENTAJE_CAMAS_POBLACION = 0.3

def SIR(y, t):
    S, I, R = y
    dsdt = -BETA*S*I/POBALCION_TOTAL
    didt = BETA*S*I/POBALCION_TOTAL - GAMMA*I
    drdt = GAMMA*I
    return dsdt, didt, drdt

def main():

    print("TP 2 - Ejercicio 4")
    I = POBALCION_TOTAL*PORCENTAJE_CONTAGIO_INICIAL
    S = POBALCION_TOTAL - I
    R = 0
    y0 = [S, I, R]

    t = np.linspace(0, DIAS, DIAS)
    camas = np.full(DIAS, PORCENTAJE_CAMAS_POBLACION)

    ret = odeint(SIR, y0, t)
    S, I, R = ret.T

    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
    ax.plot(t, S/POBALCION_TOTAL, 'b', alpha=0.5, lw=2, label='Susceptibles')
    ax.plot(t, I/POBALCION_TOTAL, 'r', alpha=0.5, lw=2, label='Infectados')
    ax.plot(t, R/POBALCION_TOTAL, 'g', alpha=0.5, lw=2, label='Recuperados')
    ax.plot(t, camas, 'black', alpha=0.5, lw=2, label='Capacidad del sistema sanitario')
    ax.set_xlabel('Tiempo / días')
    ax.set_ylabel('% población')
    ax.set_ylim(0,1.2)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    plt.show()

if __name__ == "__main__":
    main()