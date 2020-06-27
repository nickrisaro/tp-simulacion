import numpy as np

def calcular_tiempos_espera(t, media):

    tiempos_procesamiento = np.random.exponential(media, len(t))

    tiempos_de_espera = [0]
    for i in range(1, len(t)):
        tiempo_total_anterior = t[i-1] + tiempos_procesamiento[i-1] + tiempos_de_espera[i-1]
        tiempo_de_sobra = t[i] - tiempo_total_anterior
        if tiempo_de_sobra >= 0:
            tiempos_de_espera.append(0)
        else:
            tiempos_de_espera.append(-tiempo_de_sobra)

    return tiempos_de_espera

def simular_opcion_1(t, N):
    prob_u1 = 0.6
    media_u1 = 0.7
    media_u2 = 1

    u = np.random.rand(N)

    #Separo en las dos unidades
    t1 = [0]
    t2 = [0]

    for i in range(0, N):
        if u[i] < prob_u1: #La solicitud es procesada por la unidad 1
            t1.append(t[i])
        else:               #La solicitud es procesada por la unidad 2
            t2.append(t[i])

    #Calculo tiempos de espera para la unidad 1
    tiempos_espera_u1 = calcular_tiempos_espera(t1, media_u1)

    #Calculo tiempos de espera para la unidad 1
    tiempos_espera_u2 = calcular_tiempos_espera(t2, media_u2)

    tiempos_espera_totales = np.concatenate((tiempos_espera_u1, tiempos_espera_u2), axis=None)

    print("El tiempo medio de espera entre que la solicitud llega y puede ser procesada es de: " + str(np.mean(tiempos_espera_totales)))

    cantidad_solicitudes_sin_espera = 0
    for i in range(0, len(tiempos_espera_totales)):
        if tiempos_espera_totales[i] == 0:
            cantidad_solicitudes_sin_espera += 1

    print("La cantidad de solicitudes que no necesitaron esperar para ser procesadas es de " + str(cantidad_solicitudes_sin_espera) + " sobre un total de 100000")

def main():
    print ("TP2 - Ejercicio 1")

    print("Un instituto de investigacion debe decidir la inversion a realizar en equipos de diagnostico de una nueva enfermedad.")
    print("Se debe decidir la compra de equipos entre las opciones brindadas por 2 proveedores:")
    print("1) El proveedor 1 plantea utilizar 2 unidades de diagnostico en paralelo.")
    print("Con probabilidad p = 0.6 las muestras seran diagnosticadas por la unidad 1 y con probabilidad q = 1 - p son diagnosticados por la unidad 2.")
    print("El tiempo que demora cada unidad en resolver una solicitud sigue una distribucion exponencial con medias mu_1 = 0,7 hs y mu_2 = 1 h respectivamente.")
    print("2) El proveedor 2 considera utilizar 1 unidad.")
    print("En este caso la demora en resolver una solicitud sigue una distribucion exponencial con mu = 0,8 horas")
    print("Se estima que el tiempo que transcurre entre la llegada de cada muestra se puede modelar segun una distribucion exponencial con media mu = 4 horas")
    print("Simular para cada opcion 100.000 solicitudes procesadas, determinando:")
    print("a) El tiempo medio de espera entre que la solicitud llega y puede ser procesada.")
    print("b) La fraccion de las solicitudes que no esperaron para ser procesadas.")
    print("c) La opcion 1 es mas costosa que la segunda opcion y el instituto solo acepta realizar la inversion si el tiempo medio")
    print("que demora en resolver cada diagnostico (tiempo en fila + tiempo de procesamiento) es como minimo 50% menor")
    print("que la opcion 2. Que solucion le recomienda?")

    N = 100000

    media_2 = 0.8
    media_llegada_muestras = 4

    #Genero N tiempos entre arribos
    tiempos_de_arribo = np.random.exponential(media_llegada_muestras, N)
    t = np.concatenate(([0], np.cumsum(tiempos_de_arribo)), axis=None)

    #OPCION 1
    simular_opcion_1(t, N)

if __name__ == "__main__":
    main()