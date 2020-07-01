import csv
import numpy as np
import math
import matplotlib.pyplot as plt
import random

def get_centro_intervalo_for_estado(estado, intervalos):
	"Devuelve el valor medio del intervalo para un estado dado"
	return (intervalos[estado][0] + intervalos[estado][1])/2
	#return (random.uniform(intervalos[estado][0], intervalos[estado][1]))

def get_estado(value, intervalos):
	"Devuelve el estado segun si el valor se encuentra en alguno de los intervalos posibles. -1 si no"
	for i in range(0, len(intervalos)):
		if intervalos[i][0] <= value < intervalos[i][1]:
			return i
	return -1

def obtener_valores_desde_archivo(filename_accion):
	"Devuelve la lista de estados de la accion recibida por parametro"
	with open(filename_accion) as f:
		reader = csv.reader(f)
		valores = np.empty(0)
		for row in f:
			split_list = row.split(",")
			if split_list[1].strip() != "Valor":
				valores = np.append(valores, (float)(split_list[1].strip()))
		return valores

def obtener_porcentajes(valores):
	"Calcula las transiciones entre valores como porcentajes y devuelve una lista con los mismos por orden de aparicion"
	posibles_porcentajes = np.empty(0)
	for i in range (0, len(valores)):
		if i == len(valores) - 1:
			break
		porcentaje_transicion = round(valores[i + 1] * 100 / valores[i])
		posibles_porcentajes = np.append(posibles_porcentajes, porcentaje_transicion)
	return posibles_porcentajes

def armar_intervalos(porcentajes, cant_clases):
	"Genera la la lista de intervalos en base a la lista de porcentajes y la cantidad de clases"
	min_porcentaje = min(porcentajes)
	max_porcentaje = max(porcentajes)
	ancho_intervalo = math.ceil((max_porcentaje - min_porcentaje)/ cant_clases)
	aux_acc = min_porcentaje
	intervalos = []
	while (aux_acc <= max_porcentaje):
		intervalos.append((aux_acc, aux_acc + ancho_intervalo))
		aux_acc += ancho_intervalo
	return intervalos

def pruebas_get_estado_a(intervalos):
	assert(get_estado(55, intervalos) == 0)
	assert(get_estado(47, intervalos) == -1)
	assert(get_estado(290, intervalos) == -1)
	assert(get_estado(82, intervalos) == 1)
	assert(get_estado(48, intervalos) == 0)
	return

def generar_matriz_transicion(intervalos, porcentajes):
	"Genera la matriz de transición a partir de la lista de intervalos y la lista de porcentajes"
	transicion = np.zeros((len(intervalos), len(intervalos)))
	for i in range(0, len(porcentajes)):
		if i == len(porcentajes) - 1:
			break
		estado_1 = get_estado(porcentajes[i], intervalos)
		estado_2 = get_estado(porcentajes[i + 1], intervalos)
		transicion[estado_1][estado_2] += 1 
	for row in transicion:
		a = np.sum(row)
		row[row > 0] /= a
	return transicion

def simular_anual(k, transicion, valores, intervalos):
	"Simula el valor de una acción a lo largo de un año"
	p = np.zeros(k)
	estado_inicial = 3 
	p[estado_inicial] = 1
	estados_simulados = [estado_inicial]
	for i in range(0, 365):
		p = np.dot(p, transicion) #multiplico p por la matriz de transiciones
		acc_p = np.cumsum(p) #calculo el vector de prob acumulada
		u = random.uniform(0,1) #obtengo un numero random de manera uniforme
		estado_actual = next((i for i,v in enumerate(acc_p) if v > u))  #calculo el estado actual en base al numero random generado
		estados_simulados.append(estado_actual)
		#pongo el vector p en el actual estado
		p = np.zeros(math.ceil(k)) 
		p[estado_actual] = 1
	#Con los estados simulados, genero un valor inicial y le aplico los porcentajes correspondientes
	valor = random.uniform(min(valores), max(valores))
	valores_simulados = [valor]
	for estado in estados_simulados:
		porcentaje_aplicado = get_centro_intervalo_for_estado(estado, intervalos) / 100
		valor = valor * porcentaje_aplicado
		valores_simulados.append(round(valor, 2))
	return valores_simulados

