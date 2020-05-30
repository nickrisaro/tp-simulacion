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

gas_1_x = np.random.uniform(0, LIMIT_X/2, CANT_GAS_1)
gas_1_y = np.random.uniform(0, LIMIT_Y, CANT_GAS_1)
gas_1 = np.column_stack((gas_1_x,gas_1_y))

gas_2_x = np.random.uniform(LIMIT_X/2, LIMIT_X, CANT_GAS_2)
gas_2_y = np.random.uniform(0, LIMIT_Y, CANT_GAS_2)
gas_2 = np.column_stack((gas_2_x,gas_2_y))

fig = plt.figure()
ax = plt.axes(xlim=(0, LIMIT_X), ylim=(0, LIMIT_Y))
scat_gas_1 = ax.scatter([], [], s=0.5, c="g")
scat_gas_2 = ax.scatter([], [], s=0.5, c="r")

def esta_en_limites(x,y):
    return (0 <= x <= LIMIT_X and 0 <= y <= LIMIT_Y)

def random_walk_cuatro_dirs(x,y):
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
    if not esta_en_limites(new_x,new_y):
        return x,y
    return new_x,new_y

def init():
    scat_gas_1.set_offsets(gas_1)
    scat_gas_2.set_offsets(gas_2)

def calcular_densidad_derecha(instante):
    cant_gas_1_lado_der = len(gas_1.T[0][gas_1.T[0]>LIMIT_X/2]) #Obtengo aquellas parts. del gas 1 que estan del lado derecho
    cant_gas_2_lado_der = len(gas_2.T[0][gas_2.T[0]>LIMIT_X/2]) #Obtengo aquellas parts. del gas 2 que estan del lado derecho
    total_lado_der = cant_gas_1_lado_der + cant_gas_2_lado_der
    return [instante,cant_gas_1_lado_der/total_lado_der,cant_gas_2_lado_der/total_lado_der]

def calcular_densidad_izquierda(instante):
    cant_gas_1_lado_izq = len(gas_1.T[0][gas_1.T[0]<LIMIT_X/2]) #Obtengo aquellas parts. del gas 1 que estan del lado izquierdo
    cant_gas_2_lado_izq = len(gas_2.T[0][gas_2.T[0]<LIMIT_X/2]) #Obtengo aquellas parts. del gas 2 que estan del lado izquierdo
    total_lado_izq = cant_gas_1_lado_izq + cant_gas_2_lado_izq
    return [instante,cant_gas_1_lado_izq/total_lado_izq,cant_gas_2_lado_izq/total_lado_izq]

def animate_random_walk(instante, random_walk_func):
    """Esta funcion se ejecuta en cada frame del random walk aplicandole la funcion recibida por parametro a las "particulas" de cada gas obteniendo asi su nueva posicion"""
    for t in range(0, len(gas_1)):
        gas_1[t][0],gas_1[t][1] = random_walk_func(gas_1[t][0], gas_1[t][1])
    for t in range(0, len(gas_2)):
        gas_2[t][0],gas_2[t][1] = random_walk_func(gas_2[t][0], gas_2[t][1])
    densidad_lado_der.append(calcular_densidad_derecha(instante))
    densidad_lado_izq.append(calcular_densidad_izquierda(instante))

anim = FuncAnimation(fig, animate_random_walk, init_func=init, frames=CANT_INSTANTES, interval=1, repeat=False, fargs=(random_walk_cuatro_dirs,))

#Comentar la siguiente linea si no funciona, hay que instalar imagemagick
anim.save('E09-a.gif', writer='imagemagick')
plt.show()

fig, axs = plt.subplots(2)

ax_densidad_izquierda = axs[0]
ax_densidad_izquierda.plot(np.array(densidad_lado_izq).T[0], np.array(densidad_lado_izq).T[1], "-g", label="Densidad gas 1")
ax_densidad_izquierda.plot(np.array(densidad_lado_izq).T[0], np.array(densidad_lado_izq).T[2], "-r", label="Densidad gas 2")
ax_densidad_izquierda.set_title("Densidad de los gases en el lado izquierdo")

ax_densidad_derecha = axs[1]
ax_densidad_derecha.plot(np.array(densidad_lado_der).T[0], np.array(densidad_lado_der).T[1], "-g", label="Densidad gas 1")
ax_densidad_derecha.plot(np.array(densidad_lado_der).T[0], np.array(densidad_lado_der).T[2], "-r", label="Densidad gas 2")
ax_densidad_derecha.set_title("Densidad de los gases en el lado derecho")

for ax in axs.flat:
    ax.set(xlabel='Instantes de tiempo', ylabel='Densidad del gas')
    ax.set_xlim(0, CANT_INSTANTES)
    ax.set_ylim(0,1)
    ax.label_outer()

plt.legend(loc="upper right")
fig.savefig(sys.path[0] + "/E09-a-densidad-gases.png")
plt.show()
