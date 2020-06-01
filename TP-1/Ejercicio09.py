import numpy as np
import random
import matplotlib.pylab as plt
import matplotlib.animation as animation
import os
import sys
from matplotlib.animation import FuncAnimation

LIMIT_X = 10
LIMIT_Y = 20

CANT_GAS_1 = 10000
CANT_GAS_2 = 10000

CANT_INSTANTES = 3000
RW_CUATRO_DIRS_VEL = 0.1

densidad_lado_izq = []
densidad_lado_der = []

def crear_particulas_gases():
    gas_1_x = np.random.uniform(0, LIMIT_X/2, CANT_GAS_1)
    gas_1_y = np.random.uniform(0, LIMIT_Y, CANT_GAS_1)
    gas_1 = np.column_stack((gas_1_x,gas_1_y))

    gas_2_x = np.random.uniform(LIMIT_X/2, LIMIT_X, CANT_GAS_2)
    gas_2_y = np.random.uniform(0, LIMIT_Y, CANT_GAS_2)
    gas_2 = np.column_stack((gas_2_x,gas_2_y))
    return gas_1, gas_2

def choco_con_paredes_ej_a(old_x, old_y, new_x, new_y):
    return esta_fuera_de_limites(old_x, old_y, new_x, new_y)

def choco_con_paredes_ej_b(old_x, old_y, new_x, new_y):
    return esta_fuera_de_limites(old_x, old_y, new_x, new_y) or choco_con_pared_del_medio(old_x, old_y, new_x, new_y)

def choco_con_pared_del_medio(old_x, old_y, new_x, new_y):
    return (old_x < LIMIT_X/2 and new_x > LIMIT_X/2 and new_y > LIMIT_Y/2) or (old_x > LIMIT_X/2 and new_x < LIMIT_X/2 and new_y > LIMIT_Y/2)

def esta_fuera_de_limites(old_x, old_y, new_x, new_y):
    return not (0 <= new_x <= LIMIT_X and 0 <= new_y <= LIMIT_Y)

def random_walk_cuatro_dirs(x, y, choco_con_pared):
    """Esta funcion recibe la posicion de una particula y devuelve la nueva posicion para la misma dentro de los limites"""
    siguientePaso = random.randint(1,4)
    if siguientePaso == 1:
        new_x,new_y = x + RW_CUATRO_DIRS_VEL, y
    elif siguientePaso == 2:
        new_x,new_y = x, y + RW_CUATRO_DIRS_VEL
    elif siguientePaso == 3:
        new_x,new_y = x - RW_CUATRO_DIRS_VEL, y
    else:
        new_x,new_y = x, y - RW_CUATRO_DIRS_VEL
    if choco_con_pared(x, y, new_x, new_y): #si choca, se queda con los X,Y anteriores al calculo.
        return x,y
    return new_x,new_y

def init():
    scat_gas_1.set_offsets(gas_1)
    scat_gas_2.set_offsets(gas_2)

def calcular_densidad_derecha(instante):
    cant_gas_1_lado_der = len(gas_1.T[0][gas_1.T[0]>LIMIT_X/2]) #Obtengo aquellas parts. del gas 1 que estan del lado derecho
    cant_gas_2_lado_der = len(gas_2.T[0][gas_2.T[0]>LIMIT_X/2]) #Obtengo aquellas parts. del gas 2 que estan del lado derecho
    superficie = LIMIT_X/2 * LIMIT_Y
    return [instante,cant_gas_1_lado_der/superficie,cant_gas_2_lado_der/superficie]

def calcular_densidad_izquierda(instante):
    cant_gas_1_lado_izq = len(gas_1.T[0][gas_1.T[0]<LIMIT_X/2]) #Obtengo aquellas parts. del gas 1 que estan del lado izquierdo
    cant_gas_2_lado_izq = len(gas_2.T[0][gas_2.T[0]<LIMIT_X/2]) #Obtengo aquellas parts. del gas 2 que estan del lado izquierdo
    superficie = LIMIT_X/2 * LIMIT_Y
    return [instante,cant_gas_1_lado_izq/superficie,cant_gas_2_lado_izq/superficie]

