import argparse
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import matplotlib.pylab as plt
import numpy as np

LIMITE_X = 100
LIMITE_Y = 100
VELOCIDAD = 1

CANT_INSTANTES = 4000
CANT_PERSONAS = 100
PROPORCION_INICIAL_INFECTADAS = 0.05
PROBABILIDAD_CONTAGIO = 0.6
DISTANCIA_CONTAGIO = 2.0
TIEMPO_HASTA_SANAR = 20
PROBABILIDAD_SANAR = 0.8

class Grafico_epidemia:
    def __init__(self, axes):

        self.personas_sanas = np.array([])
        self.personas_infectadas = np.array([])
        self.instantes = np.array([])
        line_sanas, = axes.plot(self.instantes, self.personas_sanas, label="Sanas", color="green")
        line_infectadas, = axes.plot(self.instantes, self.personas_infectadas, label="Infectadas", color="red")
        line_sanas.axes.axis([0, CANT_INSTANTES, 0, CANT_PERSONAS])
        self.grafico_linea_sanas = line_sanas
        self.grafico_linea_infectadas = line_infectadas
        self.informar_0_porciento = True
        self.informar_50_porciento = True
        self.informar_75_porciento = True
        self.informar_90_porciento = True
        self.informar_95_porciento = True
        self.informar_100_porciento = True

    def actualizar_grafico_linea(self, instante, sanas, infectadas):

        red_patch = mpatches.Patch(color="red", label="Infectadas {0}".format(infectadas))
        green_patch = mpatches.Patch(color="green", label="Sanas {0}".format(sanas))

        self.personas_sanas = np.append(self.personas_sanas, sanas)
        self.personas_infectadas = np.append(self.personas_infectadas, infectadas)
        self.instantes = np.append(self.instantes, instante)
        self.grafico_linea_sanas.set_data(self.instantes, self.personas_sanas)
        self.grafico_linea_infectadas.set_data(self.instantes, self.personas_infectadas)
        self.grafico_linea_sanas.axes.axis([0, CANT_INSTANTES, 0, CANT_PERSONAS])
        self.grafico_linea_sanas.axes.legend(handles=[red_patch, green_patch], loc="lower right", title="Instante {0}".format(instante))

        if self.informar_0_porciento and infectadas == 0:
            print("Se alcanzó el 0% de infecciones en el instante {0}".format(instante))
            self.informar_0_porciento = False
        if self.informar_50_porciento and infectadas >= 50:
            print("Se alcanzó el 50% de infecciones en el instante {0}".format(instante))
            self.informar_50_porciento = False
        if self.informar_75_porciento and infectadas >= 75:
            print("Se alcanzó el 75% de infecciones en el instante {0}".format(instante))
            self.informar_75_porciento = False
        if self.informar_90_porciento and infectadas >= 90:
            print("Se alcanzó el 90% de infecciones en el instante {0}".format(instante))
            self.informar_90_porciento = False
        if self.informar_95_porciento and infectadas >= 95:
            print("Se alcanzó el 95% de infecciones en el instante {0}".format(instante))
            self.informar_95_porciento = False
        if self.informar_100_porciento and infectadas == 100:
            print("Se alcanzó el 100% de infecciones en el instante {0}".format(instante))
            self.informar_100_porciento = False

class Persona:

    def __init__(self, x, y, sana = True, inmovilizada = False, se_inmoviliza_al_infectarse = False, puede_sanar = False):
        self.sana = sana
        self.x = x
        self.y = y
        self.inmovilizada = inmovilizada
        self.puede_sanar = puede_sanar
        self.se_inmoviliza_al_infectarse = se_inmoviliza_al_infectarse
        self.tiempo_hasta_inmovilizarse = np.random.randint(10, 21)
        if not self.sana:
            self.instante_contagio = 0

    def esta_en_limites(self, x,y):
        return (0 <= x <= LIMITE_X and 0 <= y <= LIMITE_Y)

    def desplazarse(self):
        if self.inmovilizada:
            return
        siguientePaso = np.random.randint(1,5)
        if siguientePaso == 1:
            new_x,new_y = self.x + VELOCIDAD, self.y
        elif siguientePaso == 2:
            new_x,new_y = self.x, self.y + VELOCIDAD
        elif siguientePaso == 3:
            new_x,new_y = self.x - VELOCIDAD, self.y
        else:
            new_x,new_y = self.x, self.y - VELOCIDAD

        if self.esta_en_limites(new_x,new_y):
            self.x, self.y = new_x, new_y

    def interactuar(self, personas, instante):
        """Esta función determina si una persona sana está en contacto con personas contagiadas y si se contagia. No determina si esta persona contagia a otras"""
        if not self.sana:
            return

        for t in range(0, len(personas)):
            persona = personas[t]
            if not persona == self and not persona.sana:
                distancia_entre_personas = np.sqrt((persona.x - self.x)**2 + (persona.y - self.y)**2)
                if distancia_entre_personas <= DISTANCIA_CONTAGIO:
                    self.sana = np.random.uniform(0, 1) >= PROBABILIDAD_CONTAGIO
                    break

        if not self.sana:
            self.instante_contagio = instante

    def actualizar(self, instante):
        self.desplazarse()
        if not self.sana and self.puede_sanar and instante >= self.instante_contagio + TIEMPO_HASTA_SANAR:
            self.sana = np.random.uniform(0, 1) <= PROBABILIDAD_SANAR
            if self.sana:
                self.inmovilizada = False

        if not self.sana and self.se_inmoviliza_al_infectarse and instante >= self.instante_contagio + self.tiempo_hasta_inmovilizarse:
            self.inmovilizada = True

