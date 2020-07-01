import random as rn
import sys
import numpy as np
import matplotlib.pyplot as plt

# Cola M/M/1

def simular(ms):
	p = 1/40  # Probabilidad de ingresar al sistema
	q = 1/30  # Probabilidad de salir del sistema
	tiempos = []
	estados = []
	cantidadEnCola = 0
	cantidadVecesInactiva = 0
	solicitudEnProceso = False
	# tiempo = 0
	for tiempo in range(ms):
		if solicitudEnProceso and rn.random() <= q:
			solicitudEnProceso = False
			if (cantidadEnCola > 0):
				cantidadEnCola -=1
				solicitudEnProceso = True

		if (rn.random() <= p):
			if solicitudEnProceso: 
				cantidadEnCola += 1
			else:
				solicitudEnProceso = True

		tiempos.append(tiempo)
		estados.append(cantidadEnCola)
		if (not solicitudEnProceso):
			cantidadVecesInactiva+=1

	return tiempos, estados, cantidadVecesInactiva


tiempo = 100000
print("b. Realice un gráfico mostrando la cantidad de solicitudes en el servidor en cada instante de tiempo.")
tiempos, estados, cantidadVecesInactiva = simular(tiempo)
plt.plot(tiempos, estados)
plt.savefig(sys.path[0] + "/E02-cantidad-solicitudes-por-instante.png")

print("c. Realice un histograma mostrando cuantas veces el sistema estuvo en cada estado")
plt.figure(figsize=(15,9))
plt.hist(estados)
plt.savefig(sys.path[0] + "/E02-cantidad-solicitudes-histograma.png")
plt.clf()
plt.cla()
plt.close()

print("d. Determine el % de tiempo que el servidor se encuentra sin procesar solicitudes")

# Realizo 1000 simulaciones
cantidad_simu = 1000
cantidades_inactivas = []
rango_simulaciones = range(cantidad_simu) 
for x in rango_simulaciones:
	tiempos, estados, cantidadVecesInactiva = simular(tiempo)
	cantidades_inactivas.append(cantidadVecesInactiva)

print (max(cantidades_inactivas))
print (min(cantidades_inactivas))
plt.figure(figsize=(15,9))
plt.plot( rango_simulaciones, cantidades_inactivas)
plt.savefig(sys.path[0] + "/E02-cantidad-veces-inactivas-por-instante.png") 
print("Minimo veces inactivas", max(cantidades_inactivas))
print("Maximo de veces inactivas", min(cantidades_inactivas) )
print("Promedio de veces inactivas", sum(cantidades_inactivas) / ( tiempo * cantidad_simu ) * 100 , "%")