def simular_accion(accion, filename):
	"Realizar todas las instrucciones para simular el valor de la acción recibida por parametro"
	valores = obtener_valores_desde_archivo(filename)
	porcentajes = obtener_porcentajes(valores)
	k = math.ceil(1 + math.log2(len(valores))) #cantidad de intervalos que voy a tener segun Sturges (estos seran nuestros estados)
	intervalos = armar_intervalos(porcentajes, k)
	print("Los posibles estados de la acción " + accion + " son:")
	print(intervalos)
	transicion = generar_matriz_transicion(intervalos, porcentajes)
	print("La matriz de transición para los porcentajes de la acción " + accion + " es:")
	print(transicion)
	transicion_elevada = transicion
	for i in range(0, 50):
		transicion_elevada = np.dot(transicion_elevada, transicion)
	print("La cantidad de tiempo que la acción " + accion + " pasa en cada estado es:")
	print(transicion_elevada[0])
	
	#Descomentar para probar 100 corridas. guarda los maximos a un archivo de texto	
	maxs = []
	for i in range(0,100):
		valores_simulados = simular_anual(k, transicion, valores, intervalos)
		maxs.append(round(max(valores_simulados),2))
	maxs.sort()
	with open('test.txt', 'w') as f:
		for item in maxs:
			f.write("%s, " % item)
	valores_simulados = simular_anual(k, transicion, valores, intervalos)
	plt.scatter(range(0,367), valores_simulados)
	plt.title("Valor de la acción " + accion)
	plt.xlabel("Días")
	plt.ylabel("Valor")
	plt.show()


def simular_anual_con_mas_estados(estados, transicion, valores):
	k = len(estados)
	p = np.zeros(k)
	estado_inicial = 3 
	p[estado_inicial] = 1
	estados_simulados = [estado_inicial]
	for i in range(0, 365):
		p = np.dot(p, transicion) #multiplico p por la matriz de transiciones
		acc_p = np.cumsum(p) #calculo el vector de prob acumulada
		u = random.uniform(0,1) #obtengo un numero random de manera uniforme
		estado_actual = next((i for i,v in enumerate(acc_p) if v > u))  #calculo el estado actual en base al numero random generado
		estados_simulados.append(estado_actual)
		#pongo el vector p en el actual estado
		p = np.zeros(math.ceil(k)) 
		p[estado_actual] = 1
	#Con los estados simulados, genero un valor inicial y le aplico los porcentajes correspondientes
	valor = random.uniform(min(valores), max(valores))
	valores_simulados = [valor]
	for estado in estados_simulados:
		porcentaje_aplicado = estados[estado] / 100
		valor = valor * porcentaje_aplicado
		valores_simulados.append(round(valor, 2))
	return valores_simulados

def simular_accion_con_mas_estados(accion, filename):
	"Simula la evolucion de las acciones tomando como estados los porcentajes con incrementos de 1%"
	valores = obtener_valores_desde_archivo(filename)
	porcentajes = obtener_porcentajes(valores)
	estados = np.unique(porcentajes)
	estados.sort()
	print("Los posibles estados de la acción " + accion + " son:")
	print(estados)
	transicion = np.zeros((len(estados), len(estados)))
	for i in range(0, len(porcentajes)):
		if i == len(porcentajes) - 1:
			break
		estado_1, = np.where(estados == porcentajes[i])
		estado_2, = np.where(estados == porcentajes[i + 1])
		transicion[estado_1[0]][estado_2[0]] += 1 
	for row in transicion:
		a = np.sum(row)
		row[row > 0] /= a

	print("La matriz de transición de estados de la acción " + accion + " es:")
	print(transicion)
	transicion_elevada = transicion
	for i in range(0, 50):
		transicion_elevada = np.dot(transicion_elevada, transicion)
	print("La cantidad de tiempo que la acción " + accion + " pasa en cada estado es:")
	print(transicion_elevada[0])

	#Descomentar para 100 corridas
	#maxs = []
	#for i in range(0,100):
	#	valores_simulados = simular_anual_con_mas_estados(estados, transicion, valores)
	#	maxs.append(round(max(valores_simulados),2))
	#maxs.sort()
	#with open('test.txt', 'w') as f:
	#	for item in maxs:
	#		f.write("%s, " % item)

	valores_simulados = simular_anual_con_mas_estados(estados, transicion, valores)
	plt.scatter(range(0,367), valores_simulados)
	plt.title("Valor de la acción " + accion)
	plt.xlabel("Días")
	plt.ylabel("Valor")
	plt.show()



def main():

	#simular_accion("A", "accion A.csv")
	#simular_accion("B", "accion B.csv")
	simular_accion_con_mas_estados("A","accion A.csv")
	simular_accion_con_mas_estados("B","accion B.csv")


if __name__ == "__main__":
    main()