def animate_random_walk_ej_a(instante, random_walk_func):
    """Esta funcion se ejecuta en cada frame del random walk aplicandole la funcion recibida por parametro a las "particulas" de cada gas obteniendo asi su nueva posicion"""
    for t in range(0, len(gas_1)):
        gas_1[t][0],gas_1[t][1] = random_walk_func(gas_1[t][0], gas_1[t][1], choco_con_paredes_ej_a)
    for t in range(0, len(gas_2)):
        gas_2[t][0],gas_2[t][1] = random_walk_func(gas_2[t][0], gas_2[t][1], choco_con_paredes_ej_a)
    densidad_lado_der.append(calcular_densidad_derecha(instante))
    densidad_lado_izq.append(calcular_densidad_izquierda(instante))
   
def animate_random_walk_ej_b(instante, random_walk_func):
    """Esta funcion se ejecuta en cada frame del random walk aplicandole la funcion recibida por parametro a las "particulas" de cada gas obteniendo asi su nueva posicion"""
    for t in range(0, len(gas_1)):
        gas_1[t][0],gas_1[t][1] = random_walk_func(gas_1[t][0], gas_1[t][1], choco_con_paredes_ej_b)
    for t in range(0, len(gas_2)):
        gas_2[t][0],gas_2[t][1] = random_walk_func(gas_2[t][0], gas_2[t][1], choco_con_paredes_ej_b)
    densidad_lado_der.append(calcular_densidad_derecha(instante))
    densidad_lado_izq.append(calcular_densidad_izquierda(instante))

def plot_densidad(ax, densidad, title):
    ax.plot(np.array(densidad).T[0], np.array(densidad).T[1], "-g", label="Densidad gas 1")
    ax.plot(np.array(densidad).T[0], np.array(densidad).T[2], "-r", label="Densidad gas 2")
    ax.set_title(title)

def set_plot_axis():
    for ax in axs.flat:
        ax.set(xlabel='Instantes de tiempo', ylabel='Densidad del gas')
        ax.set_xlim(0, CANT_INSTANTES)
        ax.set_ylim(0, 100)
        ax.label_outer()
        
fig = plt.figure()
ax = plt.axes(xlim=(0, LIMIT_X), ylim=(0, LIMIT_Y))
scat_gas_1 = ax.scatter([], [], s=0.5, c="g")
scat_gas_2 = ax.scatter([], [], s=0.5, c="r")

gas_1, gas_2 = crear_particulas_gases()

ej = input("Presione la tecla 'a' o la tecla 'b': ")
while ej not in {'a','b'}:
    ej = input("Presione la tecla 'a' o la tecla 'b': ")

if ej == 'a':
    print("Ejecutando punto A)")
    anim = FuncAnimation(fig, animate_random_walk_ej_a, init_func=init, frames=CANT_INSTANTES, interval=1, repeat=False, fargs=(random_walk_cuatro_dirs,))

    #Descomentar la siguiente linea para guardar la animación. Si no funciona, hay que instalar imagemagick
    #anim.save('E09-a.gif', writer='imagemagick')
    plt.show()

    fig, axs = plt.subplots(2)

    plot_densidad(axs[0], densidad_lado_izq, "Densidad de los gases en el lado izquierdo")
    plot_densidad(axs[1], densidad_lado_der, "Densidad de los gases en el lado derecho")
    set_plot_axis()

    plt.legend(loc="upper right")
    fig.savefig(sys.path[0] + "/E09-a-densidad-gases.png")
    plt.show()
else:
    print("Ejecutando punto B) con pared en el medio superior")
    anim = FuncAnimation(fig, animate_random_walk_ej_b, init_func=init, frames=CANT_INSTANTES, interval=1, repeat=False, fargs=(random_walk_cuatro_dirs,))

    #Descomentar la siguiente linea para guardar la animación. Si no funciona, hay que instalar imagemagick
    #anim.save('E09-b.gif', writer='imagemagick')
    plt.show()

    fig, axs = plt.subplots(2)

    plot_densidad(axs[0], densidad_lado_izq, "Densidad de los gases en el lado izquierdo")
    plot_densidad(axs[1], densidad_lado_der, "Densidad de los gases en el lado derecho")
    set_plot_axis()

    plt.legend(loc="upper right")
    fig.savefig(sys.path[0] + "/E09-b-densidad-gases.png")
    plt.show()
