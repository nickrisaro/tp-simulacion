import csv
import numpy as np
import math
import matplotlib.pyplot as plt
import random

def get_centro_intervalo_for_estado(estado, intervalos):
	return (random.uniform(intervalos[estado][0], intervalos[estado][1]))

def get_estado(value, intervalos):
	"Devuelve el estado segun si el valor se encuentra en alguno de los intervalos posibles. -1 si no"
	for i in range(0, len(intervalos)):
		if intervalos[i][0] <= value < intervalos[i][1]:
			return i
	return -1

def obtener_valores_desde_archivo(filename_accion):
	"Devuelve el diccionario de estados de la accion recibida por parametro"
	with open(filename_accion) as f:
		reader = csv.reader(f)
		valores = np.empty(0)
		for row in f:
			split_list = row.split(",")
			if split_list[1].strip() != "Valor":
				valores = np.append(valores, (float)(split_list[1].strip()))
		return valores

def obtener_porcentajes(valores):
	posibles_porcentajes = np.empty(0)
	for i in range (0, len(valores)):
		if i == len(valores) - 1:
			break
		porcentaje_transicion = round(valores[i + 1] * 100 / valores[i])
		posibles_porcentajes = np.append(posibles_porcentajes, porcentaje_transicion)
	return posibles_porcentajes

def armar_intervalos(porcentajes, cant_clases):
	min_porcentaje = min(porcentajes)
	max_porcentaje = max(porcentajes)
	ancho_intervalo = ((max_porcentaje - min_porcentaje)/ cant_clases)
	aux_acc = min_porcentaje
	intervalos = []
	while (aux_acc <= max_porcentaje):
		intervalos.append((aux_acc, aux_acc + ancho_intervalo))
		aux_acc += ancho_intervalo
	return intervalos

def pruebas_get_estado_a(intervalos):
	#assert(get_estado(55, intervalos) == 0)
	#assert(get_estado(47, intervalos) == -1)
	#assert(get_estado(290, intervalos) == -1)
	#assert(get_estado(82, intervalos) == 1)
	#assert(get_estado(48, intervalos) == 0)
	return

def generar_matriz_transicion(intervalos, porcentajes):
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

def simular_anual(k_a, transicion, valores_a, intervalos):
	p = np.zeros(k_a)
	estado_inicial = 3
	p[estado_inicial] = 1
	#print("El estado inicial para la simulación del valor del a acción A es:")
	#print(p)
	estados_simulados = [estado_inicial]
	for i in range(0, 365):
		p = np.dot(p, transicion) #multiplico p por la matriz de transiciones
		acc_p = np.cumsum(p) #calculo el vector de prob acumulada
		u = random.uniform(0,1) #obtengo un numero random de manera uniforme
		estado_actual = next((i for i,v in enumerate(acc_p) if v > u)) #calculo el estado actual en base al numero random generado
		estados_simulados.append(estado_actual) #guardo el estado simulado
		#pongo el vector p en el actual estado
		p = np.zeros(math.ceil(k_a)) 
		p[estado_actual] = 1
	
	#Con los estados simulados, genero un valor inicial y le aplico los porcentajes correspondientes
	valor = random.uniform(min(valores_a), max(valores_a))
	valores_simulados = [valor]
	for estado in estados_simulados:
		porcentaje_aplicado = get_centro_intervalo_for_estado(estado, intervalos) / 100
		valor = valor * porcentaje_aplicado
		valores_simulados.append(round(valor, 2))
	return valores_simulados

def main():   
	valores_a = obtener_valores_desde_archivo("accion A.csv")
	porcentajes = obtener_porcentajes(valores_a)
	k_a = 20#math.ceil(1 + math.log2(len(valores_a))) #cantidad de intervalos que voy a tener segun Sturges (estos seran nuestros estados)
	intervalos = armar_intervalos(porcentajes, k_a)
	print("Los posibles estados de A son:")
	print(intervalos)
	pruebas_get_estado_a(intervalos)
	transicion = generar_matriz_transicion(intervalos, porcentajes)
	print("La matriz de transición para los porcentajes de la acción A es:")
	print(transicion)
	transicion_elevada = transicion
	for i in range(0, 50):
		transicion_elevada = np.dot(transicion_elevada, transicion)
	print("La cantidad de tiempo que la acción A pasa en cada estado es:")
	print(transicion_elevada[0])

#Descomentar para probar 100 corridas. Guarda los maximos a un archivo de texto	
	#maxs = []
	#for i in range(0,100):
	#	valores = simular_anual(k_a, transicion, valores_a, intervalos)
	#	maxs.append(round(max(valores),2))
	#maxs.sort()
	#with open('test.txt', 'w') as f:
	#	for item in maxs:
	#		f.write("%s," % item)
	#print(maxs)
	valores = simular_anual(k_a, transicion, valores_a, intervalos)
	plt.scatter(range(0,367), valores)  
	plt.show()

if __name__ == "__main__":
    main()



#0 -> 1er intervalo (entre 


#estados_b, estados_unicos_b = calcular_valores("accion B.csv")


#estados_a, estados_unicos_a = calcular_estados("accion A.csv")
#k = 1 + math.log(len(estados_a),2)
#hist = np.histogram(estados_a) 
#print(hist)
#plt.hist(porcentajes, bins=11)  # arguments are passed to np.histogram
#plt.show()
#estados_b, estados_unicos_b = calcular_estados("accion B.csv")