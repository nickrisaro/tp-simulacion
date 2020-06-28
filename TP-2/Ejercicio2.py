import random as rn
import sys
import matplotlib.pyplot as plt

# Cola M/M/1

def simular(ms):
	p = 1/40  # Probabilidad de ingresar al sistema
	q = 1/30  # Probabilidad de salir del sistema
	tiempos = []
	estados = []
	cantidadEnCola = 0
	cantidadVecesInactiva = 0
	# tiempo = 0
	for tiempo in range(ms):
		if (rn.random() <= p):
			cantidadEnCola += 1
		if (rn.random() <= q and cantidadEnCola > 0):
			cantidadEnCola -=1
		tiempos.append(tiempo)
		estados.append(cantidadEnCola)
		if (cantidadEnCola == 0):
			cantidadVecesInactiva+=1
	return tiempos, estados, cantidadVecesInactiva


tiempo = 100000
print("c. Realice un gráfico mostrando la cantidad de solicitudes en el servidor en cada instante de tiempo.")
tiempos, estados, cantidadVecesInactiva = simular(tiempo)
plt.plot(tiempos, estados)
plt.savefig(sys.path[0] + "/E02-cantidad-solicitudes-por-instante.png")

print("d. Realice un histograma mostrando cuantas veces el sistema estuvo en cada estado")
plt.figure(figsize=(15,9))
plt.hist(estados)
plt.savefig(sys.path[0] + "/E02-cantidad-solicitudes-histograma.png")

print("d. Determine el % de tiempo que el servidor se encuentra sin procesar solicitudes")
print(cantidadVecesInactiva / len(estados) * 100 , "%")
