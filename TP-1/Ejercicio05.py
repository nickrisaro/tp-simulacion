import Ejercicio01 as generador
import numpy as np
import matplotlib.pyplot as plot
import sys
from scipy.stats import chi2

INICIO_INTERVALO = 0.2
FIN_INTERVALO = 0.5
CANT_SIMULACIONES = 300000
SIGNIFICANCIA_CHI2 = 0.01

def gap_chi2 (frecuencias):
	"""
		Recibe el diccionario de frecuencias de gaps como parametro.
		Realiza el test chi2 para las frecuencias comparando con la hipotesis nula de que se trata de una geometrica.
		Para la frecuencia de cada gap realiza la distancia entre lo observado y lo esperado sumandolas todas.
		Luego, ese valor lo compara con el nivel de significancia de chi2 para verificar si aceptamos o rechazamos la hipotesis nula.
	"""
	D2 = 0
	CANT_GAPS = sum([valor for key, valor in frecuencias.items()])
	for valor, cant_observada in frecuencias.items():
		f_observada = cant_observada
		f_esperada = prob_esperada_gaps(valor) * CANT_GAPS
		#Descomentar para testing visual (?)
		#print("PARA EL VALOR ", valor, " OBSERVE ", f_observada, " ESPERABA OBSERVAR ", f_esperada, " EN CANT DE SIMULACIONES ", CANT_GAPS)
		D2i = np.power(f_observada - f_esperada,2) / f_esperada
		D2 += D2i
	limiteSuperior = chi2.ppf(1 - SIGNIFICANCIA_CHI2, df=len(frecuencias) - 1)
	print("Estadistico: {:.2f} ".format(D2))
	print("Limite superior: {:.2f} ".format(limiteSuperior))
	if D2 <= limiteSuperior:
		print("El test acepta la hipotesis nula. Se comporta como una Geometrica.")
	else:
		print("El test rechaza la hipótesis nula. No se comporta como una Geometrica.")

def prob_esperada_gaps(cant_gaps):
	"""
		Este metodo recibe el numero de gaps y devuelve la probabilidad esperada del mismo mediante la formula Pn = p * (1-p)**n. (Es decir, se espera una geometrica)
		Se toma p como la probabilidad del intervalo.
	"""
	prob_intervalo = FIN_INTERVALO - INICIO_INTERVALO
	prob_esperada = prob_intervalo * np.power((1 - prob_intervalo), cant_gaps)
	return prob_esperada

def pertenece_a_intervalo(valor, inicio_intervalo, fin_intervalo):
	return inicio_intervalo <= valor <= fin_intervalo 

def es_ultimo_valor(i, cant_simulaciones):
	return i == cant_simulaciones - 1

def gap_test(generador, cant_simulaciones, inicio_intervalo, fin_intervalo):
	""" 
		Recibe el generador, la cantidad de simulaciones y el intervalo como parametro.
		Calcula la cantidad de veces que sucede un gap en un intervalo para un generador dado.
		Devuelve un diccionario cuya clave es el gap y cuyo valor es la cantidad de veces que sucedio.
	"""
	gaps = np.array([])
	gap_actual = 0
	for i in range(0, cant_simulaciones):
		if (es_ultimo_valor(i, cant_simulaciones)):
			np.append(gaps, gap_actual)
			break
		valor_generado = generador.generar()
		if pertenece_a_intervalo(valor_generado, inicio_intervalo, fin_intervalo):
			gaps = np.append(gaps, gap_actual)
			gap_actual = 0
		else:
			gap_actual += 1
	unique_gaps, counts = np.unique(gaps, return_counts=True)
	return dict(zip(unique_gaps, counts))

def main():
	print("TP 1 - Ejercicio 05")	
	print("Aplicar un gap test al generador congruencial lineal implementado en el ejercicio 1 utilizando el intervalo [0,2 - 0,5]. Analizar el resultado obtenido, e indicar si la distribución de probabilidades pasa o no el test. Considerar un nivel de significación del 1%.")

	generador_unitario = generador.GCL(unitario=True)
	gaps = gap_test(generador_unitario, CANT_SIMULACIONES, INICIO_INTERVALO, FIN_INTERVALO)
	print(gaps)

	plot.bar(gaps.keys(), gaps.values(), 1.0, color='g', edgecolor="black")
	plot.savefig(sys.path[0] + "/E05-histograma.png")
	print("El histograma se guardó en {0}/E05-histograma.png".format(sys.path[0]))

	#La idea ahora es ver si la distribucion obtenida se parece a una geometrica con nivel alpha 0.1
	gap_chi2(gaps)

if __name__ == "__main__":
	main()