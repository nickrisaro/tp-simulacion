import numpy as np
import random
import matplotlib.pylab as plt
import matplotlib.animation as animation
import os
import sys
from matplotlib.animation import FuncAnimation
import matplotlib.patches as mpatches

LIMIT_X = 100
LIMIT_Y = 100
RW_CUATRO_DIRS_VEL = 1

CANT_INSTANTES = 4000
CANT_PERSONAS = 100
PROPORCION_INICIAL_INFECTADAS = 0.05
PROBABILIDAD_CONTAGIO = 0.6
DISTANCIA_CONTAGIO = 2.0

class Persona:

    def __init__(self, x, y, sana = True):
        self.sana = sana
        self.x = x
        self.y = y

    def esta_en_limites(self, x,y):
        return (0 <= x <= LIMIT_X and 0 <= y <= LIMIT_Y)

    def desplazarse(self):
        siguientePaso = random.randint(1,4)
        if siguientePaso == 1:
            new_x,new_y = self.x + RW_CUATRO_DIRS_VEL, self.y
        elif siguientePaso == 2:
            new_x,new_y = self.x, self.y + RW_CUATRO_DIRS_VEL
        elif siguientePaso == 3:
            new_x,new_y = self.x - RW_CUATRO_DIRS_VEL, self.y
        else:
            new_x,new_y = self.x, self.y - RW_CUATRO_DIRS_VEL

        if self.esta_en_limites(new_x,new_y):
            self.x, self.y = new_x, new_y

    def interactuar(self, personas):
        """Esta función determina si una persona sana está en contacto con personas contagiadas y si se contagia. No determina si esta persona contagia a otras"""
        if not self.sana:
            return

        for t in range(0, len(personas)):
            persona = personas[t]
            if not persona == self and not persona.sana:
                distancia_entre_personas = np.sqrt((persona.x - self.x)**2 + (persona.y - self.y)**2)
                if distancia_entre_personas <= DISTANCIA_CONTAGIO:
                    self.sana = False
                    break


def animate_random_walk(instante, personas, scat_personas, ax):
    """Esta funcion se ejecuta en cada frame del random walk y hace que se muevan y, posiblemente, se contagien las personas"""

    personas_x = np.array([])
    personas_y = np.array([])
    colors = np.array([])
    sanas, infectadas = 0, 0

    for t in range(0, len(personas)):
        persona = personas[t]
        persona.desplazarse()
        personas_x = np.append(personas_x, persona.x)
        personas_y = np.append(personas_y, persona.y)

    for t in range(0, len(personas)):
        persona = personas[t]
        persona.interactuar(personas)
        if persona.sana:
            colors = np.append(colors, "g")
            sanas += 1
        else:
            colors = np.append(colors, "r")
            infectadas += 1

    coordenadas = np.column_stack((personas_x,personas_y))
    scat_personas.set_offsets(coordenadas)
    scat_personas.set_color(colors)
    red_patch = mpatches.Patch(color="red", label="Infectadas {0}".format(infectadas))
    green_patch = mpatches.Patch(color="green", label="Sanas {0}".format(sanas))
    ax.legend(handles=[red_patch, green_patch], loc="lower left", title="Instante {0}".format(instante))

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

    fig = plt.figure()
    ax = plt.axes(xlim=(0, LIMIT_X), ylim=(0, LIMIT_Y))
    scat_personas = ax.scatter(personas_x, personas_y, s=100, c=colors)
    ax.legend(loc="lower left", title="Instante 0")

    anim = FuncAnimation(fig, animate_random_walk, frames=CANT_INSTANTES, interval=1, repeat=False, fargs=(personas,scat_personas, ax))
    plt.show()

if __name__ == "__main__":
    main()