def animate_random_walk(instante, personas, scat_personas, grafico_epidemia):
    """Esta funcion se ejecuta en cada frame del random walk y hace que se muevan y, posiblemente, se contagien las personas"""

    personas_x = np.array([])
    personas_y = np.array([])
    colors = np.array([])
    sanas, infectadas = 0, 0

    for t in range(0, len(personas)):
        persona = personas[t]
        persona.actualizar(instante)
        personas_x = np.append(personas_x, persona.x)
        personas_y = np.append(personas_y, persona.y)

    # TODO ver una manera más eficiente de hacer esto
    for t in range(0, len(personas)):
        persona = personas[t]
        persona.interactuar(personas, instante)
        if persona.sana:
            colors = np.append(colors, "g")
            sanas += 1
        else:
            colors = np.append(colors, "r")
            infectadas += 1

    coordenadas = np.column_stack((personas_x,personas_y))
    scat_personas.set_offsets(coordenadas)
    scat_personas.set_color(colors)

    grafico_epidemia.actualizar_grafico_linea(instante, sanas, infectadas)

def main():

    args = parser.parse_args()
    print(args)
    inmovilizar_cuando_se_infecta = args.estrategia == "2"
    puede_sanar = args.modelo == "B"
    inicial_inmovilizada = args.estrategia == "3"

    personas = np.array([])
    personas_x = np.array([])
    personas_y = np.array([])
    colors = np.array([])
    for i in range(0, CANT_PERSONAS):
        x = np.random.uniform(0, LIMITE_X)
        y = np.random.uniform(0, LIMITE_Y)

        sana = np.random.uniform(0, 1) >= PROPORCION_INICIAL_INFECTADAS

        inmovilizada = False
        if inicial_inmovilizada:
            inmovilizada = np.random.uniform(0, 1) >= 0.5

        persona = Persona(x, y, sana, inmovilizada, inmovilizar_cuando_se_infecta, puede_sanar)
        personas = np.append(personas, persona)
        personas_x = np.append(personas_x, persona.x)
        personas_y = np.append(personas_y, persona.y)
        if persona.sana:
            colors = np.append(colors, "g")
        else:
            colors = np.append(colors, "r")

    fig, axs = plt.subplots(2)
    axs[0].set_xlim(0, LIMITE_X)
    axs[0].set_ylim(0, LIMITE_Y)
    scat_personas = axs[0].scatter(personas_x, personas_y, s=100, c=colors)

    grafico_epidemia = Grafico_epidemia(axs[1])

    anim = animation.FuncAnimation(fig, animate_random_walk, frames=CANT_INSTANTES, interval=1, repeat=False, fargs=(personas,scat_personas, grafico_epidemia))
    if args.video:
        writer = animation.FFMpegWriter(fps=15, bitrate=1800)
        anim.save("Ejercicio-10-modelo-{0}-estrategia-{1}.mp4".format(args.modelo, args.estrategia), writer=writer)
    else:
        plt.show()

parser = argparse.ArgumentParser()
parser.add_argument("-m", "-modelo", dest="modelo",
                    choices=["A", "B"], help="""El modelo a simular
                                                A: Las personas enfermas no se curan
                                                B: Las personas enfermas se curan en 20 instantes de tiempo""")
parser.add_argument("-e", "-estrategia", dest="estrategia",
                    choices=["1", "2", "3"], help="""La estrategia a utilizar
                                                     1: Todos los individuos se mueven
                                                     2: Sólo se mueven los sanos
                                                     3: Se mueve la mitad de la población""")
parser.add_argument("-v", "-video", dest="video", action="store_true", help="Si está presente se guarda la animación en mp4 si no se muestra")

if __name__ == "__main__":
    main()