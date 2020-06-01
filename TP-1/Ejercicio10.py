import numpy as np
import random
import matplotlib.pylab as plt
import matplotlib.animation as animation
import os
import sys
from matplotlib.animation import FuncAnimation

LIMIT_X = 100
LIMIT_Y = 100
RW_CUATRO_DIRS_VEL = 1

CANT_INSTANTES = 3000
CANT_PERSONAS = 100
PROPORCION_INICIAL_INFECTADAS = 0.05
PROBABILIDAD_CONTAGIO = 0.6

def esta_en_limites(x,y):
    return (0 <= x <= LIMIT_X and 0 <= y <= LIMIT_Y)

def random_walk_cuatro_dirs(x,y):
    """Esta funcion recibe la posicion de una persona y devuelve la nueva posicion para la misma dentro de los limites"""
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

class Persona:

    def __init__(self, x, y, sana = True):
        self.sana = sana
        self.x = x
        self.y = y

def animate_random_walk(instante, random_walk_func, personas, scat_personas, ax):
    """Esta funcion se ejecuta en cada frame del random walk aplicandole la funcion recibida por parametro a las "particulas" de cada gas obteniendo asi su nueva posicion"""
    ax.legend(loc="lower left", title="Instante {0}".format(instante))

    personas_x = np.array([])
    personas_y = np.array([])
    colors = np.array([])
    for t in range(0, len(personas)):
        persona = personas[t]
        persona.x,persona.y = random_walk_func(persona.x,persona.y)
        personas_x = np.append(personas_x, persona.x)
        personas_y = np.append(personas_y, persona.y)
        if persona.sana:
            colors = np.append(colors, "g")
        else:
            colors = np.append(colors, "r")

    coordenadas = np.column_stack((personas_x,personas_y))
    scat_personas.set_offsets(coordenadas)
    scat_personas.set_color(colors)

def main():

    personas = np.array([])
    personas_x = np.array([])
    personas_y = np.array([])
    colors = np.array([])
    for i in range(0, CANT_PERSONAS):
        x = np.random.uniform(0, LIMIT_X)
        y = np.random.uniform(0, LIMIT_Y)

        sana = np.random.uniform(0, 1) > PROPORCION_INICIAL_INFECTADAS

        persona = Persona(x, y, sana)
        personas = np.append(personas, persona)
        personas_x = np.append(personas_x, persona.x)
        personas_y = np.append(personas_y, persona.y)
        if persona.sana:
            colors = np.append(colors, "g")
        else:
            colors = np.append(colors, "r")

    coordenadas = np.column_stack((personas_x,personas_y))


    fig = plt.figure()
    ax = plt.axes(xlim=(0, LIMIT_X), ylim=(0, LIMIT_Y))
    scat_personas = ax.scatter(personas_x, personas_y, s=100, c=colors)
    ax.legend(loc="lower left", title="Instante 0")
    scat_personas.set_offsets(coordenadas)

    anim = FuncAnimation(fig, animate_random_walk, frames=CANT_INSTANTES, interval=1, repeat=False, fargs=(random_walk_cuatro_dirs,personas,scat_personas, ax))
    plt.show()

if __name__ == "__main__":
    main()